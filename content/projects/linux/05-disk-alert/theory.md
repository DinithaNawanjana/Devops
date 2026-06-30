# Deep Dive: Threshold Alerting

## Anatomy of an alert
Every alert has the same skeleton: **measure → compare to a threshold → act
(notify) → record**. Get this right in Bash and you understand the core loop
that Prometheus Alertmanager, Nagios, and CloudWatch all formalize.

## Measuring disk usage cleanly
```bash
usage=$(df -P / | awk 'NR==2 {gsub("%","",$5); print $5}')
```
- `df -P` forces POSIX single-line output (no wrapping on long device names).
- `NR==2` skips the header row.
- `gsub("%","",$5)` strips the percent sign so `$5` is a plain integer you can
  compare with `-gt`.

## Comparison & exit semantics
`[ "$usage" -gt "$threshold" ]` does an integer test. Decide what the script's
**exit code** means — a non-zero exit when over threshold lets cron or a CI step
treat the alert as a failure.

## Why log every run
Alerting that only speaks up on failure hides *whether it ran at all*. Appending
`date usage threshold` every run gives you a heartbeat — silence then means the
checker itself died, which is its own alert.

## Common pitfalls
- Comparing the raw `45%` string numerically — the `%` makes it non-numeric.
- Off-by-one on `>` vs `>=` at the boundary.
- Hard-coding the mount point; parameterise it.

## Real-world
This is a textfile-collector script for `node_exporter`, a classic cron
disk-space guard, and the conceptual ancestor of a Prometheus
`predict_linear()` "disk will fill in 4h" alert.
