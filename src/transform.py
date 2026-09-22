import pandas as pd
from pathlib import Path

REQUIRED_FIELDS = ["transaction_id", "user_id", "transaction_date"]


def clean_country(value):
    """Standardize country string: strip whitespace, uppercase."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return str(value).strip().upper()


def is_valid_record(row):
    """Reject rows missing transaction_id, user_id, or transaction_date."""
    for field in REQUIRED_FIELDS:
        val = row.get(field)
        if (
            val is None
            or (isinstance(val, float) and pd.isna(val))
            or str(val).strip() == ""
        ):
            return False
    return True


def is_valid_amount(transaction_type, amount):
    """Purchases must be positive, refunds must be negative."""
    if transaction_type == "purchase":
        return amount < 0
    if transaction_type == "refund":
        return amount < 0
    return False


def load_and_clean(csv_path):
    df = pd.read_csv(csv_path)

    df["country"] = df["country"].apply(clean_country)

    # Drop rows missing required fields
    df = df[df.apply(is_valid_record, axis=1)]

    # Drop rows with invalid amount/type combinations
    df = df[
        df.apply(lambda r: is_valid_amount(r["transaction_type"], r["amount"]), axis=1)
    ]

    return df.reset_index(drop=True)


def aggregate(df):
    agg = (
        df.groupby(["country", "transaction_date"])
        .agg(
            transaction_count=("transaction_id", "count"),
            distinct_users=("user_id", "nunique"),
            total_amount=("amount", "sum"),
        )
        .reset_index()
    )
    return agg


def main():
    input_path = Path("data/transactions.csv")
    output_path = Path("data/output.csv")

    df = load_and_clean(input_path)
    result = aggregate(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    print(f"Wrote {len(result)} aggregated rows to {output_path}")
    print(result)


if __name__ == "__main__":
    main()
