import pandas as pd

from src.evaluate import evaluate_predictions


BASELINE_COLUMNS = {
    "baseline_yesterday": "count_lag_1",
    "baseline_lag_7": "count_lag_7",
    "baseline_rolling_7_mean": "rolling_7_mean",
}


def evaluate_baselines(df: pd.DataFrame) -> tuple[list[dict], dict[str, pd.Series]]:
    metrics = []
    predictions = {}

    for model_name, feature_column in BASELINE_COLUMNS.items():
        y_pred = df[feature_column].clip(lower=0)
        predictions[model_name] = y_pred
        metrics.append(
            evaluate_predictions(
                y_true=df["y_alert_count"],
                y_pred=y_pred,
                model_name=model_name,
            )
        )

    return metrics, predictions
