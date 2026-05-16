# Transaction Parser – Standardization Layer

import pandas as pd
import yaml
import os
from datetime import datetime

# ---------------------------------------------------
# 1. Load YAML Configuration
# ---------------------------------------------------
def load_config(config_path: str) -> dict:
    """Load YAML config and return dictionary"""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


# ---------------------------------------------------
# 2. Build Transaction Type Lookup Table
# ---------------------------------------------------
def build_lookup(config: dict) -> dict:
    """
    Convert messy transaction type names → standard types
    Expected YAML structure:
    type_normalization:
        income: [credit, sale, deposit]
        expense: [debit, purchase, withdrawal]
    """
    lookup = {}
    for canonical, variants in config["type_normalization"].items():
        for variant in variants:
            lookup[variant.lower().strip()] = canonical
    return lookup


# ---------------------------------------------------
# 3. Normalize Transaction Type Column
# ---------------------------------------------------
def normalize_transaction_types(df: pd.DataFrame, lookup: dict) -> pd.Series:
    return (
        df["transaction_type"]
        .astype(str)
        .str.lower()
        .str.strip()
        .map(lookup)
        .fillna("unknown")
    )


# ---------------------------------------------------
# 4. Add Metadata Columns
# ---------------------------------------------------
def add_metadata(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    df["ingestion_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["data_source"] = source_file
    df["transaction_id"] = range(1, len(df) + 1)
    return df


# ---------------------------------------------------
# 5. Select Standard Columns
# ---------------------------------------------------
def select_standard_columns(df: pd.DataFrame) -> pd.DataFrame:
    standard_columns = [
        "transaction_id",
        "transaction_step",
        "transaction_type",
        "transaction_amount",
        "name_orig",
        "name_dest",
        "old_balance",
        "new_balance",
        "is_fraud",
        "is_flagged_fraud",
        "data_source",
        "ingestion_time"
    ]
    return df[standard_columns]


# ---------------------------------------------------
# 6. MAIN PARSER PIPELINE
# ---------------------------------------------------
def parse_transactions(
    df: pd.DataFrame,
    config_path: str,
    source_file: str
) -> pd.DataFrame:
    """
    Full pipeline:
    load config → build lookup → rename → normalize → metadata → select cols
    """

    # Step 1 — Load config + build lookup
    config = load_config(config_path)
    lookup = build_lookup(config)

    # Step 2 — Rename columns to standard schema
    column_mapping = {
        "step": "transaction_step",
        "type": "transaction_type",
        "amount": "transaction_amount",
        "nameOrig": "name_orig",
        "nameDest": "name_dest",
        "oldbalanceOrg": "old_balance",
        "newbalanceOrig": "new_balance",
        "isFraud":"is_fraud",
        "isFlaggedFraud": "is_flagged_fraud"
    }
    df = df.rename(columns=column_mapping)

    # Step 3 — Normalize transaction types
    df["transaction_type"] = normalize_transaction_types(df, lookup)

    # Step 4 — Add metadata
    df = add_metadata(df, source_file)

    # Step 5 — Return standardized dataframe
    df = select_standard_columns(df)

    return df


# ---------------------------------------------------
# 7. Local Test Runner
# ---------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.path.append("src")

    from ingestion.loader import load_file

    df, meta = load_file("data/corrupted/your_file.csv")

    parsed_df = parse_transactions(
        df,
        "config/validation_rules.yaml",
        meta["file_name"]
    )

    print("Shape:", parsed_df.shape)
    print("Columns:", parsed_df.columns.tolist())
    print("Unique Types:", parsed_df["transaction_type"].unique())
    print("Null Types:", parsed_df["transaction_type"].isna().sum())
    print(parsed_df.head(3))