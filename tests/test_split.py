import unittest

import pandas as pd

from src.split import split_by_target_date


class SplitTests(unittest.TestCase):
    def test_split_is_chronological(self):
        df = pd.DataFrame(
            {
                "target_date": pd.date_range("2024-01-01", periods=200, freq="D"),
                "y_alert_count": range(200),
            }
        )

        train, validation, test = split_by_target_date(df)

        self.assertLess(train["target_date"].max(), validation["target_date"].min())
        self.assertLess(validation["target_date"].max(), test["target_date"].min())
        self.assertEqual(validation["target_date"].nunique(), 45)
        self.assertEqual(test["target_date"].nunique(), 90)
