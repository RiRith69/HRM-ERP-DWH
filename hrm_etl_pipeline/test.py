import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Get the directory where config.py lives
config_dir = Path(__file__).resolve().parent

# 2. Point to the .env file INSIDE this config folder
env_path = config_dir / '.env'

# 3. Load it up!
load_dotenv(dotenv_path=env_path)

# --- Your Diagnostic Check ---
print("--- ENVIRONMENT VARIABLE CHECK ---")
print("HRM_SQL_SERVER_HOST:", os.getenv('HRM_SQL_SERVER_HOST'))
print("HRM_SQL_SERVER_PORT:", os.getenv('HRM_SQL_SERVER_PORT'))
print("HRM_SQL_SERVER_DB:", os.getenv('HRM_SQL_SERVER_DB'))
print("---------------------------------")