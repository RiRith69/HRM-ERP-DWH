# main.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import logging
from sqlalchemy import create_engine, text
from config.db_config import HRM_SQL_SERVER_CONN, DW_POSTGRES_URL, ETL_Registry

# Configure explicit professional terminal logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ETL_Orchestrator")

def run_pipeline():
    logger.info("🚀 Starting One-Time Historical ETL Bulk Ingestion Pipeline...")
    
    # Initialize connection pools
    src_engine = create_engine(HRM_SQL_SERVER_CONN)
    dwh_engine = create_engine(DW_POSTGRES_URL)

    # Process each dimension configuration sequentially
    for job in ETL_Registry:
        table = job["target_table"]
        logger.info(f"⏳ Processing target destination table: {table}")
        
        try:
            # ---- STEP 1: EXTRACT ----
            with src_engine.connect() as src_conn:
                res = src_conn.execute(text(job["extract_query"]))
                raw_rows = res.fetchall()
                headers = res.keys()
            
            # Map database result tuple into a Python dictionary payload
            extracted_payload = [dict(zip(headers, row)) for row in raw_rows]
            logger.info(f"Successfully extracted {len(extracted_payload)} records into engine memory.")
            
            # ---- STEP 2: TRANSFORM ----
            cleaned_payload = job["transform_func"](extracted_payload)
            logger.info("In-memory cleanups and data formatting transformations applied.")

            # ---- STEP 3: LOAD ----
            with dwh_engine.begin() as dwh_conn:                
                # B. Batch stream cleaned dataset records directly to warehouse tables
                if cleaned_payload:
                    dwh_conn.execute(text(job["insert_query"]), cleaned_payload)
                    logger.info(f"Transaction finalized. Target table {table} loaded successfully.\n")
                else:
                    logger.warning(f"No source payload records found to insert for {table}.\n")
                    
        except Exception as error:
            logger.error(f"Critical Pipeline Failure on table target: {table}")
            logger.error(f"Error Context: {str(error)}")
            logger.error("Database transaction safely rolled back. Continuing to next pipeline table index...\n")
            continue

    logger.info("🏆 Historical Dimension Bulk ETL Pipeline Load completed successfully.")

if __name__ == "__main__":
    run_pipeline()