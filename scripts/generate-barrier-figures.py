#!/usr/bin/env python3
"""Generate the three figures for "The Barrier That Moved"."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images" / "the-barrier-that-moved"

INK = "#202124"
MUTED = "#626A73"
GRID = "#D9DEE3"
LIGHT = "#EEF1F3"
PATH_GRAY = "#A7AEB5"
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
        "svg.hashsalt": "the-barrier-that-moved",
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
        metadata={"Creator": "scripts/generate-barrier-figures.py", "Date": None},
    )
    if preview_dir is not None:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            preview_dir / f"{name}.png",
            format="png",
            dpi=220,
            bbox_inches="tight",
            metadata={"Creator": "scripts/generate-barrier-figures.py"},
        )
    plt.close(fig)


def figure_1(preview_dir: Path | None) -> None:
    """Plot the simulated path density against the two analytic trajectories."""

    rounds = 100
    paths = 200_000
    rng = np.random.default_rng(42)

    log_up = np.float32(np.log10(1.5))
    log_down = np.float32(np.log10(0.6))
    increments = np.where(
        rng.random((paths, rounds), dtype=np.float32) < 0.5,
        log_up,
        log_down,
    ).astype(np.float32, copy=False)

    log_paths = np.empty((paths, rounds + 1), dtype=np.float32)
    log_paths[:, 0] = 0.0
    np.cumsum(increments, axis=1, out=log_paths[:, 1:])
    del increments

    fig, ax = plt.subplots(figsize=(11.0, 6.35))
    fig.subplots_adjust(left=0.10, right=0.93, bottom=0.13, top=0.84)
    _figure_heading(
        fig,
        "The lie of the ensemble",
        "The simulated mass of individual lives falls while the ensemble mean rises.",
    )

    y_min, y_max = -8.0, 6.0
    bins = np.linspace(y_min, y_max, 185)
    density = np.empty((len(bins) - 1, rounds + 1), dtype=float)
    for idx in range(rounds + 1):
        counts, _ = np.histogram(log_paths[:, idx], bins=bins)
        density[:, idx] = np.log1p(counts)
    density[density == 0] = np.nan

    q05, q50, q95 = np.quantile(log_paths, [0.05, 0.50, 0.95], axis=0)
    del log_paths

    cloud_cmap = LinearSegmentedColormap.from_list(
        "path-density",
        [
            (1.0, 1.0, 1.0, 0.0),
            (0.78, 0.81, 0.84, 0.35),
            (0.42, 0.46, 0.50, 0.62),
        ],
    )
    x_edges = np.arange(-0.5, rounds + 1.5)
    ax.pcolormesh(
        x_edges,
        bins,
        density,
        cmap=cloud_cmap,
        shading="auto",
        zorder=1,
    )
    n = np.arange(rounds + 1)
    ax.fill_between(
        n,
        q05,
        q95,
        color="#C9CED3",
        alpha=0.22,
        linewidth=0,
        zorder=2,
        label="central 90% of simulated paths",
    )
    ax.plot(q50, color=INK, linewidth=1.0, linestyle=(0, (2, 2)), alpha=0.75, zorder=3)

    ensemble = n * np.log10(1.05)
    typical = n * np.log10(np.sqrt(0.9))
    ax.plot(
        n,
        ensemble,
        color=RED,
        linewidth=2.9,
        zorder=5,
        label=r"ensemble mean: $1.05^n$",
    )
    ax.plot(
        n,
        typical,
        color=BLUE,
        linewidth=2.9,
        zorder=5,
        label=r"typical life: $0.9487^n$",
    )

    ax.set_xlim(0, 106)
    ax.set_ylim(-8.8, 6.2)
    ax.set_xticks(np.arange(0, 101, 20))
    ax.set_yticks(np.arange(-8, 7, 2))
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: rf"$10^{{{int(value)}}}$")
    )
    ax.set_xlabel("Round, $n$")
    ax.set_ylabel("Wealth, $X_n$ (log scale)")
    _style_axis(ax)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98),
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor=GRID,
        borderpad=0.55,
        handlelength=2.6,
    )

    gap_x = 102
    gap_top = gap_x * np.log10(1.05)
    gap_bottom = gap_x * np.log10(np.sqrt(0.9))
    ax.annotate(
        "",
        xy=(gap_x, gap_top),
        xytext=(gap_x, gap_bottom),
        arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=0.9),
        zorder=5,
    )
    ax.text(
        gap_x + 1.1,
        (gap_top + gap_bottom) / 2,
        "ergodicity gap",
        rotation=90,
        ha="left",
        va="center",
        fontsize=8.8,
        color=MUTED,
        zorder=5,
    )

    ax.scatter(
        [100, 100],
        [ensemble[-1], typical[-1]],
        s=24,
        color=[RED, BLUE],
        edgecolors="white",
        linewidths=0.8,
        zorder=7,
    )
    ax.text(
        101.0,
        ensemble[-1],
        r"$131.5$",
        color=RED,
        fontsize=9.0,
        ha="left",
        va="center",
        zorder=7,
    )
    ax.text(
        101.0,
        typical[-1],
        r"$0.0051$",
        color=BLUE,
        fontsize=9.0,
        ha="left",
        va="center",
        zorder=7,
    )
    ax.text(
        2,
        -8.25,
        "path density from 200,000 simulated lives   |   p = 0.5   |   multipliers = 1.5, 0.6",
        fontsize=8.1,
        color=MUTED,
        family="monospace",
        zorder=6,
    )

    _save(fig, "figure-1-the-lie-of-the-ensemble", preview_dir)


def _format_year(value: float, _: int | None = None) -> str:
    year = int(round(value))
    if year < 0:
        return f"{abs(year):,} BCE"
    if year == 1:
        return "1 CE"
    return f"{year:,}"


def figure_2(preview_dir: Path | None) -> None:
    """Plot DeLong's preferred long-run world GDP-per-capita reconstruction."""

    # DeLong (1998), preferred series, 1990 international dollars.
    years = np.array(
        [
            -10000,
            -8000,
            -5000,
            -4000,
            -3000,
            -2000,
            -1600,
            -1000,
            -800,
            -500,
            -400,
            -200,
            1,
            14,
            200,
            350,
            400,
            500,
            600,
            700,
            800,
            900,
            1000,
            1100,
            1200,
            1250,
            1300,
            1340,
            1400,
            1500,
            1600,
            1650,
            1700,
            1750,
            1800,
            1850,
            1875,
            1900,
            1920,
            1925,
            1930,
            1940,
            1950,
            1955,
            1960,
            1965,
            1970,
            1975,
            1980,
            1985,
            1990,
            1995,
            2000,
        ],
        dtype=float,
    )
    gdp = np.array(
        [
            93,
            96,
            103,
            109,
            113,
            112,
            121,
            127,
            143,
            137,
            130,
            113,
            109,
            102,
            98,
            94,
            97,
            102,
            104,
            112,
            116,
            131,
            133,
            124,
            104,
            99,
            89,
            109,
            128,
            138,
            141,
            150,
            164,
            178,
            195,
            300,
            429,
            679,
            956,
            1108,
            1134,
            1356,
            1622,
            1968,
            2270,
            2736,
            3282,
            3714,
            4231,
            4634,
            5204,
            5840,
            6539,
        ],
        dtype=float,
    )
    subsistence = 115.0

    fig = plt.figure(figsize=(11.0, 7.1))
    fig.subplots_adjust(left=0.10, right=0.95, bottom=0.10, top=0.86)
    grid = fig.add_gridspec(2, 1, height_ratios=[2.05, 1.25], hspace=0.25)
    ax = fig.add_subplot(grid[0])
    zoom = fig.add_subplot(grid[1])
    _figure_heading(
        fig,
        "The Malthusian break",
        "A stationary subsistence band breaks into modern non-stationary growth.",
    )

    pre = years <= 1800
    post = years >= 1800
    ax.axhspan(80, 220, color=LIGHT, zorder=0)
    ax.axhline(
        subsistence,
        color=MUTED,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
        zorder=1,
    )
    ax.plot(
        years[pre],
        gdp[pre],
        color=INK,
        linewidth=1.6,
        marker="o",
        markersize=2.8,
        markerfacecolor="white",
        markeredgewidth=0.7,
        zorder=3,
    )
    ax.plot(
        years[post],
        gdp[post],
        color=RED,
        linewidth=2.3,
        marker="o",
        markersize=3.2,
        markerfacecolor="white",
        markeredgewidth=0.9,
        zorder=4,
    )
    ax.axvline(1800, color=RED, linewidth=1.0, linestyle=(0, (3, 3)), zorder=2)

    ax.set_xlim(-10000, 2026)
    ax.set_ylim(0, 7000)
    ax.set_xticks([-10000, -8000, -6000, -4000, -2000, 1, 2000])
    ax.xaxis.set_major_formatter(FuncFormatter(_format_year))
    ax.set_yticks(np.arange(0, 7001, 1000))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{int(value):,}"))
    ax.set_ylabel("World GDP per person\n(1990 international dollars)")
    _style_axis(ax)

    ax.text(
        -9800,
        305,
        r"subsistence band, $s \approx 115$",
        fontsize=8.5,
        color=MUTED,
        ha="left",
        va="bottom",
    )
    ax.annotate(
        "1800 CE\nbreak",
        xy=(1800, 195),
        xytext=(620, 1450),
        color=RED,
        fontsize=9.2,
        ha="right",
        va="center",
        arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.0),
        bbox=dict(boxstyle="square,pad=0.25", facecolor="white", edgecolor="none", alpha=0.92),
        zorder=6,
    )
    ax.annotate(
        "2000 CE: $6,539",
        xy=(2000, 6539),
        xytext=(760, 6250),
        color=RED,
        fontsize=9.2,
        ha="right",
        va="center",
        arrowprops=dict(arrowstyle="-", color=RED, linewidth=1.0),
        bbox=dict(boxstyle="square,pad=0.25", facecolor="white", edgecolor="none", alpha=0.92),
        zorder=6,
    )
    ax.text(
        0.01,
        0.92,
        "full scale",
        transform=ax.transAxes,
        fontsize=8.3,
        color=MUTED,
        ha="left",
        va="top",
        family="monospace",
    )

    zoom.axhspan(80, 220, color=LIGHT, zorder=0)
    zoom.axhline(
        subsistence,
        color=MUTED,
        linewidth=0.9,
        linestyle=(0, (4, 3)),
        zorder=1,
    )
    zoom.plot(
        years[pre],
        gdp[pre],
        color=INK,
        linewidth=1.5,
        marker="o",
        markersize=3.0,
        markerfacecolor="white",
        markeredgewidth=0.7,
        zorder=3,
    )
    zoom.set_xlim(-10000, 1800)
    zoom.set_ylim(75, 220)
    zoom.set_xticks([-10000, -7500, -5000, -2500, 1, 1800])
    zoom.xaxis.set_major_formatter(FuncFormatter(_format_year))
    zoom.set_yticks([80, 115, 150, 200])
    zoom.set_xlabel("Human history (axis extends to 2026; reconstruction data end at 2000)")
    zoom.set_ylabel("pre-1800\nzoom")
    _style_axis(zoom)
    zoom.text(
        0.01,
        0.94,
        "pre-industrial attractor",
        transform=zoom.transAxes,
        fontsize=8.3,
        fontweight="bold",
        ha="left",
        va="top",
        color=INK,
    )
    zoom.annotate(
        "",
        xy=(-2450, subsistence + 3),
        xytext=(-2450, 195),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=0.8),
    )
    zoom.annotate(
        "",
        xy=(-2450, subsistence - 3),
        xytext=(-2450, 82),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=0.8),
    )
    zoom.text(
        -2150,
        154,
        r"restoring force: $|\rho|<1$",
        fontsize=8.2,
        color=BLUE,
        ha="left",
        va="center",
    )
    zoom.text(
        -9800,
        subsistence + 5,
        r"$s$",
        fontsize=8.5,
        color=MUTED,
        ha="left",
        va="bottom",
    )

    _save(fig, "figure-2-the-malthusian-break", preview_dir)


def _jensen_geometry(
    ax: plt.Axes,
    x1: float,
    x2: float,
    curve,
    *,
    color: str,
    arrow_label: str,
    label_offset: tuple[float, float] = (0.12, 0.0),
) -> None:
    xm = (x1 + x2) / 2
    y1 = curve(x1)
    y2 = curve(x2)
    y_curve = curve(xm)
    y_chord = (y1 + y2) / 2
    ax.plot(
        [x1, x2],
        [y1, y2],
        color=MUTED,
        linewidth=1.0,
        linestyle=(0, (3, 2)),
        zorder=2,
    )
    ax.scatter(
        [x1, x2],
        [y1, y2],
        s=28,
        facecolors="white",
        edgecolors=MUTED,
        linewidths=0.9,
        zorder=4,
    )
    ax.scatter(
        [xm],
        [y_curve],
        s=32,
        color=color,
        edgecolors="white",
        linewidths=0.8,
        zorder=5,
    )
    ax.scatter(
        [xm],
        [y_chord],
        s=24,
        color=MUTED,
        edgecolors="white",
        linewidths=0.7,
        zorder=5,
    )
    ax.annotate(
        "",
        xy=(xm, y_chord),
        xytext=(xm, y_curve),
        arrowprops=dict(arrowstyle="-|>", color=color, linewidth=1.2),
        zorder=5,
    )
    ax.text(
        xm + label_offset[0],
        (y_curve + y_chord) / 2 + label_offset[1],
        arrow_label,
        fontsize=9.0,
        color=color,
        ha="left",
        va="center",
        bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor="none", alpha=0.90),
    )


def figure_3(preview_dir: Path | None) -> None:
    """Contrast the concave logarithm with the convex floored payoff."""

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.9))
    fig.subplots_adjust(left=0.075, right=0.97, bottom=0.17, top=0.80, wspace=0.25)
    _figure_heading(
        fig,
        "The curvature switch",
        r"The boundary condition changes the sign of the volatility term.",
    )

    x = np.linspace(0.035, 4.0, 800)
    k = 1.5

    left, right = axes
    _style_axis(left)
    _style_axis(right)

    left.plot(x, np.log(x), color=RED, linewidth=2.4, zorder=3)
    left.axvline(0, color=RED, linewidth=4.0, zorder=2)
    left.set_xlim(-0.18, 4.05)
    left.set_ylim(-3.6, 1.6)
    left.set_xlabel("Underlying wealth, $X$")
    left.set_ylabel("Transformed payoff, $\\varphi(X)$")
    left.set_title(
        "(A) Absorbing boundary",
        loc="left",
        fontweight="bold",
        color=INK,
        pad=10,
    )
    left.text(
        0.05,
        0.92,
        r"$\varphi(X)=\ln(X)$",
        transform=left.transAxes,
        fontsize=12.0,
        color=RED,
        ha="left",
        va="top",
    )
    left.text(
        0.05,
        0.84,
        r"$\varphi''(X)<0$",
        transform=left.transAxes,
        fontsize=10.2,
        color=MUTED,
        ha="left",
        va="top",
    )
    left.annotate(
        "absorbing barrier\n$L=0$",
        xy=(0.045, -3.45),
        xytext=(0.50, -2.95),
        fontsize=9.2,
        color=RED,
        arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.0),
        ha="left",
        va="center",
        bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor="none", alpha=0.90),
    )
    _jensen_geometry(
        left,
        0.5,
        2.5,
        np.log,
        color=RED,
        arrow_label="volatility drag\nnegative Jensen gap",
        label_offset=(0.18, -0.08),
    )

    floor_curve = lambda value: np.maximum(value, k)
    right.plot(x, floor_curve(x), color=BLUE, linewidth=2.4, zorder=3)
    right.plot([-0.18, k], [k, k], color=BLUE, linewidth=4.0, zorder=2)
    right.set_xlim(-0.18, 4.05)
    right.set_ylim(0.85, 4.15)
    right.set_xlabel("Underlying wealth, $X$")
    right.set_title(
        "(B) Real floor",
        loc="left",
        fontweight="bold",
        color=INK,
        pad=10,
    )
    right.text(
        0.05,
        0.92,
        r"$\varphi(X)=\max(X,K)$",
        transform=right.transAxes,
        fontsize=12.0,
        color=BLUE,
        ha="left",
        va="top",
    )
    right.text(
        0.05,
        0.84,
        r"$\varphi''=\delta_K\geq0$",
        transform=right.transAxes,
        fontsize=10.2,
        color=MUTED,
        ha="left",
        va="top",
    )
    right.scatter([k], [k], s=36, color=BLUE, edgecolors="white", linewidths=0.9, zorder=6)
    right.annotate(
        "kink at $K$\n" + r"local-time term",
        xy=(k, k),
        xytext=(2.10, 1.12),
        fontsize=9.2,
        color=BLUE,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=1.0),
        bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor="none", alpha=0.90),
    )
    right.text(
        0.10,
        k + 0.12,
        "reflecting floor",
        fontsize=9.4,
        color=BLUE,
        ha="left",
        va="bottom",
        bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor="none", alpha=0.90),
    )
    _jensen_geometry(
        right,
        0.6,
        2.6,
        floor_curve,
        color=BLUE,
        arrow_label="convexity premium\npositive Jensen gap",
        label_offset=(0.18, 0.15),
    )

    left_box = left.get_position()
    right_box = right.get_position()
    regime_y = 0.07
    fig.text(
        (left_box.x0 + left_box.x1) / 2,
        regime_y,
        "Regime A: absorbing downside | minimize volatility",
        ha="center",
        va="center",
        fontsize=9.0,
        color=RED,
        bbox=dict(boxstyle="square,pad=0.28", facecolor=RED_LIGHT, edgecolor="none"),
    )
    fig.text(
        (right_box.x0 + right_box.x1) / 2,
        regime_y,
        "Regime B: real floor | seek bounded volatility",
        ha="center",
        va="center",
        fontsize=9.0,
        color=BLUE,
        bbox=dict(boxstyle="square,pad=0.28", facecolor=BLUE_LIGHT, edgecolor="none"),
    )

    _save(fig, "figure-3-the-curvature-switch", preview_dir)


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
