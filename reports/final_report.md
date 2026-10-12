# Daily Oblast-Level Air Alert Count Forecasting

## Summary

This project forecasts next-day air-raid alert start counts for each Ukrainian
oblast using only historical alert data. The goal is not to build an operational
warning system, but to demonstrate a leakage-safe time-series forecasting
workflow with clear baselines and reproducible evaluation.

Final one-sentence result placeholder:

> After running the final pipeline, fill in which model performed best on the
> latest 90-day test period and by how much.

## Forecast Definition

The forecast is made at the end of Kyiv-local day `D`. For each oblast, the
target is the number of alert starts on Kyiv-local day `D + 1`.

In the supervised data:

- `target_date` is the day being predicted
- `forecast_date` is `target_date - 1 day`
- features may use only dates `<= forecast_date`

## Data and Preprocessing

The project uses `volunteer_data_en.csv` from
`Vadimkin/ukrainian-air-raid-sirens-dataset`.

Raw `started_at` timestamps are parsed as UTC and converted to `Europe/Kyiv`
using timezone-aware pandas conversion. The current Kyiv-local day is excluded
because it may be incomplete. For the final submission run, the pipeline should
be executed with an explicit `--as-of-date`.

Source metadata is saved in:

```text
data/source_metadata.json
```

Data quality details are saved in:

```text
reports/data_quality.md
```

Final run placeholders:

- as-of date: `TODO`
- raw source type: `TODO`
- modeled date range: `TODO`
- number of oblasts: `TODO`
- number of oblast-date rows: `TODO`

## Features

The model uses oblast identity, calendar features, lagged alert counts, shifted
rolling alert-count statistics, and shifted national historical alert features.

The first version intentionally excludes `finished_at`, alert durations, news,
media, Telegram, and same-day target information to keep the forecast timing
auditable.

## Evaluation Design

Rows are split chronologically by `target_date`:

- train: all earlier rows after feature warmup
- validation: 45 days before the test period
- test: latest 90 complete days

Validation metrics are used for model checking. Final test metrics are reserved
for final reporting.

Metrics:

- MAE
- RMSE

## Baselines and Model

Baselines:

- yesterday count
- 7-day lag
- rolling 7-day mean

Main model:

- sklearn `HistGradientBoostingRegressor(loss="poisson")`

## Validation Results

Fill this section from:

```text
reports/validation_metrics.csv
```

Placeholder table:

| model | MAE | RMSE | note |
|---|---:|---:|---|
| baseline_yesterday | TODO | TODO | TODO |
| baseline_lag_7 | TODO | TODO | TODO |
| baseline_rolling_7_mean | TODO | TODO | TODO |
| hist_gradient_boosting_poisson | TODO | TODO | TODO |

Interpretation placeholder:

> TODO: Explain whether the sklearn model improves on simple baselines on
> validation. If it does not, say that directly and use the result as evidence
> that the baseline is strong.

## Final Test Results

Fill this section from:

```text
reports/test_metrics.csv
```

Placeholder table:

| model | MAE | RMSE | note |
|---|---:|---:|---|
| baseline_yesterday | TODO | TODO | TODO |
| baseline_lag_7 | TODO | TODO | TODO |
| baseline_rolling_7_mean | TODO | TODO | TODO |
| hist_gradient_boosting_poisson | TODO | TODO | TODO |

Interpretation placeholder:

> TODO: Report final test performance on the latest 90 complete days. Do not
> change the model after seeing these results unless the test set is reset and
> the decision is clearly documented.

## Figures To Discuss

