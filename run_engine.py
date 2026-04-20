import sys
import yaml
sys.path.append("src")

from ingestion.loader import load_file
from ingestion.checksum import check_duplicate
from ingestion.detector import detect_source
from parsers.transaction_parser import parse_transactions
from validation.schema_validator import check_schema
from validation.duplicate_detector import detect_duplicates
from validation.amount_validator import validate_amounts
from validation.date_validator import validate_dates
from validation.balance_validator import validate_balances
from anomaly.anomaly_engine import run_anomaly_engine
from reporting.insight_generator import generate_insights
from reporting.report_builder import build_report

def run_engine(file_path, config_path="config/validation_rules.yaml"):
    print("=" * 55)
    print("   FINANCIAL DATA QUALITY & VALIDATION ENGINE")
    print("=" * 55)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Step 1 — Checksum
    seen = set()
    if check_duplicate(file_path, seen):
        print("ERROR: Duplicate file detected. Aborting.")
        return

    # Step 2 — Detect source
    source_info = detect_source(file_path)
    print(f"Source detected: {source_info['source_name']}")

    # Step 3 — Load
    df, meta = load_file(file_path)
    print(f"Loaded: {meta['rows_loaded']} rows from {meta['file_name']}")

    # Step 4 — Parse
    parsed_df = parse_transactions(df, config_path, meta["file_name"])
    print(f"Parsed: {len(parsed_df)} rows standardized")

    # Step 5 — Validate schema
    schema_result = check_schema(parsed_df, config)
    print(f"Schema: {'PASSED' if schema_result['passed'] else 'FAILED'}")
    if not schema_result["passed"]:
        print(f"Missing: {schema_result['missing_columns']}")
        return

    # Step 6 — Run all validators
    dup_result = detect_duplicates(parsed_df, config)
    amt_result = validate_amounts(parsed_df, config)
    date_result = validate_dates(parsed_df, config)
    bal_result = validate_balances(parsed_df, config)

    print(f"Duplicates: {dup_result['duplicate_count']}")
    print(f"Invalid amounts: {amt_result['total_invalid']}")
    print(f"Balance issues: {bal_result['total_invalid']}")

    validation_results = {
        "duplicates": dup_result,
        "amounts": amt_result,
        "dates": date_result,
        "balances": bal_result
    }

    # Step 7 — Anomaly detection
    anomaly_results = run_anomaly_engine(parsed_df, config)
    print(f"Anomalies found: {anomaly_results['total_findings']}")

    # Step 8 — Generate insights
    insights = generate_insights(validation_results, anomaly_results)
    print(f"Insights generated: {len(insights)}")

    # Step 9 — Build report
    path = build_report(validation_results, anomaly_results, insights, meta)

    print("=" * 55)
    print(f"COMPLETE. Report: {path}")
    print("=" * 55)

if __name__ == "__main__":
    run_engine("data/corrupted/your_file.csv")
