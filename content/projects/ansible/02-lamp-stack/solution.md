# Solution

```bash
mkdir -p /root/ansible
cat > /root/ansible/lamp.yml <<'YML'
- hosts: web
  become: true
  tasks:
    - name: Install LAMP packages
      ansible.builtin.apt:
        name:
          - apache2
          - mysql-server
          - php
        state: present
        update_cache: true
YML
```
