# Project Tasks

In `/root/site/` build a containerized static site:

1. **`/root/site/html/index.html`** containing the text `Hello Docker`.
2. **`/root/site/Dockerfile`** that is `FROM nginx:alpine` and **COPYs** your
   `html/` into `/usr/share/nginx/html/`.

Then (in the lab terminal) build and run it:

```bash
cd /root/site
docker build -t static-site .
docker run -d --name web -p 8081:80 static-site
curl http://localhost:8081      # Hello Docker
```

Click **Check**.
