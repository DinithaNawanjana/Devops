# Solution

```bash
mkdir -p /root/mesh
cat > /root/mesh/virtualservice.yaml <<'YML'
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts: [reviews]
  http:
    - route:
        - destination: { host: reviews, subset: v1 }
          weight: 90
        - destination: { host: reviews, subset: v2 }
          weight: 10
YML
cat > /root/mesh/peerauth.yaml <<'YML'
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
YML
```
