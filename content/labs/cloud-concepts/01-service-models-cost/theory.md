# Cloud Service Models & Cost Basics

## IaaS / PaaS / SaaS

| Model | You manage | Provider manages | Example |
|-------|-----------|------------------|---------|
| **IaaS** | OS, runtime, app | Hardware, virtualization | EC2, Compute Engine |
| **PaaS** | Just your app/code | OS, runtime, scaling | App Engine, Heroku, RDS |
| **SaaS** | Nothing (just use it) | Everything | Gmail, Salesforce |

Rule of thumb: **IaaS = most control**, **SaaS = least effort**.

## Regions & Availability Zones

- A **Region** is a geographic location (e.g. `us-east-1`).
- Each region has multiple **Availability Zones (AZ)** — isolated datacenters.
- Deploy across **multiple AZs** to survive a single datacenter failure;
  deploy across **regions** for geographic resilience / lower latency.

## Cost basics

Most compute is billed **per hour** (or per second). A rough monthly estimate:

```
monthly_cost = hourly_rate × 730        # ~730 hours in an average month
```

Tagging resources and watching this number is the foundation of **FinOps**.
