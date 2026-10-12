import numpy as np
import pandas as pd

from src.config import MAX_LAG_DAYS


LAG_DAYS = [1, 2, 3, 7, 14, 28]
ROLLING_WINDOWS = [7, 14, 28]


def build_supervised_table(daily: pd.DataFrame) -> pd.DataFrame:
    """Build target-date rows with features known by the previous day."""
    df = daily.sort_values(["oblast", "date_kyiv"]).copy()
    df = df.rename(
        columns={
            "date_kyiv": "target_date",
            "alert_count": "y_alert_count",
            "has_alert": "y_has_alert",
        }
    )
    df["forecast_date"] = df["target_date"] - pd.Timedelta(days=1)

    grouped_counts = df.groupby("oblast")["y_alert_count"]

    for lag in LAG_DAYS:
        df[f"count_lag_{lag}"] = grouped_counts.shift(lag)

    df["target_day_of_week"] = df["target_date"].dt.dayofweek
    df["target_month"] = df["target_date"].dt.month
    df["target_day_of_year"] = df["target_date"].dt.dayofyear
    df["target_is_weekend"] = df["target_day_of_week"].isin([5, 6]).astype(int)
    df["days_since_start"] = (df["target_date"] - df["target_date"].min()).dt.days

    return df.reset_index(drop=True)
