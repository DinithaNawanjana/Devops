# Base sandbox for Linux / Bash / Shell-scripting / Networking labs.
#   docker build -t lab-linux:latest lab-images/lab-linux
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash coreutils findutils grep sed gawk \
      curl wget iputils-ping iproute2 dnsutils netcat-openbsd \
      vim nano less tree procps htop \
      python3 python3-pip \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Keep the container alive; the platform execs an interactive shell into it.
CMD ["sleep", "infinity"]
