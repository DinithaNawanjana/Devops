# Sandbox for the Kubernetes track: kubectl + kind + helm + a local cluster.
#   docker build -t lab-k8s:latest lab-images/lab-k8s
#
# kind runs a Kubernetes cluster in Docker, so this image expects access to a
# Docker daemon (dind sidecar or mounted socket) at lab time.
FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV KUBECTL_VERSION=v1.31.0
ENV KIND_VERSION=v0.24.0
ENV HELM_VERSION=v3.16.1

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git vim nano less bash \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" -o /usr/local/bin/kubectl \
    && curl -fsSL "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64" -o /usr/local/bin/kind \
    && curl -fsSL "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz" -o /tmp/helm.tgz \
    && tar -xzf /tmp/helm.tgz -C /tmp \
    && mv /tmp/linux-amd64/helm /usr/local/bin/helm \
    && rm -rf /tmp/helm.tgz /tmp/linux-amd64 \
    && chmod +x /usr/local/bin/kubectl /usr/local/bin/kind \
    && kubectl version --client && kind version && helm version

WORKDIR /root
CMD ["sleep", "infinity"]
