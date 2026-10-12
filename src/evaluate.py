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
