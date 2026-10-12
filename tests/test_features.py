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

    def test_same_target_date_value_does_not_change_same_row_features(self):
        target_date = pd.Timestamp("2024-01-29")
        base = build_supervised_table(make_daily_table())
        mutated = build_supervised_table(
            make_daily_table(overrides={("Alpha", target_date): 999})
        )

        base_row = base[
            (base["oblast"] == "Alpha") & (base["target_date"] == target_date)
        ].iloc[0]
        mutated_row = mutated[
            (mutated["oblast"] == "Alpha") & (mutated["target_date"] == target_date)
        ].iloc[0]

        self.assertEqual(mutated_row["y_alert_count"], 999)
        feature_columns = [
            column
            for column in base.columns
            if column.startswith("count_lag_")
            or column.startswith("rolling_")
            or column.startswith("national_")
        ]
        for column in feature_columns:
            self.assertEqual(base_row[column], mutated_row[column], column)
