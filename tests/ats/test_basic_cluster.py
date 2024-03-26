import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List

import pykube
import pytest
from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_deployments_to_run

logger = logging.getLogger(__name__)

namespace_name = "default"

timeout: int = 360


@pytest.fixture(scope="module")
def teleport_cert(kube_cluster: Cluster):
    teleport_cluster_address = "test.example.com:443"

    # Run the Docker command to generate the certificate files
    subprocess.run(
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
        ],
        check=True,
    )

    # Create the secret using the generated certificate files
    subprocess.run(
        [
            "kubectl",
            "create",
            "secret",
            "generic",
            "teleport-event-handler-client-tls",
            "--from-file=ca.crt=ca.crt,client.crt=client.crt,client.key=client.key",
        ],
        check=True,
    )
@pytest.fixture(scope="module")
def fake_secret(kube_cluster: Cluster):
    secret_data = {
        "auth_id": "test"
    }

    secret = client.V1Secret(
        metadata=client.V1ObjectMeta(name="test-id"),
        type="Opaque",
        data=secret_data
    )

    kube_cluster.kube_client.create_namespaced_secret(namespace_name, secret)

# scope "module" means this is run only once, for the first test case requesting! It might be tricky
# if you want to assert this multiple times
@pytest.fixture(scope="module")
def app_deployment(kube_cluster: Cluster) -> List[pykube.Deployment]:
    deployments = wait_for_deployments_to_run(
        kube_cluster.kube_client,
        ["teleport-plugin-event-handler"],
        "default",
        timeout,
    )
    return deployments


# when we start the tests on circleci, we have to wait for pods to be available, hence
# this additional delay and retries
@pytest.mark.smoke
@pytest.mark.upgrade
@pytest.mark.flaky(reruns=5, reruns_delay=10)
def test_pods_available(kube_cluster: Cluster, app_deployment: List[pykube.Deployment]):
    for d in app_deployment:
        assert int(d.obj["status"]["readyReplicas"]) > 0
