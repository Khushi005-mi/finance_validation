from fastapi import FastAPI, UploadFile, File
import shutil
import os
import sys
sys.path.append('src')

from run_engine import run_engine

app = FastAPI(title="Financial Validation Engine")

@app.get("/")
def home():
    return {"status": "running", "service": "Financial Validation Engine"}

@app.get("/health")
def health():
    return {"status": "healthy"}