#!/usr/bin/env python3
"""Blueprint article audit cited in "The Particle and the Pressure"

Reads the article sitemap at blueprint.bryanjohnson.com, downloads every article page,
and reports how many mention isometric training (isometric, wall sit/squat, handgrip),
how many mention a blood-pressure term, and which blood-pressure levers are named.

Usage:
    python3 scripts/blueprint-article-audit.py --data-dir /tmp/blueprint [--json out.json]

Used only as data about the public record of the protocol, not as a source for any
scientific claim. Absence from published articles is not proof that an idea is never used.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import html
import json
import re
import time
import urllib.request
from pathlib import Path

SITEMAP = "https://blueprint.bryanjohnson.com/sitemap_articles_1.xml"
UA = {"User-Agent": "Mozilla/5.0"}
BP = r"blood pressure|hypertensi"
ISO = r"\bisometric|\bwall[- ]?(?:sit|squat)s?\b|\bhand ?grip"
LEVERS = {"sauna": r"\bsauna", "candesartan": r"candesartan", "ARB": r"angiotensin[- ]receptor blocker|\barb\b",
          "salt/sodium": r"\bsodium\b|\bsalt\b", "exercise": r"\bexercise", "nitric oxide": r"nitric oxide"}


def get(url: str, tries: int = 5) -> str:
    for a in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8", "ignore")
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(4 + 4 * a)
    raise RuntimeError("unreachable")


def text_of(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    a.data_dir.mkdir(parents=True, exist_ok=True)

    urls = sorted(set(re.findall(r"<loc>(https://blueprint\.bryanjohnson\.com/blogs/[^<]+)</loc>", get(SITEMAP))))

    def fetch(u: str) -> Path:
        p = a.data_dir / (hashlib.md5(u.encode()).hexdigest() + ".txt")
        if not p.exists() or p.stat().st_size < 2000:
            p.write_text(u + "\n" + text_of(get(u)))
        return p

    with cf.ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(fetch, urls))

    res = {"articles": len(paths), "mention_bp": 0, "mention_isometric": 0, "iso_titles": [], "levers": {}}
    bp_pages = []
    for p in paths:
        u, _, t = p.read_text().partition("\n")
        low = t.lower()
        if re.search(BP, low):
            res["mention_bp"] += 1
            bp_pages.append((u, low))
        if re.search(ISO, low):
            res["mention_isometric"] += 1
            res["iso_titles"].append(u)
    for name, pat in LEVERS.items():
        res["levers"][name] = sum(bool(re.search(pat, low)) for _, low in bp_pages)
    print(json.dumps(res, indent=1))
    if a.json:
        a.json.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
