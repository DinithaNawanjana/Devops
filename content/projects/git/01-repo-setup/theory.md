# Deep Dive: Repository Hygiene

## A repo is a contract
The first commits set the tone for everyone who joins later. A well-formed repo
declares three things up front: **what to ignore**, **what the project is**, and
**how branches are used**.

## .gitignore — keep the repo clean
Git tracks everything you `add`, so a `.gitignore` is how you keep build
artifacts, dependencies (`node_modules/`), secrets, and logs out of history.
Once a file is committed, ignoring it later does **not** remove it — you must
`git rm --cached`. Patterns are gitignore-glob: `*.log`, `dir/`, `!keep.me` to
re-include.

## README — the front door
The README is the first thing a human (and now an LLM) reads. Minimum: what the
project does, how to run it, how to contribute.

## A branching model
Even a one-line policy ("`main` is always deployable; work on `develop`/feature
branches") prevents chaos. It's the seed of Git Flow, GitHub Flow, and
trunk-based development.

## Pitfalls
- Committing secrets before adding `.gitignore` — they live in history forever
  (use `git filter-repo`/BFG to purge).
- A `main` that isn't deployable, so nobody trusts it.

## Real-world
Every repo template, `npm init`, and `gh repo create` scaffolds exactly these
files for exactly these reasons.
