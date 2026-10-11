from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PREDICTIONS_DIR = DATA_DIR / "predictions"
SOURCE_METADATA_PATH = DATA_DIR / "source_metadata.json"

REPORTS_DIR = PROJECT_ROOT / "reports"
PLOTS_DIR = REPORTS_DIR / "figures"
DATA_QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality.md"

RAW_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "Vadimkin/ukrainian-air-raid-sirens-dataset/"
    "main/datasets/volunteer_data_en.csv"
)

RAW_CSV_PATH = RAW_DIR / "volunteer_data_en.csv"
PROCESSED_DAILY_PATH = PROCESSED_DIR / "daily_oblast_alert_counts.csv"
VALIDATION_METRICS_PATH = REPORTS_DIR / "validation_metrics.csv"
TEST_METRICS_PATH = REPORTS_DIR / "test_metrics.csv"
TEST_PREDICTIONS_PATH = PREDICTIONS_DIR / "test_predictions.csv"

KYIV_TZ = "Europe/Kyiv"
VALIDATION_DAYS = 45
TEST_DAYS = 90
MAX_LAG_DAYS = 28

RANDOM_STATE = 42
