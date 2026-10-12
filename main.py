import argparse
from pathlib import Path

import pandas as pd

from src.baselines import evaluate_baselines
from src.config import (
    DATA_QUALITY_REPORT_PATH,
    PLOTS_DIR,
    PROCESSED_DAILY_PATH,
    RAW_CSV_PATH,
    SOURCE_METADATA_PATH,
    TEST_PREDICTIONS_PATH,
    TEST_METRICS_PATH,
    VALIDATION_METRICS_PATH,
)
from src.data_quality import write_data_quality_report
from src.download import get_raw_csv
from src.evaluate import evaluate_predictions, save_metrics, save_test_predictions
from src.features import build_supervised_table
from src.model import train_model
from src.preprocess import build_daily_oblast_table, load_raw_alerts
from src.split import split_by_target_date


def parse_args():
    parser = argparse.ArgumentParser(
        description="Daily oblast-level next-day air alert count forecasting."
    )
    parser.add_argument(
        "--raw-path",
        type=Path,
        default=None,
        help="Optional local volunteer_data_en.csv path. If omitted, the file is downloaded.",
    )
    parser.add_argument(
        "--as-of-date",
        type=str,
        default=None,
        help=(
            "Optional Kyiv-local current date in YYYY-MM-DD format. "
            "The pipeline excludes this date as potentially incomplete."
        ),
    )
    parser.add_argument(
        "--skip-plots",
        action="store_true",
        help="Skip matplotlib plot generation. Metrics and predictions are still saved.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    raw_path = get_raw_csv(
        local_path=args.raw_path,
        destination=RAW_CSV_PATH,
        metadata_path=SOURCE_METADATA_PATH,
    )
    raw_alerts = load_raw_alerts(raw_path)

    daily = build_daily_oblast_table(raw_alerts, as_of_date=args.as_of_date)
    PROCESSED_DAILY_PATH.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(PROCESSED_DAILY_PATH, index=False)
    write_data_quality_report(raw_path, daily, DATA_QUALITY_REPORT_PATH)

    supervised = build_supervised_table(daily)
    train_df, val_df, test_df = split_by_target_date(supervised)

    validation_baseline_metrics, _ = evaluate_baselines(val_df)
    for metric in validation_baseline_metrics:
        metric["split"] = "validation"

    validation_model, feature_columns = train_model(train_df)
    validation_model_pred = validation_model.predict(val_df[feature_columns]).clip(min=0)
    validation_model_metrics = evaluate_predictions(
        y_true=val_df["y_alert_count"],
        y_pred=validation_model_pred,
        model_name="hist_gradient_boosting_poisson",
        split="validation",
    )
    save_metrics(
        validation_baseline_metrics + [validation_model_metrics],
        VALIDATION_METRICS_PATH,
    )

    baseline_metrics, baseline_test_predictions = evaluate_baselines(test_df)
    for metric in baseline_metrics:
        metric["split"] = "test"

    final_train_df = pd.concat([train_df, val_df], ignore_index=True)
    model, feature_columns = train_model(final_train_df)
    model_test_pred = model.predict(test_df[feature_columns]).clip(min=0)
    model_metrics = evaluate_predictions(
        y_true=test_df["y_alert_count"],
        y_pred=model_test_pred,
        model_name="hist_gradient_boosting_poisson",
        split="test",
    )

    metrics = baseline_metrics + [model_metrics]
    save_metrics(metrics, TEST_METRICS_PATH)

    save_test_predictions(
        test_df=test_df,
        baseline_predictions=baseline_test_predictions,
        model_predictions=model_test_pred,
        output_path=TEST_PREDICTIONS_PATH,
    )


if __name__ == "__main__":
    main()
