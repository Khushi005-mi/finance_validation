import pandas as pd

def monitor_trends(df, config):
    threshold = config["anomaly_rules"]["amount_spike_threshold"]

    amount_per_step = df.groupby("transaction_step")["transaction_amount"].sum().reset_index()
    amount_per_step.columns = ["step", "total_amount"]

    mean_amount = amount_per_step["total_amount"].mean()

    amount_per_step["spike_flag"] = amount_per_step["total_amount"] > mean_amount * (1 + threshold)
    amount_per_step["drop_flag"] = amount_per_step["total_amount"] < mean_amount * (1 - threshold)
    amount_per_step["anomaly_flag"] = amount_per_step["spike_flag"] | amount_per_step["drop_flag"]

    anomalies = amount_per_step[amount_per_step["anomaly_flag"] == True]

    return {
        "mean_amount_per_step": round(float(mean_amount), 2),
        "spike_count": int(amount_per_step["spike_flag"].sum()),
        "drop_count": int(amount_per_step["drop_flag"].sum()),
        "total_anomalies": int(amount_per_step["anomaly_flag"].sum()),
        "anomaly_steps": anomalies[["step", "total_amount"]].to_dict(orient="records")
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
    result = monitor_trends(parsed_df, config)
    print(f"Mean amount per step: {result['mean_amount_per_step']}")
    print(f"Amount spikes: {result['spike_count']}")
    print(f"Amount drops: {result['drop_count']}")
    print(f"Total anomalies: {result['total_anomalies']}")
    print(f"Sample: {result['anomaly_steps'][:3]}")
