# Model Card

## Model Objective

Predict the next-day number of air-raid alert starts for each Ukrainian oblast.
The forecast is made at the end of Kyiv-local day `D` for target day `D + 1`.

## Input Features

The model uses:

- oblast identity
- calendar features for the target date
- oblast-level historical alert count lags
- oblast-level shifted rolling statistics
- national historical alert count lags and shifted rolling statistics

All historical features are computed using dates before the target date.

## Baselines

The project compares the model against:

- yesterday count
- 7-day lag
- rolling 7-day mean

These baselines are deliberately simple and leakage-safe.

## Model

The main model is sklearn `HistGradientBoostingRegressor(loss="poisson")`.
Poisson loss is used because the target is a non-negative count.

## Validation and Test Split

Rows are split chronologically by `target_date`:

- validation: 45 days immediately before the test period
- test: latest 90 complete days
- train: all earlier supervised rows after feature warmup

Validation metrics are used for model checking. Test metrics are reserved for
final reporting.

## Metrics

The project reports:

- MAE
- RMSE

MAE is the main metric because it is easy to interpret as the average absolute
count error per oblast-day.

## Intended Use

This model is intended for educational time-series forecasting, leakage-safe
evaluation practice, and comparison of simple historical baselines with a
tabular machine-learning model.

## Non-Intended Use

This is not an operational air-raid warning system. It must not be used to make
safety decisions, ignore official alerts, or infer whether a specific place is
safe.

## Limitations

The model uses historical alert-start data only. It does not use intelligence,
military activity, official warnings, news, weather, or real-time event streams.
The future can change abruptly, so recent performance may not generalize to
future periods.
