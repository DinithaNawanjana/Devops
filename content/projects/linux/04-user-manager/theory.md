# Deep Dive: User Management & Idempotent State

## Modelling state in a file
Real user management touches `/etc/passwd`, `useradd`, and PAM — privileged,
hard to test. This project teaches the *logic* against a simple
`user:fullname` database file, which is exactly how you'd prototype before
wiring in real system calls.

## Idempotence is the whole game
An operation is **idempotent** if running it twice has the same effect as
running it once. `add alice` must not create a duplicate the second time:
```bash
grep -q "^$user:" "$DB" || echo "$user:$full" >> "$DB"
```
The `grep -q … ||` guard is the canonical idempotent-append pattern. This single
idea is the foundation of configuration management (Ansible, Puppet) — every
"resource" is just an idempotent assertion about desired state.

## Argument dispatch with `case`
A subcommand CLI (`add`/`del`/`list`/`count`) is a `case "$1" in … esac`
dispatcher. Validate arity (`$#`) and print a usage line on the `*)` default.

## Editing in place
`sed -i "/^$user:/d" "$DB"` deletes a matching line. Anchoring with `^` and the
`:` delimiter prevents `alice` from also matching `alice2`.

## Common pitfalls
- Unanchored patterns deleting/ matching the wrong rows.
- Word-splitting on names with spaces — quote every expansion (`"$full"`).
- Race conditions if two runs edit the file at once (real tooling locks).

## Real-world
This is the mental model behind `useradd`/`userdel` wrappers, bulk onboarding
scripts, and the idempotent `user:` module in Ansible.
