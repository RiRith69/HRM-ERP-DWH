# config/__init__.py
import logging

# 1. Setup localized logging configuration for the config module
logger = logging.getLogger("cadt_dw_config")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

logger.info("⚙️ Initializing Configuration Package...")

# 2. Hoist the get_engines function from db_config.py to package level
try:
    from .db_config import get_engine
    logger.info("✅ Core database connection engines successfully exported.")
except ImportError as e:
    logger.error(f"❌ Failed to import connection engines from db_config: {e}")
    raise

# 3. Define explicit public exports for this package folder
__all__ = ["get_engine"]