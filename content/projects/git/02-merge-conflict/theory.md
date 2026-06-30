# Deep Dive: How Merges (and Conflicts) Work

## What a merge really is
A merge combines two lines of history. Git finds the **merge base** (the common
ancestor), then applies both sides' changes. If the two sides changed
*different* regions, Git merges automatically. If they changed the **same
lines**, Git can't choose — that's a conflict, and it asks you.

## Reading the markers
```
<<<<<<< HEAD
your side
=======
their side
>>>>>>> feature
```
Everything between `<<<` and `===` is the current branch; between `===` and
`>>>` is the branch being merged. Resolving = editing the file to the final
desired content and **removing all markers**, then `git add` + `git commit`.

## Fast-forward vs. merge commit
If your branch hasn't moved, Git just slides the pointer forward (fast-forward,
no new commit). If both moved, Git records a **merge commit** with *two
parents* — visible as a fork-and-join in the graph.

## Pitfalls
- Committing with conflict markers still in the file (tests/CI catch this).
- `git checkout --theirs/--ours` blindly, discarding real work.
- Resolving the same conflict repeatedly across rebases — enable `git rerere`.

## Real-world
Every pull request that "has conflicts" lands you here; mastering it is daily
bread on any team.
