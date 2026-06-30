# Base sandbox for Linux / Bash / Shell-scripting / Networking labs.
#   docker build -t lab-linux:latest lab-images/lab-linux
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash coreutils findutils grep sed gawk jq \
      curl wget iputils-ping iproute2 dnsutils netcat-openbsd openssh-client \
      git \
      vim nano less tree procps htop \
      python3 python3-pip python3-venv \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Default git identity so learners can commit immediately.
RUN git config --system user.email "learner@devops.local" \
    && git config --system user.name "DevOps Learner" \
    && git config --system init.defaultBranch main

WORKDIR /root

# Keep the container alive; the platform execs an interactive shell into it.
CMD ["sleep", "infinity"]
