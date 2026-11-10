#!/usr/bin/env python3
"""Robbins chapter 11 vocabulary audit cited in sections 2-3 of "The Particle and the Pressure"

Extracts the text of a printed page range from a PDF of *Robbins, Cotran & Kumar Pathologic
Basis of Disease*, 11th ed. (ISBN 978-0-443-26452-8), and counts the mechanism vocabulary:
retention, proteoglycan, transcytosis and apolipoprotein B. Prints the surrounding sentence
for every hit so each one can be classified by hand as structural or as apoB binding.

The PDF's page labels are offset from its page indices by a constant (front matter). The
script finds that offset by reading the running head of a probe page, so the page numbers
on the command line are the printed ones.

Usage:
    python3 scripts/robbins-atherosclerosis-audit.py --pdf ROBBINS.pdf --first 449 --last 458
    python3 scripts/robbins-atherosclerosis-audit.py --pdf ROBBINS.pdf --first 441 --last 478

Requires the poppler `pdftotext` binary. A word set in a figure image rather than as text
will not be extracted, so a zero count is evidence about the text layer, not about the page.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

TERMS = ["retention", "proteoglycan", "transcytosis", "apolipoprotein b", "apolipoprotein"]


def page_text(pdf: str, i: int, layout: bool = True) -> str:
    cmd = ["pdftotext", "-f", str(i), "-l", str(i)] + (["-layout"] if layout else []) + [pdf, "-"]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def find_offset(pdf: str, probe_printed: int = 454) -> int:
    """Locate the PDF index whose running head prints `probe_printed`."""
    for i in range(probe_printed, probe_printed + 60):
        head = page_text(pdf, i)[:400]
        if re.search(r"\b%d\b" % probe_printed, head) and "CHAPTER 11" in head:
            return i - probe_printed
    raise SystemExit("could not locate the printed page number; pass --offset")


def norm(t: str) -> str:
    t = t.replace("­", "")
    t = re.sub(r"-\s*\n\s*", "", t)          # de-hyphenate across line breaks
    return re.sub(r"\s+", " ", t)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--first", type=int, required=True, help="first PRINTED page")
    ap.add_argument("--last", type=int, required=True, help="last PRINTED page")
    ap.add_argument("--offset", type=int, help="PDF index minus printed page (found automatically)")
    a = ap.parse_args()

    off = a.offset if a.offset is not None else find_offset(a.pdf)
    print("printed-to-PDF offset: +%d" % off)

    per_page = {}
    whole = []
    for printed in range(a.first, a.last + 1):
        t = norm(page_text(a.pdf, printed + off))
        whole.append(t)
        for term in TERMS:
            n = len(re.findall(re.escape(term), t.lower()))
            if n:
                per_page.setdefault(term, []).append((printed, n))
    text = " ".join(whole)
    low = text.lower()

    print("\nprinted pp. %d-%d  (%d chars of extracted text)" % (a.first, a.last, len(text)))
    for term in TERMS:
        hits = re.findall(re.escape(term), low)
        pages = per_page.get(term, [])
        where = ", ".join("p.%d×%d" % (p, n) for p, n in pages) or "—"
        print("  %-18s %2d   %s" % (term, len(hits), where))

    print()
    for term in TERMS[:4]:
        for m in re.finditer(re.escape(term), low):
            s, e = max(0, m.start() - 160), min(len(text), m.end() + 120)
            print("  [%s] ...%s...\n" % (term, text[s:e].strip()))


if __name__ == "__main__":
    main()
