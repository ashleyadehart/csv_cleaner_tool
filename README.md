# CSV Cleaner Tool

A Python-based data cleaning and profiling automation tool designed to standardize messy CSV files and generate a professional data quality report.

This project demonstrates practical data engineering skills including:

- Data cleaning
- Currency normalization
- Date parsing
- Duplicate detection
- Missing value analysis
- Outlier scanning (IQR method)
- CLI-based automation
- Unit testing with pytest

---

## Project Purpose

Messy CSV exports from accounting software, payment platforms, or spreadsheets often contain:

- Inconsistent date formats
- Currency symbols and commas
- Extra whitespace
- Duplicate records
- Mixed capitalization
- Missing values

This tool automates the cleaning process and produces:

1. A cleaned CSV file
2. A Markdown data quality report

---

## Features

- Standardizes column names (lowercase, underscore format)
- Trims whitespace
- Converts currency strings to floats
- Parses date columns to datetime
- Standardizes text to title case
- Removes exact duplicates
- Generates data quality metrics
- Performs simple outlier detection (IQR method)

---

## Project Structure

```
csv_cleaner_tool/
├── data/
│   ├── input/
│   └── output/
├── src/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── profiler.py
│   └── cli.py
├── tests/
│   └── test_cleaner.py
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup Virtual Environment
```
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

---

## Running the Tool
From the project root:
```
python -m src.cli \
  --input data/input/messy_transactions.csv \
  --output data/output/cleaned_transactions.csv \
  --report data/output/data_quality_report.md
```

After running, you will find:

- cleaned_transactions.csv
- data_quality_report.md

inside the data/output/ directory.

---

## Example Cleaning Logic

### Before Cleaning

| date      | description       | amount    |
|-----------|-------------------|-----------|
| 01/5/2025 |  SHELL gas        | "$45.20"  |
|           | Starbucks         | "$6.50"   |

### After Cleaning

| date       | description | amount |
|------------|-------------|--------|
| 2025-01-05 | Shell Gas   | 45.20  |
| NaT        | Starbucks   | 6.50   |

---

## Data Quality Report Includes

- Row count before and after cleaning
- Number of duplicates removed
- Missing values by column
- Column data types
- Outlier scan for numeric columns

---

## Running Tests

This project includes unit tests to validate cleaning logic.

From the project root:
```
pytest
```

The project uses a pytest.ini file to properly configure the Python path when using a src directory structure.

---

## Streamlit App (UI Mode)

Run the browser-based UI locally:
`
streamlit run streamlit_app.py
`

## Configuration Philosophy

Cleaning rules are defined in a structured CleanConfig dataclass to ensure:

- Transparency
- Auditability
- Flexibility
- Clear rule-based logic

Future versions may allow JSON or YAML configuration.

---

## Assumptions & Limitations

- Input CSV is properly formatted (comma-delimited)
- Currency columns are explicitly defined
- Date columns are explicitly defined
- Outlier detection uses a basic IQR method
- Tool does not replace full financial auditing procedures

---

## Future Enhancements

- Configurable JSON/YAML cleaning profiles
- Automatic column type detection
- Interactive Streamlit interface
- Batch folder processing
- Logging system
- Packaging for pip installation