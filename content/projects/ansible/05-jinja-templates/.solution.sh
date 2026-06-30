#!/bin/bash
set -e
mkdir -p /root/ansible/templates
cat > /root/ansible/templates/site.conf.j2 <<'J2'
server {
    listen {{ http_port }};
    server_name {{ domain }};
}
J2
cat > /root/ansible/template.yml <<'YML'
- hosts: web
  become: true
  vars:
    http_port: 80
    domain: example.com
  tasks:
    - name: Render nginx config
      ansible.builtin.template:
        src: templates/site.conf.j2
        dest: /etc/nginx/conf.d/site.conf
YML
