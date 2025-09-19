# Debugging inside the K8s Cluster

To debug permissions (and maybe other things), it can be useful to spin up a debug pod and exec onto it, so things can be tested from within the k8s cluster.

One way to do this is create the following debug.yaml file (change the service account/namespace)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dri-debug-your-name
  namespace: your_namespace
  labels:
    app: dri-debug-your-name
spec:
  serviceAccountName: dri-your-service-account
  containers:
  - name: dri-debug-your-name
    image: python:3.12-bookworm
    command: ["/bin/bash"]
    args: ["-c", "while true; do sleep 30; done"]
  restartPolicy: Always
```

```bash
kubectl -n your_namespace apply -f debug.yaml
kubectl -n your_namespace exec -it dri-debug-your-name -- /bin/bash
```

This will give you an environment with python installed, debugging can be done using shell commands or python scripts, `apt install <x>` to install any required packages.


Once debugging has finished, it's important to tidy up and remove the pod, this can be done via:
```bash
kubectl -n timeseries delete -f debug.yaml
```
