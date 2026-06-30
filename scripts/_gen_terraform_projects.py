#!/usr/bin/env python3
"""Authoring helper: Terraform project set (spec §5). HCL authoring graded
structurally; learners run `terraform` for real in the lab-terraform sandbox.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "terraform"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


CLEAN = "#!/bin/sh\ncd /root || exit 0\nrm -rf tf\nmkdir -p tf\nexit 0\n"

# 01 docker container
proj(
    dir="01-docker-container", id="proj-tf-docker", title="Project: Local Docker Container",
    minutes=35, points=250, prereq="[docker-01]",
    theory="""# Project: Provision a Container with Terraform

The `kreuzwerker/docker` provider lets Terraform manage Docker. Declare a
`docker_image` and a `docker_container` resource, then `terraform apply`.
""",
    instructions="""# Project Tasks

Create `/root/tf/main.tf` that:

1. Configures the **`docker` provider**.
2. Declares a **`docker_image`** and a **`docker_container`** resource
   (e.g. an nginx container).

Run `terraform init && terraform apply` in the lab. Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

resource "docker_container" "web" {
  name  = "tf-web"
  image = docker_image.nginx.image_id
  ports {
    internal = 80
    external = 8080
  }
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q 'provider "docker"' "$F" && echo "STEP:docker provider configured:PASS" || { echo "STEP:docker provider configured:FAIL:add provider \\"docker\\""; fail=1; }
grep -q 'resource "docker_container"' "$F" && echo "STEP:declares a container resource:PASS" || { echo "STEP:declares a container resource:FAIL:add a docker_container resource"; fail=1; }
exit $fail
""",
)

# 02 variables + outputs
proj(
    dir="02-variables-outputs", id="proj-tf-vars", title="Project: Variables, Outputs & tfvars",
    minutes=35, points=250, prereq="[proj-tf-docker]",
    theory="""# Project: Parameterize with Variables

`variable` blocks make configs reusable; `output` blocks expose values;
`terraform.tfvars` supplies the values.
""",
    instructions="""# Project Tasks

In `/root/tf/`:

1. `variables.tf` with at least one **`variable`** block.
2. `outputs.tf` with at least one **`output`** block.
3. `terraform.tfvars` assigning the variable.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/variables.tf <<'TF'
variable "container_name" {
  type    = string
  default = "app"
}
variable "external_port" {
  type    = number
  default = 8080
}
TF
cat > /root/tf/outputs.tf <<'TF'
output "url" {
  value = "http://localhost:${var.external_port}"
}
TF
cat > /root/tf/terraform.tfvars <<'TF'
container_name = "myapp"
external_port  = 9090
TF
""",
    validate="""#!/bin/sh
fail=0
grep -q "^variable " /root/tf/variables.tf 2>/dev/null && echo "STEP:defines variables:PASS" || { echo "STEP:defines variables:FAIL:add a variable block in variables.tf"; fail=1; }
grep -q "^output " /root/tf/outputs.tf 2>/dev/null && echo "STEP:defines outputs:PASS" || { echo "STEP:defines outputs:FAIL:add an output block in outputs.tf"; fail=1; }
[ -f /root/tf/terraform.tfvars ] && echo "STEP:supplies a tfvars file:PASS" || { echo "STEP:supplies a tfvars file:FAIL:create terraform.tfvars"; fail=1; }
exit $fail
""",
)

# 03 module
proj(
    dir="03-reusable-module", id="proj-tf-module", title="Project: Reusable Module",
    minutes=45, points=300, prereq="[proj-tf-vars]",
    theory="""# Project: Modules

A module is a directory of `.tf` files you call from elsewhere with a `module`
block and a `source`.
""",
    instructions="""# Project Tasks

1. Create a module at `/root/tf/modules/webserver/main.tf`.
2. Call it from `/root/tf/main.tf` with a **`module`** block and a **`source`**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf/modules/webserver
cat > /root/tf/modules/webserver/main.tf <<'TF'
variable "name" { type = string }
resource "docker_container" "this" {
  name  = var.name
  image = "nginx:alpine"
}
TF
cat > /root/tf/main.tf <<'TF'
module "web" {
  source = "./modules/webserver"
  name   = "web-1"
}
TF
""",
    validate="""#!/bin/sh
fail=0
[ -f /root/tf/modules/webserver/main.tf ] && echo "STEP:module directory exists:PASS" || { echo "STEP:module directory exists:FAIL:create modules/webserver/main.tf"; fail=1; }
if grep -q "^module " /root/tf/main.tf 2>/dev/null && grep -q "source" /root/tf/main.tf 2>/dev/null; then echo "STEP:root calls the module:PASS"; else echo "STEP:root calls the module:FAIL:add a module block with source"; fail=1; fi
exit $fail
""",
)

# 04 remote state / backend
proj(
    dir="04-remote-state", id="proj-tf-backend", title="Project: Configure a Backend",
    minutes=35, points=250, prereq="[proj-tf-module]",
    theory="""# Project: State Backends

The `backend` block in `terraform {}` controls where state is stored — local
file, or an S3-style remote.
""",
    instructions="""# Project Tasks

Create `/root/tf/backend.tf` with a `terraform { backend "..." { } }` block
(a `local` backend with an explicit `path` is fine).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/backend.tf <<'TF'
terraform {
  backend "local" {
    path = "state/terraform.tfstate"
  }
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/backend.tf
fail=0
[ -f "$F" ] && echo "STEP:backend.tf exists:PASS" || { echo "STEP:backend.tf exists:FAIL:create tf/backend.tf"; exit 1; }
grep -q 'backend "' "$F" && echo "STEP:configures a backend:PASS" || { echo "STEP:configures a backend:FAIL:add a backend block"; fail=1; }
exit $fail
""",
)

# 05 workspaces
proj(
    dir="05-workspaces", id="proj-tf-workspaces", title="Project: Multi-env Workspaces",
    minutes=40, points=300, prereq="[proj-tf-backend]",
    theory="""# Project: Workspaces

`terraform workspace` keeps separate state per environment. Reference
`terraform.workspace` in your config to vary names/sizes by env.
""",
    instructions="""# Project Tasks

Create `/root/tf/main.tf` that uses **`terraform.workspace`** in a resource name
(so dev/stage/prod get distinct resources). Optionally add `/root/tf/setup-ws.sh`
that creates the `dev`, `stage`, `prod` workspaces.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_container" "app" {
  name  = "app-${terraform.workspace}"
  image = "nginx:alpine"
}
TF
cat > /root/tf/setup-ws.sh <<'SH'
#!/bin/sh
for ws in dev stage prod; do terraform workspace new "$ws" 2>/dev/null || true; done
SH
chmod +x /root/tf/setup-ws.sh
""",
    validate="""#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q "terraform.workspace" "$F" && echo "STEP:uses terraform.workspace:PASS" || { echo "STEP:uses terraform.workspace:FAIL:reference terraform.workspace"; fail=1; }
exit $fail
""",
)

# 06 vpc + subnets
proj(
    dir="06-vpc-subnets", id="proj-tf-vpc", title="Project: VPC + Subnets",
    minutes=45, points=300, prereq="[proj-tf-workspaces]",
    theory="""# Project: Network with VPC + Subnets

Model a network: an `aws_vpc` plus `aws_subnet`s (use `count` for several). Apply
against LocalStack or a real cloud.
""",
    instructions="""# Project Tasks

Create `/root/tf/network.tf` declaring an **`aws_vpc`** and one or more
**`aws_subnet`** resources.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/network.tf <<'TF'
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/network.tf
fail=0
[ -f "$F" ] && echo "STEP:network.tf exists:PASS" || { echo "STEP:network.tf exists:FAIL:create tf/network.tf"; exit 1; }
grep -q 'resource "aws_vpc"' "$F" && echo "STEP:declares a VPC:PASS" || { echo "STEP:declares a VPC:FAIL:add an aws_vpc resource"; fail=1; }
grep -q 'resource "aws_subnet"' "$F" && echo "STEP:declares subnets:PASS" || { echo "STEP:declares subnets:FAIL:add aws_subnet resources"; fail=1; }
exit $fail
""",
)

# 07 count / for_each
proj(
    dir="07-count-foreach", id="proj-tf-loops", title="Project: count & for_each",
    minutes=40, points=300, prereq="[proj-tf-vpc]",
    theory="""# Project: Dynamic Resources

`count` creates N copies; `for_each` iterates a set/map — both avoid copy-paste.
""",
    instructions="""# Project Tasks

Create `/root/tf/loops.tf` that uses **both** `count` (in one resource) and
**`for_each`** (in another).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/loops.tf <<'TF'
resource "docker_container" "workers" {
  count = 3
  name  = "worker-${count.index}"
  image = "nginx:alpine"
}

resource "docker_container" "services" {
  for_each = toset(["api", "web", "cache"])
  name     = each.key
  image    = "nginx:alpine"
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/loops.tf
fail=0
[ -f "$F" ] && echo "STEP:loops.tf exists:PASS" || { echo "STEP:loops.tf exists:FAIL:create tf/loops.tf"; exit 1; }
grep -q "count" "$F" && echo "STEP:uses count:PASS" || { echo "STEP:uses count:FAIL:use count in a resource"; fail=1; }
grep -q "for_each" "$F" && echo "STEP:uses for_each:PASS" || { echo "STEP:uses for_each:FAIL:use for_each in a resource"; fail=1; }
exit $fail
""",
)

# 08 import
proj(
    dir="08-import-existing", id="proj-tf-import", title="Project: Import Existing Infra",
    minutes=40, points=300, prereq="[proj-tf-loops]",
    theory="""# Project: Import into State

`terraform import <address> <id>` brings already-existing infrastructure under
Terraform management without recreating it.
""",
    instructions="""# Project Tasks

1. In `/root/tf/main.tf`, write the **resource block** for an existing container.
2. In `/root/tf/import.sh`, run **`terraform import`** mapping that resource to
   the real object id.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_container" "legacy" {
  name  = "legacy-app"
  image = "nginx:alpine"
}
TF
cat > /root/tf/import.sh <<'SH'
#!/bin/sh
# Bring the already-running container under management:
terraform import docker_container.legacy "$(docker ps -q --filter name=legacy-app)"
SH
chmod +x /root/tf/import.sh
""",
    validate="""#!/bin/sh
fail=0
grep -q 'resource "docker_container"' /root/tf/main.tf 2>/dev/null && echo "STEP:resource block defined:PASS" || { echo "STEP:resource block defined:FAIL:declare the resource to import into"; fail=1; }
grep -q "terraform import" /root/tf/import.sh 2>/dev/null && echo "STEP:runs terraform import:PASS" || { echo "STEP:runs terraform import:FAIL:import.sh should call terraform import"; fail=1; }
exit $fail
""",
)

# 09 terraform + ansible
proj(
    dir="09-terraform-ansible", id="proj-tf-ansible", title="Project: Terraform + Ansible",
    minutes=50, points=350, prereq="[proj-tf-import]",
    theory="""# Project: Provision then Configure

Terraform creates the infrastructure; a `local-exec` provisioner then hands off
to Ansible to configure it.
""",
    instructions="""# Project Tasks

Create `/root/tf/main.tf` with a resource (or `null_resource`) whose
**`provisioner "local-exec"`** runs **`ansible-playbook`** to configure it.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "null_resource" "configure" {
  provisioner "local-exec" {
    command = "ansible-playbook -i inventory.ini site.yml"
  }
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q "provisioner" "$F" && echo "STEP:uses a provisioner:PASS" || { echo "STEP:uses a provisioner:FAIL:add a local-exec provisioner"; fail=1; }
grep -q "ansible" "$F" && echo "STEP:hands off to Ansible:PASS" || { echo "STEP:hands off to Ansible:FAIL:run ansible-playbook from the provisioner"; fail=1; }
exit $fail
""",
)

# 10 mini-infra
proj(
    dir="10-mini-infra", id="proj-tf-infra", title="Project: Full Mini-Infra",
    minutes=60, points=450, prereq="[proj-tf-ansible]",
    theory="""# Project: Network + Compute + Storage

Tie it together: a network, compute, and storage resource — plus `output`s that
surface the important values.
""",
    instructions="""# Project Tasks

Create `/root/tf/main.tf` declaring at least **three resources** spanning
network, compute, and storage, plus at least one **`output`**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_network" "appnet" {
  name = "appnet"
}

resource "docker_volume" "data" {
  name = "appdata"
}

resource "docker_container" "app" {
  name     = "app"
  image    = "nginx:alpine"
  networks_advanced { name = docker_network.appnet.name }
  volumes {
    volume_name    = docker_volume.data.name
    container_path = "/data"
  }
}

output "container_name" {
  value = docker_container.app.name
}
TF
""",
    validate="""#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
n=$(grep -c '^resource ' "$F")
[ "${n:-0}" -ge 3 ] && echo "STEP:three+ resources (net/compute/storage):PASS" || { echo "STEP:three+ resources (net/compute/storage):FAIL:declare >=3 resources, found ${n:-0}"; fail=1; }
grep -q "^output " "$F" && echo "STEP:exposes an output:PASS" || { echo "STEP:exposes an output:FAIL:add an output block"; fail=1; }
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
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: terraform\n"
            f"level: intermediate\nestimated_minutes: {p['minutes']}\n"
            f"image: lab-terraform:latest\nprerequisites: {p['prereq']}\n"
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
    print(f"Wrote {len(PROJECTS)} terraform projects to {BASE}")


if __name__ == "__main__":
    main()
