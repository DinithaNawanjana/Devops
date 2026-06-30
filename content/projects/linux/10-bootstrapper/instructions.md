# Project Tasks

`setup.sh` created `/root/packages.txt` (one package per line). Write
`/root/bootstrap.sh <name>` that scaffolds `/root/<name>/`:

1. Create the directories `src/`, `bin/`, and `config/` under `/root/<name>/`.
2. Write `/root/<name>/README.md` whose first line contains the project `<name>`.
3. Read `/root/packages.txt` and write `/root/<name>/installed.txt` with one
   line per package, each formatted `installed: <package>`.

Run `./bootstrap.sh myapp`, then click **Check** (the checker uses `myapp`).
