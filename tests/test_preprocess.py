import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.preprocess import build_daily_oblast_table, load_raw_alerts


class PreprocessTests(unittest.TestCase):
    def _write_csv(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "alerts.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_utc_timestamp_converts_to_kyiv_date(self):
        path = self._write_csv(
            "region,started_at,finished_at,naive\n"
            "Kyiv,2024-06-01T21:30:00Z,,false\n"
        )

        df = load_raw_alerts(path)

        self.assertEqual(df.loc[0, "date_kyiv"], pd.Timestamp("2024-06-02"))

    def test_missing_oblast_dates_are_filled_with_zero_and_current_day_excluded(self):
        path = self._write_csv(
            "region,started_at,finished_at,naive\n"
            "Alpha,2024-06-01T09:00:00Z,,false\n"
            "Alpha,2024-06-03T09:00:00Z,,false\n"
            "Beta,2024-06-02T09:00:00Z,,false\n"
            "Beta,2024-06-04T09:00:00Z,,false\n"
        )
        raw = load_raw_alerts(path)

        daily = build_daily_oblast_table(raw, as_of_date="2024-06-04")

        self.assertEqual(daily["date_kyiv"].max(), pd.Timestamp("2024-06-03"))
        alpha_june_2 = daily[
            (daily["oblast"] == "Alpha")
            & (daily["date_kyiv"] == pd.Timestamp("2024-06-02"))
        ].iloc[0]
        beta_june_1 = daily[
            (daily["oblast"] == "Beta")
            & (daily["date_kyiv"] == pd.Timestamp("2024-06-01"))
        ].iloc[0]

        self.assertEqual(alpha_june_2["alert_count"], 0)
        self.assertEqual(beta_june_1["alert_count"], 0)

    def test_missing_required_columns_raise_clear_error(self):
        path = self._write_csv(
            "region,started_at,finished_at\n"
            "Kyiv,2024-06-01T09:00:00Z,\n"
        )

        with self.assertRaisesRegex(ValueError, "missing required columns.*naive"):
            load_raw_alerts(path)
