# Deep Dive: Branching Strategies

## Why a model at all
Branches are cheap; *coordination* is not. A branching model is a shared
agreement about where work happens and how it reaches production, so people
don't step on each other.

## The feature-branch flow
- `main` — always releasable.
- `develop` — integration branch where features land.
- `feature/*` — one branch per unit of work, branched off `develop`, merged
  back when done.

Merging with **`--no-ff`** forces a merge commit even when a fast-forward was
possible, preserving the feature boundary in history (you can see where a
feature began and ended).

## The spectrum
- **Git Flow**: develop + release + hotfix branches — heavy, good for versioned
  releases.
- **GitHub Flow**: just `main` + short-lived feature branches + PRs — light,
  good for continuous deployment.
- **Trunk-based**: commit to `main` behind feature flags — fastest, needs strong
  CI.

## Pitfalls
- Long-lived feature branches → merge hell. Integrate often.
- Choosing a heavy model for a tiny team.

## Real-world
The model you pick shapes your whole CI/CD pipeline; most modern teams trend
toward GitHub Flow or trunk-based.
