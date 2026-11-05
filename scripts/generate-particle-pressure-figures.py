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

    _save(fig, "figure-4-two-causal-chains", preview_dir)


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
         "see section 26", BLUE),
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

    _save(fig, "figure-8-where-pressure-acts", preview_dir)


FIGURES = {
    "chains": figure_chains,
    "numbers": figure_same_size,
    "routes": figure_four_routes,
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
