#!/usr/bin/env python3
"""Generate the figures for "The Blind Ledger".

DESIGN LANGUAGE (one spec shared by all three figures)
------------------------------------------------------
Canvas      : every figure is one fixed size (FIGSIZE), saved without a
              tight bounding box, so the SVGs have identical dimensions and
              scale uniformly inside the 650px reading column.
Semantics   : BLUE  = tangible / recorded / "what the ledger sees".
              RED   = intangible / "dark matter" / the residual / work-around.
              These hues mean the same thing in every figure.
Saturation  : saturated tone = a measured quantity (data lines, the recorded
              bar); pale tone = a share or residual region (area fills).
Neutrals    : INK = primary text + the measured line; MUTED = secondary text,
              ticks, annotations, sources; GRID = gridlines and light edges.
Type scale  : title 13 bold caps; subtitle 10; axis 10.5; ticks 9.5;
              annotation 9 (colored to its series); source 7.6 monospace.
Layout      : heading block top-left at a fixed position; a monospace source
              line in the bottom-left footer; annotations colored to match
              the series they describe.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images" / "the-blind-ledger"

# One canvas for every figure -> uniform scale in the reading column.
FIGSIZE = (7.4, 4.6)

# Shared palette (see DESIGN LANGUAGE above).
INK = "#202124"
MUTED = "#626A73"
GRID = "#D9DEE3"
BLUE = "#2D6282"        # tangible / recorded / what the ledger sees
BLUE_LIGHT = "#DCE8EF"
RED = "#B24A45"         # intangible / dark matter / the residual
RED_LIGHT = "#F1E2E0"

# Consistent footer position for the monospace source line.
SOURCE_X = 0.062
SOURCE_Y = 0.038


mpl.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10.5,
        "axes.titlesize": 11.5,
        "axes.labelsize": 10.5,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.edgecolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.unicode_minus": False,
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none",
        "svg.hashsalt": "the-blind-ledger",
    }
)


def _style_axis(ax: plt.Axes, *, grid: bool = True, axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=3, width=0.7, colors=MUTED)
    if grid:
        ax.grid(axis=axis, color=GRID, linewidth=0.7, alpha=0.7)
        ax.set_axisbelow(True)


def _figure_heading(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.062, 0.955, title.upper(), ha="left", va="top",
             fontsize=13, fontweight="bold", color=INK)
    fig.text(0.062, 0.905, subtitle, ha="left", va="top",
             fontsize=10, color=MUTED)


def _source(fig: plt.Figure, text: str) -> None:
    fig.text(SOURCE_X, SOURCE_Y, text, fontsize=7.6, color=MUTED, family="monospace")


def _save(fig: plt.Figure, name: str, preview_dir: Path | None) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / f"{name}.svg",
        format="svg",
        metadata={"Creator": "scripts/generate-blind-ledger-figures.py", "Date": None},
    )
    if preview_dir is not None:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            preview_dir / f"{name}.png",
            format="png",
            dpi=220,
            metadata={"Creator": "scripts/generate-blind-ledger-figures.py"},
        )
    plt.close(fig)


def _pct(value: float, _: int | None = None) -> str:
    return f"{int(round(value))}%"


def _callout(ax: plt.Axes, x: float, y: float, text: str, *, ha: str = "left") -> None:
    ax.text(x, y, text, fontsize=8.4, color=INK, ha=ha, va="center",
            bbox=dict(boxstyle="square,pad=0.32", facecolor="white",
                      edgecolor=GRID, linewidth=0.8), zorder=8)


def figure_1(preview_dir: Path | None) -> None:
    """The Ocean Tomo IAMV inversion: intangible share rises, 1975-2025."""

    # Ocean Tomo / J.S. Held IAMV study, S&P 500 constituents.
    # Anchors cited in the essay: 1975 = 17%, 1985 = 32%, 2005 = 79%, 2025 = 92%.
    years = np.array([1975, 1985, 1995, 2005, 2015, 2020, 2025], dtype=float)
    intangible = np.array([17, 32, 68, 79, 84, 90, 92], dtype=float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.135, right=0.95, top=0.79, bottom=0.155)
    _figure_heading(
        fig,
        "The fifty-year inversion",
        "Tangible vs intangible share of S&P 500 market value, 1975-2025.",
    )

    # Intangible grows from the bottom (red); tangible is the shrinking top (blue).
    ax.fill_between(years, 0, intangible, color=RED_LIGHT, zorder=1)
    ax.fill_between(years, intangible, 100, color=BLUE_LIGHT, zorder=1)
    ax.plot(years, intangible, color=INK, linewidth=2.0, zorder=4)
    ax.scatter(years, intangible, s=22, color=INK, edgecolors="white",
               linewidths=0.9, zorder=5)

    # The steep stretch the essay singles out: 1985-2005, +47 pp.
    ax.axvspan(1985, 2005, color=MUTED, alpha=0.06, zorder=0)
    ax.annotate("", xy=(2005, 94), xytext=(1985, 94),
                arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=0.9))
    ax.text(1995, 88, "+47 pp in 20 years", ha="center", va="center",
            fontsize=9, color=MUTED)

    # Crossover (intangible overtakes tangible) near 1990.
    ax.scatter([1990], [50], s=30, color=INK, edgecolors="white",
               linewidths=0.9, zorder=6)
    ax.annotate("~1990 crossover", xy=(1990, 50), xytext=(1996, 34),
                fontsize=8.4, color=MUTED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=0.8))

    # Band labels, colored to the semantics.
    ax.text(1981, 73, "Tangible", color=BLUE, fontsize=12.5, fontweight="bold",
            ha="left", va="center")
    ax.text(2012, 24, "Intangible", color=RED, fontsize=12.5, fontweight="bold",
            ha="right", va="center")

    # Endpoint callouts in open space (no line overlap).
    _callout(ax, 1976.5, 52, "1975\n17% intangible", ha="left")
    _callout(ax, 2024, 62, "2025\n92% intangible", ha="right")

    ax.set_xlim(1975, 2025)
    ax.set_ylim(0, 100)
    ax.set_xticks([1975, 1985, 1995, 2005, 2015, 2025])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(_pct))
    ax.set_ylabel("Share of S&P 500 market value")
    _style_axis(ax)

    _source(fig, "source: Ocean Tomo / J.S. Held IAMV study  |  intangible share = residual of market cap")

    _save(fig, "figure-1-the-fifty-year-inversion", preview_dir)


def figure_2(preview_dir: Path | None) -> None:
    """Two readings of accounting's erosion (Lev & Gu)."""

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.105, right=0.965, top=0.80, bottom=0.175, wspace=0.34)
    _figure_heading(
        fig,
        "The end of accounting",
        "One erosion, two readings: relevance falls as work-arounds rise.",
    )

    left, right = axes
    _style_axis(left)
    _style_axis(right)

    # Panel A (BLUE = the ledger's reach): R^2 of earnings + book value vs market cap.
    ya, yb = 1953, 2013
    decline_x = np.linspace(ya, yb, 200)
    decline_y = 0.86 - (0.86 - 0.50) * (decline_x - ya) / (yb - ya)
    left.fill_between(decline_x, 0, decline_y, color=BLUE_LIGHT, alpha=0.8, zorder=1)
    left.plot(decline_x, decline_y, color=BLUE, linewidth=2.4, zorder=3)
    left.scatter([ya, yb], [0.86, 0.50], s=28, color=BLUE,
                 edgecolors="white", linewidths=0.9, zorder=5)
    left.set_xlim(1950, 2016)
    left.set_ylim(0, 1.0)
    left.set_xticks([1955, 1985, 2015])
    left.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    left.set_yticks(np.arange(0, 1.01, 0.25))
    left.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.2f}"))
    left.set_ylabel(r"$R^2$ : accounting $\rightarrow$ market cap")
    left.set_title("(A) Explanatory power", loc="left", fontweight="bold",
                   color=INK, pad=8, fontsize=10.5)
    left.annotate("0.80-0.90", xy=(ya, 0.86), xytext=(1957, 0.93),
                  fontsize=8.6, color=BLUE, ha="left", va="center")
    left.annotate("~0.50", xy=(yb, 0.50), xytext=(1986, 0.30),
                  fontsize=8.6, color=BLUE, ha="left", va="center",
                  arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=0.9))

    # Panel B (RED = the work-around): firms reporting non-GAAP earnings, 2003->2013.
    yrs = np.array([2003, 2013], dtype=float)
    share = np.array([20, 40], dtype=float)
    right.fill_between(yrs, 0, share, color=RED_LIGHT, alpha=0.8, zorder=1)
    right.plot(yrs, share, color=RED, linewidth=2.4, zorder=3,
               marker="o", markersize=6, markerfacecolor="white", markeredgewidth=1.4)
    right.set_xlim(2001, 2015)
    right.set_ylim(0, 50)
    right.set_xticks([2003, 2008, 2013])
    right.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    right.set_yticks(np.arange(0, 51, 10))
    right.yaxis.set_major_formatter(FuncFormatter(_pct))
    right.set_ylabel("Firms disclosing non-GAAP earnings")
    right.set_title("(B) The work-around", loc="left", fontweight="bold",
                    color=INK, pad=8, fontsize=10.5)
    right.annotate("20%", xy=(2003, 20), xytext=(2003.3, 12),
                   fontsize=9, color=RED, ha="left", va="center")
    right.annotate("40%", xy=(2013, 40), xytext=(2012.7, 45),
                   fontsize=9, color=RED, ha="right", va="center")
    right.text(0.05, 0.90, "doubled in\na decade", transform=right.transAxes,
               fontsize=8.6, fontweight="bold", color=INK, ha="left", va="top")

    _source(fig, "source: Lev & Gu, The End of Accounting (2016)  |  R^2 endpoints cited; path schematic")

    _save(fig, "figure-2-the-end-of-accounting", preview_dir)


def figure_3(preview_dir: Path | None) -> None:
    """How much of market value the balance sheet records: NVIDIA vs Berkshire."""

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.06, right=0.95, top=0.82, bottom=0.225)
    _figure_heading(
        fig,
        "What the ledger sees",
        "Share of market value recorded on the balance sheet.",
    )

    rows = [
        ("NVIDIA", "Apr 2026", 4.0, "$195.5B equity of $4.9T market cap  ·  25× gap"),
        ("Berkshire Hathaway", "YE 2018", 69.0, "$212.5K book vs $306K price per share  ·  1.4×"),
    ]
    y = np.array([1.0, 0.0])
    height = 0.34

    for yi, (name, period, visible, note) in zip(y, rows):
        # recorded = BLUE (measured); dark matter = pale RED (residual).
        ax.barh(yi, visible, height=height, color=BLUE, zorder=3)
        ax.barh(yi, 100 - visible, left=visible, height=height,
                color=RED_LIGHT, edgecolor=RED, linewidth=0.9, zorder=2)
        # headline above the bar
        ax.text(0, yi + height / 2 + 0.13,
                f"{name} ({period}) — {int(round(visible))}% on the books",
                va="bottom", ha="left", fontsize=10, color=INK, fontweight="bold")
        # value marker at the recorded (blue) end
        if visible >= 25:
            ax.text(visible - 1.8, yi, f"{int(round(visible))}%", va="center",
                    ha="right", fontsize=9.5, color="white", fontweight="bold")
        else:
            ax.text(visible + 1.8, yi, f"{int(round(visible))}%", va="center",
                    ha="left", fontsize=9.5, color=BLUE, fontweight="bold")
        # supporting figures below the bar (parse_math off so "$" stays literal)
        ax.text(0, yi - height / 2 - 0.12, note, va="top", ha="left",
                fontsize=8.4, color=MUTED, parse_math=False)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.95, 1.5)
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, 101, 20))
    ax.xaxis.set_major_formatter(FuncFormatter(_pct))
    ax.set_xlabel("Percent of market value")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=3, width=0.7, colors=MUTED)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.6)
    ax.set_axisbelow(True)

    handles = [
        Patch(facecolor=BLUE, label="recorded on the balance sheet"),
        Patch(facecolor=RED_LIGHT, edgecolor=RED, linewidth=0.9,
              label="intangible “dark matter” (residual)"),
    ]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(SOURCE_X, 0.028),
               ncol=2, frameon=False, handlelength=1.2, handleheight=1.1,
               columnspacing=1.8, fontsize=8.6)

    _save(fig, "figure-3-the-ledger-dark-matter", preview_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, default=None,
                        help="Optional directory for high-resolution PNG previews.")
    args = parser.parse_args()

    figure_1(args.preview_dir)
    figure_2(args.preview_dir)
    figure_3(args.preview_dir)


if __name__ == "__main__":
    main()
