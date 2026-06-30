#!/usr/bin/env python3
"""Authoring helper: the Git project set (spec §5). Standard folder format.

Git projects are verified by inspecting repository end-state, so each ships
`_solution_cmds` (the commands a learner runs) embedded in solution.md and used
by scripts/_test_git_projects.sh: setup -> solution_cmds -> validate.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "git"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


GITCFG = 'git config user.email "l@d.local"; git config user.name "L"'

# ── 01 Repo bootstrap ────────────────────────────────────
proj(
    dir="01-repo-setup", id="proj-git-repo", title="Project: Bootstrap a Repo",
    minutes=30, points=200, prereq="[git-01]",
    theory="""# Project: Bootstrap a Repo

Every project starts the same way: a repo, a sensible `.gitignore`, a `README`,
and a branching model (`main` for releases, `develop` for integration).
""",
    instructions="""# Project Tasks

Work in `/root/repo` (an empty git repo on `main`). Set it up properly:

1. Create a **`.gitignore`** containing at least `node_modules/` and `*.log`.
2. Create a **`README.md`** and commit it (plus `.gitignore`) on `main`.
3. Create a **`develop`** branch.

Click **Check** when done.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
exit 0
""",
    solution="""cd /root/repo
printf 'node_modules/\\n*.log\\n' > .gitignore
echo "# My Project" > README.md
git add .gitignore README.md
git commit -qm "chore: initial project scaffold"
git branch develop
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -f .gitignore ] && grep -q "node_modules" .gitignore && grep -q "\\*.log" .gitignore; then
  echo "STEP:.gitignore has patterns:PASS"; else echo "STEP:.gitignore has patterns:FAIL:add node_modules/ and *.log"; fail=1; fi
if git cat-file -p main:README.md >/dev/null 2>&1; then
  echo "STEP:README committed on main:PASS"; else echo "STEP:README committed on main:FAIL:commit README.md"; fail=1; fi
if git rev-parse --verify develop >/dev/null 2>&1; then
  echo "STEP:develop branch exists:PASS"; else echo "STEP:develop branch exists:FAIL:create a develop branch"; fail=1; fi
exit $fail
""",
)

# ── 02 Merge conflict ────────────────────────────────────
proj(
    dir="02-merge-conflict", id="proj-git-conflict", title="Project: Resolve a Merge Conflict",
    minutes=35, points=250, prereq="[proj-git-repo]",
    theory="""# Project: Resolve a Merge Conflict

When two branches change the same line, Git can't auto-merge. It marks the file
with `<<<<<<<`, `=======`, `>>>>>>>` and waits for you to resolve, then commit.
""",
    instructions="""# Project Tasks

`/root/repo` has two branches that both edited `config.txt`. On `main`:

1. `git merge feature` — this will **conflict** on `config.txt`.
2. **Resolve** so `config.txt` contains exactly `color=purple` (remove all
   conflict markers).
3. **Commit** the merge.

Click **Check** when the merge is committed.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo "color=blue" > config.txt; git add config.txt; git commit -qm "base"
git switch -qc feature
echo "color=green" > config.txt; git add config.txt; git commit -qm "feature: green"
git switch -q main
echo "color=red" > config.txt; git add config.txt; git commit -qm "main: red"
exit 0
""",
    solution="""cd /root/repo
git merge feature || true          # conflicts on config.txt
echo "color=purple" > config.txt   # resolve
git add config.txt
git commit -qm "merge: resolve color to purple"
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if grep -q "color=purple" config.txt 2>/dev/null; then
  echo "STEP:resolved to purple:PASS"; else echo "STEP:resolved to purple:FAIL:config.txt must contain color=purple"; fail=1; fi
if ! grep -q "<<<<<<<" config.txt 2>/dev/null; then
  echo "STEP:no conflict markers left:PASS"; else echo "STEP:no conflict markers left:FAIL:remove <<<< ==== >>>> markers"; fail=1; fi
parents=$(git rev-list --parents -n1 HEAD | wc -w)
if [ "$parents" -ge 3 ]; then
  echo "STEP:merge commit recorded:PASS"; else echo "STEP:merge commit recorded:FAIL:commit the merge (HEAD should have 2 parents)"; fail=1; fi
exit $fail
""",
)

# ── 03 Pre-commit hook ───────────────────────────────────
proj(
    dir="03-pre-commit-hook", id="proj-git-hook", title="Project: Pre-commit Lint Hook",
    minutes=40, points=250, prereq="[proj-git-conflict]",
    theory="""# Project: Pre-commit Hook

Git runs `.git/hooks/pre-commit` before each commit. Exit non-zero to **block**
the commit — perfect for catching lint issues or stray `TODO`s.
""",
    instructions="""# Project Tasks

In `/root/repo`:

1. Install an executable **`.git/hooks/pre-commit`** that **blocks** a commit if
   any staged change contains the text `TODO`.
2. Prove it: commit a clean file `a.txt` (should succeed), then try to commit a
   file `b.txt` containing `TODO` (should be rejected, so `b.txt` never lands).

Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo init > base.txt; git add base.txt; git commit -qm "base"
exit 0
""",
    solution="""cd /root/repo
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "pre-commit: TODO found, blocking commit"
  exit 1
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit
echo "clean code" > a.txt; git add a.txt; git commit -qm "add a"
echo "TODO: finish" > b.txt; git add b.txt; git commit -qm "add b" || true
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -x .git/hooks/pre-commit ]; then
  echo "STEP:pre-commit hook installed:PASS"; else echo "STEP:pre-commit hook installed:FAIL:add executable .git/hooks/pre-commit"; fail=1; fi
if git cat-file -p main:a.txt >/dev/null 2>&1; then
  echo "STEP:clean commit allowed:PASS"; else echo "STEP:clean commit allowed:FAIL:a.txt should be committed"; fail=1; fi
if ! git cat-file -p main:b.txt >/dev/null 2>&1; then
  echo "STEP:TODO commit blocked:PASS"; else echo "STEP:TODO commit blocked:FAIL:b.txt (with TODO) must be rejected by the hook"; fail=1; fi
exit $fail
""",
)

# ── 04 Git flow ──────────────────────────────────────────
proj(
    dir="04-git-flow", id="proj-git-flow", title="Project: Feature-branch Flow",
    minutes=35, points=250, prereq="[proj-git-hook]",
    theory="""# Project: Feature-branch Flow

A lightweight Git Flow: integrate work on `develop`, build each feature on a
`feature/*` branch, and merge it back with `--no-ff` so the history shows the
feature boundary.
""",
    instructions="""# Project Tasks

In `/root/repo` (on `main`):

1. Create a **`develop`** branch.
2. From `develop`, create **`feature/login`**, add `login.txt`, and commit it.
3. Merge `feature/login` back into `develop` (a `--no-ff` merge is ideal).

After this, `develop` must contain `login.txt`. Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo app > app.txt; git add app.txt; git commit -qm "base"
exit 0
""",
    solution="""cd /root/repo
git branch develop
git switch -q develop
git switch -qc feature/login
echo "login page" > login.txt; git add login.txt; git commit -qm "feat: login"
git switch -q develop
git merge --no-ff -m "merge feature/login" feature/login
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
git rev-parse --verify develop >/dev/null 2>&1 && { echo "STEP:develop branch exists:PASS"; } || { echo "STEP:develop branch exists:FAIL:create develop"; fail=1; }
git rev-parse --verify feature/login >/dev/null 2>&1 && { echo "STEP:feature/login branch exists:PASS"; } || { echo "STEP:feature/login branch exists:FAIL:create feature/login"; fail=1; }
if git cat-file -p develop:login.txt >/dev/null 2>&1; then
  echo "STEP:login.txt merged into develop:PASS"; else echo "STEP:login.txt merged into develop:FAIL:merge feature/login into develop"; fail=1; fi
exit $fail
""",
)

# ── 05 Squash history ────────────────────────────────────
proj(
    dir="05-squash-history", id="proj-git-squash", title="Project: Clean Up History",
    minutes=40, points=300, prereq="[proj-git-flow]",
    theory="""# Project: Clean Up History

Before sharing, collapse messy "wip" commits into one meaningful commit. You can
use `git rebase -i` to squash, or `git reset --soft` to recombine — either way
the file content is preserved, only the history changes.
""",
    instructions="""# Project Tasks

`/root/repo` on `main` has 1 base commit plus **3 messy commits** (`wip`,
`wip2`, `fix typo`). Squash the **3 messy commits into a single commit** with the
message `feat: add feature`, keeping the final file contents.

Result: `main` has exactly **2 commits**, and `app.txt` still ends with `done`.
Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo "v0" > app.txt; git add app.txt; git commit -qm "base"
echo "wip1" >> app.txt; git add app.txt; git commit -qm "wip"
echo "wip2" >> app.txt; git add app.txt; git commit -qm "wip2"
echo "done" >> app.txt; git add app.txt; git commit -qm "fix typo"
exit 0
""",
    solution="""cd /root/repo
# Recombine the last 3 commits into one (keeps the working tree/content).
git reset --soft HEAD~3
git commit -qm "feat: add feature"
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
n=$(git rev-list --count main)
if [ "$n" = "2" ]; then echo "STEP:history squashed to 2 commits:PASS"; else echo "STEP:history squashed to 2 commits:FAIL:main has $n commits, expected 2"; fail=1; fi
subj=$(git log -1 --pretty=%s main)
if [ "$subj" = "feat: add feature" ]; then echo "STEP:squashed commit message correct:PASS"; else echo "STEP:squashed commit message correct:FAIL:HEAD subject is '$subj'"; fail=1; fi
if git cat-file -p main:app.txt 2>/dev/null | grep -q "done"; then echo "STEP:file content preserved:PASS"; else echo "STEP:file content preserved:FAIL:app.txt should still contain 'done'"; fail=1; fi
exit $fail
""",
)

# ── 06 Remote push ───────────────────────────────────────
proj(
    dir="06-remote-push", id="proj-git-remote", title="Project: Push to a Remote",
    minutes=35, points=250, prereq="[proj-git-squash]",
    theory="""# Project: Push to a Remote

A **remote** is another copy of the repo (here a bare repo at
`/root/remote.git`). You push branches to share them — the basis of the
fork-and-PR workflow.
""",
    instructions="""# Project Tasks

`/root/work` is a repo whose `origin` points at the bare remote
`/root/remote.git` (with `main` already pushed). In `/root/work`:

1. Create a branch **`feature`**, add `feat.txt`, and commit it.
2. **Push `feature`** to `origin`.

Click **Check** (the checker inspects the remote).
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf remote.git work
git init -q --bare remote.git
git init -q -b main work
cd work && {GITCFG}
echo base > app.txt; git add app.txt; git commit -qm "base"
git remote add origin /root/remote.git
git push -q origin main
exit 0
""",
    solution="""cd /root/work
git switch -qc feature
echo "feature work" > feat.txt; git add feat.txt; git commit -qm "feat: work"
git push -q origin feature
""",
    validate="""#!/bin/sh
fail=0
if git --git-dir=/root/remote.git rev-parse --verify feature >/dev/null 2>&1; then
  echo "STEP:feature pushed to origin:PASS"; else echo "STEP:feature pushed to origin:FAIL:push the feature branch to origin"; fail=1; fi
if git --git-dir=/root/remote.git show feature:feat.txt >/dev/null 2>&1; then
  echo "STEP:feat.txt present on remote:PASS"; else echo "STEP:feat.txt present on remote:FAIL:remote feature should contain feat.txt"; fail=1; fi
exit $fail
""",
)

# ── 07 Semver tags ───────────────────────────────────────
proj(
    dir="07-semver-tags", id="proj-git-tags", title="Project: Tag a Release",
    minutes=30, points=200, prereq="[proj-git-remote]",
    theory="""# Project: Semantic Version Tags

Releases are marked with **annotated** tags (`git tag -a`), which store a
message, author, and date. SemVer: `MAJOR.MINOR.PATCH`.
""",
    instructions="""# Project Tasks

In `/root/repo` (one commit on `main`):

1. Create an **annotated** tag **`v1.0.0`**.
2. Make another commit, then create an **annotated** tag **`v1.1.0`**.

Afterwards `git describe --tags` should report `v1.1.0`. Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo v1 > app.txt; git add app.txt; git commit -qm "base"
exit 0
""",
    solution="""cd /root/repo
git tag -a v1.0.0 -m "release 1.0.0"
echo "more" >> app.txt; git add app.txt; git commit -qm "feat: more"
git tag -a v1.1.0 -m "release 1.1.0"
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ "$(git cat-file -t v1.0.0 2>/dev/null)" = "tag" ]; then echo "STEP:v1.0.0 annotated tag:PASS"; else echo "STEP:v1.0.0 annotated tag:FAIL:create annotated tag v1.0.0"; fail=1; fi
if [ "$(git cat-file -t v1.1.0 2>/dev/null)" = "tag" ]; then echo "STEP:v1.1.0 annotated tag:PASS"; else echo "STEP:v1.1.0 annotated tag:FAIL:create annotated tag v1.1.0"; fail=1; fi
d=$(git describe --tags 2>/dev/null)
if [ "$d" = "v1.1.0" ]; then echo "STEP:describe reports v1.1.0:PASS"; else echo "STEP:describe reports v1.1.0:FAIL:got '$d'"; fail=1; fi
exit $fail
""",
)

# ── 08 Reflog recovery ───────────────────────────────────
proj(
    dir="08-reflog-recovery", id="proj-git-reflog", title="Project: Recover a Lost Commit",
    minutes=40, points=300, prereq="[proj-git-tags]",
    theory="""# Project: Recover with Reflog

`git reflog` records where `HEAD` has been — even after a `reset --hard` that
seemingly destroyed a commit. You can recover the lost work from there.
""",
    instructions="""# Project Tasks

In `/root/repo`, a commit that added `lost.txt` (containing `treasure`) was
dropped by a `git reset --hard`. It's gone from the working tree but still in the
**reflog**.

1. Use `git reflog` to find the dropped commit.
2. Restore `lost.txt` and **commit it** back onto `main`.

Click **Check** when `lost.txt` is back in history.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo keep > keep.txt; git add keep.txt; git commit -qm "add keep"
echo treasure > lost.txt; git add lost.txt; git commit -qm "add lost"
git reset -q --hard HEAD~1
exit 0
""",
    solution="""cd /root/repo
# Find the dropped commit in the reflog and restore its file.
lost=$(git reflog | grep -m1 "add lost" | awk '{print $1}')
git checkout "$lost" -- lost.txt
git add lost.txt
git commit -qm "restore: recover lost.txt via reflog"
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -f lost.txt ] && grep -q "treasure" lost.txt; then echo "STEP:lost.txt recovered:PASS"; else echo "STEP:lost.txt recovered:FAIL:restore lost.txt (treasure)"; fail=1; fi
if git cat-file -p main:lost.txt 2>/dev/null | grep -q "treasure"; then echo "STEP:recovery committed on main:PASS"; else echo "STEP:recovery committed on main:FAIL:commit the recovered lost.txt"; fail=1; fi
exit $fail
""",
)

# ── 09 Submodules ────────────────────────────────────────
proj(
    dir="09-submodules", id="proj-git-submodule", title="Project: Add a Submodule",
    minutes=40, points=300, prereq="[proj-git-reflog]",
    theory="""# Project: Submodules

A **submodule** embeds another repo at a fixed commit inside yours — handy for
shared libraries. `git submodule add <url> <path>` records it in `.gitmodules`.
""",
    instructions="""# Project Tasks

`/root/lib.git` is a bare library repo. In the app repo `/root/app`:

1. Add `/root/lib.git` as a **submodule** at path **`vendor/lib`**.
2. Commit the result.

> Adding a submodule from a local path may need
> `git -c protocol.file.allow=always submodule add …`.

Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf lib-src lib.git app
git init -q -b main lib-src
cd lib-src && {GITCFG}
echo "lib v1" > lib.txt; git add lib.txt; git commit -qm "lib base"
cd /root
git clone -q --bare lib-src lib.git
git init -q -b main app
cd app && {GITCFG}
echo "# app" > README.md; git add README.md; git commit -qm "init"
exit 0
""",
    solution="""cd /root/app
git -c protocol.file.allow=always submodule add /root/lib.git vendor/lib
git commit -qm "chore: add lib submodule"
""",
    validate="""#!/bin/sh
cd /root/app 2>/dev/null || { echo "STEP:app repo exists:FAIL:/root/app missing"; exit 1; }
fail=0
if [ -f .gitmodules ] && grep -q "vendor/lib" .gitmodules; then echo "STEP:.gitmodules references vendor/lib:PASS"; else echo "STEP:.gitmodules references vendor/lib:FAIL:add submodule at vendor/lib"; fail=1; fi
if [ -f vendor/lib/lib.txt ] && grep -q "lib v1" vendor/lib/lib.txt; then echo "STEP:submodule content checked out:PASS"; else echo "STEP:submodule content checked out:FAIL:vendor/lib/lib.txt missing"; fail=1; fi
exit $fail
""",
)

# ── 10 Changelog generator ───────────────────────────────
proj(
    dir="10-changelog", id="proj-git-changelog", title="Project: Generate a Changelog",
    minutes=35, points=250, prereq="[proj-git-submodule]",
    theory="""# Project: Changelog from Commits

Conventional commit subjects (`feat:`, `fix:`) make it easy to auto-generate a
changelog with `git log --pretty`.
""",
    instructions="""# Project Tasks

`/root/repo` has three commits with conventional subjects. Write
`/root/repo/changelog.sh` that writes `CHANGELOG.md` with one bullet
(`- <subject>`) per commit, then run it.

`CHANGELOG.md` must list all three subjects:
`feat: add login`, `fix: correct typo`, `feat: add logout`. Click **Check**.
""",
    setup=f"""#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && {GITCFG}
echo a > app.txt; git add app.txt; git commit -qm "feat: add login"
echo b >> app.txt; git add app.txt; git commit -qm "fix: correct typo"
echo c >> app.txt; git add app.txt; git commit -qm "feat: add logout"
exit 0
""",
    solution="""cd /root/repo
cat > changelog.sh <<'GEN'
#!/bin/bash
set -euo pipefail
echo "# Changelog" > CHANGELOG.md
git log --pretty='- %s' >> CHANGELOG.md
GEN
chmod +x changelog.sh
./changelog.sh
""",
    validate="""#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -x changelog.sh ] && [ -f CHANGELOG.md ]; then echo "STEP:changelog.sh produced CHANGELOG.md:PASS"; else echo "STEP:changelog.sh produced CHANGELOG.md:FAIL:create and run changelog.sh"; fail=1; fi
miss=""
for s in "feat: add login" "fix: correct typo" "feat: add logout"; do
  grep -qF "$s" CHANGELOG.md 2>/dev/null || miss="$miss; $s"
done
if [ -z "$miss" ]; then echo "STEP:all commit subjects listed:PASS"; else echo "STEP:all commit subjects listed:FAIL:missing$miss"; fail=1; fi
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
            f"id: {p['id']}\n"
            f"title: \"{p['title']}\"\n"
            f"track: git\nlevel: beginner\n"
            f"estimated_minutes: {p['minutes']}\n"
            f"image: lab-linux:latest\n"
            f"prerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n",
            encoding="utf-8",
        )
        write_exec(d / ".solution.sh", "#!/bin/bash\nset -e\n" + p["solution"])
    print(f"Wrote {len(PROJECTS)} git projects to {BASE}")


if __name__ == "__main__":
    main()
