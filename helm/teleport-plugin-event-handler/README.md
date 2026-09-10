# teleport-plugin-event-handler

A Helm chart for Teleport Event Handler Plugin

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| teleport.address | string | `"test.example.com:443"` | Host/port combination of the teleport auth server |
| teleport.identitySecretName | string | `"teleport-event-handler-identity"` | Name of the Kubernetes secret that contains the credentials for the connection |
| teleport.identitySecretPath | string | `"identity"` | Key of the field in the secret specified by teleport.identitySecretName |
| eventHandler.storagePath | string | `"/var/lib/teleport/plugins/event-handler/storage"` | Path to the directory where event-handler's state is stored |
| eventHandler.timeout | string | `"10s"` | Maximum time to wait for incoming events before sending them to fluentd. |
| eventHandler.batch | int | `20` | Maximum number of events fetched from Teleport in one request |
| fluentd.url | string | `"https://fluentd.fluentd.svc.cluster.local/events.log"` | URL of fluentd where the event logs will be sent to. |
| fluentd.sessionUrl | string | `"https://fluentd.fluentd.svc.cluster.local/session.log"` | URL of fluentd where the session logs will be sent to. |
| fluentd.certificate.secretName | string | `"teleport-event-handler-client-tls"` | Name of the secret where credentials for the connection is stored. It must contain the client's private key, certificate and fluentd's CA certificate. See the default paths below. |
| fluentd.certificate.caPath | string | `"ca.crt"` | Path of the CA certificate in the secret described by fluentd.certificate.secretName. |
| fluentd.certificate.certPath | string | `"client.crt"` | Path of the client's certificate in the secret described by fluentd.certificate.secretName. |
| fluentd.certificate.keyPath | string | `"client.key"` | Path of the client private key in the secret described by fluentd.certificate.secretName. |
| persistentVolumeClaim.enabled | bool | `false` | Instructs the Helm chart to include a PersistentVolumeClaim for the storage. This storage will be mounted to the path specified by eventHandler.storagePath. |
| persistentVolumeClaim.size | string | `"1Gi"` | Sets the size of the created PersistentVolumeClaim. Don't forget to append the proper suffix! |
| persistentVolumeClaim.storageClassName | string | `""` | Sets the storage class name of the created PersistentVolumeClaim. Kubernetes will use the default one when omitted. |
| persistentVolumeClaim.existingClaim | string | `""` | Specifies an already existing PersistentVolumeClaim which should be mounted to the path specified by eventHandler.storagePath. persistentVolumeClaim.enabled must be set to false for this option to take precedence. Ignored when persistentVolumeClaim.enabled is true. |
| persistentVolumeClaim.volumeName | string | `"storage"` |  |
| image.repository | string | `"public.ecr.aws/gravitational/teleport-plugin-event-handler"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.tag | string | `""` |  |
| imagePullSecrets | list | `[]` |  |
| nameOverride | string | `""` |  |
| fullnameOverride | string | `""` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| securityContext.runAsNonRoot | bool | `false` |  |
| securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| securityContext.allowPrivilegeEscalation | bool | `false` |  |
| securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| securityContext.readOnlyRootFilesystem | bool | `false` |  |
| resources.requests.cpu | string | `"500m"` |  |
| resources.requests.memory | string | `"1Gi"` |  |
| resources.limits.cpu | string | `"500m"` |  |
| resources.limits.memory | string | `"1Gi"` |  |
| nodeSelector | object | `{}` |  |
| tolerations | list | `[]` |  |
| affinity | object | `{}` |  |
| volumes | list | `[]` |  |
| volumeMounts | list | `[]` |  |
