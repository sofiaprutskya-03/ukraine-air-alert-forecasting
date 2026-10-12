from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate_predictions(y_true, y_pred, model_name: str, split: str | None = None) -> dict:
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    metrics = {
        "model": model_name,
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": rmse,
        "n_rows": len(y_true),
    }
    if split is not None:
        metrics = {"split": split, **metrics}
    return metrics


def save_metrics(metrics: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df = pd.DataFrame(metrics).sort_values("mae")
    metrics_df.to_csv(output_path, index=False)
    print(metrics_df.to_string(index=False))


def save_test_predictions(
    test_df: pd.DataFrame,
    baseline_predictions: dict[str, pd.Series],
    model_predictions,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = test_df[
        [
            "oblast",
            "target_date",
            "forecast_date",
            "y_alert_count",
            "count_lag_1",
            "count_lag_7",
            "rolling_7_mean",
        ]
    ].copy()

    for name, values in baseline_predictions.items():
        output[name] = values.to_numpy()
    output["hist_gradient_boosting_poisson"] = model_predictions

    output.to_csv(output_path, index=False)
