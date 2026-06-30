#!/usr/bin/env python3
"""Generate content/tracks/<slug>/track.yaml for the full curriculum (spec §4).

Idempotent — safe to re-run. Edit the TRACKS list to adjust the catalog.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS_DIR = ROOT / "content" / "tracks"

# (slug, title, level, description)
TRACKS = [
    # 🟢 Beginner
    ("linux", "Linux Fundamentals", "beginner", "Filesystem, permissions, processes, package management."),
    ("bash", "Command Line & Bash", "beginner", "Navigation, pipes, redirection, globbing."),
    ("shell-scripting", "Shell Scripting", "beginner", "Variables, loops, conditionals, functions, cron."),
    ("networking", "Networking Basics", "beginner", "TCP/IP, DNS, HTTP(S), ports, firewalls, SSH."),
    ("git", "Git & Version Control", "beginner", "Branching, merging, rebasing, GitHub/GitLab."),
    ("python-devops", "Python for DevOps", "beginner", "Scripting, requests, file/OS handling, virtualenv."),
    ("cloud-concepts", "Cloud Concepts", "beginner", "IaaS/PaaS/SaaS, regions/AZ, VMs, billing basics."),
    # 🟡 Intermediate
    ("docker", "Docker", "intermediate", "Images, containers, Dockerfile, volumes, networks, Compose."),
    ("cicd", "CI/CD Fundamentals", "intermediate", "Jenkins, GitHub Actions, GitLab CI pipelines."),
    ("ansible", "Ansible", "intermediate", "Inventory, playbooks, roles, templating, vault."),
    ("terraform", "Terraform (Intro)", "intermediate", "Providers, resources, state, variables, outputs."),
    ("cloud-core", "AWS / Azure / GCP Core", "intermediate", "Compute, storage, IAM, networking (VPC)."),
    ("web-servers", "Web Servers & Proxies", "intermediate", "Nginx, Apache, reverse proxy, TLS, load balancing."),
    # 🟠 Advanced
    ("kubernetes", "Kubernetes Core", "advanced", "Pods, deployments, services, ingress, configmaps, secrets."),
    ("advanced-cicd", "Advanced CI/CD", "advanced", "Multi-stage pipelines, testing, artifacts, blue-green/canary."),
    ("terraform-advanced", "Terraform Advanced", "advanced", "Modules, remote state, workspaces, provisioners."),
    ("monitoring", "Monitoring & Observability", "advanced", "Prometheus, Grafana, Loki, alerting."),
    ("logging", "Logging Stack", "advanced", "ELK / EFK, log aggregation, parsing."),
    ("devsecops", "DevSecOps", "advanced", "SAST/DAST, image scanning, secrets mgmt, policy-as-code."),
    # 🔴 Expert
    ("kubernetes-advanced", "Kubernetes Advanced", "expert", "Helm, Operators, CRDs, HPA/VPA, multi-cluster."),
    ("gitops", "GitOps", "expert", "ArgoCD, FluxCD, declarative delivery."),
    ("service-mesh", "Service Mesh", "expert", "Istio, Linkerd, traffic management, mTLS."),
    ("sre", "SRE Practices", "expert", "SLI/SLO/SLA, error budgets, incident response, on-call."),
    ("platform-engineering", "Platform Engineering", "expert", "Internal Developer Platforms, Backstage, golden paths."),
    ("chaos-engineering", "Chaos Engineering", "expert", "Fault injection, resilience testing (Litmus, Chaos Mesh)."),
    ("finops", "FinOps", "expert", "Cloud cost analysis, optimization, tagging strategies."),
]


def main() -> None:
    for order, (slug, title, level, desc) in enumerate(TRACKS, start=1):
        d = TRACKS_DIR / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "track.yaml").write_text(
            f"slug: {slug}\n"
            f"title: \"{title}\"\n"
            f"level: {level}\n"
            f"order_index: {order}\n"
            f"description: \"{desc}\"\n",
            encoding="utf-8",
        )
    print(f"Wrote {len(TRACKS)} track.yaml files to {TRACKS_DIR}")


if __name__ == "__main__":
    main()
