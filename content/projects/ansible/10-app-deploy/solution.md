# Solution

```bash
mkdir -p /root/ansible
cat > /root/ansible/deploy.yml <<'YML'
- hosts: web
  become: true
  tasks:
    - name: Clone the app
      ansible.builtin.git:
        repo: https://example.com/app.git
        dest: /opt/app
        version: main
    - name: Start the service
      ansible.builtin.service:
        name: app
        state: started
        enabled: true
    - name: Health check
      ansible.builtin.uri:
        url: http://localhost:8080/health
        status_code: 200
YML
```
