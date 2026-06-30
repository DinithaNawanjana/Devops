# Deep Dive: Images, Layers & the Build Cache

## What an image is
An image is a **stack of read-only layers** plus metadata (entrypoint, env,
ports). Each Dockerfile instruction (`FROM`, `COPY`, `RUN`) creates one layer.
At run time Docker adds a thin writable layer on top — that's your container.

## Why layer order matters
Docker **caches** layers: if an instruction and everything before it is
unchanged, it reuses the cache. So put rarely-changing steps first (install
deps) and frequently-changing steps last (copy source). Get this backwards and
every code change rebuilds everything.

## This project's pattern
`FROM nginx:alpine` gives you a production web server; `COPY html/ →
/usr/share/nginx/html/` lays your site on top. The base image already knows how
to start nginx, so you write almost nothing.

## Pitfalls
- `COPY . .` invalidating the cache on every change because you copied
  everything (use a `.dockerignore`).
- Editing files in a running container — changes vanish when it's recreated;
  images are immutable, rebuild instead.
- Using `:latest` — non-reproducible builds; pin tags.

## Real-world
This is how static sites, SPAs, and documentation get shipped — build artifacts
baked into an nginx image and rolled out behind a CDN or ingress.
