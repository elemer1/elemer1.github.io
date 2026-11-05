#!/usr/bin/env python3
"""Generate the figures for "The Particle Builds It. The Pressure Detonates It."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images" / "the-particle-and-the-pressure"

INK = "#202124"
MUTED = "#626A73"
GRID = "#D9DEE3"
LIGHT = "#EEF1F3"
RED = "#B24A45"
BLUE = "#2D6282"
BLUE_LIGHT = "#DCE8EF"
RED_LIGHT = "#F1E2E0"


mpl.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.edgecolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.unicode_minus": False,
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none",
        "svg.hashsalt": "the-particle-and-the-pressure",
    }
)


def _figure_heading(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.055, 0.972, title.upper(), ha="left", va="top",
             fontsize=12, fontweight="bold", color=INK)
    fig.text(0.055, 0.922, subtitle, ha="left", va="top", fontsize=9.5, color=MUTED)


def _save(fig: plt.Figure, name: str, preview_dir: Path | None) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / f"{name}.svg",
        format="svg",
        bbox_inches="tight",
        metadata={"Creator": "scripts/generate-particle-pressure-figures.py", "Date": None},
    )
    if preview_dir is not None:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_dir / f"{name}.png", format="png", dpi=200,
                    bbox_inches="tight",
                    metadata={"Creator": "scripts/generate-particle-pressure-figures.py"})
    plt.close(fig)


def _blank_axes(fig: plt.Figure, rect=(0.0, 0.0, 1.0, 1.0)) -> plt.Axes:
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()
    return ax


def _box(ax, x, y, w, h, text, *, face, edge, textcolor=INK, weight="normal",
         size=8.6, lw=0.9, radius=1.6, zorder=3):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            linewidth=lw, facecolor=face, edgecolor=edge, zorder=zorder,
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=size, color=textcolor, fontweight=weight,
            linespacing=1.35, zorder=zorder + 1)


def _arrow(ax, x0, y0, x1, y1, *, color=MUTED, lw=1.0, style="-|>", ls="-",
           mutation=9, zorder=2):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle=style, linestyle=ls,
            mutation_scale=mutation, linewidth=lw, color=color,
            shrinkA=0, shrinkB=0, zorder=zorder,
        )
    )


# --------------------------------------------------------------------------
# Figure 1 — the two causal chains
# --------------------------------------------------------------------------
def figure_chains(preview_dir: Path | None) -> None:
    fig = plt.figure(figsize=(11.2, 5.35))
    _figure_heading(
        fig,
        "Two causal chains",
        "The same disease, ordered two ways. What is step 3 in the pathology textbook is step 1 in the experimental record.",
    )
    ax = _blank_axes(fig, (0.045, 0.045, 0.915, 0.845))

    n = 6
    gap = 2.6
    w = (100 - gap * (n - 1)) / n
    xs = [i * (w + gap) for i in range(n)]

    injury = [
        "Endothelial\ninjury and\ndysfunction",
        "Higher permeability,\nleukocyte\nadhesion",
        "Lipoprotein\naccumulation\n(LDL, oxidized)",
        "Monocytes enter,\nbecome macrophages,\nthen foam cells",
        "SMC migration,\nproliferation,\nmatrix",
        "Plaque",
    ]
    retention = [
        "ApoB particles\nin plasma\n(particle count)",
        "Transcytosis\nacross intact\nendothelium",
        "Binding to intimal\nproteoglycans\n(apoB site B)",
        "Retention and\naggregation",
        "Oxidation,\ninflammation,\nfoam cells",
        "Plaque",
    ]

    y_top, y_bot, bh = 61.0, 12.0, 18.0

    ax.text(0, y_top + bh + 9.4, "RESPONSE TO INJURY", ha="left", va="bottom",
            fontsize=9.6, fontweight="bold", color=RED)
    ax.text(0, y_top + bh + 4.2,
            "Ross, 1976 and 1986. The framework of Robbins & Cotran, 11th ed. (2026), pp. 451–452:\n"
            "“EC injury is the cornerstone of the response-to-injury hypothesis.”",
            ha="left", va="bottom", fontsize=8.2, color=MUTED, linespacing=1.4)

    for i, (x, label) in enumerate(zip(xs, injury)):
        last = i == n - 1
        _box(ax, x, y_top, w, bh, label,
             face=RED_LIGHT if not last else LIGHT,
             edge=RED if not last else MUTED,
             weight="bold" if i == 0 else "normal")
        ax.text(x + 1.6, y_top + bh - 2.6, str(i + 1), ha="left", va="top",
                fontsize=7.4, color=RED if not last else MUTED, fontweight="bold")
        if not last:
            _arrow(ax, x + w + 0.3, y_top + bh / 2, x + w + gap - 0.3, y_top + bh / 2,
                   color=RED, lw=1.0)

    for i, (x, label) in enumerate(zip(xs, retention)):
        last = i == n - 1
        crit = i == 3
        _box(ax, x, y_bot, w, bh, label,
             face=BLUE_LIGHT if not last else LIGHT,
             edge=BLUE if not last else MUTED,
             weight="bold" if i in (0, 3) else "normal",
             lw=1.7 if crit else 0.9)
        ax.text(x + 1.6, y_bot + bh - 2.6, str(i + 1), ha="left", va="top",
                fontsize=7.4, color=BLUE if not last else MUTED, fontweight="bold")
        if not last:
            _arrow(ax, x + w + 0.3, y_bot + bh / 2, x + w + gap - 0.3, y_bot + bh / 2,
                   color=BLUE, lw=1.0)

    ax.text(0, y_bot - 5.4, "RESPONSE TO RETENTION", ha="left", va="top",
            fontsize=9.6, fontweight="bold", color=BLUE)
    ax.text(0, y_bot - 10.6,
            "Williams & Tabas, 1995. Mechanism filled in by Borén 1998 (the binding site), "
            "Skålén 2002 (the decisive experiment) and Huang 2019 (the gate).",
            ha="left", va="top", fontsize=8.2, color=MUTED, linespacing=1.4)

    # the rate-limiting marker
    xr = xs[3] + w / 2
    _arrow(ax, xr, y_bot + bh + 8.6, xr, y_bot + bh + 1.0, color=BLUE, lw=1.2)
    ax.text(xr, y_bot + bh + 9.4,
            "Rate-limiting step. Disable apoB’s proteoglycan binding and mice\n"
            "develop far less atherosclerosis at the same plasma LDL (Skålén 2002).",
            ha="center", va="bottom", fontsize=8.2, color=BLUE, linespacing=1.4)

    # the demotion
    _arrow(ax, xs[0] + w / 2, y_bot + bh + 0.6, xs[2] + w / 2, y_top - 0.6,
           color=MUTED, lw=1.0, ls=(0, (3.2, 2.4)), style="-|>")
    ax.text(xs[1] + w / 2 + 1.0, (y_top + y_bot + bh) / 2 - 1.0,
            "the same event:\nstep 1, or step 3",
            ha="center", va="center", fontsize=8.0, color=MUTED,
            linespacing=1.4,
            bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                      edgecolor="none"))

    _save(fig, "figure-5-two-causal-chains", preview_dir)


# --------------------------------------------------------------------------
# Figure 2 — four numbers of the same size
# --------------------------------------------------------------------------
def figure_same_size(preview_dir: Path | None) -> None:
    rows = [
        ("Arm supported on the lap\ninstead of a desk", 3.9, None, "error"),
        ("Arm hanging unsupported\nat the side", 6.5, None, "error"),
        ("Potassium-enriched salt\nsubstitute (DECIDE-Salt)", 7.1, None, "nondrug"),
        ("Isometric exercise training\n(270-trial meta-analysis)", 8.2, None, "nondrug"),
        ("Baxdrostat, first aldosterone-\nsynthase inhibitor", 8.7, 9.8, "drug"),
    ]
    style = {
        "error": (RED_LIGHT, RED),
        "nondrug": (BLUE_LIGHT, BLUE),
        "drug": (BLUE, BLUE),
    }

    fig = plt.figure(figsize=(9.4, 5.1))
    _figure_heading(
        fig,
        "Five numbers of the same size",
        "Effect on systolic blood pressure, in mmHg. Two are measurement errors, one is a new drug class, two are free.",
    )
    ax = fig.add_axes((0.30, 0.135, 0.655, 0.655))

    for i, (label, lo, hi, kind) in enumerate(rows):
        face, edge = style[kind]
        ax.barh(i, lo, height=0.52, color=face, edgecolor=edge, linewidth=1.1, zorder=3)
        if hi is not None:
            ax.barh(i, hi - lo, left=lo, height=0.52, color="white",
                    edgecolor=edge, linewidth=1.1, hatch="////", zorder=3)
            txt = f"{lo:.1f}–{hi:.1f}"
            xend = hi
        else:
            txt = f"{lo:.1f}"
            xend = lo
        ax.text(xend + 0.22, i, txt, ha="left", va="center", fontsize=9.4,
                color=edge, fontweight="bold", zorder=4)

    ax.axvline(5.0, color=INK, linewidth=0.9, linestyle=(0, (3.2, 2.4)), zorder=2)
    ax.text(5.18, 5.62,
            "5 mmHg ≈ 10% fewer major cardiovascular events",
            ha="left", va="top", fontsize=8.2, color=INK, zorder=4)
    ax.text(5.18, 5.17,
            "BPLTTC, 48 trials, 344,716 participants",
            ha="left", va="top", fontsize=7.6, color=MUTED, zorder=4)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.6, color=INK, linespacing=1.4)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(-0.62, len(rows) + 0.75)
    ax.set_xlabel("Systolic effect (mmHg)", fontsize=9, color=INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, colors=INK)
    ax.tick_params(axis="x", length=3, width=0.7, colors=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)

    fig.text(0.30, 0.005,
             "Red: uncorrected error in routine clinical measurement.   "
             "Solid blue: FDA-approved drug.   Outlined blue: no drug, no cost.",
             ha="left", va="bottom", fontsize=7.8, color=MUTED)

    _save(fig, "figure-1-four-numbers-of-the-same-size", preview_dir)


# --------------------------------------------------------------------------
# Figure 3 — the four routes pressure acts on the plaque
# --------------------------------------------------------------------------
def figure_four_routes(preview_dir: Path | None) -> None:
    fig = plt.figure(figsize=(11.2, 5.45))
    _figure_heading(
        fig,
        "Where pressure acts on the plaque",
        "Four routes, four stages of one lesion’s life. Three of them build it; the fourth detonates it.",
    )
    ax = _blank_axes(fig, (0.045, 0.045, 0.915, 0.845))

    stages = [
        ("ENTRY", "Route 1 · Convection",
         "Transmural pressure drives water\nfiltration through the wall, carrying\nLDL into the intima by convection\nas well as diffusion.",
         "Tarbell 2003", BLUE),
        ("RETENTION", "Route 2 · Strain",
         "Cyclic strain on smooth-muscle cells\nraises versican ×3.2 and biglycan ×2.0\nand drops decorin to ⅓: more apoB\nretained per particle delivered.",
         "Lee, Libby, Wight 2001", BLUE),
        ("REMODELING", "Route 3 · Wall stress",
         "Laplace stress (pressure × radius ÷\nthickness) drives medial hypertrophy,\nelastin fatigue and collagen — the\nstiffening that raises pressure again.",
         "see section 33", BLUE),
        ("RUPTURE", "Route 4 · Cap load",
         "Cap stress rises with luminal pressure\nand concentrates at plaque shoulders;\nruptured caps are thinner than ~65 μm.\nPulse pressure adds the fatigue.",
         "Richardson 1989; Burke 1997", RED),
    ]

    n = 4
    gap = 2.4
    w = (100 - gap * (n - 1)) / n
    xs = [i * (w + gap) for i in range(n)]

    ribbon_y, ribbon_h = 76.0, 9.5
    box_y, box_h = 31.0, 41.0

    for i, (stage, route, body, cite, color) in enumerate(stages):
        x = xs[i]
        # chevron ribbon
        tip = 3.0
        pts = [(x, ribbon_y), (x + w - tip, ribbon_y),
               (x + w, ribbon_y + ribbon_h / 2), (x + w - tip, ribbon_y + ribbon_h),
               (x, ribbon_y + ribbon_h)]
        if i > 0:
            pts.append((x + tip, ribbon_y + ribbon_h / 2))
        ax.add_patch(Polygon(pts, closed=True, facecolor=color,
                             edgecolor="none", zorder=3))
        ax.text(x + w / 2 + (tip / 2 if i > 0 else 0), ribbon_y + ribbon_h / 2,
                stage, ha="center", va="center", fontsize=9.4,
                color="white", fontweight="bold", zorder=4)

        _box(ax, x, box_y, w, box_h, "",
             face=RED_LIGHT if color is RED else BLUE_LIGHT, edge=color, lw=1.1)
        ax.text(x + w / 2, box_y + box_h - 4.5, route, ha="center", va="top",
                fontsize=9.0, color=color, fontweight="bold", zorder=5)
        ax.text(x + w / 2, box_y + box_h - 12.5, body, ha="center", va="top",
                fontsize=8.3, color=INK, linespacing=1.52, zorder=5)
        ax.text(x + w / 2, box_y + 3.4, cite, ha="center", va="bottom",
                fontsize=7.6, color=MUTED, style="italic", zorder=5)

        if i < n - 1:
            _arrow(ax, x + w + 0.2, box_y + box_h / 2, x + w + gap - 0.2,
                   box_y + box_h / 2, color=MUTED, lw=1.0)

    # the reversibility band
    split = xs[3] - gap / 2
    ax.plot([0, split], [24.0, 24.0], color=BLUE, lw=2.4, solid_capstyle="butt")
    ax.plot([split, 100], [24.0, 24.0], color=RED, lw=2.4, solid_capstyle="butt")
    ax.text(split / 2, 21.0,
            "Accumulated. Five years of treatment recovers only about half the\n"
            "predicted coronary benefit: 14% fewer coronary events.",
            ha="center", va="top", fontsize=8.3, color=BLUE, linespacing=1.5)
    ax.text(100, 21.0,
            "Immediate. The same five years delivers\n"
            "essentially all of the predicted stroke\n"
            "benefit: 42% fewer strokes.",
            ha="right", va="top", fontsize=8.3, color=RED, linespacing=1.5)
    ax.text(50, 2.0,
            "The asymmetry is the signature of the mechanism: the 1990 overview of antihypertensive trials (Collins et al.) "
            "cashed in all of pressure’s\nstroke benefit in five years and half of its coronary benefit, because routes 1–3 are "
            "written into thirty years of accumulated plaque.",
            ha="center", va="bottom", fontsize=8.2, color=MUTED, linespacing=1.5)

    _save(fig, "figure-11-where-pressure-acts", preview_dir)


# --------------------------------------------------------------------------
# Figure 2 — two clocks: evidence versus institutions
# --------------------------------------------------------------------------
def figure_two_clocks(preview_dir: Path | None) -> None:
    fig = plt.figure(figsize=(11.2, 6.9))
    _figure_heading(
        fig,
        "Two clocks",
        "What the evidence established (above the line) and what the institutions did about it (below). Brackets measure the lag.",
    )
    ax = fig.add_axes((0.035, 0.03, 0.93, 0.84))
    x0, x1 = 1970, 2032
    ax.set_xlim(x0, x1)
    ax.set_ylim(-98, 96)
    ax.set_axis_off()

    ax.plot([x0 + 1, x1 - 0.5], [0, 0], color=INK, lw=1.1, zorder=2)
    for yr in range(1970, 2031, 10):
        ax.plot([yr, yr], [-1.6, 1.6], color=INK, lw=0.9, zorder=2)
        ax.text(yr, -3.6, str(yr), ha="center", va="top", fontsize=8.4, color=MUTED)

    # Heights descend within each cluster so no later stem crosses an earlier label.
    evidence = [
        (1976, 34, "1976  Ross & Glomset:\nresponse to injury"),
        (1980, 12, "1980  Sniderman: normal\nLDL-C, high apoB"),
        (1995, 56, "1995  Williams & Tabas:\nresponse to retention"),
        (2002, 34, "2002  Skålén: retention\nis rate-limiting"),
        (2006, 12, "2006  PCSK9 carriers:\n88% fewer events"),
        (2017, 78, "2017  EAS consensus:\nLDL causes ASCVD"),
        (2020, 56, "2020  Multivariable MR:\napoB carries the risk"),
        (2021, 34, "2021  BPLTTC: no BP\nthreshold below 120"),
        (2023, 12, "2023  Isometric:\n−8 mmHg, 270 RCTs"),
    ]
    for yr, h, label in evidence:
        color = MUTED if yr == 1976 else BLUE
        ax.plot([yr, yr], [0, h - 1.2], color=color, lw=0.8, zorder=1)
        ax.scatter([yr], [0], s=26, color=color, zorder=3)
        ax.text(yr + 0.3, h, label, ha="left", va="bottom", fontsize=7.6,
                color=INK if yr != 1976 else MUTED, linespacing=1.3)

    inst = [
        (2018, -9, "2018  ACC/AHA drops LDL-C targets;\napoB a risk enhancer at ≥ 130"),
        (2025, -21, "2025  AHA/ACC lists isometric handgrip,\nfor people already hypertensive"),
        (2026, -33, "2026  Robbins 11e: injury is step 1;\n“retention” appears zero times"),
        (2026.35, -45, "2026  ACC/AHA: apoB Class 2a,\nonly after LDL-C goals are met"),
    ]
    for yr, h, label in inst:
        ax.plot([yr, yr], [0, h + 1.0], color=RED, lw=0.8, zorder=1)
        ax.scatter([yr], [0], s=26, color=RED, zorder=3)
        ax.text(yr - 0.35, h, label, ha="right", va="top", fontsize=7.6,
                color=INK, linespacing=1.3)

    def bracket(a, b, y, text, color):
        ax.plot([a, a, b, b], [y + 2.2, y, y, y + 2.2], color=color, lw=1.2,
                solid_capstyle="butt", zorder=2)
        ax.text(a + 0.4, y - 1.6, text, ha="left", va="top", fontsize=8.2,
                color=color, fontweight="bold")

    bracket(1976, 2026, -60, "50 years: the 1976 frame is still the one taught", MUTED)
    bracket(1980, 2026, -71, "46 years: apoB, from first clinical signal to first ACC/AHA recommendation", RED)
    bracket(1995, 2026, -82, "31 years: retention, from hypothesis to a textbook without the word", RED)
    ax.add_patch(FancyBboxPatch((1976, -96), 17, 4.2,
                                boxstyle="round,pad=0,rounding_size=0.6",
                                facecolor=LIGHT, edgecolor=GRID, lw=0.8))
    ax.text(1976 + 8.5, -93.9, "17 years: average lag", ha="center",
            va="center", fontsize=7.6, color=MUTED)
    ax.text(1993.6, -93.9, "research-to-practice average for scale (Morris, Wooding & Grant 2011)",
            ha="left", va="center", fontsize=7.2, color=MUTED, style="italic")

    ax.text(x0 + 1, 92, "EVIDENCE", ha="left", va="top", fontsize=8.6,
            color=BLUE, fontweight="bold")
    ax.text(x0 + 1, -9, "INSTITUTIONS", ha="left", va="top", fontsize=8.6,
            color=RED, fontweight="bold")
    _save(fig, "figure-2-two-clocks", preview_dir)


# --------------------------------------------------------------------------
# Figure 7 — the 2026 ACC/AHA recommendations, transcribed
# --------------------------------------------------------------------------
COR_STYLE = {
    "1": ("#2E7D4F", "#E3F1E8"),
    "2a": ("#B58A00", "#FBF3D5"),
    "2b": ("#C4621A", "#FBE7D8"),
}


def figure_guideline_card(preview_dir: Path | None) -> None:
    rows = [
        ("2a", "B-NR", "3.3 · 1",
         "In adults on lipid-lowering therapy (particularly with ASCVD, CKM syndrome, type 2 diabetes\n"
         "or elevated TG), “measurement of apoB is reasonable to guide decisions regarding further\n"
         "therapeutic intensification” — once LDL-C and/or non-HDL-C goals have been achieved."),
        ("2b", "B-NR", "3.3 · 2",
         "“In adults not on LLT, measurement of apoB may be reasonable to enhance ASCVD risk\n"
         "assessment.”"),
        ("2a", "B-NR", "4.2.9 · 7",
         "In adults with TG ≥ 150 mg/dL, “measurement of non–HDL-C or apoB is preferred over LDL-C.”"),
        ("1", "B-NR", "3.4 · 1",
         "“In all adults, measurement of Lp(a) concentration is recommended at least once for\n"
         "ASCVD risk assessment.”"),
        ("1", "A", "4.2.3.7 · 2",
         "Adults aged 30–59 at low (< 3%) 10-year risk, with LDL-C < 160 mg/dL and 30-year risk\n"
         "< 10%: counselling on health behaviours is recommended."),
        ("2a", "C-LD", "4.2.3.7 · 3",
         "Same group with LDL-C 160–189 mg/dL or 30-year risk ≥ 10%: a moderate-intensity statin is\n"
         "reasonable, to reduce cumulative exposure to atherogenic lipoproteins."),
    ]
    fig = plt.figure(figsize=(9.4, 6.9))
    _figure_heading(
        fig,
        "2026 ACC/AHA dyslipidemia guideline: six recommendations",
        "Transcribed, not a screenshot. Quotation marks mark the guideline’s wording; the rest is condensed.",
    )
    ax = _blank_axes(fig, (0.045, 0.03, 0.92, 0.85))
    top = 96.0
    head_h = 5.5
    row_h = 14.2
    cols = [(0, 9.5, "COR"), (9.5, 9.5, "LOE"), (19, 12.5, "Section · rec."), (31.5, 68.5, "Recommendation")]
    for x, w, label in cols:
        ax.add_patch(FancyBboxPatch((x, top - head_h), w, head_h,
                                    boxstyle="square,pad=0", facecolor=INK,
                                    edgecolor="white", lw=1.2))
        ax.text(x + w / 2 if label != "Recommendation" else x + 1.6, top - head_h / 2, label,
                ha="center" if label != "Recommendation" else "left", va="center",
                fontsize=8.6, color="white", fontweight="bold")
    y = top - head_h
    for cor, loe, sec, text in rows:
        edge, face = COR_STYLE[cor]
        y0 = y - row_h
        ax.add_patch(FancyBboxPatch((0, y0), 9.5, row_h, boxstyle="square,pad=0",
                                    facecolor=edge, edgecolor="white", lw=1.2))
        ax.text(4.75, y0 + row_h / 2, cor, ha="center", va="center", fontsize=12,
                color="white", fontweight="bold")
        for x, w, t, fs in [(9.5, 9.5, loe, 9.0), (19, 12.5, sec, 8.2)]:
            ax.add_patch(FancyBboxPatch((x, y0), w, row_h, boxstyle="square,pad=0",
                                        facecolor=face, edgecolor="white", lw=1.2))
            ax.text(x + w / 2, y0 + row_h / 2, t, ha="center", va="center",
                    fontsize=fs, color=INK)
        ax.add_patch(FancyBboxPatch((31.5, y0), 68.5, row_h, boxstyle="square,pad=0",
                                    facecolor=face, edgecolor="white", lw=1.2))
        ax.text(33.1, y0 + row_h / 2, text, ha="left", va="center", fontsize=7.9,
                color=INK, linespacing=1.45)
        y = y0
    ax.text(0, y - 3.0,
            "COR: 1 = is recommended · 2a = is reasonable · 2b = may be reasonable.   "
            "LOE: A = high-quality RCTs · B-NR = non-randomized · C-LD = limited data.",
            ha="left", va="top", fontsize=7.6, color=MUTED)
    ax.text(0, y - 7.2,
            "Source: J Am Coll Cardiol 2026, doi:10.1016/j.jacc.2025.11.016 (sections 3.3, 3.4, 4.2.3.7, 4.2.9), "
            "as reproduced by Guideline Central.",
            ha="left", va="top", fontsize=7.4, color=MUTED, style="italic")
    _save(fig, "figure-7-acc-aha-2026-apob-recommendations", preview_dir)


# --------------------------------------------------------------------------
# Figure 8 — NHANES apoB distribution (author's analysis)
# --------------------------------------------------------------------------
# Output of scripts/nhanes-apob-analysis.py (NHANES 2013–2016, untreated adults 20+).
NHANES_BINS = list(range(20, 205, 5))
NHANES_SHARE = [0.0017, 0.001, 0.0018, 0.0035, 0.0092, 0.0117, 0.0232, 0.034, 0.041, 0.0596,
                0.0669, 0.0681, 0.0765, 0.0828, 0.0818, 0.0739, 0.0684, 0.0571, 0.0472, 0.0437,
                0.0343, 0.024, 0.0206, 0.0172, 0.0156, 0.0086, 0.0105, 0.0059, 0.0033, 0.0008,
                0.0022, 0.0005, 0.0015, 0.0001, 0.0002, 0.0014]
NHANES_LDL_BANDS = [  # (lo, hi, p10, p50, p90)
    (40, 60, 37.4, 49.7, 63.9), (60, 80, 50, 62, 76), (80, 100, 64, 73, 86),
    (100, 120, 78, 88, 101), (120, 140, 89, 101, 115), (140, 150, 98, 109.1, 123),
    (150, 160, 105, 117, 136),
    (160, 190, 113, 131, 150),
]


def figure_nhanes(preview_dir: Path | None) -> None:
    fig = plt.figure(figsize=(9.4, 8.2))
    _figure_heading(
        fig,
        "Where 60 sits, and what an LDL-C below 160 can hide",
        "ApoB in U.S. adults not taking cholesterol medication, NHANES 2013–2016 (author’s analysis, survey-weighted, n = 3,809).",
    )
    ax = fig.add_axes((0.085, 0.53, 0.88, 0.33))
    lefts = NHANES_BINS[:-1]
    for x, h in zip(lefts, NHANES_SHARE):
        color = BLUE if x < 60 else "#AEB8C1"
        ax.bar(x, h * 100, width=4.6, align="edge", color=color, edgecolor="none", zorder=3)
    ymax = 9.6
    def vmark(x, label, color, y, ls=(0, (3, 2.4)), ha="left"):
        ax.axvline(x, color=color, lw=1.0, ls=ls, zorder=4)
        ax.text(x + (0.8 if ha == "left" else -0.8), y, label, ha=ha, va="top",
                fontsize=7.8, color=color, linespacing=1.3, zorder=5)
    vmark(28, "Newborn\n≈ 28", MUTED, ymax - 0.2)
    vmark(60, "Aim: below 60\n8.6% of adults", BLUE, ymax - 0.2)
    vmark(91, "Median 91", INK, ymax - 0.2)
    vmark(130, "≥ 130: 2018 ACC/AHA\nrisk enhancer (8.8%)", RED, ymax - 0.2)
    ax.set_xlim(20, 200)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("ApoB (mg/dL)", fontsize=9)
    ax.set_ylabel("Share of adults (%)", fontsize=9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    bx = fig.add_axes((0.085, 0.075, 0.88, 0.33))
    for lo, hi, p10, p50, p90 in NHANES_LDL_BANDS:
        x = (lo + hi) / 2
        color = RED if lo >= 160 else BLUE
        bx.plot([x, x], [p10, p90], color=color, lw=2.0, alpha=0.45, solid_capstyle="round", zorder=3)
        bx.scatter([x], [p50], s=34, color=color, zorder=4)
        bx.text(x + 1.6, p50, f"{p50:.0f}", ha="left", va="center", fontsize=8, color=color)
    bx.axvline(160, color=INK, lw=1.0, ls=(0, (3, 2.4)), zorder=2)
    bx.text(158, 52, "2026 ACC/AHA gate for adults 30–59\nat low calculated risk: below 160,\ncounselling only (Class 1, LOE A)",
            ha="right", va="center", fontsize=7.8, color=INK, linespacing=1.35)
    bx.axhspan(0, 60, color=BLUE_LIGHT, alpha=0.55, zorder=1)
    bx.text(193, 56, "apoB below 60", ha="right", va="top", fontsize=7.8, color=BLUE)
    bx.set_xlim(40, 195)
    bx.set_ylim(30, 160)
    bx.set_xlabel("LDL cholesterol band (mg/dL, Friedewald)", fontsize=9)
    bx.set_ylabel("ApoB (mg/dL): median, 10th–90th pct", fontsize=9)
    bx.set_xticks([40, 60, 80, 100, 120, 140, 160, 190])
    for sp in ("top", "right"):
        bx.spines[sp].set_visible(False)
    bx.spines["left"].set_color(GRID)
    bx.spines["bottom"].set_color(GRID)
    bx.grid(axis="y", color=GRID, lw=0.6, alpha=0.7)
    bx.set_axisbelow(True)
    fig.text(0.085, 0.455, "Same population, by LDL-C. Below the gate, one adult aged 30–59 in three has apoB ≥ 100 mg/dL.",
             ha="left", va="bottom", fontsize=9.0, color=INK, fontweight="bold")
    _save(fig, "figure-8-nhanes-apob-distribution", preview_dir)


# --------------------------------------------------------------------------
# Figure 12 — exercise modes (Edwards 2023)
# --------------------------------------------------------------------------
def figure_exercise_modes(preview_dir: Path | None) -> None:
    rows = [  # mode, SBP, DBP, SUCRA (SBP)
        ("Isometric", 8.24, 4.00, 98.3),
        ("Combined aerobic + resistance", 6.04, 2.54, 75.7),
        ("Dynamic resistance", 4.55, 3.04, 46.1),
        ("Aerobic endurance", 4.49, 2.53, 40.5),
        ("High-intensity interval", 4.08, 2.50, 39.4),
    ]
    fig = plt.figure(figsize=(9.4, 4.9))
    _figure_heading(
        fig,
        "The ranking nobody quotes",
        "Reduction in resting blood pressure vs control, by exercise mode. 270 RCTs, 15,827 participants (Edwards et al., BJSM 2023).",
    )
    ax = fig.add_axes((0.31, 0.20, 0.50, 0.61))
    n = len(rows)
    for i, (mode, sbp, dbp, sucra) in enumerate(rows):
        y = n - 1 - i
        iso = i == 0
        ax.barh(y + 0.17, sbp, height=0.32, color=BLUE if iso else "#AEB8C1", zorder=3)
        ax.barh(y - 0.17, dbp, height=0.32, color=BLUE_LIGHT if iso else "#DDE2E6",
                edgecolor=BLUE if iso else "#AEB8C1", lw=0.8, zorder=3)
        ax.text(sbp + 0.12, y + 0.17, f"{sbp:.2f}", va="center", fontsize=8.4,
                color=BLUE if iso else MUTED, fontweight="bold" if iso else "normal")
        ax.text(dbp + 0.12, y - 0.17, f"{dbp:.2f}", va="center", fontsize=8.0, color=MUTED)
        ax.text(1.11, y, f"{sucra:.0f}%", transform=ax.get_yaxis_transform(),
                ha="center", va="center", fontsize=9.2,
                color=BLUE if iso else MUTED, fontweight="bold" if iso else "normal")
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8.8, color=INK)
    ax.set_xlim(0, 9.6)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlabel("Reduction (mmHg)", fontsize=9)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    ax.text(1.11, n - 0.45, "SUCRA\n(systolic)", transform=ax.get_yaxis_transform(),
            ha="center", va="bottom", fontsize=8.2, color=MUTED)
    fig.text(0.31, 0.02,
             "Solid bars: systolic. Outlined bars: diastolic. SUCRA = probability-based rank for systolic reduction (100% = certainly best).\n"
             "Within isometric training, the wall squat ranked first for systolic reduction, ahead of leg extension and handgrip.",
             ha="left", va="bottom", fontsize=7.6, color=MUTED, linespacing=1.45)
    _save(fig, "figure-12-exercise-modes-edwards-2023", preview_dir)


# --------------------------------------------------------------------------
# Figure 13 — the isometric "drug" as a dosing card
# --------------------------------------------------------------------------
def figure_isometric_protocol(preview_dir: Path | None) -> None:
    import math
    from matplotlib.patches import Arc, Circle, Rectangle, Wedge

    fig = plt.figure(figsize=(11.2, 5.0))
    _figure_heading(
        fig,
        "The “drug,” as a dosing card",
        "Two forms, one dose: four two-minute holds, one to two minutes’ rest, three times a week. About 42 minutes a week.",
    )
    # --- Panel A: wall squat ---
    a = fig.add_axes((0.02, 0.04, 0.31, 0.80))
    a.set_xlim(0, 100); a.set_ylim(0, 100); a.set_aspect("equal"); a.set_axis_off()
    a.add_patch(Rectangle((8, 8), 4, 84, facecolor=LIGHT, edgecolor=GRID, lw=0.8))
    a.plot([8, 96], [8, 8], color=MUTED, lw=1.4)
    hip = (16.5, 40); knee = (47, 43); ankle = (47, 10); shoulder = (16.0, 71)
    head = (17.2, 81.5)
    lw = 7.5
    for p, q in [(hip, knee), (knee, ankle), (hip, shoulder)]:
        a.plot([p[0], q[0]], [p[1], q[1]], color=BLUE, lw=lw, solid_capstyle="round", zorder=3)
    a.add_patch(Circle(head, 5.4, facecolor=BLUE, edgecolor="none", zorder=3))
    a.plot([ankle[0], ankle[0] + 8], [ankle[1], ankle[1]], color=BLUE, lw=lw - 1.5,
           solid_capstyle="round", zorder=3)
    elbow = (20.5, 52); hand = (34, 46.5)
    a.plot([shoulder[0] + 1, elbow[0], hand[0]], [shoulder[1] - 2, elbow[1], hand[1]],
           color=BLUE, lw=lw - 2.5, solid_capstyle="round", zorder=4)
    # knee angle arc
    th1 = math.degrees(math.atan2(hip[1] - knee[1], hip[0] - knee[0])) % 360
    th2 = math.degrees(math.atan2(ankle[1] - knee[1], ankle[0] - knee[0])) % 360
    a.add_patch(Arc(knee, 16, 16, theta1=th1, theta2=th2, color=RED, lw=1.6, zorder=5))
    a.text(knee[0] + 4, knee[1] - 6, "knee angle:\nset so the hold\nis hard by 2 min", fontsize=7.8,
           color=RED, ha="left", va="top", linespacing=1.3)
    a.text(12.5, 95, "Back flat on the wall", fontsize=7.8, color=MUTED, ha="left", va="center")
    a.text(60, 74, "Breathe throughout.\nNo breath-holding\n(no Valsalva).", fontsize=7.8,
           color=INK, ha="left", va="top", linespacing=1.35)
    a.text(50, 2.5, "A · Wall squat (best-ranked for systolic reduction)", fontsize=8.6,
           color=INK, fontweight="bold", ha="center", va="center")

    # --- Panel B: handgrip with gauge ---
    b = fig.add_axes((0.35, 0.04, 0.27, 0.80))
    b.set_xlim(0, 100); b.set_ylim(0, 100); b.set_aspect("equal"); b.set_axis_off()
    cx, cy, r = 50, 60, 27
    b.add_patch(Wedge((cx, cy), r, 0, 180, width=7, facecolor=LIGHT, edgecolor=GRID, lw=0.8))
    # 30–40% band: angle = 180 - pct*1.8
    b.add_patch(Wedge((cx, cy), r, 180 - 40 * 1.8, 180 - 30 * 1.8, width=7,
                      facecolor=BLUE, edgecolor="none"))
    for pct in (0, 25, 50, 75, 100):
        ang = math.radians(180 - pct * 1.8)
        b.text(cx + (r + 5.5) * math.cos(ang), cy + (r + 5.5) * math.sin(ang), f"{pct}%",
               fontsize=7.4, color=MUTED, ha="center", va="center")
    ang = math.radians(180 - 35 * 1.8)
    b.plot([cx, cx + (r - 9) * math.cos(ang)], [cy, cy + (r - 9) * math.sin(ang)], color=INK, lw=2.0)
    b.add_patch(Circle((cx, cy), 2.2, facecolor=INK))
    b.text(cx, cy - 8, "30–40% of maximal\nvoluntary contraction", fontsize=8.2, color=BLUE,
           ha="center", va="top", fontweight="bold", linespacing=1.3)
    # device body
    b.add_patch(FancyBboxPatch((30, 14), 40, 14, boxstyle="round,pad=0,rounding_size=6",
                               facecolor="white", edgecolor=BLUE, lw=1.6))
    for k in range(4):
        b.add_patch(FancyBboxPatch((33 + k * 9, 10), 7, 8, boxstyle="round,pad=0,rounding_size=3",
                                   facecolor=BLUE_LIGHT, edgecolor=BLUE, lw=1.0))
    b.text(50, 21, "handgrip", fontsize=7.6, color=MUTED, ha="center", va="center")
    b.text(50, 2.5, "B · Isometric handgrip (the 2025 AHA/ACC form)", fontsize=8.6,
           color=INK, fontweight="bold", ha="center", va="center")

    # --- Panel C: session timeline ---
    c = fig.add_axes((0.65, 0.085, 0.33, 0.70))
    c.set_xlim(-0.5, 15.5); c.set_ylim(0, 10); c.set_axis_off()
    t = 0.0
    for k in range(4):
        c.add_patch(Rectangle((t, 5.0), 2.0, 2.2, facecolor=BLUE, edgecolor="none"))
        c.text(t + 1.0, 6.1, f"hold {k + 1}\n2 min", fontsize=7.4, color="white",
               ha="center", va="center", linespacing=1.2)
        # exertion ramp
        c.plot([t, t + 2.0], [7.6, 9.0], color=RED, lw=1.4)
        t += 2.0
        if k < 3:
            c.add_patch(Rectangle((t, 5.0), 1.5, 2.2, facecolor=LIGHT, edgecolor=GRID, lw=0.6))
            c.text(t + 0.75, 6.1, "rest\n1–2", fontsize=7.0, color=MUTED, ha="center",
                   va="center", linespacing=1.2)
            t += 1.5
    c.text(0, 9.6, "perceived exertion rising to 7–8/10 by the end of each hold", fontsize=7.6,
           color=RED, ha="left", va="bottom")
    c.plot([0, t], [4.3, 4.3], color=MUTED, lw=0.8)
    c.text(t / 2, 3.9, "one session ≈ 14 minutes", fontsize=8.2, color=INK, ha="center", va="top")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    on = {0, 2, 4}
    for i, d in enumerate(days):
        x = i * 2.15 + 0.3
        c.add_patch(FancyBboxPatch((x, 0.6), 1.7, 1.5, boxstyle="round,pad=0,rounding_size=0.3",
                                   facecolor=BLUE if i in on else "white",
                                   edgecolor=BLUE if i in on else GRID, lw=0.9))
        c.text(x + 0.85, 1.35, d, fontsize=7.4, color="white" if i in on else MUTED,
               ha="center", va="center")
    c.text(7.4, -0.05, "C · One session, three times a week",
           fontsize=8.6, color=INK, fontweight="bold", ha="center", va="center")
    _save(fig, "figure-13-isometric-protocol", preview_dir)


# --------------------------------------------------------------------------
# Figure 14 — one route below 60
# --------------------------------------------------------------------------
def figure_route_below_60(preview_dir: Path | None) -> None:
    start = 110.0
    steps = [  # label, (low fractional reduction, high)
        ("High-intensity\nstatin", (0.35, 0.40)),
        ("+ ezetimibe", (0.15, 0.15)),
        ("+ PCSK9\nantibody", (0.45, 0.55)),
    ]
    lo = hi = start
    pts = [("Untreated", start, start)]
    for label, (r_lo, r_hi) in steps:
        hi, lo = hi * (1 - r_lo), lo * (1 - r_hi)
        pts.append((label, lo, hi))
    fig = plt.figure(figsize=(9.4, 5.2))
    _figure_heading(
        fig,
        "One route below 60",
        "An illustrative adult with untreated apoB 110 mg/dL. Typical proportional reductions; your own laboratory results decide.",
    )
    ax = fig.add_axes((0.09, 0.13, 0.86, 0.68))
    ax.axhspan(0, 60, color=BLUE_LIGHT, alpha=0.7, zorder=1)
    ax.text(3.45, 58, "target: apoB below 60", ha="right", va="top", fontsize=8.4, color=BLUE,
            fontweight="bold")
    ax.axhline(65, color=MUTED, lw=0.9, ls=(0, (3, 2.4)), zorder=2)
    ax.text(-0.55, 66.5, "ESC very-high-risk goal: 65", ha="left", va="bottom", fontsize=7.8, color=MUTED,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none"), zorder=6)
    for i, (label, l, h) in enumerate(pts):
        color = RED if i == 0 else (BLUE if h < 60 else "#7E8A95")
        ax.bar(i, h, width=0.55, color=color, alpha=0.18 if l != h else 0.35, zorder=3,
               edgecolor=color, lw=1.2)
        if l != h:
            ax.bar(i, l, width=0.55, color=color, alpha=0.55, zorder=4)
            txt = f"≈ {l:.0f}–{h:.0f}"
        else:
            txt = f"{h:.0f}"
        ax.text(i, h + 2.5, txt, ha="center", va="bottom", fontsize=9.4, color=color,
                fontweight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none"))
        if i > 0:
            r_lo, r_hi = steps[i - 1][1]
            pct = f"−{r_lo * 100:.0f}%" if r_lo == r_hi else f"−{r_lo * 100:.0f} to {r_hi * 100:.0f}%"
            ax.annotate("", xy=(i - 0.30, (l + h) / 2), xytext=(i - 0.70, (pts[i - 1][1] + pts[i - 1][2]) / 2),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9))
            ax.text(i - 0.5, max(h, pts[i - 1][2]) + 13, pct, ha="center", va="bottom", fontsize=8.0,
                    color=MUTED)
    ax.set_xticks(range(len(pts)))
    ax.set_xticklabels([p[0] for p in pts], fontsize=9, color=INK, linespacing=1.3)
    ax.set_ylim(0, 135)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylabel("ApoB (mg/dL)", fontsize=9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    fig.text(0.09, 0.015,
             "Step 3 is for people who start higher, have high Lp(a), or have imaged plaque. Re-measure apoB 6–12 weeks after each step.",
             ha="left", va="bottom", fontsize=7.8, color=MUTED)
    _save(fig, "figure-14-the-route-below-60", preview_dir)


FIGURES = {
    "chains": figure_chains,
    "numbers": figure_same_size,
    "routes": figure_four_routes,
    "clocks": figure_two_clocks,
    "guideline": figure_guideline_card,
    "nhanes": figure_nhanes,
    "modes": figure_exercise_modes,
    "isometric": figure_isometric_protocol,
    "route60": figure_route_below_60,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=sorted(FIGURES), action="append")
    parser.add_argument("--preview-dir", type=Path, default=None,
                        help="also write PNG previews here")
    args = parser.parse_args()

    names = args.only or sorted(FIGURES)
    for name in names:
        FIGURES[name](args.preview_dir)
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
