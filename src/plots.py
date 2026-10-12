import os
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MPLCONFIGDIR = PROJECT_ROOT / ".matplotlib-cache"


MODEL_COLUMN = "hist_gradient_boosting_poisson"


def _get_pyplot():
    """Import matplotlib only when plots are requested.

    Matplotlib can scan system fonts during import on macOS. Keeping the import
    lazy prevents plotting dependency issues from blocking metrics generation.
    """
    os.environ.setdefault("MPLCONFIGDIR", str(DEFAULT_MPLCONFIGDIR))
    DEFAULT_MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def plot_predictions_over_time(predictions_path: Path, output_path: Path) -> None:
    plt = _get_pyplot()
    df = pd.read_csv(predictions_path, parse_dates=["target_date"])
    daily = (
        df.groupby("target_date", as_index=False)[["y_alert_count", MODEL_COLUMN]]
        .sum()
        .sort_values("target_date")
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(daily["target_date"], daily["y_alert_count"], label="Actual", linewidth=2)
    ax.plot(daily["target_date"], daily[MODEL_COLUMN], label="Model prediction", linewidth=2)
    ax.set_title("Total daily alert starts across oblasts: actual vs predicted")
    ax.set_xlabel("Target date")
    ax.set_ylabel("Alert starts")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_mae_by_oblast(predictions_path: Path, output_path: Path) -> None:
    plt = _get_pyplot()
    df = pd.read_csv(predictions_path)
    df["abs_error"] = (df["y_alert_count"] - df[MODEL_COLUMN]).abs()
    by_oblast = df.groupby("oblast", as_index=False)["abs_error"].mean()
    by_oblast = by_oblast.sort_values("abs_error", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(by_oblast["oblast"], by_oblast["abs_error"])
    ax.set_title("Model MAE by oblast on test period")
    ax.set_xlabel("Mean absolute error")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_recent_oblast_heatmap(predictions_path: Path, output_path: Path) -> None:
    plt = _get_pyplot()
    df = pd.read_csv(predictions_path, parse_dates=["target_date"])
    heatmap_data = (
        df.pivot_table(
            index="oblast",
            columns="target_date",
            values="y_alert_count",
            aggfunc="sum",
            fill_value=0,
        )
        .sort_index()
    )

    fig_width = max(12, heatmap_data.shape[1] * 0.12)
    fig_height = max(7, heatmap_data.shape[0] * 0.28)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    image = ax.imshow(heatmap_data.values, aspect="auto", cmap="YlOrRd")

    tick_count = min(10, heatmap_data.shape[1])
    tick_positions = np.linspace(0, heatmap_data.shape[1] - 1, tick_count, dtype=int)
    tick_labels = [
        pd.Timestamp(heatmap_data.columns[position]).strftime("%Y-%m-%d")
        for position in tick_positions
    ]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    ax.set_title("Actual alert starts by oblast and target date on test period")
    ax.set_xlabel("Target date")
    ax.set_ylabel("Oblast")

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Alert starts")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_model_error_over_time(predictions_path: Path, output_path: Path) -> None:
    plt = _get_pyplot()
    df = pd.read_csv(predictions_path, parse_dates=["target_date"])
    daily = (
        df.groupby("target_date", as_index=False)[["y_alert_count", MODEL_COLUMN]]
        .sum()
        .sort_values("target_date")
    )
    daily["national_abs_error"] = (
        daily["y_alert_count"] - daily[MODEL_COLUMN]
    ).abs()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        daily["target_date"],
        daily["national_abs_error"],
        label="National total absolute error",
        linewidth=2,
        color="#8b1e3f",
    )
    ax.set_title("Model absolute error over time for national daily total")
    ax.set_xlabel("Target date")
    ax.set_ylabel("Absolute error")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
