import pandas as pd

def run_anomaly_engine(df, config):
    import sys
    sys.path.append("src")
    from anomaly.volume_monitor import monitor_volume
    from anomaly.trend_monitor import monitor_trends

    findings = []

    # Run volume monitor
    volume_result = monitor_volume(df, config)
    if volume_result["total_anomalies"] > 0:
        findings.append({
            "type": "volume_anomaly",
            "severity": "high" if volume_result["spike_count"] > 0 else "medium",
            "message": f"Found {volume_result['spike_count']} volume spikes and {volume_result['drop_count']} drops across steps.",
            "details": volume_result["anomaly_steps"][:5]
        })

    # Run trend monitor
    trend_result = monitor_trends(df, config)
    if trend_result["total_anomalies"] > 0:
        findings.append({
            "type": "amount_trend_anomaly",
            "severity": "high" if trend_result["spike_count"] > 0 else "medium",
            "message": f"Found {trend_result['spike_count']} amount spikes and {trend_result['drop_count']} drops.",
            "details": trend_result["anomaly_steps"][:5]
        })

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda x: severity_order.get(x["severity"], 99))

    return {
        "total_findings": len(findings),
        "findings": findings
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
    result = run_anomaly_engine(parsed_df, config)
    print(f"Total findings: {result['total_findings']}")
    for i, finding in enumerate(result['findings']):
        print(f"\nFinding {i+1}:")
        print(f"  Type: {finding['type']}")
        print(f"  Severity: {finding['severity']}")
        print(f"  Message: {finding['message']}")
