# Sandbox for the Terraform track. Includes the Docker provider use-case tools.
#   docker build -t lab-terraform:latest lab-images/lab-terraform
FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TERRAFORM_VERSION=1.9.8

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip git ca-certificates vim nano less \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -o /tmp/tf.zip \
    && unzip /tmp/tf.zip -d /usr/local/bin \
    && rm /tmp/tf.zip \
    && terraform version

WORKDIR /root
CMD ["sleep", "infinity"]
