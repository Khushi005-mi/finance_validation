# Schema Validator – Validation Layer

import pandas as pd
import yaml


def check_required_columns(df: pd.DataFrame, schema: dict) -> list:
    """
    Check whether all required columns exist in dataframe.
    Returns list of missing columns.
    """
    required_columns = schema['schema']['required_columns']
    missing_columns = [col for col in required_columns if col not in df.columns]
    return missing_columns


def validate_column_types(df: pd.DataFrame, schema: dict) -> dict:
    """
    Validate dataframe column data types against expected schema.
    Returns dictionary of mismatched columns.
    """
    expected_types = schema['schema']['column_types']
    type_mismatches = {}

    for col, expected_type in expected_types.items():
        if col not in df.columns:
            continue

        actual_dtype = str(df[col].dtype)

        if expected_type == "int" and "int" not in actual_dtype:
            type_mismatches[col] = {
                "expected": "int",
                "actual": actual_dtype
            }

        elif expected_type == "float" and "float" not in actual_dtype:
            type_mismatches[col] = {
                "expected": "float",
                "actual": actual_dtype
            }

        elif expected_type == "object" and "object" not in actual_dtype:
            type_mismatches[col] = {
                "expected": "object",
                "actual": actual_dtype
            }

    return type_mismatches


def check_schema(df: pd.DataFrame, config: dict) -> dict:
    """
    Master schema validation function.
    Combines required column check + datatype validation.
    """

    missing_columns = check_required_columns(df, config)
    type_mismatches = validate_column_types(df, config)

    passed = True if not missing_columns and not type_mismatches else False

    results = {
        "passed": passed,
        "missing_columns": missing_columns,
        "type_mismatches": type_mismatches,
        "total_columns_checked": len(config['schema']['required_columns']),
        "missing_count": len(missing_columns),
        "type_mismatch_count": len(type_mismatches)
    }

    return results


# ---------------- LOCAL TEST RUNNER ---------------- #

if __name__ == "__main__":
    import sys
    sys.path.append('src')

    from ingestion.loader import load_file
    from parsers.transaction_parser import parse_transactions

    # Load raw file
    df, meta = load_file('data/corrupted/your_file.csv')

    # Parse and standardize data
    parsed_df = parse_transactions(
        df,
        'config/validation_rules.yaml',
        meta['file_name']
    )

    # Load validation config
    with open('config/validation_rules.yaml') as f:
        config = yaml.safe_load(f)

    # Run schema validation
    result = check_schema(parsed_df, config)

    print("\n--- SCHEMA VALIDATION ---")
    print(f"Passed: {result['passed']}")
    print(f"Missing columns: {result['missing_columns']}")
    print(f"Type mismatches: {result['type_mismatches']}")
    print(f"Total checked: {result['total_columns_checked']}")