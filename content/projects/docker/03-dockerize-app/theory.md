# Deep Dive: Writing a Good Application Dockerfile

## The job of a Dockerfile
Turn source code into a self-contained, runnable image: choose a base runtime,
install dependencies, copy code, declare the port, and define the start command.

## Instruction essentials
- `FROM python:3.11-alpine` — a minimal runtime base.
- `WORKDIR /app` — sets (and creates) the working directory.
- `COPY` — dependencies first (`requirements.txt`), then code, to exploit the
  layer cache.
- `EXPOSE 5000` — **documentation** of the listening port (it doesn't publish;
  `-p` does).
- `CMD ["python","app.py"]` — the default process. Exec-form (JSON array) runs
  without a shell, so signals (SIGTERM) reach your app for clean shutdown.

## CMD vs ENTRYPOINT
`CMD` is the default command (easily overridden); `ENTRYPOINT` is the fixed
executable with `CMD` as its default args. Use ENTRYPOINT for "this image *is* a
tool".

## Pitfalls
- Shell-form `CMD python app.py` wraps your app in `/bin/sh`, which swallows
  signals → slow/forced kills.
- Running as root (add a non-root `USER`).
- Copying the whole context without `.dockerignore` (slow, leaks secrets).

## Real-world
Every microservice ships as an image built from a Dockerfile like this; the
quality of the Dockerfile decides your image size, build speed, and security.
