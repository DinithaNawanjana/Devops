# Ports, HTTP & Sockets

Services listen on **ports**. A client connects to `host:port` to talk to them.
Web servers conventionally use `80` (HTTP) and `443` (HTTPS), but you can run
one on any free port.

## Spinning up a quick server

Python ships a one-liner static server:

```bash
python3 -m http.server 8000        # serves the current dir on :8000
```

## Talking to it

```bash
curl http://localhost:8000/                 # fetch the index
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/   # just the status
curl -I http://localhost:8000/              # headers only
```

## Inspecting ports

```bash
ss -ltnp            # listening TCP sockets (with PIDs)
nc -z localhost 8000 && echo "open"   # is the port open?
```

## HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 301/302 | Redirect |
| 404 | Not Found |
| 500 | Server Error |

In this lab you'll start a server, query it, and capture the results to files.
