# Solution

```bash
mkdir -p /root/ansible/group_vars
cat > /root/ansible/inventory.ini <<'INI'
[web]
web1 ansible_host=10.0.0.1

[db]
db1 ansible_host=10.0.0.2

[cache]
cache1 ansible_host=10.0.0.3
INI
cat > /root/ansible/group_vars/web.yml <<'YML'
http_port: 80
YML
```
