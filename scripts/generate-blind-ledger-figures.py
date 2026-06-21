#!/usr/bin/env python3
"""Generate the figures for "The Blind Ledger".

All figures share one fixed canvas size and are saved without a tight
bounding box, so each SVG has identical intrinsic dimensions. That keeps
them visually uniform and correctly scaled when displayed inside the
650px reading column (no breakout).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images" / "the-blind-ledger"

# One canvas for every figure -> uniform scale in the reading column.
FIGSIZE = (7.4, 4.6)

INK = "#202124"
MUTED = "#626A73"
GRID = "#D9DEE3"
LIGHT = "#EEF1F3"
RESIDUAL = "#C9CED3"
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
    fig.text(0.065, 0.955, title.upper(), ha="left", va="top",
             fontsize=13, fontweight="bold", color=INK)
    fig.text(0.065, 0.905, subtitle, ha="left", va="top",
             fontsize=10, color=MUTED)


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


def figure_1(preview_dir: Path | None) -> None:
    """The Ocean Tomo IAMV inversion: tangible vs intangible share, 1975-2025."""

    # Ocean Tomo / J.S. Held IAMV study, S&P 500 constituents.
    # Anchors cited in the essay: 1975 = 17%, 1985 = 32%, 2005 = 79%, 2025 = 92%.
    years = np.array([1975, 1985, 1995, 2005, 2015, 2020, 2025], dtype=float)
    intangible = np.array([17, 32, 68, 79, 84, 90, 92], dtype=float)
    tangible = 100 - intangible

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.135, right=0.95, top=0.79, bottom=0.13)
    _figure_heading(
        fig,
        "The fifty-year inversion",
        "Intangibles' share of S&P 500 market value, 1975-2025 (Ocean Tomo IAMV).",
    )

    ax.fill_between(years, 0, tangible, color=BLUE_LIGHT, zorder=1)
    ax.fill_between(years, tangible, 100, color=RED_LIGHT, zorder=1)
    ax.plot(years, tangible, color=INK, linewidth=2.0, zorder=4)
    ax.scatter(years, tangible, s=22, color=INK, edgecolors="white",
               linewidths=0.9, zorder=5)

    # The steep stretch the essay singles out: 1985-2005, +47 pp.
    ax.axvspan(1985, 2005, color=MUTED, alpha=0.07, zorder=0)
    ax.annotate("", xy=(2005, 96), xytext=(1985, 96),
                arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=0.9))
    ax.text(1995, 90, "+47 pp in 20 years", ha="center", va="center",
            fontsize=9, color=MUTED)

    # Crossover (intangible = tangible = 50%), interpolated near 1990.
    ax.scatter([1990], [50], s=30, color=RED, edgecolors="white",
               linewidths=0.9, zorder=6)
    ax.text(1991.5, 56, "~1990 crossover", fontsize=8.4, color=MUTED,
            ha="left", va="center")

    # Band labels.
    ax.text(2011, 66, "intangible", color=RED, fontsize=12, fontweight="bold",
            ha="center", va="center")
    ax.text(1980, 9, "tangible", color=BLUE, fontsize=12, fontweight="bold",
            ha="left", va="center")

    # Endpoint callouts.
    ax.text(1976, 77, "1975\n83% tangible", fontsize=8.4, color=INK,
            ha="left", va="top",
            bbox=dict(boxstyle="square,pad=0.3", facecolor="white",
                      edgecolor=GRID, linewidth=0.8))
    ax.text(2024.5, 64, "2025\n92% intangible", fontsize=8.4, color=INK,
            ha="right", va="top",
            bbox=dict(boxstyle="square,pad=0.3", facecolor="white",
                      edgecolor=GRID, linewidth=0.8))

    ax.set_xlim(1975, 2025)
    ax.set_ylim(0, 100)
    ax.set_xticks([1975, 1985, 1995, 2005, 2015, 2025])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(_pct))
    ax.set_ylabel("Share of S&P 500 market value")
    _style_axis(ax)

    ax.text(1975.4, 2.5,
            "source: Ocean Tomo / J.S. Held IAMV study   |   share = residual of market cap",
            fontsize=7.6, color=MUTED, family="monospace", zorder=7)

    _save(fig, "figure-1-the-fifty-year-inversion", preview_dir)


def figure_2(preview_dir: Path | None) -> None:
    """Two readings of accounting's erosion (Lev & Gu)."""

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.105, right=0.965, top=0.80, bottom=0.16, wspace=0.34)
    _figure_heading(
        fig,
        "The end of accounting",
        "One erosion, two readings: relevance falls as work-arounds rise.",
    )

    left, right = axes
    _style_axis(left)
    _style_axis(right)

    # Panel A: explanatory power (R-squared) of earnings + book value vs market cap.
    ya, yb = 1953, 2013
    decline_x = np.linspace(ya, yb, 200)
    decline_y = 0.86 - (0.86 - 0.50) * (decline_x - ya) / (yb - ya)
    left.fill_between(decline_x, 0, decline_y, color=BLUE_LIGHT, alpha=0.7, zorder=1)
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

    # Panel B: share of listed firms reporting non-GAAP earnings, 2003 -> 2013.
    yrs = np.array([2003, 2013], dtype=float)
    share = np.array([20, 40], dtype=float)
    right.fill_between(yrs, 0, share, color=RED_LIGHT, alpha=0.7, zorder=1)
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

    fig.text(0.105, 0.045, "source: Lev & Gu, The End of Accounting (2016)  |  R² endpoints cited; path schematic",
             fontsize=7.6, color=MUTED, family="monospace")

    _save(fig, "figure-2-the-end-of-accounting", preview_dir)


def figure_3(preview_dir: Path | None) -> None:
    """How much of market value the balance sheet records: NVIDIA vs Berkshire."""

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.06, right=0.95, top=0.82, bottom=0.20)
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
        ax.barh(yi, visible, height=height, color=INK, zorder=3)
        ax.barh(yi, 100 - visible, left=visible, height=height,
                color=LIGHT, edgecolor=GRID, linewidth=0.8, zorder=2)
        # headline above the bar
        ax.text(0, yi + height / 2 + 0.13,
                f"{name} ({period}) — {int(round(visible))}% on the books",
                va="bottom", ha="left", fontsize=10, color=INK, fontweight="bold")
        # value marker at the filled end
        if visible >= 25:
            ax.text(visible - 1.6, yi, f"{int(round(visible))}%", va="center",
                    ha="right", fontsize=9.5, color="white", fontweight="bold")
        else:
            ax.text(visible + 1.6, yi, f"{int(round(visible))}%", va="center",
                    ha="left", fontsize=9.5, color=INK, fontweight="bold")
        # supporting figures below the bar (parse_math off so "$" stays literal)
        ax.text(0, yi - height / 2 - 0.12, note, va="top", ha="left",
                fontsize=8.4, color=MUTED, parse_math=False)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.9, 1.48)
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

    # Legend strip.
    ax.text(0.0, -0.74, "■", color=INK, fontsize=11, va="center", ha="left",
            transform=ax.get_yaxis_transform())
    ax.text(0.025, -0.74, "recorded on the balance sheet", color=MUTED, fontsize=8.4,
            va="center", ha="left", transform=ax.get_yaxis_transform())
    ax.text(0.52, -0.74, "■", color=RESIDUAL, fontsize=11, va="center", ha="left",
            transform=ax.get_yaxis_transform())
    ax.text(0.545, -0.74, "intangible “dark matter”", color=MUTED, fontsize=8.4,
            va="center", ha="left", transform=ax.get_yaxis_transform())

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
