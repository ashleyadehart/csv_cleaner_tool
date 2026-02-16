# streamlit_app.py
from __future__ import annotations

import os
from pathlib import Path

from io import BytesIO
import pandas as pd
import streamlit as st

from src.cleaner import CleanConfig, clean_dataframe
from src.profiler import build_data_quality_report

st.set_page_config(page_title="CSV Cleaner Tool", layout="wide")

# -----------------------------
# Session State (prevents reset on download)
# -----------------------------
if "has_results" not in st.session_state:
    st.session_state.has_results = False
    st.session_state.df_after = None
    st.session_state.report_md = ""
    st.session_state.output_dir = str(Path("data/output").resolve())
    st.session_state.cleaned_path = ""
    st.session_state.report_path = ""

st.title("CSV Cleaner Tool")
st.caption("Upload a CSV → clean it → download a cleaned CSV + a data quality report (Markdown).")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded is None:
    st.info("Upload a CSV to get started.")
    st.stop()

# Read uploaded CSV
try:
    df_before = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"Could not read CSV. Error: {e}")
    st.stop()

st.subheader("Preview: Raw Data")
st.dataframe(df_before.head(20), use_container_width=True)

# Column selection UI
all_cols = list(df_before.columns)

st.subheader("Cleaning Settings")

col1, col2, col3 = st.columns(3)

with col1:
    date_cols = st.multiselect(
        "Date columns",
        options=all_cols,
        default=[c for c in all_cols if c.strip().lower() in ("date", "transaction_date")],
    )

with col2:
    currency_cols = st.multiselect(
        "Currency / numeric columns to sanitize (e.g., $1,234.56)",
        options=all_cols,
        default=[c for c in all_cols if c.strip().lower() in ("amount", "total", "price")],
    )

with col3:
    text_cols = st.multiselect(
        "Text columns to standardize (Title Case)",
        options=all_cols,
        default=[c for c in all_cols if c.strip().lower() in ("description", "category", "notes")],
    )

drop_dupes = st.checkbox("Remove exact duplicate rows", value=True)
trim_strings = st.checkbox("Trim whitespace in text fields", value=True)
standardize_case = st.checkbox("Standardize selected text columns to Title Case", value=True)
parse_dates = st.checkbox("Parse selected date columns", value=True)
currency_to_float = st.checkbox("Convert selected currency columns to float", value=True)

st.divider()

# -----------------------------
# Run Cleaner (stores outputs in session_state)
# -----------------------------
run = st.button("Run Cleaner", type="primary")

if run:
    config = CleanConfig(
        drop_exact_duplicates=drop_dupes,
        trim_strings=trim_strings,
        standardize_case=standardize_case,
        parse_dates=parse_dates,
        currency_to_float=currency_to_float,
        date_columns=tuple(date_cols),
        currency_columns=tuple(currency_cols),
        text_columns=tuple(text_cols),
    )

    df_after = clean_dataframe(df_before, config)
    report_md = build_data_quality_report(df_before, df_after)

    # Save to session state so the app doesn't "reset" after download clicks
    st.session_state.df_after = df_after
    st.session_state.report_md = report_md
    st.session_state.has_results = True

    # Save outputs to /data/output
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    cleaned_path = output_dir / "cleaned.csv"
    report_path = output_dir / "data_quality_report.md"

    df_after.to_csv(cleaned_path, index=False)
    report_path.write_text(report_md, encoding="utf-8")

    st.session_state.output_dir = str(output_dir.resolve())
    st.session_state.cleaned_path = str(cleaned_path.resolve())
    st.session_state.report_path = str(report_path.resolve())

    st.success("Outputs generated! Download below or open the output folder.")

# If we don't have results yet, don't show download section
if not st.session_state.has_results:
    st.info("Click **Run Cleaner** to generate outputs.")
    st.stop()

# Pull persisted results
df_after = st.session_state.df_after
report_md = st.session_state.report_md

# -----------------------------
# Results UI
# -----------------------------
st.subheader("Results")
c1, c2, c3 = st.columns(3)
c1.metric("Rows (before)", len(df_before))
c2.metric("Rows (after)", len(df_after))
c3.metric("Duplicates removed", max(0, len(df_before) - len(df_after)))

st.subheader("Preview: Cleaned Data")
st.dataframe(df_after.head(20), use_container_width=True)

st.subheader("Data Quality Report (Markdown)")
st.markdown(report_md)

# -----------------------------
# Download + Open Folder
# -----------------------------
cleaned_csv_bytes = df_after.to_csv(index=False).encode("utf-8")
report_bytes = report_md.encode("utf-8")

st.divider()
st.subheader("Download")

d1, d2 = st.columns(2)
with d1:
    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_csv_bytes,
        file_name="cleaned.csv",
        mime="text/csv",
    )
with d2:
    st.download_button(
        label="Download Data Quality Report (.md)",
        data=report_bytes,
        file_name="data_quality_report.md",
        mime="text/markdown",
    )

st.caption(f"Saved locally to: `{st.session_state.output_dir}`")

# Windows-only open folder button
if st.button("Open Output Folder"):
    try:
        os.startfile(st.session_state.output_dir)  # Windows
    except Exception as e:
        st.error(f"Could not open folder: {e}")

