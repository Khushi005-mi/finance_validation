import pandas as pd
import os

# ====================================
# SOURCE FINGERPRINT DEFINITIONS
# ====================================
SOURCE_FINGERPRINTS = {
    "paysim": ["step", "nameOrig", "nameDest", "isFraud"],
    "bank_statement": ["date", "narration", "debit", "credit"],
    "payment_gateway": ["transaction_id", "gateway_fee", "status"]
}


# ====================================
# FILE SOURCE DETECTION FUNCTION
# ====================================
def detect_source(file_path: str) -> dict:
    """
    Input:  file path
    Output: dict with file_type and source_name
    """

    # 1️⃣ GET FILE EXTENSION
    extension = os.path.splitext(file_path)[1].lower()

    # 2️⃣ LOAD FIRST 5 ROWS ONLY (FAST SAMPLING)
    if extension == '.csv':
        df = pd.read_csv(file_path, nrows=5)
    elif extension in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, nrows=5)
    else:
        raise ValueError(f"Unsupported: {extension}")

    # 3️⃣ EXTRACT COLUMN NAMES IN LOWERCASE
    columns = set(col.lower() for col in df.columns)

    # 4️⃣ MATCH COLUMNS AGAINST KNOWN SOURCE FINGERPRINTS
    detected_source = "unknown"
    for source_name, fingerprint in SOURCE_FINGERPRINTS.items():
        if all(col.lower() in columns for col in fingerprint):
            detected_source = source_name
            break

    # 5️⃣ RETURN DETECTION RESULT
    return {
        "file_type": extension,
        "source_name": detected_source,
        "columns_found": list(columns)
    }


# ====================================
# LOCAL TEST / DEMO RUN
# ====================================
if __name__ == "__main__":
    path = "data/corrupted/your_file.csv"
    result = detect_source(path)

    print(f"File type: {result['file_type']}")
    print(f"Source: {result['source_name']}")
    print(f"Columns: {result['columns_found']}")