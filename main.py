#!/usr/bin/env python3
"""news-image-20261123 entry.

Writes the summary image of Monday 23 November 2026 world news to
/output/entry.png. Deterministic, no network, standard library only:
the image is composed in the repository (see compose.py) and copied
here verbatim, so every run writes the same bytes.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out = Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out)


if __name__ == "__main__":
    main()
