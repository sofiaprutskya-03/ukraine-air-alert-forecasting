# Ukraine Air Alert Next-Day Forecasting

Leakage-safe Python project for forecasting next-day air-raid alert starts by
Ukrainian oblast using only historical alert data.

## Why This Scope

The task is intentionally scoped to daily oblast-level alert counts. This keeps
the project realistic under a short deadline while still demonstrating the
important engineering choices: reproducible data snapshots, timezone-aware
preprocessing, chronological evaluation, simple baselines, and explicit leakage
control.

The first version does not use news, media, Telegram, or other text signals.
Those signals can be useful, but they are easy to misuse unless publication time
and forecast time are handled very carefully.

## Exact Forecast Definition

Forecast moment: the end of Kyiv-local day `D`.

Target: for each oblast, predict the number of alert starts on Kyiv-local day
`D + 1`.

In the modeling table:

- `target_date` is the day being predicted
- `forecast_date = target_date - 1 day`
- features for `target_date` may use only dates `<= forecast_date`

## Leakage-Safe Design

The pipeline avoids leakage by:

- converting UTC timestamps to `Europe/Kyiv` with timezone-aware pandas logic
- excluding the current Kyiv-local day because it may be incomplete
- filling missing oblast-date combinations with zero alert starts
- shifting lag features before they are used
- shifting counts before rolling features are calculated
- splitting train, validation, and test chronologically by `target_date`
- saving validation metrics separately from final test metrics

See `reports/leakage_audit.md` for the checklist.

## Repository Structure

```text
.
├── main.py
├── requirements.txt
├── src/
│   ├── config.py
│   ├── download.py
│   ├── preprocess.py
│   ├── features.py
│   ├── split.py
│   ├── baselines.py
│   ├── model.py
│   ├── evaluate.py
│   └── plots.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── predictions/
│   └── source_metadata.json
└── reports/
    ├── final_report.md
    ├── data_quality.md
    ├── leakage_audit.md
    ├── model_card.md
    ├── validation_metrics.csv
    ├── test_metrics.csv
    └── figures/
```

## Quickstart

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m unittest discover tests
```

Run with download:

```bash
MPLCONFIGDIR=.matplotlib-cache python main.py --as-of-date 2026-10-12
```

Run without plots in restricted environments:

```bash
python main.py --as-of-date 2026-10-12 --skip-plots
```

Run from a local CSV:

```bash
MPLCONFIGDIR=.matplotlib-cache python main.py --raw-path data/raw/volunteer_data_en.csv --as-of-date 2026-10-12
```

For submission, pass `--as-of-date` explicitly. If it is omitted, the pipeline
uses today's date in `Europe/Kyiv`, which is convenient but less reproducible.

Syntax checks such as `python -m py_compile main.py src/*.py` are useful but not
enough. The real smoke test is a full pipeline run:

```bash
MPLCONFIGDIR=.matplotlib-cache python main.py --as-of-date 2026-10-12
```

If Matplotlib font discovery is slow or blocked on the machine, use
`--skip-plots`. Metrics, data quality, and predictions do not depend on
Matplotlib and are saved before plotting is attempted.

## Outputs

The main generated artifacts are:

```text
data/source_metadata.json
data/processed/daily_oblast_alert_counts.csv
data/predictions/test_predictions.csv
reports/validation_metrics.csv
reports/test_metrics.csv
reports/data_quality.md
reports/figures/actual_vs_predicted.png
reports/figures/mae_by_oblast.png
reports/figures/recent_oblast_heatmap.png
reports/figures/model_error_over_time.png
```

For final submission, the compact report artifacts can be committed so reviewers
can inspect the results without rerunning the pipeline. Large raw, processed,
and prediction CSVs are ignored by default.

Plots are useful but non-critical. If plot generation fails, the pipeline keeps
the metrics and prediction artifacts.

## How To Interpret Reports

Use `reports/validation_metrics.csv` to discuss model choice and debugging.
Use `reports/test_metrics.csv` only for final performance.

Use the figures as follows:

- `actual_vs_predicted.png`: national daily total, actual vs model prediction
- `mae_by_oblast.png`: which oblasts are harder to forecast
- `recent_oblast_heatmap.png`: actual alert-count pattern across the test period
- `model_error_over_time.png`: whether national-level error clusters on some days

`reports/model_card.md` explains intended and non-intended use.
`reports/data_quality.md` summarizes raw row counts, modeled date coverage,
regions, invalid timestamps, and known scope limitations for the actual run.

## Limitations

The model uses historical alert starts only. It does not know future military
activity, official warnings, weather, infrastructure events, or news. It is an
educational forecasting benchmark, not an operational warning system.
