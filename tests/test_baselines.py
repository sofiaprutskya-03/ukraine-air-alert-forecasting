import unittest

import pandas as pd

from src.baselines import evaluate_baselines


class BaselineTests(unittest.TestCase):
    def test_baseline_predictions_match_expected_feature_columns(self):
        df = pd.DataFrame(
            {
                "y_alert_count": [3, 4, 5],
                "count_lag_1": [1, 2, 3],
                "count_lag_7": [7, 8, 9],
                "rolling_7_mean": [2.5, 3.5, 4.5],
            }
        )

        _, predictions = evaluate_baselines(df)

        pd.testing.assert_series_equal(
            predictions["baseline_yesterday"],
            df["count_lag_1"],
            check_names=False,
        )
        pd.testing.assert_series_equal(
            predictions["baseline_lag_7"],
            df["count_lag_7"],
            check_names=False,
        )
        pd.testing.assert_series_equal(
            predictions["baseline_rolling_7_mean"],
            df["rolling_7_mean"],
            check_names=False,
        )
