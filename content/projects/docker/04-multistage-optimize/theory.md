# Project: Multi-stage Build

A multi-stage Dockerfile builds artifacts in a fat "builder" stage, then copies
only the result into a slim final image — smaller, fewer CVEs.

```dockerfile
FROM golang:alpine AS builder
RUN go build -o /app ...
FROM alpine
COPY --from=builder /app /app
```
