# Deep Dive: Multi-stage Builds

## The fat-image problem
If you build *and* run in the same image, the final artifact carries compilers,
headers, dev dependencies, and build caches — bloating size and CVE surface. A
Go binary that's 10 MB can ship in a 900 MB image if you're careless.

## How multi-stage fixes it
Use several `FROM` stages in one Dockerfile. Earlier stages build; the final
stage starts from a slim base and `COPY --from=<stage>` only the finished
artifact. Build tools never reach the final image.
```dockerfile
FROM golang:alpine AS builder
RUN go build -o /app
FROM alpine          # or scratch / distroless
COPY --from=builder /app /app
```

## How small can you go
- `alpine` — ~5 MB, has a shell/package manager.
- `distroless` — no shell, just your app + runtime; smaller attack surface.
- `scratch` — empty; only works for fully static binaries.

## Pitfalls
- Copying more than the artifact (defeats the purpose).
- A `scratch`/distroless image with a dynamically-linked binary → "not found"
  at runtime (missing libc).
- Forgetting CA certs/timezone data that the slim base lacks.

## Real-world
Standard practice for compiled languages and even Node/Python (build deps in one
stage, runtime-only in the next); smaller images deploy and scale faster.
