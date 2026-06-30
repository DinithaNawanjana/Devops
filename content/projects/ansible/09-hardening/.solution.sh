#!/bin/bash
set -e
mkdir -p /root/ansible
cat > /root/ansible/harden.yml <<'YML'
- hosts: all
  become: true
  tasks:
    - name: Disable root SSH login
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
    - name: Enable UFW firewall
      community.general.ufw:
        state: enabled
        policy: deny
YML
