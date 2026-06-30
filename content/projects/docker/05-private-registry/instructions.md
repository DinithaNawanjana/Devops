# Project Tasks

Write `/root/registry/run.sh` that:

1. Starts a **`registry:2`** container publishing port **5000**.
2. Builds a small image and **tags it `localhost:5000/demo:1`**.
3. **Pushes** it to the local registry.

```bash
cd /root/registry
./run.sh
curl http://localhost:5000/v2/_catalog    # {"repositories":["demo"]}
```

Click **Check**.
