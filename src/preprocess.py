from pathlib import Path

import pandas as pd

from src.config import KYIV_TZ


REQUIRED_COLUMNS = {"region", "started_at", "finished_at", "naive"}


def load_raw_alerts(path: Path) -> pd.DataFrame:
    """Load volunteer alert data and keep only the columns needed for this project."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Raw CSV is missing required columns: {sorted(missing)}")

    df = df[list(REQUIRED_COLUMNS)].copy()
    df = df.rename(columns={"region": "oblast"})
    df["oblast"] = df["oblast"].astype(str).str.strip()

    df["started_at_utc"] = pd.to_datetime(df["started_at"], utc=True, errors="coerce")
    df = df.dropna(subset=["oblast", "started_at_utc"])

    # Timezone-aware conversion is essential. Manual +2/+3 hour offsets would be
    # wrong around daylight-saving transitions and can move alerts to wrong dates.
    started_at_kyiv = df["started_at_utc"].dt.tz_convert(KYIV_TZ)
    df["date_kyiv"] = started_at_kyiv.dt.tz_localize(None).dt.normalize()

    return df


def parse_as_of_date(as_of_date: str | None) -> pd.Timestamp:
    """Return the Kyiv-local current date used to decide complete data coverage."""
    if as_of_date is None:
        return pd.Timestamp.now(tz=KYIV_TZ).tz_localize(None).normalize()

    parsed = pd.Timestamp(as_of_date)
    if parsed.tzinfo is not None:
        parsed = parsed.tz_convert(KYIV_TZ).tz_localize(None)
    return parsed.normalize()


def build_daily_oblast_table(
    raw_alerts: pd.DataFrame, as_of_date: str | None = None
) -> pd.DataFrame:
    """Create one row per oblast-date and fill missing combinations with zero alerts."""
    if raw_alerts.empty:
        raise ValueError("No raw alerts available after loading and timestamp parsing.")

    current_kyiv_day = parse_as_of_date(as_of_date)
    max_raw_date = raw_alerts["date_kyiv"].max()
    max_complete_date = min(max_raw_date, current_kyiv_day - pd.Timedelta(days=1))
    min_date = raw_alerts["date_kyiv"].min()

    if max_complete_date < min_date:
        raise ValueError("No complete Kyiv-local dates available for modeling.")

    usable = raw_alerts.loc[raw_alerts["date_kyiv"].between(min_date, max_complete_date)]

    counts = (
        usable.groupby(["oblast", "date_kyiv"])
        .size()
        .rename("alert_count")
        .reset_index()
    )

    oblasts = sorted(usable["oblast"].dropna().unique())
    dates = pd.date_range(min_date, max_complete_date, freq="D")
    full_index = pd.MultiIndex.from_product(
        [oblasts, dates], names=["oblast", "date_kyiv"]
    )

    daily = (
        counts.set_index(["oblast", "date_kyiv"])
        .reindex(full_index)
        .fillna({"alert_count": 0})
        .reset_index()
    )
    daily["alert_count"] = daily["alert_count"].astype(int)
    daily["has_alert"] = daily["alert_count"] > 0
    daily["is_observed_date"] = True

    return daily.sort_values(["oblast", "date_kyiv"]).reset_index(drop=True)
