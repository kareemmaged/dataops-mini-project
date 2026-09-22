import pandas as pd
import pytest
from src.transform import clean_country, is_valid_record, is_valid_amount, aggregate


def test_clean_country_standardizes_value():
    assert clean_country(" egypt ") == "EGYPT"
    assert clean_country("Egypt") == "EGYPT"
    assert clean_country("EGYPT") == "EGYPT"


def test_null_user_id_is_rejected():
    row = {"transaction_id": "T1", "user_id": None, "transaction_date": "2026-01-01"}
    assert is_valid_record(row) is False


def test_valid_record_is_accepted():
    row = {"transaction_id": "T1", "user_id": "U1", "transaction_date": "2026-01-01"}
    assert is_valid_record(row) is True


def test_negative_purchase_fails_validation():
    assert is_valid_amount("purchase", -30.00) is False


def test_positive_refund_fails_validation():
    assert is_valid_amount("refund", 20.00) is False


def test_positive_purchase_passes_validation():
    assert is_valid_amount("purchase", 30.00) is True


def test_negative_refund_passes_validation():
    assert is_valid_amount("refund", -10.00) is True


def test_aggregation_produces_correct_total_amount():
    df = pd.DataFrame(
        {
            "transaction_id": ["T1", "T2", "T3"],
            "user_id": ["U1", "U2", "U1"],
            "country": ["EGYPT", "EGYPT", "EGYPT"],
            "transaction_date": ["2026-01-05", "2026-01-05", "2026-01-05"],
            "transaction_type": ["purchase", "purchase", "refund"],
            "amount": [100.0, 50.0, -20.0],
        }
    )
    result = aggregate(df)
    row = result.iloc[0]
    assert row["transaction_count"] == 3
    assert row["distinct_users"] == 2
    assert row["total_amount"] == 130.0