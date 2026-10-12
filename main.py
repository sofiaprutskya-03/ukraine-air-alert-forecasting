import argparse
from pathlib import Path

import pandas as pd

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
from src.download import get_raw_csv
from src.preprocess import build_daily_oblast_table, load_raw_alerts


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
