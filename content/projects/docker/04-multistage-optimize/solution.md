# Solution

```bash
mkdir -p /root/ms
cat > /root/ms/Dockerfile <<'DF'
FROM alpine:3.19 AS builder
RUN mkdir -p /out && echo "built artifact" > /out/app.txt

FROM alpine:3.19
COPY --from=builder /out/app.txt /app/app.txt
CMD ["cat", "/app/app.txt"]
DF
```
