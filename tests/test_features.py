import unittest

import pandas as pd

from src.features import build_supervised_table


def make_daily_table(overrides=None):
    overrides = overrides or {}
    rows = []
    dates = pd.date_range("2024-01-01", periods=40, freq="D")
    for day_index, date in enumerate(dates):
        for oblast, base in [("Alpha", 0), ("Beta", 100)]:
            count = base + day_index
            count = overrides.get((oblast, date), count)
            rows.append(
                {
                    "oblast": oblast,
                    "date_kyiv": date,
                    "alert_count": count,
                    "has_alert": count > 0,
                    "is_observed_date": True,
                }
            )
    return pd.DataFrame(rows)


class FeatureLeakageTests(unittest.TestCase):
    def test_lag_rolling_and_national_features_use_past_dates_only(self):
        supervised = build_supervised_table(make_daily_table())
        target_date = pd.Timestamp("2024-01-29")
        row = supervised[
            (supervised["oblast"] == "Alpha")
            & (supervised["target_date"] == target_date)
        ].iloc[0]

        self.assertEqual(row["count_lag_1"], 27)
        self.assertEqual(row["count_lag_7"], 21)
        self.assertEqual(row["rolling_7_mean"], 24)
        self.assertEqual(row["national_count_lag_1"], 154)
