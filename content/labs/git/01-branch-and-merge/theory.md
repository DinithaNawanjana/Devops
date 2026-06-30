# Branching & Merging

A **branch** is a movable pointer to a commit. Branching lets you develop a
feature in isolation, then **merge** it back into your main line.

## Core commands

```bash
git init                       # start a repo
git add <file> && git commit -m "msg"
git branch                     # list branches
git switch -c feature          # create + switch to 'feature'
git switch main                # switch back
git merge feature              # merge 'feature' into the current branch
git log --oneline --graph      # visualize history
```

## The typical flow

1. Start on `main`, commit a baseline.
2. `git switch -c feature` — branch off.
3. Make commits on `feature`.
4. `git switch main`, then `git merge feature`.

If `main` hasn't moved, Git does a **fast-forward** merge. If both branches
have new commits, Git creates a **merge commit** combining them.

## Inspecting

- `git status` — what's staged / modified
- `git log --oneline` — compact history
- `git branch --merged` — which branches are folded into the current one
