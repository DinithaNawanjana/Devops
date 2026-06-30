"""Loads catalog content (tracks + labs) from the on-disk content/ tree.

Layout (see spec §3):

    content/
      tracks/<slug>/track.yaml        # track metadata + lesson list
      labs/<track>/<slug>/
        lab.yaml                      # metadata
        theory.md                     # the lesson
        instructions.md               # step-by-step task
        setup.sh                      # runs on container start
        validate.sh                   # checker, exit 0 = pass
        solution.md                   # revealed after completion

Content is read live (the dir is bind-mounted read-only), cached in memory,
and re-scanned on demand. No DB rows needed to add content — drop a folder.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import markdown as md
import yaml

from .config import settings

_MD_EXT = ["fenced_code", "tables", "toc", "sane_lists"]


def _render_md(text: str) -> str:
    return md.markdown(text, extensions=_MD_EXT)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class Lab:
    def __init__(self, track: str, slug: str, meta: dict, path: Path, kind: str = "lab"):
        self.path = path
        self.track = track
        self.slug = slug
        self.type = kind  # "lab" | "project"
        self.id: str = meta.get("id", f"{track}-{slug}")
        self.title: str = meta.get("title", slug)
        self.level: str = meta.get("level", "beginner")
        self.image: str = meta.get("image", "lab-linux:latest")
        self.estimated_minutes: int = int(meta.get("estimated_minutes", 20))
        self.points: int = int(meta.get("points", 100))
        self.prerequisites: list[str] = list(meta.get("prerequisites", []))

    def summary(self) -> dict:
        return {
            "id": self.id,
            "track": self.track,
            "slug": self.slug,
            "title": self.title,
            "level": self.level,
            "type": self.type,
            "estimated_minutes": self.estimated_minutes,
            "points": self.points,
            "prerequisites": self.prerequisites,
        }

    def detail(self) -> dict:
        d = self.summary()
        d.update(
            {
                "image": self.image,
                "theory_html": _render_md(_read(self.path / "theory.md")),
                "instructions_html": _render_md(_read(self.path / "instructions.md")),
                "has_solution": (self.path / "solution.md").exists(),
            }
        )
        return d

    def setup_script(self) -> str:
        return _read(self.path / "setup.sh")

    def validate_script(self) -> str:
        return _read(self.path / "validate.sh")

    def solution_html(self) -> str:
        return _render_md(_read(self.path / "solution.md"))


class Track:
    def __init__(self, slug: str, meta: dict):
        self.slug = slug
        self.title: str = meta.get("title", slug)
        self.level: str = meta.get("level", "beginner")
        self.order_index: int = int(meta.get("order_index", 999))
        self.description: str = meta.get("description", "")


@lru_cache(maxsize=1)
def _catalog() -> tuple[dict[str, Track], dict[str, Lab]]:
    tracks: dict[str, Track] = {}
    labs: dict[str, Lab] = {}

    tracks_dir = settings.content_dir / "tracks"
    if tracks_dir.exists():
        for tdir in sorted(p for p in tracks_dir.iterdir() if p.is_dir()):
            meta = yaml.safe_load(_read(tdir / "track.yaml")) or {}
            tracks[tdir.name] = Track(tdir.name, meta)

    # Labs and projects share the same folder format; only the root differs.
    for kind, root, metafile in (
        ("lab", settings.content_dir / "labs", "lab.yaml"),
        ("project", settings.content_dir / "projects", "project.yaml"),
    ):
        if not root.exists():
            continue
        for track_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            for item_dir in sorted(p for p in track_dir.iterdir() if p.is_dir()):
                meta = yaml.safe_load(_read(item_dir / metafile)) or {}
                lab = Lab(track_dir.name, item_dir.name, meta, item_dir, kind=kind)
                labs[lab.id] = lab

    return tracks, labs


def reload() -> None:
    _catalog.cache_clear()


def list_tracks() -> list[dict]:
    tracks, labs = _catalog()
    out = []
    for t in sorted(tracks.values(), key=lambda x: x.order_index):
        track_items = [lb for lb in labs.values() if lb.track == t.slug]
        out.append(
            {
                "slug": t.slug,
                "title": t.title,
                "level": t.level,
                "order_index": t.order_index,
                "description": t.description,
                "lab_count": sum(1 for lb in track_items if lb.type == "lab"),
                "project_count": sum(1 for lb in track_items if lb.type == "project"),
            }
        )
    return out


def list_labs(track: str | None = None, kind: str = "lab") -> list[dict]:
    _, labs = _catalog()
    items = [
        lb
        for lb in labs.values()
        if (track is None or lb.track == track) and lb.type == kind
    ]
    items.sort(key=lambda lb: (lb.track, lb.slug))
    return [lb.summary() for lb in items]


def list_all() -> list[Lab]:
    """All labs + projects (for the skill tree)."""
    _, labs = _catalog()
    return sorted(labs.values(), key=lambda lb: (lb.track, lb.type, lb.slug))


def get_lab(lab_id: str) -> Lab | None:
    _, labs = _catalog()
    return labs.get(lab_id)
