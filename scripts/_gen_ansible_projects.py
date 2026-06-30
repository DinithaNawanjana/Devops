#!/usr/bin/env python3
"""Authoring helper: Ansible project set (spec §5). Playbook/role/inventory
authoring graded structurally (deterministic). Learners can actually run these
in the lab-ansible sandbox. Standard folder format + reference solution.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "ansible"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


# 01 nginx playbook
proj(
    dir="01-nginx-playbook", id="proj-ans-nginx", title="Project: Nginx Playbook",
    minutes=35, points=250, prereq="[linux-01]",
    theory="""# Project: Install & Configure Nginx

A playbook is a YAML list of plays: each targets `hosts:`, may `become:` root,
and runs `tasks:` using modules like `apt` and `service`.
""",
    instructions="""# Project Tasks

Create `/root/ansible/nginx.yml` — a play that:

1. Targets a `web` host group and uses `become`.
2. **Installs nginx** (apt/package module).
3. Ensures the **nginx service is started** (service module).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
F=/root/ansible/nginx.yml
fail=0
[ -f "$F" ] && echo "STEP:nginx.yml exists:PASS" || { echo "STEP:nginx.yml exists:FAIL:create ansible/nginx.yml"; exit 1; }
grep -q "hosts:" "$F" && grep -q "tasks:" "$F" && echo "STEP:targets hosts with tasks:PASS" || { echo "STEP:targets hosts with tasks:FAIL:add hosts: and tasks:"; fail=1; }
grep -q "nginx" "$F" && echo "STEP:installs nginx:PASS" || { echo "STEP:installs nginx:FAIL:install the nginx package"; fail=1; }
grep -q "service:" "$F" && echo "STEP:manages the service:PASS" || { echo "STEP:manages the service:FAIL:use the service module"; fail=1; }
exit $fail
""",
)

# 02 LAMP/LEMP
proj(
    dir="02-lamp-stack", id="proj-ans-lamp", title="Project: Provision a LAMP Stack",
    minutes=45, points=300, prereq="[proj-ans-nginx]",
    theory="""# Project: LAMP / LEMP Stack

Install a web server, a database, and PHP in one play, then enable the services.
""",
    instructions="""# Project Tasks

Create `/root/ansible/lamp.yml` that installs a **web server** (apache2 or
nginx), **mysql-server**, and **php** in a single play.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
F=/root/ansible/lamp.yml
fail=0
[ -f "$F" ] && echo "STEP:lamp.yml exists:PASS" || { echo "STEP:lamp.yml exists:FAIL:create ansible/lamp.yml"; exit 1; }
grep -qiE "apache2|nginx" "$F" && echo "STEP:installs a web server:PASS" || { echo "STEP:installs a web server:FAIL:install apache2 or nginx"; fail=1; }
grep -qi "mysql" "$F" && echo "STEP:installs mysql:PASS" || { echo "STEP:installs mysql:FAIL:install mysql-server"; fail=1; }
grep -qi "php" "$F" && echo "STEP:installs php:PASS" || { echo "STEP:installs php:FAIL:install php"; fail=1; }
exit $fail
""",
)

# 03 user + ssh keys
proj(
    dir="03-user-ssh-keys", id="proj-ans-users", title="Project: Users & SSH Keys",
    minutes=35, points=250, prereq="[proj-ans-lamp]",
    theory="""# Project: User & SSH Key Management

The `user` module creates accounts; `authorized_key` installs SSH public keys —
the basis of passwordless, auditable access.
""",
    instructions="""# Project Tasks

Create `/root/ansible/users.yml` that:

1. Creates a `deploy` **user** (user module).
2. Installs an SSH public key for it (**authorized_key** module).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
F=/root/ansible/users.yml
fail=0
[ -f "$F" ] && echo "STEP:users.yml exists:PASS" || { echo "STEP:users.yml exists:FAIL:create ansible/users.yml"; exit 1; }
grep -q "user:" "$F" && echo "STEP:creates a user:PASS" || { echo "STEP:creates a user:FAIL:use the user module"; fail=1; }
grep -q "authorized_key" "$F" && echo "STEP:installs an SSH key:PASS" || { echo "STEP:installs an SSH key:FAIL:use authorized_key"; fail=1; }
exit $fail
""",
)

# 04 role
proj(
    dir="04-web-role", id="proj-ans-role", title="Project: Role-based Web Tier",
    minutes=45, points=300, prereq="[proj-ans-users]",
    theory="""# Project: Roles

Roles package tasks/handlers/templates into a reusable unit under `roles/<name>/`.
A play then just lists `roles:`.
""",
    instructions="""# Project Tasks

Build a `web` role:

1. `/root/ansible/roles/web/tasks/main.yml` with at least one task.
2. `/root/ansible/site.yml` — a play that applies the role via `roles:`.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible/roles/web/tasks\nexit 0\n",
    solution="""mkdir -p /root/ansible/roles/web/tasks
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
""",
    validate="""#!/bin/sh
fail=0
[ -f /root/ansible/roles/web/tasks/main.yml ] && echo "STEP:role tasks/main.yml exists:PASS" || { echo "STEP:role tasks/main.yml exists:FAIL:create roles/web/tasks/main.yml"; fail=1; }
[ -f /root/ansible/site.yml ] && grep -q "roles:" /root/ansible/site.yml && echo "STEP:play applies the role:PASS" || { echo "STEP:play applies the role:FAIL:site.yml should list roles: - web"; fail=1; }
grep -q "nginx" /root/ansible/roles/web/tasks/main.yml 2>/dev/null && echo "STEP:role does real work:PASS" || { echo "STEP:role does real work:FAIL:add a task to the role"; fail=1; }
exit $fail
""",
)

# 05 jinja templates
proj(
    dir="05-jinja-templates", id="proj-ans-jinja", title="Project: Jinja2 Templates",
    minutes=40, points=250, prereq="[proj-ans-role]",
    theory="""# Project: Templated Config

The `template` module renders a Jinja2 `.j2` file with variables into a config
on the target.
""",
    instructions="""# Project Tasks

1. Create `/root/ansible/templates/site.conf.j2` using at least one Jinja2
   variable (`{{ ... }}`).
2. Create `/root/ansible/template.yml` that defines `vars:` and uses the
   **template** module to render it.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible/templates\nexit 0\n",
    solution="""mkdir -p /root/ansible/templates
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
""",
    validate="""#!/bin/sh
fail=0
J=/root/ansible/templates/site.conf.j2
[ -f "$J" ] && grep -q "{{" "$J" && echo "STEP:Jinja2 template with a variable:PASS" || { echo "STEP:Jinja2 template with a variable:FAIL:create templates/site.conf.j2 with {{ var }}"; fail=1; }
P=/root/ansible/template.yml
[ -f "$P" ] && grep -q "template:" "$P" && echo "STEP:uses the template module:PASS" || { echo "STEP:uses the template module:FAIL:use ansible template module"; fail=1; }
grep -q "vars:" "$P" 2>/dev/null && echo "STEP:defines variables:PASS" || { echo "STEP:defines variables:FAIL:define vars: in the play"; fail=1; }
exit $fail
""",
)

# 06 vault
proj(
    dir="06-ansible-vault", id="proj-ans-vault", title="Project: Ansible Vault",
    minutes=35, points=300, prereq="[proj-ans-jinja]",
    theory="""# Project: Encrypted Secrets with Vault

`ansible-vault encrypt` turns a vars file into ciphertext (a file beginning with
`$ANSIBLE_VAULT;1.1;AES256`). A play loads it via `vars_files`.
""",
    instructions="""# Project Tasks

1. Create an **encrypted** vars file `/root/ansible/secrets.yml`
   (`ansible-vault encrypt` — it must begin with `$ANSIBLE_VAULT`).
2. Create `/root/ansible/vault.yml` that loads it via **`vars_files`**.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
fail=0
S=/root/ansible/secrets.yml
[ -f "$S" ] && head -1 "$S" | grep -q '\\$ANSIBLE_VAULT' && echo "STEP:secrets.yml is vault-encrypted:PASS" || { echo "STEP:secrets.yml is vault-encrypted:FAIL:encrypt secrets.yml with ansible-vault"; fail=1; }
P=/root/ansible/vault.yml
[ -f "$P" ] && grep -q "vars_files:" "$P" && echo "STEP:play loads the vault file:PASS" || { echo "STEP:play loads the vault file:FAIL:reference secrets.yml via vars_files"; fail=1; }
exit $fail
""",
)

# 07 rolling update
proj(
    dir="07-rolling-update", id="proj-ans-rolling", title="Project: Rolling Update",
    minutes=40, points=300, prereq="[proj-ans-vault]",
    theory="""# Project: Rolling Updates & Handlers

`serial:` updates hosts in batches for zero downtime; a `notify` triggers a
`handler` (e.g. restart) only when something changed.
""",
    instructions="""# Project Tasks

Create `/root/ansible/rolling.yml` that:

1. Uses **`serial:`** to update hosts in batches.
2. Has a task that **`notify`**s a **handler** (e.g. restart the app).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
cat > /root/ansible/rolling.yml <<'YML'
- hosts: web
  become: true
  serial: 1
  tasks:
    - name: Deploy new version
      ansible.builtin.copy:
        content: "v2\\n"
        dest: /opt/app/version
      notify: restart app
  handlers:
    - name: restart app
      ansible.builtin.service:
        name: app
        state: restarted
YML
""",
    validate="""#!/bin/sh
F=/root/ansible/rolling.yml
fail=0
[ -f "$F" ] && echo "STEP:rolling.yml exists:PASS" || { echo "STEP:rolling.yml exists:FAIL:create ansible/rolling.yml"; exit 1; }
grep -q "serial:" "$F" && echo "STEP:batched with serial:PASS" || { echo "STEP:batched with serial:FAIL:add serial:"; fail=1; }
grep -q "handlers:" "$F" && grep -q "notify:" "$F" && echo "STEP:notify triggers a handler:PASS" || { echo "STEP:notify triggers a handler:FAIL:add a handler and notify it"; fail=1; }
exit $fail
""",
)

# 08 inventory groups
proj(
    dir="08-inventory-groups", id="proj-ans-inventory", title="Project: Inventory & Group Vars",
    minutes=35, points=250, prereq="[proj-ans-rolling]",
    theory="""# Project: Inventory Groups

Group hosts (`[web]`, `[db]`, `[cache]`) in an inventory; `group_vars/<group>.yml`
sets variables per group.
""",
    instructions="""# Project Tasks

1. Create `/root/ansible/inventory.ini` with **`[web]`, `[db]`, `[cache]`**
   groups (at least one host each).
2. Create `/root/ansible/group_vars/web.yml` with a variable.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible/group_vars\nexit 0\n",
    solution="""mkdir -p /root/ansible/group_vars
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
""",
    validate="""#!/bin/sh
F=/root/ansible/inventory.ini
fail=0
if [ -f "$F" ] && grep -q "\\[web\\]" "$F" && grep -q "\\[db\\]" "$F" && grep -q "\\[cache\\]" "$F"; then
  echo "STEP:inventory has web/db/cache groups:PASS"
else echo "STEP:inventory has web/db/cache groups:FAIL:define [web] [db] [cache]"; fail=1; fi
[ -f /root/ansible/group_vars/web.yml ] && echo "STEP:group_vars for web:PASS" || { echo "STEP:group_vars for web:FAIL:create group_vars/web.yml"; fail=1; }
exit $fail
""",
)

# 09 hardening
proj(
    dir="09-hardening", id="proj-ans-harden", title="Project: Server Hardening",
    minutes=45, points=300, prereq="[proj-ans-inventory]",
    theory="""# Project: Idempotent Hardening

Baseline security: disable root SSH login, enable a firewall — written
idempotently with `lineinfile`/modules so re-runs are safe.
""",
    instructions="""# Project Tasks

Create `/root/ansible/harden.yml` that:

1. **Disables root SSH login** (set `PermitRootLogin no` in sshd_config, e.g.
   via the **lineinfile** module).
2. Enables a firewall (ufw or similar).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
F=/root/ansible/harden.yml
fail=0
[ -f "$F" ] && echo "STEP:harden.yml exists:PASS" || { echo "STEP:harden.yml exists:FAIL:create ansible/harden.yml"; exit 1; }
grep -q "PermitRootLogin" "$F" && echo "STEP:disables root SSH login:PASS" || { echo "STEP:disables root SSH login:FAIL:set PermitRootLogin no"; fail=1; }
grep -q "lineinfile:" "$F" && echo "STEP:uses an idempotent module:PASS" || { echo "STEP:uses an idempotent module:FAIL:use lineinfile for the edit"; fail=1; }
grep -qiE "ufw|firewall|iptables" "$F" && echo "STEP:enables a firewall:PASS" || { echo "STEP:enables a firewall:FAIL:enable ufw/firewall"; fail=1; }
exit $fail
""",
)

# 10 app deploy
proj(
    dir="10-app-deploy", id="proj-ans-deploy", title="Project: Full App Deployment",
    minutes=55, points=400, prereq="[proj-ans-harden]",
    theory="""# Project: Full App Deployment

End to end: clone the repo, lay down config, start the service, and verify it
with a health check (`uri` module).
""",
    instructions="""# Project Tasks

Create `/root/ansible/deploy.yml` that:

1. **Clones** an app repo (git module).
2. **Starts the service** (service module).
3. **Health-checks** it (uri module against a URL).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf ansible\nmkdir -p ansible\nexit 0\n",
    solution="""mkdir -p /root/ansible
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
""",
    validate="""#!/bin/sh
F=/root/ansible/deploy.yml
fail=0
[ -f "$F" ] && echo "STEP:deploy.yml exists:PASS" || { echo "STEP:deploy.yml exists:FAIL:create ansible/deploy.yml"; exit 1; }
grep -q "git:" "$F" && echo "STEP:clones the repo:PASS" || { echo "STEP:clones the repo:FAIL:use the git module"; fail=1; }
grep -q "service:" "$F" && echo "STEP:starts the service:PASS" || { echo "STEP:starts the service:FAIL:use the service module"; fail=1; }
grep -q "uri:" "$F" && echo "STEP:runs a health check:PASS" || { echo "STEP:runs a health check:FAIL:use the uri module"; fail=1; }
exit $fail
""",
)


def write_exec(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    for p in PROJECTS:
        d = BASE / p["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "project.yaml").write_text(
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: ansible\n"
            f"level: intermediate\nestimated_minutes: {p['minutes']}\n"
            f"image: lab-ansible:latest\nprerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n", encoding="utf-8"
        )
        write_exec(d / ".solution.sh", "#!/bin/bash\nset -e\n" + p["solution"])
    print(f"Wrote {len(PROJECTS)} ansible projects to {BASE}")


if __name__ == "__main__":
    main()
