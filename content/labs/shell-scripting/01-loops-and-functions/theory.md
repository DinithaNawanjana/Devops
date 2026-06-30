# Loops, Conditionals & Functions

Bash scripts turn one-off commands into reusable tools.

## Variables & arguments

```bash
name="world"
echo "hello $name"
echo "first arg: $1"     # positional argument
echo "all args: $@"
```

## Conditionals

```bash
if [ "$1" = "start" ]; then
  echo "starting"
elif [ -f /etc/config ]; then
  echo "config exists"
else
  echo "nothing to do"
fi
```

Common test flags: `-f` file exists, `-d` dir exists, `-z` empty string,
`-n` non-empty, `-eq/-lt/-gt` numeric comparisons.

## Loops

```bash
for i in 1 2 3; do echo "$i"; done
for f in *.txt; do echo "$f"; done

n=0
while [ "$n" -lt 3 ]; do echo "$n"; n=$((n+1)); done
```

## Functions

```bash
greet() {
  local who="$1"
  echo "hi $who"
}
greet "alice"
```

## Exit codes

`exit 0` = success, non-zero = failure. `$?` holds the last command's code.
