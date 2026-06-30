# Run Your First Container

A **container** is an isolated process tree with its own filesystem, created
from an **image** (a read-only template).

## Core commands

```bash
docker run hello-world          # pull + run a container
docker run -d nginx             # detached (background)
docker run -d --name web -p 8080:80 nginx
docker ps                       # list running containers
docker ps -a                    # include stopped
docker images                   # list local images
docker logs <name>              # view container output
docker exec -it <name> sh       # shell into a running container
docker stop <name>              # stop
docker rm <name>                # remove
```

## Port publishing

`-p HOST:CONTAINER` maps a host port to a container port. With
`-p 8080:80`, traffic to host `:8080` reaches Nginx on `:80` in the container.

## Naming

`--name web` gives the container a stable name so you don't have to copy IDs.

> This lab runs **Docker-in-Docker** — the daemon inside your sandbox is
> isolated from the host, so experiment freely.
