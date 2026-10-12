import numpy as np
import pandas as pd

from src.config import MAX_LAG_DAYS


LAG_DAYS = [1, 2, 3, 7, 14, 28]
ROLLING_WINDOWS = [7, 14, 28]


# Group-wise rolling aggregates computed safely over shifted time-series
def _safe_grouped_rolling_mean(
    shifted_counts: pd.Series, oblasts: pd.Series, window: int
) -> pd.Series:
    return (
        shifted_counts.groupby(oblasts)
        .rolling(window=window, min_periods=window)
        .mean()
        .reset_index(level=0, drop=True)
    )


def _safe_grouped_rolling_max(
    shifted_counts: pd.Series, oblasts: pd.Series, window: int
) -> pd.Series:
    return (
        shifted_counts.groupby(oblasts)
        .rolling(window=window, min_periods=window)
        .max()
        .reset_index(level=0, drop=True)
    )


def _safe_grouped_rolling_std(
    shifted_counts: pd.Series, oblasts: pd.Series, window: int
) -> pd.Series:
    return (
        shifted_counts.groupby(oblasts)
        .rolling(window=window, min_periods=window)
        .std()
        .reset_index(level=0, drop=True)
    )


def build_supervised_table(daily: pd.DataFrame) -> pd.DataFrame:
    """Build target-date rows with features known by the previous day.

    Leakage warning: the current row's alert_count is the target for target_date.
    Every lag or rolling feature below is shifted first, so it only uses dates
    <= target_date - 1.
    """
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
    shifted_counts = grouped_counts.shift(1)

    for lag in LAG_DAYS:
        df[f"count_lag_{lag}"] = grouped_counts.shift(lag)

    for window in ROLLING_WINDOWS:
        df[f"rolling_{window}_mean"] = _safe_grouped_rolling_mean(
            shifted_counts, df["oblast"], window
        )

    df["rolling_7_max"] = _safe_grouped_rolling_max(shifted_counts, df["oblast"], 7)
    df["rolling_28_std"] = _safe_grouped_rolling_std(shifted_counts, df["oblast"], 28)

    national = (
        daily.groupby("date_kyiv", as_index=False)["alert_count"]
        .sum()
        .rename(columns={"date_kyiv": "target_date", "alert_count": "national_count"})
        .sort_values("target_date")
    )
    national["national_count_lag_1"] = national["national_count"].shift(1)
    national["national_rolling_7_mean"] = (
        national["national_count"].shift(1).rolling(window=7, min_periods=7).mean()
    )
    df = df.merge(
        national[["target_date", "national_count_lag_1", "national_rolling_7_mean"]],
        on="target_date",
        how="left",
    )

    df["target_day_of_week"] = df["target_date"].dt.dayofweek
    df["target_month"] = df["target_date"].dt.month
    df["target_day_of_year"] = df["target_date"].dt.dayofyear
    df["target_is_weekend"] = df["target_day_of_week"].isin([5, 6]).astype(int)
    df["days_since_start"] = (df["target_date"] - df["target_date"].min()).dt.days

    feature_start = df["target_date"].min() + pd.Timedelta(days=MAX_LAG_DAYS)
    df = df.loc[df["target_date"] >= feature_start].copy()

    numeric_columns = [
        column
        for column in df.columns
        if column.startswith("count_lag_")
        or column.startswith("rolling_")
        or column.startswith("national_")
    ]
    df[numeric_columns] = df[numeric_columns].replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=numeric_columns)

    return df.reset_index(drop=True)
