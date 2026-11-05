#!/usr/bin/env python3
"""Huberman Lab transcript audit cited in "The Particle Builds It. The Pressure Detonates It."

Reads the episode URLs from https://www.hubermanlab.com/sitemap.xml, downloads each episode
page (which carries the full transcript), and reports how many episodes mention blood
pressure / hypertension, how many mention isometric training (isometric, wall sit/squat,
handgrip), and how many isometric mentions fall within 700 characters of a blood-pressure term.

Usage:
    python3 scripts/huberman-transcript-audit.py --data-dir /tmp/huberman
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import html
import re
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0"}
BP = r"blood pressure|hypertensi"
ISO = r"\bisometric|\bwall[- ](?:sit|squat)s?\b|\bhand ?grip"


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")


def text_of(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, required=True)
    a = ap.parse_args()
    a.data_dir.mkdir(parents=True, exist_ok=True)
    urls = sorted(set(re.findall(r"<loc>(https://www\.hubermanlab\.com/episode/[^<]+)</loc>",
                                 get("https://www.hubermanlab.com/sitemap.xml"))))

    def fetch(u: str) -> Path:
        p = a.data_dir / (hashlib.md5(u.encode()).hexdigest() + ".txt")
        if not p.exists():
            p.write_text(u + "\n" + text_of(get(u)))
        return p

    with cf.ThreadPoolExecutor(16) as ex:
        paths = list(ex.map(fetch, urls))

    n = bp = iso = ctx = 0
    for p in paths:
        u, _, t = p.read_text().partition("\n")
        low = t.lower()
        n += 1
        bp += bool(re.search(BP, low))
        hits = list(re.finditer(ISO, low))
        iso += bool(hits)
        ctx += any(re.search(BP, low[max(0, m.start() - 700):m.end() + 700]) for m in hits)
    print(f"episodes={n} mention_bp={bp} mention_isometric={iso} isometric_near_bp={ctx}")


if __name__ == "__main__":
    main()
