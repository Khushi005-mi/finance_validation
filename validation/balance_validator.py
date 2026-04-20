import pandas as pd

# 1. Balance Validation Function
def validate_balances(df: pd.DataFrame, config: dict) -> dict:
    df = df.copy()

    # 2. Rule Check — old_balance - amount should equal new_balance
    df["balance_diff"] = (df["old_balance"] - df["transaction_amount"]).round(2)
    df["expected_new"] = df["balance_diff"]
    df["balance_mismatch"] = (df["expected_new"] - df["new_balance"]).abs() > 0.01

    # 3. Rule Check — Zero Balance With Non-Zero Transaction
    df["zero_balance_with_non_zero"] = (
        (df["old_balance"] == 0) &
        (df["new_balance"] == 0) &
        (df["transaction_amount"] > 0)
    )

    # 4. Overall Balance Validation Flag
    df["balance_invalid"] = (
        df["balance_mismatch"] |
        df["zero_balance_with_non_zero"]
    )

    # 5. Calculate Validation Metrics
    total = len(df)
    result = {
        "mismatch_count": int(df["balance_mismatch"].sum()),
        "zero_balance_count": int(df["zero_balance_with_non_zero"].sum()),
        "total_invalid": int(df["balance_invalid"].sum()),
        "invalid_pct": round(df["balance_invalid"].sum() / total, 4),
        "flagged_df": df
    }

    return result


# 6. Local Test Runner (Standalone Execution)
if __name__ == "__main__":
    import sys, yaml
    sys.path.append("src")
    from ingestion.loader import load_file
    from parsers.transaction_parser import parse_transactions

    # Load Raw File
    df, meta = load_file("data/corrupted/your_file.csv")

    # Parse and Standardize Data
    parsed_df = parse_transactions(
        df,
        "config/validation_rules.yaml",
        meta["file_name"]
    )

    # Load Validation Config
    with open("config/validation_rules.yaml") as f:
        config = yaml.safe_load(f)

    # Run Balance Validation
    result = validate_balances(parsed_df, config)

    print(f"Balance mismatches: {result['mismatch_count']}")
    print(f"Zero balance flags: {result['zero_balance_count']}")
    print(f"Total invalid: {result['total_invalid']}")
    print(f"Invalid %: {result['invalid_pct'] * 100:.2f}%")