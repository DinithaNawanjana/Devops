# Deep Dive: Tagging & Semantic Versioning

## Lightweight vs. annotated tags
- **Lightweight**: just a pointer to a commit (a named bookmark).
- **Annotated** (`git tag -a`): a real Git object with a message, tagger, and
  date — and can be GPG-signed. **Releases should always be annotated** so the
  tag carries provenance.

## Semantic Versioning
`MAJOR.MINOR.PATCH`:
- **MAJOR** — breaking changes.
- **MINOR** — new, backward-compatible features.
- **PATCH** — backward-compatible bug fixes.

This contract lets dependents pin ranges (`^1.4.0`) and know what upgrading
risks. `git describe --tags` names any commit relative to the nearest tag
(`v1.1.0-3-gabc123` = 3 commits past v1.1.0).

## Pitfalls
- Lightweight tags for releases — no metadata, easy to clobber.
- Forgetting `git push --tags` (tags don't push with commits by default).
- Re-tagging an existing version — breaks anyone who pinned it.

## Real-world
CI release pipelines trigger on tag pushes; package registries (npm, PyPI,
container registries) key releases on SemVer tags.
