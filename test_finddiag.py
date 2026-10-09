"""
FinDiag QA tests.

Place this file in the same folder as app.py, then run:
    python -m pytest -q test_finddiag.py

If your Streamlit source file has another name, change `import app as app_module`.
These tests check helper logic; they do not replace a manual browser test of the UI.
"""
from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from openpyxl import Workbook

import app as app_module


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1234", 1234.0),
        ("1 234,56", 1234.56),
        ("1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        ("(1 234)", -1234.0),
        ("1 234-", -1234.0),
        ("15%", 15.0),
    ],
)
def test_number_parsing(value, expected):
    assert app_module.parse_number(value) == pytest.approx(expected)


@pytest.mark.parametrize("value", [None, np.nan, pd.NA, "", "   ", "-", "N/A", "nan"])
def test_missing_values_are_nan_not_zero(value):
    assert app_module.is_missing_value(value)
    assert np.isnan(app_module.parse_number(value))


def test_invalid_number_does_not_become_zero():
    assert np.isnan(app_module.parse_number("not a number"))


def test_zero_is_preserved_as_zero():
    assert app_module.parse_number("0") == 0.0
    assert app_module.parse_number(0) == 0.0


def test_ambiguous_thousands_format_is_flagged():
    number, status = app_module._parse_number_detail("1,234")
    assert number == pytest.approx(1234.0)
    assert status == "ambiguous"


def test_validation_flags_missing_invalid_and_duplicate_rows_without_deleting_data():
    df = pd.DataFrame(
        {
            "Revenue": ["1 000,00", "1 000,00", "bad"],
            "Net Income": ["100,00", "100,00", "N/A"],
            "Notes": ["ok", "ok", ""],
        }
    )
    original_shape = df.shape
    messages, counts = app_module.validate_data(df)

    assert df.shape == original_shape
    assert counts["rows"] == 3
    assert counts["missing_values"] >= 1
    assert counts["duplicate_rows"] == 1
    assert counts["invalid_numeric"] == 1
    message_keys = {key for key, _ in messages}
    assert "invalid_numeric_detail" in message_keys
    assert "duplicate_rows" in message_keys


def test_financial_metrics_calculate_expected_ratios():
    df = pd.DataFrame(
        {
            "Revenue": [1000],
            "Net Income": [100],
            "Total Assets": [500],
            "Current Assets": [200],
            "Inventory": [50],
            "Current Liabilities": [100],
            "Total Liabilities": [250],
            "Equity": [250],
        }
    )
    metrics = app_module.calculate_financial_metrics(df)

    assert metrics["net_margin"] == pytest.approx(0.10)
    assert metrics["roa"] == pytest.approx(0.20)
    assert metrics["current_ratio"] == pytest.approx(2.0)
    assert metrics["quick_ratio"] == pytest.approx(1.5)
    assert metrics["debt_ratio"] == pytest.approx(0.50)
    assert metrics["equity_ratio"] == pytest.approx(0.50)


def test_zero_denominator_returns_unavailable_ratio():
    assert app_module.safe_divide(10, 0) is None
    assert app_module.safe_divide(None, 5) is None


def test_excel_reader_skips_blank_rows_and_makes_duplicate_headers_unique():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Financials"
    sheet.append(["", "", ""])
    sheet.append(["Year", "Revenue", "Revenue", "Net Income"])
    sheet.append([2023, "1.234,50", "2,000", "100,00"])
    sheet.append([2024, "2.345,50", "3,000", "200,00"])

    buffer = BytesIO()
    workbook.save(buffer)

    df, info = app_module.read_worksheet(
        buffer.getvalue(), "Financials", "openpyxl"
    )

    assert list(df.columns) == ["Year", "Revenue", "Revenue (2)", "Net Income"]
    assert len(df) == 2
    assert info["duplicates"] == ["Revenue"]


def test_empty_dataframe_is_handled_by_validation():
    messages, counts = app_module.validate_data(pd.DataFrame())
    assert counts["rows"] == 0
    assert counts["columns"] == 0
    assert messages
