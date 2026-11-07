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
    # Keep the generated path data free of trailing whitespace in source control.
    svg_path = OUTPUT_DIR / f"{name}.svg"
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
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
        "Two accounts of the early lesion. The upper row condenses the textbook sequence; the lower row follows the particle.",
    )
    ax = _blank_axes(fig, (0.045, 0.045, 0.915, 0.845))

    n = 6
    gap = 2.6
    w = (100 - gap * (n - 1)) / n
    xs = [i * (w + gap) for i in range(n)]

    injury = [
        "Endothelial injury\nand dysfunction:\npermeability, adhesion",
        "Lipoprotein\naccumulation\n(LDL, oxidized)",
        "Monocytes enter,\nbecome macrophages,\nthen foam cells",
        "Platelet\nadhesion",
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
            "Ross and Glomset, 1976. Robbins, Cotran & Kumar, 11th ed., pp. 451–452.\n"
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
            "In mice, altering the particle’s binding to proteoglycans\n"
            "substantially reduced atherosclerosis (Skålén et al., 2002).",
            ha="center", va="bottom", fontsize=8.2, color=BLUE, linespacing=1.4)

    # Compare the location of lipoproteins in each account.
    _arrow(ax, xs[1] + w / 2, y_bot + bh + 0.6, xs[1] + w / 2, y_top - 0.6,
           color=MUTED, lw=1.0, ls=(0, (3.2, 2.4)), style="-|>")
    ax.text(xs[1] + w / 2 + 1.0, (y_top + y_bot + bh) / 2 - 1.0,
            "lipoproteins in\nthe arterial wall",
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
        ("Isometric training\n(19 trials in the review)", 8.2, None, "nondrug"),
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
        "Absolute differences in systolic readings (mmHg). Each comparison comes from a different study.",
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
            "5 mmHg drug-trial reference",
            ha="left", va="top", fontsize=8.2, color=INK, zorder=4)
    ax.text(5.18, 5.17,
            "BPLTTC, 48 trials, 344,716 participants",
            ha="left", va="top", fontsize=7.6, color=MUTED, zorder=4)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.6, color=INK, linespacing=1.4)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(-0.62, len(rows) + 0.75)
    ax.set_xlabel("Magnitude of systolic difference (mmHg)", fontsize=9, color=INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, colors=INK)
    ax.tick_params(axis="x", length=3, width=0.7, colors=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)

    fig.text(0.30, 0.005,
             "Red: upward reading bias.   "
             "Solid blue: drug effect.   Outlined blue: exercise or salt substitution.",
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
        "Four routes, four stages of one lesion’s life. From delivery to possible cap rupture.",
    )
    ax = _blank_axes(fig, (0.045, 0.045, 0.915, 0.845))

    stages = [
        ("ENTRY", "Route 1 · Convection",
         "Transmural pressure drives water\nfiltration through the wall, carrying\nLDL into the intima by convection\nas well as diffusion.",
         "Tarbell 2003", BLUE),
        ("RETENTION", "Route 2 · Strain",
         "Cyclic strain on smooth-muscle cells\nraises versican ×3.2 and biglycan ×2.0\nand drops decorin to ⅓. The cells\nmake a different binding matrix.",
         "Lee, Libby, Wight 2001", BLUE),
        ("REMODELING", "Route 3 · Wall stress",
         "Laplace stress (pressure × radius ÷\nthickness) drives medial hypertrophy,\nelastin fatigue and collagen — the\nstiffening that raises pressure again.",
         "see section 33", BLUE),
        ("RUPTURE", "Route 4 · Cap load",
         "Cap stress rises with luminal pressure\nand concentrates at plaque shoulders;\nmany ruptured caps were very thin\nin coronary autopsy studies.",
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
            "Coronary events. The trials achieved about half the\n"
            "predicted coronary benefit: 14% fewer coronary events.",
            ha="center", va="top", fontsize=8.3, color=BLUE, linespacing=1.5)
    ax.text(100, 21.0,
            "Stroke. The observed reduction approached\n"
            "the epidemiological prediction:\n"
            "42% fewer strokes.",
            ha="right", va="top", fontsize=8.3, color=RED, linespacing=1.5)
    ax.text(50, 2.0,
            "Collins et al. (1990) reported different magnitudes of clinical benefit for stroke and coronary disease. "
            "\nThe trial comparison did not measure "
            "particle retention or local cap stress.",
            ha="center", va="bottom", fontsize=8.2, color=MUTED, linespacing=1.5)

    _save(fig, "figure-15-where-pressure-acts", preview_dir)


# --------------------------------------------------------------------------
# Figure 2 — two clocks: evidence versus institutions
# --------------------------------------------------------------------------
def figure_two_clocks(preview_dir: Path | None) -> None:
    fig = plt.figure(figsize=(11.2, 7.6))
    _figure_heading(
        fig,
        "Two clocks",
        "Selected experiments, textbook editions and guideline decisions, plotted by year.",
    )
    ax = fig.add_axes((0.035, 0.03, 0.93, 0.84))
    x0, x1 = 1970, 2032
    ax.set_xlim(x0, x1)
    ax.set_ylim(-124, 96)
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
        (2002, 34, "2002  Skålén: impaired LDL binding,\nless plaque in mice"),
        (2006, 12, "2006  PCSK9 carriers:\n88% fewer events"),
        (2017, 78, "2017  EAS consensus:\nLDL causes ASCVD"),
        (2020, 56, "2020  Multivariable MR:\napoB carries the risk"),
        (2021, 34, "2021  BPLTTC: drug benefit\nacross baseline BP groups"),
        (2023, 12, "2023  Isometric trials:\n−8 mmHg resting SBP"),
    ]
    for yr, h, label in evidence:
        color = MUTED if yr == 1976 else BLUE
        ax.plot([yr, yr], [0, h - 1.2], color=color, lw=0.8, zorder=1)
        ax.scatter([yr], [0], s=26, color=color, zorder=3)
        ax.text(yr + 0.3, h, label, ha="left", va="bottom", fontsize=7.6,
                color=INK if yr != 1976 else MUTED, linespacing=1.3)

    inst = [
        (2017, -9, "2017  ACC/AHA prints a handgrip dose\nand a 4 mmHg estimate under Normotension"),
        (2018, -22, "2018  ACC/AHA lists apoB ≥130 mg/dL\nas a risk enhancer"),
        (2025, -35, "2025  AHA/ACC repeats the handgrip dose;\nseparate estimates with/without hypertension"),
        (2025, -48, "2025  Robbins 11e: injury and dysfunction\nopen the printed sequence"),
        (2026.35, -61, "2026  ACC/AHA: selective apoB testing\nbefore and during treatment"),
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

    bracket(1976, 2025, -76, "49 years: injury hypothesis to the publication of Robbins 11e", MUTED)
    bracket(1980, 2026, -87, "46 years: a clinical discordance report to the dedicated ACC/AHA measurement section", RED)
    bracket(1995, 2025, -98, "30 years: retention hypothesis to the publication of Robbins 11e", RED)
    bracket(2017, 2026, -109, "9 years: a handgrip dose in print, still filed as an adjunct for raised pressure", RED)

    # Medicine's own average research-to-practice lag, for scale.
    ax.plot([1976, 1993], [-119.5, -119.5], color=MUTED, lw=5.0, alpha=0.30,
            solid_capstyle="butt", zorder=1)
    ax.text(1993.6, -119.5, "17 years: the average research-to-practice lag (Morris 2011)",
            ha="left", va="center", fontsize=8.0, color=MUTED)
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
         "On lipid therapy: once LDL-C and/or non-HDL-C is at goal, apoB can guide\n"
         "intensification, particularly with ASCVD, CKM syndrome, diabetes or high TG."),
        ("2b", "B-NR", "3.3 · 2",
         "Before lipid therapy: consider apoB to refine risk, inform treatment initiation\n"
         "or characterize an inherited lipid disorder."),
        ("2a", "B-NR", "4.2.9 · 7",
         "With triglycerides ≥150 mg/dL, prefer non-HDL-C or apoB to LDL-C\n"
         "for clinical decision-making."),
        ("1", "B-NR", "3.4 · 1",
         "Measure Lp(a) at least once in adulthood to assess ASCVD risk."),
        ("1", "A", "4.2.3.7 · 2",
         "Age 30–59, 10-year risk <3%, LDL-C <160 and 30-year risk <10%:\n"
         "counsel on health behaviours. LDL-C is in mg/dL."),
        ("2a", "C-LD", "4.2.3.7 · 3",
         "Age 30–59, 10-year risk <3% and LDL-C 160–189 or 30-year risk ≥10%:\n"
         "a moderate-intensity statin is reasonable."),
    ]
    fig = plt.figure(figsize=(9.4, 6.9))
    _figure_heading(
        fig,
        "2026 ACC/AHA dyslipidemia guideline: six recommendations",
        "Selected recommendations condensed from the published guideline.",
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
            "Source: J Am Coll Cardiol 2026, doi:10.1016/j.jacc.2025.11.016 (sections 3.3, 3.4, 4.2.3.7, 4.2.9).",
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
    bx.text(158, 52, "Age 30–59, low 10- and 30-year risk:\nLDL-C <160 mg/dL, lifestyle counselling\nrecommended (Class 1, LOE A)",
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
    _save(fig, "figure-4-nhanes-apob-distribution", preview_dir)


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
        "Exercise and resting blood pressure",
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
             "Solid bars: systolic. Outlined bars: diastolic. SUCRA summarizes the distribution of possible ranks.\n"
             "Within isometric training, the wall squat ranked first for systolic reduction, ahead of leg extension and handgrip.",
             ha="left", va="bottom", fontsize=7.6, color=MUTED, linespacing=1.45)
    _save(fig, "figure-17-exercise-modes-edwards-2023", preview_dir)


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
        "Four two-minute holds per session. Table 12 handgrip uses one-minute rests; the example at right uses two.",
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
    a.text(50, 2.5, "A · Wall squat", fontsize=8.6,
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
            c.add_patch(Rectangle((t, 5.0), 2.0, 2.2, facecolor=LIGHT, edgecolor=GRID, lw=0.6))
            c.text(t + 1.0, 6.1, "rest\n2 min", fontsize=7.0, color=MUTED, ha="center",
                   va="center", linespacing=1.2)
            t += 2.0
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
    _save(fig, "figure-9-isometric-protocol", preview_dir)


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
    _save(fig, "figure-19-the-route-below-60", preview_dir)


# --------------------------------------------------------------------------
# Figure 15 — discordance: the same cholesterol, a different number of particles
# --------------------------------------------------------------------------
def figure_discordance(preview_dir: Path | None) -> None:
    """Two real people from the NHANES 150-159 mg/dL LDL-C band.

    Both report the same cholesterol mass. The 10th and 90th percentiles of
    apoB in that band (105 and 136 mg/dL) differ by 30%: thirty-one more
    particles presented to the artery wall behind an identical lab result.
    """
    fig = plt.figure(figsize=(10.4, 6.6))
    _figure_heading(
        fig,
        "The same cholesterol, a different number of particles",
        "Two untreated U.S. adults whose lipid panel reads LDL-C 155 mg/dL, at the 10th and 90th percentiles of apoB "
        "for that band (NHANES 2013\u20132016, author\u2019s analysis).",
    )
    rect = (0.045, 0.085, 0.915, 0.76)
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    # keep the dots circular: match the data box to the physical aspect of the axes
    w_in, h_in = 10.4 * rect[2], 6.6 * rect[3]
    ax.set_xlim(0, 100)
    top = 100 * h_in / w_in
    ax.set_ylim(0, top)
    ax.set_aspect("equal")

    COLS, PITCH, R = 15, 2.62, 1.03
    GRID_TOP = top - 10.6
    deepest = GRID_TOP - (-(-136 // COLS) - 1) * PITCH   # bottom row of the taller panel
    label_y = deepest - 4.4
    bar_y = label_y - 10.6

    def draw(x0, tag, pct, extra, color_tag):
        n = 105 + extra
        ax.text(x0, top - 1.4, f"Person {tag}", ha="left", va="top",
                fontsize=10.6, fontweight="bold", color=color_tag)
        ax.text(x0, top - 5.8, pct, ha="left", va="top", fontsize=8.4, color=MUTED)
        for i in range(n):
            cx = x0 + 1.0 + (i % COLS) * PITCH
            cy = GRID_TOP - (i // COLS) * PITCH
            is_extra = i >= 105
            c = RED if is_extra else BLUE
            ax.add_patch(plt.Circle((cx, cy), R, facecolor=c,
                                    alpha=0.95 if is_extra else 0.55,
                                    edgecolor=c, linewidth=0.4, zorder=3))
        ax.text(x0, label_y, f"apoB  {n} mg/dL", ha="left", va="top",
                fontsize=11.8, fontweight="bold", color=color_tag)

    draw(4.0, "A", "10th percentile of this LDL-C band", 0, BLUE)
    draw(52.0, "B", "90th percentile of this LDL-C band", 31, RED)

    # bracket the surplus
    surplus_top = GRID_TOP - 7 * PITCH + R + 0.5
    ax.annotate("", xy=(52.0, deepest - R - 0.4), xytext=(52.0, surplus_top),
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.4))
    ax.text(50.6, (surplus_top + deepest) / 2, "31 more\nparticles",
            ha="right", va="center", fontsize=8.8, color=RED,
            fontweight="bold", linespacing=1.35)

    # the identical laboratory result both panels produce
    for x0 in (4.0, 52.0):
        ax.add_patch(FancyBboxPatch(
            (x0, bar_y), 42.0, 7.6,
            boxstyle="round,pad=0,rounding_size=1.2",
            linewidth=0.9, facecolor=LIGHT, edgecolor=GRID, zorder=2))
        ax.text(x0 + 21.0, bar_y + 3.8, "LDL-C  155 mg/dL", ha="center", va="center",
                fontsize=11.0, fontweight="bold", color=INK, zorder=3)
    ax.text(49.0, bar_y - 2.2, "identical on the report", ha="center", va="top",
            fontsize=8.6, color=MUTED, fontstyle="italic")

    fig.text(0.045, 0.028,
             "One dot is one unit of apoB, which is one atherogenic particle. Person B\u2019s particles are the more "
             "cholesterol-depleted, which is why the extra thirty-one do not raise the\ncholesterol result. The count is what "
             "crosses the endothelium and binds to the matrix. One adult in ten in this band sits at each end.",
             ha="left", va="bottom", fontsize=8.4, color=MUTED, linespacing=1.5)
    _save(fig, "figure-10-discordance-same-ldl", preview_dir)


# --------------------------------------------------------------------------
# Figure 16 — the Lp(a) accounting behind the HORIZON puzzle
# --------------------------------------------------------------------------
def figure_lpa_accounting(preview_dir: Path | None) -> None:
    """Why a null trial is harder to explain than it looks.

    Illustrative arithmetic for a patient at trial entry: Lp(a) is a seventh
    of the circulating particles and, weighted per particle, about half of the
    residual particle-weighted risk.
    """
    fig = plt.figure(figsize=(9.6, 5.9))
    _figure_heading(
        fig,
        "A sixth of the particles, more than half of the risk",
        "Illustrative accounting for a patient entering Lp(a)HORIZON on intensive therapy "
        "(LDL-C \u2248 66 mg/dL, Lp(a) \u2248 190 nmol/L). Not trial data.",
    )
    ax = fig.add_axes((0.10, 0.11, 0.56, 0.72))

    other, lpa_count = 980.0, 190.0
    lpa_weighted = 190.0 * 6.6  # Bjornson per-particle weighting

    bars = [
        (0, "Particle count\n(nmol/L)", other, lpa_count),
        (1, "Weighted by\nper-particle risk", other, lpa_weighted),
    ]
    for x, label, a, b in bars:
        ax.bar(x, a, width=0.52, color="#AEB8C1", edgecolor="none", zorder=3)
        ax.bar(x, b, width=0.52, bottom=a, color=RED, edgecolor="none", zorder=3)
        share = b / (a + b) * 100
        ax.text(x, a + b + 48, f"Lp(a) = {share:.0f}%", ha="center", va="bottom",
                fontsize=10.2, fontweight="bold", color=RED)
        ax.text(x, a / 2, f"{a:,.0f}", ha="center", va="center",
                fontsize=9.0, color=INK)
        ax.text(x, a + b / 2, f"{b:,.0f}", ha="center", va="center",
                fontsize=9.0, color="white", fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_xticklabels([b[1] for b in bars], fontsize=9.2)
    ax.set_ylabel("LDL-equivalent particles (nmol/L)", fontsize=9)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 2500)
    ax.tick_params(axis="x", length=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    ax.annotate("", xy=(0.74, 1900), xytext=(0.26, 1250),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1,
                                connectionstyle="arc3,rad=-0.25"))
    ax.text(0.5, 2010, "\u00d7 6.6 per particle", ha="center", va="bottom",
            fontsize=8.6, color=MUTED, fontweight="bold")

    side = _blank_axes(fig, (0.70, 0.11, 0.285, 0.72))
    side.text(0, 97, "WHY THE NULL IS PUZZLING", ha="left", va="top",
              fontsize=8.6, fontweight="bold", color=INK)
    side.text(0, 87,
              "Intensive LDL lowering removes non-Lp(a)\nparticles and leaves Lp(a) untouched.\n"
              "It does not dilute the Lp(a) problem.\nIt concentrates it.\n\n"
              "Phase 2 pelacarsen lowered Lp(a) by\n70\u201380%. Converted at Burgess\u2019s exchange\n"
              "rate, that is roughly 0.7 mmol/L of\nLDL-C equivalent, which the CTT\n"
              "relationship turns into a mid-teens\nrelative risk reduction over five years.\n\n"
              "The trial reported no reduction in its\nprimary composite.",
              ha="left", va="top", fontsize=8.2, color=MUTED, linespacing=1.55)
    _save(fig, "figure-11-lpa-particle-accounting", preview_dir)


# --------------------------------------------------------------------------
# Figure 17 — the integral, and what the interaction term implies
# --------------------------------------------------------------------------
def figure_integral(preview_dir: Path | None) -> None:
    """Risk as the area under two curves, and the cost of starting late."""
    fig = plt.figure(figsize=(11.0, 6.0))
    _figure_heading(
        fig,
        "Risk is an area, not a probability",
        "Left: the two exposures accumulate from adolescence. Right: what one intervention buys, started twenty years apart. "
        "Illustrative, on the model of section 34.",
    )

    ages = list(range(18, 81))
    apob = [95 + 0.42 * (a - 18) for a in ages]
    sbp = [112 + 0.52 * (a - 18) for a in ages]

    # ---- left panel: the two exposure curves ----
    ax = fig.add_axes((0.055, 0.175, 0.375, 0.63))
    ax.fill_between(ages, 0, sbp, color=RED, alpha=0.08, zorder=1)
    ax.fill_between(ages, 0, apob, color=BLUE, alpha=0.14, zorder=2)
    ax.plot(ages, sbp, color=RED, lw=1.9, zorder=4)
    ax.plot(ages, apob, color=BLUE, lw=1.9, zorder=4)
    ax.text(79, sbp[-1] + 4, "systolic pressure (mmHg)", ha="right", va="bottom",
            fontsize=8.6, color=RED, fontweight="bold")
    ax.text(79, apob[-1] - 13, "apoB (mg/dL)", ha="right", va="top",
            fontsize=8.6, color=BLUE, fontweight="bold")
    ax.text(48, 42, "the integral:\nexposure \u00d7 years", ha="center", va="center",
            fontsize=9.4, color=BLUE, fontweight="bold", linespacing=1.4)
    ax.set_xlim(18, 80)
    ax.set_ylim(0, 185)
    ax.set_xlabel("Age (years)", fontsize=9)
    ax.set_ylabel("Exposure level", fontsize=9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.6)
    ax.set_axisbelow(True)

    # ---- right panel: cumulative apoB x pressure, three start ages ----
    bx = fig.add_axes((0.555, 0.175, 0.355, 0.63))

    def cumulative(start=None, factor=1.0):
        out, acc = [], 0.0
        for a in ages:
            b = 95 + 0.42 * (a - 18)
            p = 112 + 0.52 * (a - 18)
            if start is not None and a >= start:
                b *= factor
                p -= 8.0
            acc += b * p / 1000.0
            out.append(acc)
        return out

    base, s35, s55 = cumulative(), cumulative(35, 0.55), cumulative(55, 0.55)

    bx.fill_between(ages, s35, base, color=BLUE, alpha=0.12, zorder=2)
    bx.plot(ages, base, color=INK, lw=1.8, zorder=4)
    bx.plot(ages, s55, color=MUTED, lw=1.8, zorder=4)
    bx.plot(ages, s35, color=BLUE, lw=2.1, zorder=5)

    for a, color in ((35, BLUE), (55, MUTED)):
        bx.axvline(a, color=color, lw=0.9, ls=(0, (3, 2.4)), zorder=1)
        bx.text(a, base[-1] * 1.045, f"age {a}", ha="center", va="bottom",
                fontsize=8.2, color=color, fontweight="bold")

    bx.text(80.6, base[-1], "no change", ha="left", va="center",
            fontsize=8.6, color=INK)
    bx.text(80.6, s55[-1], "act at 55", ha="left", va="center",
            fontsize=8.6, color=MUTED)
    bx.text(80.6, s35[-1], "act at 35", ha="left", va="center",
            fontsize=8.6, color=BLUE, fontweight="bold")

    pct35 = (1 - s35[-1] / base[-1]) * 100
    pct55 = (1 - s55[-1] / base[-1]) * 100
    bx.text(20.5, base[-1] * 0.92,
            f"By age 80 the accumulated\nexposure is {pct35:.0f}% lower if the\n"
            f"change is made at 35,\nand {pct55:.0f}% lower at 55.",
            ha="left", va="top", fontsize=8.8, color=INK, linespacing=1.55)
    bx.annotate("plaque never built", xy=(71, (base[57] + s35[57]) / 2),
                xytext=(58, base[-1] * 0.30), fontsize=8.8, color=BLUE,
                fontweight="bold", ha="center", va="center",
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0,
                                connectionstyle="arc3,rad=-0.25"))

    bx.set_xlim(18, 80)
    bx.set_ylim(0, base[-1] * 1.12)
    bx.set_xlabel("Age (years)", fontsize=9)
    bx.set_ylabel("Cumulative apoB \u00d7 pressure", fontsize=9)
    bx.set_yticks([])
    for sp in ("top", "right", "left"):
        bx.spines[sp].set_visible(False)
    bx.spines["bottom"].set_color(GRID)

    fig.text(0.055, 0.035,
             "One intervention \u2014 a 45% lower apoB and an 8 mmHg lower systolic pressure \u2014 applied twenty years apart. "
             "Ten-year risk, which decides treatment in every\nguideline of section 4, is close to identical for these three "
             "people when they are 45. The quantity that differs is the one nobody calculates.",
             ha="left", va="bottom", fontsize=8.4, color=MUTED, linespacing=1.55)
    _save(fig, "figure-16-the-integral", preview_dir)


# Only the figures the essay still carries are registered. The functions for the
# retired ones are kept below the fold; re-add a line here to bring one back.
FIGURES = {
    "numbers": figure_same_size,
    "clocks": figure_two_clocks,
    "nhanes": figure_nhanes,
    "isometric": figure_isometric_protocol,
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
