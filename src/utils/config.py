# Responsibilities of utils/config.py

# This file should:

# Load environment variables (.env)
# Define project folder paths
# Store database + storage configs
# Store pipeline constants
# Provide reusable config objects

# This prevents hard-coding values across the system.
"""
utils/config.py
Central configuration for the Financial Data Platform
"""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# ---------------------------------------------------
# 1. LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()  # loads .env file

# ---------------------------------------------------
# 2. PROJECT ROOT PATHS
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

# Create folders if not exist
for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR, REPORT_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# 3. DATABASE CONFIG
# ---------------------------------------------------

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

DB_CONFIG = DatabaseConfig(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 5432)),
    name=os.getenv("DB_NAME", "finance_db"),
    user=os.getenv("DB_USER", "admin"),
    password=os.getenv("DB_PASSWORD", "password")
)

# ---------------------------------------------------
# 4. STORAGE CONFIG
# ---------------------------------------------------

@dataclass
class StorageConfig:
    raw_data_path: Path
    processed_data_path: Path
    reports_path: Path

STORAGE_CONFIG = StorageConfig(
    raw_data_path=RAW_DATA_DIR,
    processed_data_path=PROCESSED_DATA_DIR,
    reports_path=REPORT_DIR
)

# ---------------------------------------------------
# 5. PIPELINE SETTINGS
# ---------------------------------------------------

@dataclass
class PipelineSettings:
    batch_size: int
    max_retries: int
    log_level: str

PIPELINE_SETTINGS = PipelineSettings(
    batch_size=int(os.getenv("BATCH_SIZE", 5000)),
    max_retries=int(os.getenv("MAX_RETRIES", 3)),
    log_level=os.getenv("LOG_LEVEL", "INFO")
)

# ---------------------------------------------------
# 6. REPORT SETTINGS
# ---------------------------------------------------

@dataclass
class reportsettings:
    default_currency : str
    company_name : str
REPORT_SETTINGS  = reportsettings(
    DEFAULT_CURRENCY =  os.getenv("DEFAULT_CURRENCY", "INR"),
    COMPANY_NAME = os.getenv("COMPANY_NAME","Your company name")
)
# ---------------------------------------------------
# 7. GLOBAL HELPER FUNCTIONS
# ---------------------------------------------------

def get_database_url():
    """Return database connection string"""
    return (
        f"postgresql://{DB_CONFIG.user}:{DB_CONFIG.password}"
        f"@{DB_CONFIG.host}:{DB_CONFIG.port}/{DB_CONFIG.name}"
    )