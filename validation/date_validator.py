import pandas as pd

def validate_dates(df, config):
    df = df.copy()
    df["step_is_null"] = df["transaction_step"].isna()
    df["step_is_invalid"] = df["transaction_step"] <= 0
    df["step_out_of_range"] = df["transaction_step"] > 743
    df["date_invalid"] = df["step_is_null"] | df["step_is_invalid"] | df["step_out_of_range"]
    total = len(df)
    return {
        "null_count": int(df["step_is_null"].sum()),
        "invalid_count": int(df["step_is_invalid"].sum()),
        "out_of_range_count": int(df["step_out_of_range"].sum()),
        "total_invalid": int(df["date_invalid"].sum()),
        "invalid_pct": round(df["date_invalid"].sum() / total, 4),
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
    result = validate_dates(parsed_df, config)
    print(f"Null steps: {result['null_count']}")
    print(f"Invalid steps: {result['invalid_count']}")
    print(f"Out of range: {result['out_of_range_count']}")
    print(f"Total invalid: {result['total_invalid']}")
    print(f"Invalid %: {result['invalid_pct'] * 100:.2f}%")
