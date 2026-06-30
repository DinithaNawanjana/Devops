# Deep Dive: Interactive TUIs in Bash

## When a menu is the right interface
For runbooks and guided ops tools, a menu-driven script is friendlier than a
pile of flags — operators pick an action instead of memorizing syntax. The
pattern is a `while` loop around a `read` and a `case` dispatch.

## The loop
```bash
while true; do
  print_menu
  read -r choice || break      # `|| break` handles EOF (Ctrl-D / piped input)
  case "$choice" in
    1) action_one ;;
    q|Q) break ;;
    *) echo "unknown choice" ;;
  esac
done
```

## Reading input robustly
- `read -r` — the `-r` stops backslashes being interpreted; almost always what
  you want.
- The `|| break` on `read` is crucial: when input is **piped** (or the user
  hits Ctrl-D), `read` returns non-zero at EOF. Without the guard you get an
  infinite loop. This is also what makes the tool **scriptable/testable**:
  `printf '1\nq\n' | ./admin.sh`.

## Separating presentation from logic
Keep each action in its own function. The menu just routes; functions do the
work. This is the same MVC instinct that scales to real apps.

## Common pitfalls
- No EOF handling → infinite loop when piped.
- Unquoted `$choice` in tests.
- Doing heavy work inline so the tool can't be unit-tested.

## Real-world
Installer TUIs, `raspi-config`, interactive deployment helpers, and "break-glass"
operator consoles all use this shape.
