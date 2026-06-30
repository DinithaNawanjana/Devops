# Solution

```bash
mkdir -p /root/ansible/roles/web/tasks
cat > /root/ansible/roles/web/tasks/main.yml <<'YML'
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
YML
cat > /root/ansible/site.yml <<'YML'
- hosts: web
  become: true
  roles:
    - web
YML
```
