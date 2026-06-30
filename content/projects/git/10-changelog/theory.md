# Deep Dive: Changelogs from Commit History

## Why automate it
A changelog answers "what changed between releases?" for users and operators.
Hand-maintained changelogs rot; generating from commit messages keeps them
honest — and *forces* good commit hygiene.

## Conventional Commits
A lightweight convention: `type(scope): subject`, e.g. `feat: add login`,
`fix: correct typo`. Because the type is machine-readable, tools can:
- group changes into Features / Fixes / Breaking,
- auto-pick the next SemVer bump (`feat` → minor, `fix` → patch, `!`/`BREAKING
  CHANGE` → major).

## The generation
At its simplest:
```bash
git log --pretty='- %s' v1.0.0..HEAD
```
emits a bullet per commit since the last tag. `%s` is the subject; the
`tag..HEAD` range scopes it to the unreleased commits.

## Pitfalls
- Garbage in, garbage out — vague commit subjects make a useless changelog
  (this is *why* teams enforce Conventional Commits via a commit-msg hook).
- Including merge commits as noise (`--no-merges`).

## Real-world
`semantic-release`, `release-please`, and GitHub's auto-generated release notes
all build on exactly this commit-message-to-changelog pipeline.
