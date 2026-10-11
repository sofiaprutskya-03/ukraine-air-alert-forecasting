import pandas as pd

from src.config import TEST_DAYS, VALIDATION_DAYS


def split_by_target_date(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Chronological split by target_date.

    No random split is allowed for this forecasting task because random rows
    would train on future dates and leak future distribution information.
    """
    max_date = df["target_date"].max()
    test_start = max_date - pd.Timedelta(days=TEST_DAYS - 1)
    val_end = test_start - pd.Timedelta(days=1)
    val_start = val_end - pd.Timedelta(days=VALIDATION_DAYS - 1)

    train = df[df["target_date"] < val_start].copy()
    validation = df[df["target_date"].between(val_start, val_end)].copy()
    test = df[df["target_date"] >= test_start].copy()

    if train.empty or validation.empty or test.empty:
        raise ValueError(
            "Not enough dates for train/validation/test split. "
            "Need at least warmup + 45 validation days + 90 test days."
        )

    print(f"Train: {train['target_date'].min().date()} to {train['target_date'].max().date()}")
    print(
        "Validation: "
        f"{validation['target_date'].min().date()} to {validation['target_date'].max().date()}"
    )
    print(f"Test: {test['target_date'].min().date()} to {test['target_date'].max().date()}")

    return train, validation, test
