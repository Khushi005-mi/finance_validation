import pandas as pd
import os
import chardet
from datetime import datetime


def detect_encoding(file_path):
    """Detect file encoding safely"""
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(100000))
    return result["encoding"]


def build_metadata(file_path, data, encoding):
    """Create metadata dictionary"""
    if isinstance(data, dict):
        rows = sum(len(df) for df in data.values())
        columns = list({col for df in data.values() for col in df.columns})
    else:
        rows = len(data)
        columns = data.columns.tolist()

    metadata = {
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "rows_loaded": rows,
        "columns": columns,
        "loaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
        "encoding": encoding
    }
    return metadata


def load_file(file_path: str):
    """
    Returns:
        data (DataFrame or dict of DataFrames)
        metadata (dict)
    """

    # 1) File existence
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    # 2) File type detection
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in [".csv", ".xlsx"]:
        raise ValueError(f"Unsupported file type: {file_extension}")

    try:
        # ===== CSV =====
        if file_extension == ".csv":
            encoding = detect_encoding(file_path)
            print(f"Detected encoding: {encoding}")

            df = pd.read_csv(
                file_path,
                encoding=encoding,
                on_bad_lines="skip"
            )

            metadata = build_metadata(file_path, df, encoding)
            return df, metadata

        # ===== EXCEL =====
        if file_extension == ".xlsx":
            excel_file = pd.ExcelFile(file_path)
            sheets = excel_file.sheet_names

            data_frames = {}
            for sheet in sheets:
                data_frames[sheet] = excel_file.parse(sheet)

            metadata = build_metadata(file_path, data_frames, "N/A")
            return data_frames, metadata

    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


# Test run
if __name__ == "__main__":
    file = "data/raw/sample.csv"
    data, meta = load_file(file)

    print("\nMetadata:")
    print(meta)

    if isinstance(data, dict):
        for sheet, df in data.items():
            print(f"{sheet} → {df.shape}")
    else:
        print(data.head())