#!/usr/bin/env python3
"""NHANES apoB analysis behind Figure 4 of "The Particle and the Pressure"

Downloads the 2013-2014 and 2015-2016 NHANES apoB, triglyceride/LDL, demographic
and blood-pressure/cholesterol questionnaire files from the CDC, restricts to
adults aged 20+ in the fasting subsample who are not taking prescribed
cholesterol medication (BPQ100D != 1), and reports survey-weighted point
estimates (WTSAF2YR / 2 for the pooled four years).

Usage:
    python3 scripts/nhanes-apob-analysis.py --data-dir /tmp/nhanes [--json out.json]

No variance estimation for the complex survey design is attempted; the
numbers are point estimates.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{name}.xpt"
CYCLES = [("2013", "H"), ("2015", "I")]
TABLES = ["APOB", "TRIGLY", "DEMO", "BPQ"]
LDL_BANDS = [(40, 60), (60, 80), (80, 100), (100, 120), (120, 140), (140, 150), (150, 160), (160, 190)]


def fetch(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    for year, suffix in CYCLES:
        for table in TABLES:
            name = f"{table}_{suffix}"
            out = data_dir / f"{name}.xpt"
            if not out.exists():
                req = urllib.request.Request(BASE.format(year=year, name=name),
                                             headers={"User-Agent": "Mozilla/5.0"})
                out.write_bytes(urllib.request.urlopen(req).read())


def load(data_dir: Path) -> pd.DataFrame:
    frames = []
    for _, s in CYCLES:
        read = lambda t: pd.read_sas(data_dir / f"{t}_{s}.xpt", format="xport")
        d = (read("APOB")
             .merge(read("TRIGLY").drop(columns="WTSAF2YR"), on="SEQN", how="left")
             .merge(read("DEMO")[["SEQN", "RIDAGEYR"]], on="SEQN")
             .merge(read("BPQ")[["SEQN", "BPQ100D"]], on="SEQN", how="left"))
        frames.append(d)
    d = pd.concat(frames)
    d = d[(d.RIDAGEYR >= 20) & d.LBXAPB.notna() & (d.WTSAF2YR > 0) & (d.BPQ100D != 1)].copy()
    d["w"] = d.WTSAF2YR / 2
    return d


def wq(v, w, qs):
    o = np.argsort(v)
    v, w = np.asarray(v)[o], np.asarray(w)[o]
    c = np.cumsum(w) / w.sum()
    return [float(np.interp(q, c, v)) for q in qs]


def share(mask, w):
    return float(w[mask].sum() / w.sum())


def analyse(d: pd.DataFrame) -> dict:
    v, w = d.LBXAPB.values, d.w.values
    out = {
        "n": int(len(d)),
        "median": wq(v, w, [0.5])[0],
        "p25_p75": wq(v, w, [0.25, 0.75]),
        "below60": share(v < 60, w),
        "at_or_above130": share(v >= 130, w),
        "by_age_below60": {},
    }
    for lab, lo, hi in [("20-39", 20, 40), ("40-59", 40, 60), ("60+", 60, 200)]:
        s = d[(d.RIDAGEYR >= lo) & (d.RIDAGEYR < hi)]
        out["by_age_below60"][lab] = share(s.LBXAPB.values < 60, s.w.values)
    bins = np.arange(20, 205, 5)
    h, _ = np.histogram(d.LBXAPB.clip(20, 199.9), bins=bins, weights=d.w)
    out["hist_bins"] = bins.tolist()
    out["hist_share"] = (h / h.sum()).tolist()
    dl = d[d.LBDLDL.notna()]
    out["ldl_bands"] = []
    for lo, hi in LDL_BANDS:
        s = dl[(dl.LBDLDL >= lo) & (dl.LBDLDL < hi)]
        p10, p50, p90 = wq(s.LBXAPB.values, s.w.values, [0.1, 0.5, 0.9])
        out["ldl_bands"].append({"lo": lo, "hi": hi, "n": int(len(s)), "p10": p10, "p50": p50, "p90": p90})
    mid = dl[(dl.RIDAGEYR >= 30) & (dl.RIDAGEYR < 60) & (dl.LBDLDL < 160)]
    out["age30_59_ldl_below160_share_apob_ge100"] = share(mid.LBXAPB.values >= 100, mid.w.values)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    fetch(a.data_dir)
    res = analyse(load(a.data_dir))
    text = json.dumps(res, indent=1)
    if a.json:
        a.json.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
