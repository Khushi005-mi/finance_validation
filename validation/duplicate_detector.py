import pandas as pd
import yaml

def detect_duplicates(df, config):
    subset_cols = config["duplicate_rules"]["subset_columns"]

    missing = [col for col in subset_cols if col not in df.columns]
    if missing:
        return {"error": f"Missing columns: {missing}", "duplicate_count": 0, "duplicate_pct": 0.0, "flagged_df": df}

    df = df.copy()
    df["is_duplicate"] = df.duplicated(subset=subset_cols, keep="first")

    duplicate_count = int(df["is_duplicate"].sum())
    duplicate_pct = round(duplicate_count / len(df), 4)

    return {"duplicate_count": duplicate_count, "duplicate_pct": duplicate_pct, "flagged_df": df}


if __name__ == "__main__":
    import sys, yaml
    sys.path.append("src")
    from ingestion.loader import load_file
    from parsers.transaction_parser import parse_transactions

    df, meta = load_file("data/corrupted/your_file.csv")
    parsed_df = parse_transactions(df, "config/validation_rules.yaml", meta["file_name"])

    with open("config/validation_rules.yaml") as f:
        config = yaml.safe_load(f)

    result = detect_duplicates(parsed_df, config)
    print(f"Duplicates found: {result['duplicate_count']}")
    print(f"Duplicate %: {result['duplicate_pct'] * 100:.2f}%")
