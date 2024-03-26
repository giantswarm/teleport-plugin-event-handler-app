[![CircleCI][]](https://dl.circleci.com/status-badge/redirect/gh/giantswarm/teleport-plugin-event-handler-app/tree/main)[Read me after cloning this template (GS staff only)](https://handbook.giantswarm.io/docs/dev-and-releng/app-developer-processes/adding_app_to_appcatalog/)

# teleport-plugin-event-handler chart

Giant Swarm offers a teleport-plugin-event-handler App which can be installed in workload clusters.
Here we define the teleport-plugin-event-handler chart with its templates and default configuration.

**What is this app?**

The teleport-plugin-event-handler app provides a way to handle events generated by Teleport, an identity-aware access proxy for managing access to infrastructure. It allows you to process and react to Teleport events based on your specific requirements.

**Why did we add it?**

We added this app to provide our customers with a convenient way to integrate Teleport event handling into their Giant Swarm workload clusters. This app enables customers to customize their response to Teleport events and perform actions based on those events.

**Who can use it?**

This app is available for all Giant Swarm customers who want to handle Teleport events in their workload clusters. It is particularly useful for customers who need to monitor and respond to access requests, audit logs, and other Teleport-related events.

## Installing

There are several ways to install this app onto a workload cluster.

- [Using GitOps to instantiate the App](https://docs.giantswarm.io/advanced/gitops/apps/)
- [Using our web interface](https://docs.giantswarm.io/platform-overview/web-interface/app-platform/#installing-an-app).
- By creating an [App resource](https://docs.giantswarm.io/use-the-api/management-api/crd/apps.application.giantswarm.io/) in the management cluster as explained in [Getting started with App Platform](https://docs.giantswarm.io/getting-started/app-platform/).

## Configuring

### values.yaml

**This is an example of a values file you could upload using our web interface.**```yaml
# values.yaml
eventHandler:  enabled: true  slackWebhookURL: "https://hooks.slack.com/services/your-slack-webhook-url"  teleportAddr: "your-teleport-address"  teleportIdentityFile: "/path/to/identity/file"```

### Sample App CR and ConfigMap for the management cluster

If you have access to the Kubernetes API on the management cluster, you could create
the App CR and ConfigMap directly.

Here is an example that would install the app to
workload cluster `abc12`:
```yaml
# appCR.yaml
apiVersion: application.giantswarm.io/v1alpha1
kind: App
metadata:
  name: teleport-plugin-event-handler
  namespace: abc12
spec:
  catalog: giantswarm
  version: 1.0.0
  kubeConfig:
    inCluster: false
    context:
      name: abc12-kubeconfig
  config:
    configMap:
      name: teleport-plugin-event-handler-app-config
      namespace: abc12
```
```yaml
# user-values-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: teleport-plugin-event-handler-app-config
  namespace: abc12
data:
  values: |
    eventHandler:
      enabled: true
      slackWebhookURL: "https://hooks.slack.com/services/your-slack-webhook-url"
      teleportAddr: "your-teleport-address"
      teleportIdentityFile: "/path/to/identity/file"
```

See our [full reference on how to configure apps](https://docs.giantswarm.io/getting-started/app-platform/app-configuration/) for more details.

## Compatibility

This app has been tested to work with the following workload cluster release versions:

- AWS: v15.0.0+
- Azure: v15.0.0+
- KVM: v15.0.0+

## Limitations

Some apps have restrictions on how they can be deployed.
Not following these limitations will most likely result in a broken deployment.

- The app requires a Teleport cluster to be set up and accessible.
- The Slack webhook URL must be provided for sending event notifications to Slack.

## Credit

- [Teleport Event Handler Helm Repository](https://github.com/giantswarm/teleport-plugin-event-handler-app)