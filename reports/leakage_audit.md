# Leakage Audit

## Forecast Moment

The forecast is made at the end of Kyiv-local day `D`. At that moment, the
pipeline predicts the number of alert starts for each oblast on Kyiv-local day
`D + 1`.

## Target Date vs Forecast Date

Each supervised row has:

- `target_date`: the day being predicted
- `forecast_date`: `target_date - 1 day`

Features for a row may use information only from dates `<= forecast_date`.

## Shifted Lag Features

Lag features such as `count_lag_1`, `count_lag_7`, and `count_lag_28` are built
with group-wise shifts by oblast. For target date `T`, these features refer to
dates before `T`, never to `T` itself.

## Shifted Rolling Features

Rolling features are computed after shifting daily counts by one day. This means
`rolling_7_mean` for target date `T` summarizes `T-7` through `T-1`, not `T`
through future dates.

## Chronological Split

Rows are split by `target_date`:

- latest 90 complete days: test
- previous 45 days: validation
- all earlier supervised rows: train

No random split is used.

## Intentionally Excluded Features

The first version excludes:

- alert counts from the target date
- same-day national totals for the target date
- centered or future rolling windows
- alert duration and `finished_at`
- post-forecast news, media, Telegram, or attack reports
- random train/test splitting

## Remaining Limitations

The model uses only historical alert-start patterns, so it cannot know future
military, political, weather, or infrastructure events. It should be interpreted
as a time-series benchmark, not as a real-time safety system.
