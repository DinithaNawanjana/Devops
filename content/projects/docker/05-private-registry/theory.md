# Deep Dive: Registries & Image Distribution

## What a registry is
A registry stores and serves images by `name:tag`. Docker Hub is the public one;
`registry:2` is the open-source server you can run yourself for private or
air-gapped use. Pushing/pulling is just HTTP against a documented API
(`/v2/...`).

## Names encode the registry
`localhost:5000/demo:1` means *host* `localhost:5000`, *repo* `demo`, *tag* `1`.
The hostname prefix is how the client knows which registry to talk to; with no
prefix, Docker defaults to Docker Hub.

## The push flow
`docker tag` gives the image a name pointing at your registry, then
`docker push` uploads each **layer** (deduplicated — shared layers upload once).
`curl http://localhost:5000/v2/_catalog` lists what's stored.

## Pitfalls
- HTTP registries are "insecure" to Docker — you must add them to
  `insecure-registries` or use TLS.
- No auth/garbage-collection by default — fine for a lab, not for production.
- Forgetting that the tag is part of the identity (`demo` ≠ `demo:1`).

## Real-world
Every team runs or rents a registry (ECR, GCR, Harbor, GitHub Packages); it's
the handoff point between CI (which builds/pushes) and CD (which pulls/deploys).
