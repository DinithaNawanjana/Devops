#!/bin/bash
set -e
mkdir -p /root/ansible
cat > /root/ansible/users.yml <<'YML'
- hosts: all
  become: true
  tasks:
    - name: Create deploy user
      ansible.builtin.user:
        name: deploy
        shell: /bin/bash
    - name: Install SSH key
      ansible.posix.authorized_key:
        user: deploy
        key: "{{ lookup('file', 'id_rsa.pub') }}"
YML
