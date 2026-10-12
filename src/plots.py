import os
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MPLCONFIGDIR = PROJECT_ROOT / ".matplotlib-cache"


MODEL_COLUMN = "hist_gradient_boosting_poisson"


def _get_pyplot():
    """Import matplotlib only when plots are requested."""
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
