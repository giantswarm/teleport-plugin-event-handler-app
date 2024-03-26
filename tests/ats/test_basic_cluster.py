import logging
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import List

import re
import pykube
import pytest
from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_deployments_to_run

logger = logging.getLogger(__name__)

namespace_name = "default"
timeout: int = 360

def run_subprocess(command: list, check: bool = True):
    try:
        result = subprocess.run(
            command,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info(f"Command {' '.join(command)} executed successfully: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {' '.join(command)} failed with error: {e.stderr}")
        if check:
            raise

@pytest.fixture(scope="module")
def teleport_cert(kube_cluster: Cluster):
    teleport_cluster_address = "test.example.com:443"

    logger.info("Generating certificate files for Teleport plugin.")
    # Run the Docker command to generate the certificate files
    run_subprocess(
        [
            "docker",
            "run",
            "-v",
            f"{Path.cwd()}:/opt/teleport-plugin",
            "-w",
            "/opt/teleport-plugin",
            "public.ecr.aws/gravitational/teleport-plugin-event-handler:15.1.9",
            "configure",
            ".",
            teleport_cluster_address,
        ]
    )

    logger.info("Creating Kubernetes secret for Teleport plugin.")
    # Create the secret using the generated certificate files
    run_subprocess(
        [
            "kubectl",
            "create",
            "secret",
            "generic",
            "teleport-event-handler-client-tls",
            "--from-file=ca.crt=ca.crt,client.crt=client.crt,client.key=client.key",
            "-n",
            namespace_name,
        ]
    )

@pytest.fixture(scope="module")
def identity_file():
    logger.info("Applying identity.yaml to configure Kubernetes resources.")
    # Apply the identity.yaml file using kubectl
    run_subprocess(["kubectl", "apply", "-f", "identity.yaml", "-n", namespace_name])

@pytest.fixture(scope="module")
def app_deployment(kube_cluster: Cluster) -> List[pykube.Deployment]:
    logger.info("Fetching deployments to identify those related to the Teleport plugin.")
    all_deployments = pykube.Deployment.objects(kube_cluster.kube_client).filter(namespace=namespace_name)
    # Filter deployments by name pattern
    pattern = r'.*-event-handler'
    teleport_deployments = [d for d in all_deployments if re.match(pattern, d.name)]
    if not teleport_deployments:
        logger.warning("No Teleport plugin deployments found with the expected name pattern.")
    else:
        logger.info(f"Found {len(teleport_deployments)} deployments matching the Teleport plugin pattern.")

    # Ensure deployments are ready
    for deployment in teleport_deployments:
        wait_for_deployments_to_run(
            kube_cluster.kube_client,
            [deployment.name],
            namespace_name,
            timeout,
        )
    return teleport_deployments

@pytest.mark.smoke
@pytest.mark.upgrade
@pytest.mark.flaky(reruns=5, reruns_delay=10)
def test_pods_available(kube_cluster: Cluster, app_deployment: List[pykube.Deployment]):
    assert app_deployment, "No deployments found matching the Teleport plugin pattern."
    for d in app_deployment:
        ready_replicas = int(d.obj["status"].get("readyReplicas", 0))
        logger.info(f"Checking deployment {d.name} for ready replicas: {ready_replicas}")
        assert ready_replicas > 0, f"Deployment {d.name} has {ready_replicas} ready replicas, expected more than 0."
