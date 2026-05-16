import pandas as pd

def monitor_volume(df, config):
    threshold = config["anomaly_rules"]["volume_spike_threshold"]
    volume_per_step = df.groupby("transaction_step")["transaction_id"].count().reset_index()
    volume_per_step.columns = ["step", "transaction_count"]
    mean_volume = volume_per_step["transaction_count"].mean()
    volume_per_step["spike_flag"] = volume_per_step["transaction_count"] > mean_volume * (1 + threshold)
    volume_per_step["drop_flag"] = volume_per_step["transaction_count"] < mean_volume * (1 - threshold)
    volume_per_step["anomaly_flag"] = volume_per_step["spike_flag"] | volume_per_step["drop_flag"]
    anomalies = volume_per_step[volume_per_step["anomaly_flag"] == True]
    return {
        "mean_volume": round(float(mean_volume), 2),
        "spike_count": int(volume_per_step["spike_flag"].sum()),
        "drop_count": int(volume_per_step["drop_flag"].sum()),
        "total_anomalies": int(volume_per_step["anomaly_flag"].sum()),
        "anomaly_steps": anomalies[["step", "transaction_count"]].to_dict(orient="records")
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
    result = monitor_volume(parsed_df, config)
    print(f"Mean volume: {result['mean_volume']}")
    print(f"Spikes: {result['spike_count']}")
    print(f"Drops: {result['drop_count']}")
    print(f"Total anomalies: {result['total_anomalies']}")
    print(f"Sample: {result['anomaly_steps'][:3]}")
