from __future__ import annotations

import pandas as pd


def build_data_quality_report(df_before: pd.DataFrame, df_after: pd.DataFrame) -> str:
    lines = []
    lines.append("# Data Quality Report\n")
    lines.append(f"Rows (before): **{len(df_before)}**\n")
    lines.append(f"Rows (after): **{len(df_after)}**\n")
    lines.append(f"Duplicates removed: **{len(df_before) - len(df_after)}**\n")

    lines.append("\n## Missing Values (After Cleaning)\n")
    missing = df_after.isna().sum().sort_values(ascending=False)
    missing_pct = (missing / len(df_after) * 100).round(1) if len(df_after) else missing
    lines.append("| Column | Missing | Missing % |\n")
    lines.append("|---|---:|---:|\n")
    for col in df_after.columns:
        lines.append(f"| {col} | {int(missing[col])} | {missing_pct[col]} |\n")

    lines.append("\n## Column Types (After Cleaning)\n")
    lines.append("| Column | dtype |\n")
    lines.append("|---|---|\n")
    for col in df_after.columns:
        lines.append(f"| {col} | {df_after[col].dtype} |\n")

    # Simple outlier check for numeric columns using IQR
    numeric_cols = df_after.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("\n## Simple Outlier Scan (IQR)\n")
        for col in numeric_cols:
            series = df_after[col].dropna()
            if series.empty:
                continue
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = df_after[(df_after[col] < lower) | (df_after[col] > upper)][col]
            lines.append(f"- **{col}**: {len(outliers)} potential outliers (bounds {lower:.2f} to {upper:.2f})\n")

    return "".join(lines)
