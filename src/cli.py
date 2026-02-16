from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.cleaner import CleanConfig, clean_dataframe
from src.profiler import build_data_quality_report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Clean a CSV and generate a data quality report.")
    p.add_argument("--input", required=True, help="Path to input CSV")
    p.add_argument("--output", required=True, help="Path to cleaned output CSV")
    p.add_argument("--report", required=True, help="Path to output Markdown report")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    report_path = Path(args.report)

    df_before = pd.read_csv(input_path)

    config = CleanConfig(
        date_columns=("date",),
        currency_columns=("amount",),
        text_columns=("description", "category", "notes"),
    )

    df_after = clean_dataframe(df_before, config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    df_after.to_csv(output_path, index=False)

    report_md = build_data_quality_report(df_before, df_after)
    report_path.write_text(report_md, encoding="utf-8")

    print(f"✅ Cleaned CSV saved to: {output_path}")
    print(f"✅ Report saved to: {report_path}")


if __name__ == "__main__":
    main()
