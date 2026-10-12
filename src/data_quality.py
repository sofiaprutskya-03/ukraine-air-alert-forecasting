from pathlib import Path

import pandas as pd


def _count_true_values(series: pd.Series) -> int:
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
        .sum()
    )


def write_data_quality_report(
    raw_path: Path, daily: pd.DataFrame, output_path: Path
) -> None:
    """Write a compact data-quality report for the actual pipeline run."""
    raw = pd.read_csv(raw_path)

    raw_row_count = len(raw)
    invalid_started_at_count = "not available"
    if "started_at" in raw.columns:
        parsed_started_at = pd.to_datetime(raw["started_at"], utc=True, errors="coerce")
        invalid_started_at_count = int(parsed_started_at.isna().sum())

    naive_true_count = "column not present"
    if "naive" in raw.columns:
        naive_true_count = int(_count_true_values(raw["naive"]))

    region_column = "region" if "region" in raw.columns else None
    raw_rows_per_region = pd.Series(dtype="int64")
    if region_column is not None:
        raw_rows_per_region = raw[region_column].fillna("UNKNOWN").value_counts().sort_index()

    modeled_regions = sorted(daily["oblast"].dropna().unique())
    modeled_rows_per_region = daily.groupby("oblast").size().sort_index()
    modeled_start = daily["date_kyiv"].min().date()
    modeled_end = daily["date_kyiv"].max().date()

    lines = [
        "# Data Quality Report",
        "",
        "## Source Summary",
        "",
        f"- raw CSV path: `{raw_path}`",
        f"- raw row count: `{raw_row_count}`",
        f"- invalid `started_at` count: `{invalid_started_at_count}`",
        f"- `naive=true` count: `{naive_true_count}`",
        "",
        "## Modeled Daily Table",
        "",
        f"- modeled date range: `{modeled_start}` to `{modeled_end}`",
        f"- number of regions: `{len(modeled_regions)}`",
        f"- modeled oblast-date rows: `{len(daily)}`",
        "",
        "## Region List",
        "",
    ]
    lines.extend([f"- {region}" for region in modeled_regions])

    lines.extend(["", "## Raw Rows Per Region", ""])
    if raw_rows_per_region.empty:
        lines.append("- not available because the raw file has no `region` column")
    else:
        lines.extend(
            [f"- {region}: `{count}`" for region, count in raw_rows_per_region.items()]
        )

    lines.extend(["", "## Modeled Rows Per Region", ""])
    lines.extend(
        [f"- {region}: `{count}`" for region, count in modeled_rows_per_region.items()]
    )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This project models alert starts present in the selected dataset, not every possible real-world siren state.",
            "- The pipeline does not infer missing alerts, correct historical reporting gaps, or adjust for special regional conditions unless they are represented in the source rows.",
            "- The current Kyiv-local day is excluded because it may be incomplete.",
            "- The model should not be interpreted as an operational safety or warning system.",
            "",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
