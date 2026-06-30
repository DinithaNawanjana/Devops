# Solution

```bash
mkdir -p /root/ansible
cat > /root/ansible/rolling.yml <<'YML'
- hosts: web
  become: true
  serial: 1
  tasks:
    - name: Deploy new version
      ansible.builtin.copy:
        content: "v2\n"
        dest: /opt/app/version
      notify: restart app
  handlers:
    - name: restart app
      ansible.builtin.service:
        name: app
        state: restarted
YML
```
