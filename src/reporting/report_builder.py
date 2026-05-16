
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

def build_report(validation_results, anomaly_results, insights, meta):
    os.makedirs("outputs/reports", exist_ok=True)

    template_str = '''<!DOCTYPE html>
<html>
<head>
    <title>Financial Data Quality Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f8; }
        h1 { color: #1f4e79; border-bottom: 3px solid #1f4e79; padding-bottom: 10px; }
        h2 { color: #2e6da4; margin-top: 30px; }
        .card { background: white; padding: 20px; margin-top: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .metric span { font-size: 22px; font-weight: bold; color: #1f4e79; }
        .high { border-left: 6px solid #e53935; background: #ffebee; padding: 15px; margin-top: 10px; border-radius: 4px; }
        .medium { border-left: 6px solid #fb8c00; background: #fff7e6; padding: 15px; margin-top: 10px; border-radius: 4px; }
        .low { border-left: 6px solid #43a047; background: #e8f5e9; padding: 15px; margin-top: 10px; border-radius: 4px; }
    </style>
</head>
<body>
<h1>Financial Data Quality Report</h1>
<p><strong>Generated:</strong> {{ generated_date }}</p>
<p><strong>Source:</strong> {{ meta.file_name }} | <strong>Rows:</strong> {{ meta.rows_loaded }} | <strong>Size:</strong> {{ meta.file_size_mb }} MB</p>

<h2>Data Quality Summary</h2>
<div class="card">
    <div class="metric">Duplicates: <span>{{ validation_results.duplicates.duplicate_count }}</span></div>
    <div class="metric">Invalid Amounts: <span>{{ validation_results.amounts.total_invalid }}</span></div>
    <div class="metric">Balance Issues: <span>{{ validation_results.balances.total_invalid }}</span></div>
    <div class="metric">Anomalies: <span>{{ anomaly_results.total_findings }}</span></div>
</div>

<h2>Insights & Actions</h2>
{% for insight in insights %}
<div class="{{ insight.severity }}">
    <strong>[{{ insight.severity | upper }}] {{ insight.category }}</strong><br>
    {{ insight.finding }}<br>
    <em>Action: {{ insight.action }}</em>
</div>
{% endfor %}

<h2>Anomaly Details</h2>
{% for finding in anomaly_results.findings %}
<div class="card">
    <strong>{{ finding.type | upper }}</strong> — Severity: {{ finding.severity }}<br>
    {{ finding.message }}
</div>
{% endfor %}

</body>
</html>'''

    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(template_str)

    html = template.render(
        generated_date=datetime.now().strftime("%d %B %Y %H:%M"),
        meta=meta,
        validation_results=validation_results,
        anomaly_results=anomaly_results,
        insights=insights
    )

    filename = f"outputs/reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w") as f:
        f.write(html)

    print(f"Report saved: {filename}")
    return filename
