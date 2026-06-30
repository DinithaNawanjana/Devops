# Project: Containerize a Static Site

Package a static website into an Nginx image. The pattern: `FROM nginx:alpine`,
then `COPY` your HTML into `/usr/share/nginx/html/`.
