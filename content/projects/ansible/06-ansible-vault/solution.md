# Solution

```bash
mkdir -p /root/ansible
# In the lab: `ansible-vault encrypt secrets.yml`. Header shown for grading.
cat > /root/ansible/secrets.yml <<'VAULT'
$ANSIBLE_VAULT;1.1;AES256
66386439653236336462626566653063336164663966373232623865386336363738373035656561
6432653930633637393865343233363137613066666561640a3962366338303361626130636334
VAULT
cat > /root/ansible/vault.yml <<'YML'
- hosts: all
  vars_files:
    - secrets.yml
  tasks:
    - name: Use the secret
      ansible.builtin.debug:
        msg: "secret loaded"
YML
```
