import pandas as pd

from src.cleaner import CleanConfig, clean_dataframe


def test_currency_conversion_and_duplicate_drop():
    df = pd.DataFrame(
        {
            "date": ["01/01/2025", "01/01/2025"],
            "description": ["  shell gas ", "  shell gas "],
            "amount": ["$10.00", "$10.00"],
            "category": ["fuel", "fuel"],
        }
    )

    config = CleanConfig()
    cleaned = clean_dataframe(df, config)

    # duplicates dropped
    assert len(cleaned) == 1
    # amount converted
    assert cleaned.loc[0, "amount"] == 10.0
    # date parsed to datetime
    assert str(cleaned.loc[0, "date"].date()) == "2025-01-01"
