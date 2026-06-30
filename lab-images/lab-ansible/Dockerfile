# Sandbox for the Ansible track.
#   docker build -t lab-ansible:latest lab-images/lab-ansible
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      openssh-client sshpass git curl vim nano less \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir ansible-core ansible-lint jinja2

# A localhost inventory so learners can run playbooks against the sandbox.
RUN mkdir -p /etc/ansible \
    && printf 'localhost ansible_connection=local\n' > /etc/ansible/hosts

WORKDIR /root
CMD ["sleep", "infinity"]
