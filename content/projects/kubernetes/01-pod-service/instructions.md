# Project Tasks

In `/root/k8s/`:

1. `pod.yaml` — a `Pod` (e.g. nginx) with labels.
2. `service.yaml` — a `Service` whose `selector` matches the pod's labels.

Apply with `kubectl apply -f .`. Click **Check**.
