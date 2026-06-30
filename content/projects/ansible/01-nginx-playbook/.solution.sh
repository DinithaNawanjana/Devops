#!/bin/bash
set -e
mkdir -p /root/ansible
cat > /root/ansible/nginx.yml <<'YML'
- hosts: web
  become: true
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true
    - name: Ensure nginx running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
YML
