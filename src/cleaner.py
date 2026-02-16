from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Tuple

import pandas as pd


@dataclass
class CleanConfig:
    drop_exact_duplicates: bool = True
    trim_strings: bool = True
    standardize_case: bool = True  # title case for text fields
    parse_dates: bool = True
    currency_to_float: bool = True
    date_columns: Tuple[str, ...] = ("date",)
    currency_columns: Tuple[str, ...] = ("amount",)
    text_columns: Tuple[str, ...] = ("description", "category", "notes")


def _clean_currency_to_float(val: object) -> Optional[float]:
    """
    Convert values like "$1,234.50" or " 120.00 " to float.
    Returns None for blanks/unparseable.
    """
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s == "":
        return None

    # Remove currency symbols and commas
    s = s.replace("$", "").replace(",", "")
    # Keep digits, decimal point, and minus sign only
    s = re.sub(r"[^0-9\.\-]", "", s)

    if s in ("", "-", ".", "-.", ".-"):
        return None

    try:
        return float(s)
    except ValueError:
        return None


def _to_title_case(val: object) -> object:
    if pd.isna(val):
        return val
    s = str(val)
    return s.title()


def clean_dataframe(df: pd.DataFrame, config: CleanConfig) -> pd.DataFrame:
    out = df.copy()

    # Normalize column names: strip + lower + replace spaces with underscores
    out.columns = (
        out.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    if config.trim_strings:
        for col in out.columns:
            if out[col].dtype == "object":
                out[col] = out[col].astype(str).str.strip().replace({"nan": None})

    # Parse date columns if present
    if config.parse_dates:
        for col in config.date_columns:
            col_norm = col.strip().lower().replace(" ", "_")
            if col_norm in out.columns:
                out[col_norm] = pd.to_datetime(out[col_norm], errors="coerce")

    # Currency conversion
    if config.currency_to_float:
        for col in config.currency_columns:
            col_norm = col.strip().lower().replace(" ", "_")
            if col_norm in out.columns:
                out[col_norm] = out[col_norm].apply(_clean_currency_to_float)

    # Standardize case for text columns
    if config.standardize_case:
        for col in config.text_columns:
            col_norm = col.strip().lower().replace(" ", "_")
            if col_norm in out.columns:
                out[col_norm] = out[col_norm].apply(_to_title_case)

    # Drop exact duplicate rows
    if config.drop_exact_duplicates:
        out = out.drop_duplicates()

    return out
