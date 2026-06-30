# Your Task

Two parts: a concept check, then a tiny cost script.

### Part 1 — Concept check

Create `/root/answers.txt` with these four lines (values are `IaaS`, `PaaS`, or
`SaaS`, or `AZ`):

```
most_control=<which model gives you the most control over the OS?>
managed_runtime=<which model runs your code but manages the OS/runtime?>
email_service=<Gmail is an example of which model?>
survive_dc_failure=<deploy across multiple WHAT to survive one datacenter failing? (answer: AZ)>
```

So the first line should read `most_control=IaaS`, and so on.

### Part 2 — Cost estimate

`setup.sh` created `/root/rate.txt` containing an hourly rate in USD. Write
`/root/cost.sh` that reads it and writes the **monthly** estimate
(`rate × 730`) to `/root/monthly_cost.txt`.

```bash
rate=$(cat /root/rate.txt)
awk -v r="$rate" 'BEGIN { printf "%.2f\n", r * 730 }' > /root/monthly_cost.txt
```

Click **Check** when both files are in place.
