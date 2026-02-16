# Data Quality Report
Rows (before): **6**
Rows (after): **5**
Duplicates removed: **1**

## Missing Values (After Cleaning)
| Column | Missing | Missing % |
|---|---:|---:|
| date | 3 | 60.0 |
| description | 0 | 0.0 |
| amount | 0 | 0.0 |
| category | 0 | 0.0 |
| notes | 3 | 60.0 |

## Column Types (After Cleaning)
| Column | dtype |
|---|---|
| date | datetime64[us] |
| description | str |
| amount | float64 |
| category | str |
| notes | str |

## Simple Outlier Scan (IQR)
- **amount**: 1 potential outliers (bounds -51.55 to 103.25)
