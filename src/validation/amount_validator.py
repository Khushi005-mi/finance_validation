import pandas as pd
import yaml

def validate_amounts(df, config):
    rules = config["amount_rules"]
    df = df.copy()

    df["amount_is_null"] = df["transaction_amount"].isna()
    df["amount_is_negative"] = df["transaction_amount"] < 0
    df["amount_is_zero"] = df["transaction_amount"] == 0
    df["amount_out_of_range"] = df["transaction_amount"] > rules["max_value"]

    df["amount_invalid"] = (
        df["amount_is_null"] |
        df["amount_is_negative"] |
        df["amount_is_zero"] |
        df["amount_out_of_range"]
    )

    total = len(df)
    return {
        "null_count": int(df["amount_is_null"].sum()),
        "negative_count": int(df["amount_is_negative"].sum()),
        "zero_count": int(df["amount_is_zero"].sum()),
        "out_of_range_count": int(df["amount_out_of_range"].sum()),
        "total_invalid": int(df["amount_invalid"].sum()),
        "invalid_pct": round(df["amount_invalid"].sum() / total, 4),
        "flagged_df": df
    }


if __name__ == "__main__":
    import sys, yaml
    sys.path.append("src")
    from ingestion.loader import load_file
    from parsers.transaction_parser import parse_transactions

    df, meta = load_file("data/corrupted/your_file.csv")
    parsed_df = parse_transactions(df, "config/validation_rules.yaml", meta["file_name"])

    with open("config/validation_rules.yaml") as f:
        config = yaml.safe_load(f)

    result = validate_amounts(parsed_df, config)
    print(f"Null amounts: {result['null_count']}")
    print(f"Negative amounts: {result['negative_count']}")
    print(f"Zero amounts: {result['zero_count']}")
    print(f"Out of range: {result['out_of_range_count']}")
    print(f"Total invalid: {result['total_invalid']}")
    print(f"Invalid %: {result['invalid_pct'] * 100:.2f}%")
