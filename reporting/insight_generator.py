
def generate_insights(validation_results, anomaly_results):
    insights = []

    # Insight 1 — Duplicate transactions
    dup = validation_results.get("duplicates", {})
    if dup.get("duplicate_count", 0) > 0:
        insights.append({
            "category": "Data Quality",
            "severity": "high",
            "finding": f"{dup['duplicate_count']} duplicate transactions detected ({dup['duplicate_pct']*100:.2f}%).",
            "action": "Review and remove duplicate entries before reporting."
        })

    # Insight 2 — Invalid amounts
    amt = validation_results.get("amounts", {})
    if amt.get("total_invalid", 0) > 0:
        insights.append({
            "category": "Data Quality",
            "severity": "high",
            "finding": f"{amt['total_invalid']} invalid amounts found ({amt['invalid_pct']*100:.2f}%). Includes {amt['null_count']} nulls, {amt['negative_count']} negatives, {amt['zero_count']} zeros.",
            "action": "Investigate source systems for missing or incorrect amount values."
        })

    # Insight 3 — Balance mismatches
    bal = validation_results.get("balances", {})
    if bal.get("total_invalid", 0) > 0:
        insights.append({
            "category": "Balance Integrity",
            "severity": "medium",
            "finding": f"{bal['total_invalid']} transactions have balance inconsistencies ({bal['invalid_pct']*100:.2f}%).",
            "action": "Verify balance update logic in source transaction system."
        })

    # Insight 4 — Anomaly findings
    for finding in anomaly_results.get("findings", []):
        insights.append({
            "category": "Anomaly",
            "severity": finding["severity"],
            "finding": finding["message"],
            "action": "Investigate affected time steps for unusual activity."
        })

    return insights

if __name__ == "__main__":
    validation_results = {
        "duplicates": {"duplicate_count": 497, "duplicate_pct": 0.0049},
        "amounts": {"total_invalid": 5310, "invalid_pct": 0.0528, "null_count": 5019, "negative_count": 191, "zero_count": 100},
        "balances": {"total_invalid": 70889, "invalid_pct": 0.7054}
    }
    anomaly_results = {
        "findings": [
            {"type": "volume_anomaly", "severity": "high", "message": "3 volume spikes and 7 drops detected."}
        ]
    }
    insights = generate_insights(validation_results, anomaly_results)
    print(f"Total insights: {len(insights)}")
    for i, insight in enumerate(insights):
        print(f"\n{i+1}. [{insight['severity'].upper()}] {insight['category']}")
        print(f"   Finding: {insight['finding']}")
        print(f"   Action: {insight['action']}")
