import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.config import RANDOM_STATE


CATEGORICAL_FEATURES = ["oblast"]
NUMERIC_FEATURES = [
    "count_lag_1",
    "count_lag_2",
    "count_lag_3",
    "count_lag_7",
    "count_lag_14",
    "count_lag_28",
    "rolling_7_mean",
    "rolling_14_mean",
    "rolling_28_mean",
    "rolling_7_max",
    "rolling_28_std",
    "national_count_lag_1",
    "national_rolling_7_mean",
    "target_day_of_week",
    "target_month",
    "target_day_of_year",
    "target_is_weekend",
    "days_since_start",
]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def make_model_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("oblast", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ],
        sparse_threshold=0.0,
    )

    model = HistGradientBoostingRegressor(
        loss="poisson",
        learning_rate=0.05,
        max_iter=300,
        random_state=RANDOM_STATE,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


def train_model(train_df: pd.DataFrame) -> tuple[Pipeline, list[str]]:
    """Train the sklearn model on the rows supplied by the caller."""
    pipeline = make_model_pipeline()
    pipeline.fit(train_df[FEATURE_COLUMNS], train_df["y_alert_count"])
    return pipeline, FEATURE_COLUMNS
