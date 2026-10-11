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
