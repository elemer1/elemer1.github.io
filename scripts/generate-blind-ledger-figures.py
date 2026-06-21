#!/usr/bin/env python3
"""Generate the figures for "The Blind Ledger"."""

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
        "svg.hashsalt": "the-blind-ledger",
    }
)


def _style_axis(ax: plt.Axes, *, grid: bool = True) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=3, width=0.7, colors=MUTED)
    if grid:
        ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.7)
        ax.set_axisbelow(True)


def _figure_heading(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(
        0.07,
        0.965,
        title.upper(),
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.925,
        subtitle,
        ha="left",
        va="top",
        fontsize=9.5,
        color=MUTED,
    )


def _save(fig: plt.Figure, name: str, preview_dir: Path | None) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / f"{name}.svg",
        format="svg",
        bbox_inches="tight",
        metadata={"Creator": "scripts/generate-blind-ledger-figures.py", "Date": None},
    )
    if preview_dir is not None:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            preview_dir / f"{name}.png",
            format="png",
            dpi=220,
            bbox_inches="tight",
            metadata={"Creator": "scripts/generate-blind-ledger-figures.py"},
        )
    plt.close(fig)


def _pct(value: float, _: int | None = None) -> str:
    return f"{int(round(value))}%"


def figure_1(preview_dir: Path | None) -> None:
    """The Ocean Tomo IAMV inversion: tangible vs intangible share, 1975-2025."""

    # Ocean Tomo / J.S. Held IAMV study, S&P 500 constituents.
    # Anchors cited in the essay: 1975 = 17%, 1985 = 32%, 2005 = 79%, 2025 = 92%.
    # Intermediate years use the study's published decade points.
    years = np.array([1975, 1985, 1995, 2005, 2015, 2020, 2025], dtype=float)
    intangible = np.array([17, 32, 68, 79, 84, 90, 92], dtype=float)
    tangible = 100 - intangible

    fig, ax = plt.subplots(figsize=(11.0, 6.2))
    fig.subplots_adjust(left=0.085, right=0.965, bottom=0.12, top=0.84)
    _figure_heading(
        fig,
        "The fifty-year inversion",
        "Intangibles' share of S&P 500 market value, 1975-2025 (Ocean Tomo IAMV).",
    )

    ax.fill_between(years, 0, tangible, color=BLUE_LIGHT, zorder=1)
    ax.fill_between(years, tangible, 100, color=RED_LIGHT, zorder=1)
    ax.plot(years, tangible, color=INK, linewidth=2.0, zorder=4)
    ax.scatter(
        years,
        tangible,
        s=26,
        color=INK,
        edgecolors="white",
        linewidths=0.9,
        zorder=5,
    )

    # The steep stretch the essay singles out: 1985-2005, +47 pp.
    ax.axvspan(1985, 2005, color=MUTED, alpha=0.07, zorder=0)
    ax.annotate(
        "",
        xy=(2005, 96),
        xytext=(1985, 96),
        arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=0.9),
    )
    ax.text(
        1995,
        91,
        "+47 pp in 20 years",
        ha="center",
        va="center",
        fontsize=9.0,
        color=MUTED,
    )

    # Crossover (intangible = tangible = 50%), interpolated near 1990.
    ax.scatter([1990], [50], s=34, color=RED, edgecolors="white", linewidths=0.9, zorder=6)
    ax.annotate(
        "~1990: intangibles\novertake tangibles",
        xy=(1990, 50),
        xytext=(1997, 22),
        fontsize=8.8,
        color=MUTED,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=0.9),
    )

    # Band labels.
    ax.text(2009, 68, "intangible", color=RED, fontsize=12, fontweight="bold",
            ha="center", va="center")
    ax.text(1980, 9, "tangible", color=BLUE, fontsize=12, fontweight="bold",
            ha="left", va="center")

    # Endpoint callouts.
    ax.text(1976, 78, "1975\n83% tangible\n17% intangible", fontsize=8.6, color=INK,
            ha="left", va="top",
            bbox=dict(boxstyle="square,pad=0.3", facecolor="white", edgecolor=GRID, linewidth=0.8))
    ax.text(2024.6, 68, "2025\n92% intangible\n8% tangible", fontsize=8.6, color=INK,
            ha="right", va="top",
            bbox=dict(boxstyle="square,pad=0.3", facecolor="white", edgecolor=GRID, linewidth=0.8))

    ax.set_xlim(1975, 2025)
    ax.set_ylim(0, 100)
    ax.set_xticks([1975, 1985, 1995, 2005, 2015, 2025])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(_pct))
    ax.set_ylabel("Share of S&P 500 market value")
    _style_axis(ax)

    ax.text(
        1975.4,
        2.5,
        "source: Ocean Tomo / J.S. Held IAMV study   |   intangible share = (market cap - net tangible assets) / market cap",
        fontsize=7.6,
        color=MUTED,
        family="monospace",
        zorder=7,
    )

    _save(fig, "figure-1-the-fifty-year-inversion", preview_dir)


def figure_2(preview_dir: Path | None) -> None:
    """Two readings of accounting's erosion (Lev & Gu)."""

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4))
    fig.subplots_adjust(left=0.075, right=0.97, bottom=0.16, top=0.80, wspace=0.26)
    _figure_heading(
        fig,
        "The end of accounting",
        "Two readings of one erosion: statutory relevance falls as work-arounds rise.",
    )

    left, right = axes
    _style_axis(left)
    _style_axis(right)

    # Panel A: explanatory power (R-squared) of earnings + book value vs market cap.
    # Lev & Gu (2016): ~0.80-0.90 in the 1950s declining steadily to ~0.50 recently.
    # Endpoints are cited; the intermediate path is a monotone schematic.
    ya, yb = 1953, 2013
    decline_x = np.linspace(ya, yb, 200)
    decline_y = 0.86 - (0.86 - 0.50) * (decline_x - ya) / (yb - ya)
    left.fill_between(decline_x, 0, decline_y, color=BLUE_LIGHT, alpha=0.7, zorder=1)
    left.plot(decline_x, decline_y, color=BLUE, linewidth=2.6, zorder=3)
    left.scatter([ya, yb], [0.86, 0.50], s=34, color=BLUE,
                 edgecolors="white", linewidths=0.9, zorder=5)
    left.set_xlim(1950, 2016)
    left.set_ylim(0, 1.0)
    left.set_xticks([1955, 1975, 1995, 2015])
    left.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    left.set_yticks(np.arange(0, 1.01, 0.25))
    left.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.2f}"))
    left.set_ylabel(r"$R^2$ : accounting $\rightarrow$ market cap")
    left.set_title("(A) Explanatory power", loc="left", fontweight="bold", color=INK, pad=10)
    left.annotate("1950s: 0.80-0.90", xy=(ya, 0.86), xytext=(1958, 0.93),
                  fontsize=8.8, color=BLUE, ha="left", va="center")
    left.annotate("recent: ~0.50", xy=(yb, 0.50), xytext=(1988, 0.30),
                  fontsize=8.8, color=BLUE, ha="left", va="center",
                  arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=0.9))
    left.text(0.04, 0.06, "earnings + book value regressed on market cap",
              transform=left.transAxes, fontsize=7.6, color=MUTED, family="monospace")

    # Panel B: share of listed firms reporting non-GAAP earnings, 2003 -> 2013.
    yrs = np.array([2003, 2013], dtype=float)
    share = np.array([20, 40], dtype=float)
    right.plot(yrs, share, color=RED, linewidth=2.6, zorder=3,
               marker="o", markersize=6, markerfacecolor="white", markeredgewidth=1.4)
    right.fill_between(yrs, 0, share, color=RED_LIGHT, alpha=0.7, zorder=1)
    right.set_xlim(2001, 2015)
    right.set_ylim(0, 50)
    right.set_xticks([2003, 2008, 2013])
    right.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    right.set_yticks(np.arange(0, 51, 10))
    right.yaxis.set_major_formatter(FuncFormatter(_pct))
    right.set_ylabel("Listed firms disclosing non-GAAP earnings")
    right.set_title("(B) The market's work-around", loc="left", fontweight="bold", color=INK, pad=10)
    right.annotate("20%", xy=(2003, 20), xytext=(2003.3, 13),
                   fontsize=9.4, color=RED, ha="left", va="center")
    right.annotate("40%", xy=(2013, 40), xytext=(2012.7, 44),
                   fontsize=9.4, color=RED, ha="right", va="center")
    right.text(0.04, 0.92, "doubled in a decade", transform=right.transAxes,
               fontsize=9.0, fontweight="bold", color=INK, ha="left", va="top")
    right.text(0.04, 0.06, "source: Lev & Gu, The End of Accounting (2016)",
               transform=right.transAxes, fontsize=7.6, color=MUTED, family="monospace")

    _save(fig, "figure-2-the-end-of-accounting", preview_dir)


def figure_3(preview_dir: Path | None) -> None:
    """How much of market value the balance sheet records: NVIDIA vs Berkshire."""

    fig, ax = plt.subplots(figsize=(11.0, 4.9))
    fig.subplots_adjust(left=0.20, right=0.965, bottom=0.22, top=0.82)
    _figure_heading(
        fig,
        "What the ledger sees",
        "Share of market value recorded on the balance sheet.",
    )

    rows = [
        ("NVIDIA\n(Apr 2026)", 4.0, "$195.5B equity\nof $4.9T market cap", "25×"),
        ("Berkshire Hathaway\n(YE 2018)", 69.0, "$212.5K book vs\n$306K price per share", "1.4×"),
    ]
    y = np.arange(len(rows))[::-1]
    height = 0.46

    for yi, (_, visible, note, mult) in zip(y, rows):
        ax.barh(yi, visible, height=height, color=INK, zorder=3)
        ax.barh(yi, 100 - visible, left=visible, height=height,
                color=LIGHT, edgecolor=GRID, linewidth=0.8, zorder=2)
        label = f"{int(round(visible))}% on the books"
        if visible >= 25:
            ax.text(visible - 1.6, yi + 0.04, label, va="center", ha="right",
                    fontsize=9.5, color="white", fontweight="bold")
        else:
            ax.text(visible + 1.6, yi + 0.04, label, va="center", ha="left",
                    fontsize=9.5, color=INK, fontweight="bold")
        # absolute figures below the bar, ratio tag above it
        ax.text(99, yi - height / 2 - 0.10, note, va="top", ha="right",
                fontsize=8.2, color=MUTED)
        ax.text(99, yi + height / 2 + 0.06, f"market cap / book = {mult}",
                va="bottom", ha="right", fontsize=8.0, color=MUTED, style="italic")

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.85, len(rows) - 0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=9.5, color=INK)
    ax.set_xticks(np.arange(0, 101, 20))
    ax.xaxis.set_major_formatter(FuncFormatter(_pct))
    ax.set_xlabel("Percent of market value")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=3, width=0.7, colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.6)
    ax.set_axisbelow(True)

    # Legend strip.
    ax.text(0.0, -0.74, "■", color=INK, fontsize=11, va="center", ha="left",
            transform=ax.get_yaxis_transform())
    ax.text(0.02, -0.74, "recorded on the balance sheet", color=MUTED, fontsize=8.4,
            va="center", ha="left", transform=ax.get_yaxis_transform())
    ax.text(0.42, -0.74, "■", color="#C9CED3", fontsize=11, va="center", ha="left",
            transform=ax.get_yaxis_transform())
    ax.text(0.44, -0.74, "intangible “dark matter” (residual)", color=MUTED, fontsize=8.4,
            va="center", ha="left", transform=ax.get_yaxis_transform())

    _save(fig, "figure-3-the-ledger-dark-matter", preview_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preview-dir",
        type=Path,
        default=None,
        help="Optional directory for high-resolution PNG previews.",
    )
    args = parser.parse_args()

    figure_1(args.preview_dir)
    figure_2(args.preview_dir)
    figure_3(args.preview_dir)


if __name__ == "__main__":
    main()
