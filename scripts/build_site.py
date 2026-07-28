#!/usr/bin/env python3
"""Build the docs portal from the canonical readable GDD v17 source."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "gdd-source" / "index.html"
ECONOMY_SOURCE = ROOT / "economy-source" / "index.html"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: build_site.py <site-dir>")

    site = Path(sys.argv[1])
    gdd = site / "gdd" / "index.html"
    economy = site / "economy" / "index.html"
    html = SOURCE.read_text(encoding="utf-8")
    for expected in [
        "Game Design Document · v17",
        "<title>Idle Bud — Game Design Document v17</title>",
        "Idle Bud — Game Design Document v17</footer>",
    ]:
        if expected not in html:
            raise RuntimeError(f"Fonte canônica inválida: {expected}")

    gdd.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, gdd)

    economy_html = ECONOMY_SOURCE.read_text(encoding="utf-8")
    for expected in [
        "<title>Idle Bud — Economia v1.0</title>",
        "Economia do Idle Bud",
        "Marketplace",
        "Crédito Alpha = Cash gasto válido no Alpha × 1,30",
        "Idle Bud — Economia v1.0",
    ]:
        if expected not in economy_html:
            raise RuntimeError(f"Fonte canônica de Economia inválida: {expected}")

    economy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ECONOMY_SOURCE, economy)

    from build_docs_portal import main as build_portal

    old_argv = sys.argv
    try:
        sys.argv = ["build_docs_portal.py", str(site), str(gdd)]
        build_portal()
    finally:
        sys.argv = old_argv

    (site / ".nojekyll").touch()


if __name__ == "__main__":
    main()
