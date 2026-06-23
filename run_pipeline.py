import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# --- Diagnostic Check ---
print("--- ENVIRONMENT VARIABLE CHECK ---")
print("HRM_SQL_SERVER_HOST:", os.getenv('HRM_SQL_SERVER_HOST'))
print("HRM_SQL_SERVER_PORT:", os.getenv('HRM_SQL_SERVER_PORT'))
print("HRM_SQL_SERVER_DB:", os.getenv('HRM_SQL_SERVER_DB'))
print("---------------------------------")