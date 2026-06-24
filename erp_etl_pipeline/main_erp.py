from registry.dim_erp_registry import ETL_Registry
from registry.fact_erp_registry import ETL_Fact_Registry
from runner.dim_runner import run_dim_etl
from runner.fact_runner import run_fact_etl
from config.db_config import ERP_SQL_SERVER_CONN, DW_POSTGRES_URL

def run_erp_pipeline():
    source_conn = ERP_SQL_SERVER_CONN()
    dw_conn     = DW_POSTGRES_URL()

    print("=== Loading Dimensions ===")
    run_dim_etl(ETL_Registry, source_conn, dw_conn)   # dims FIRST

    print("=== Loading Facts ===")
    run_fact_etl(ETL_Fact_Registry, source_conn, dw_conn) # facts AFTER

if __name__ == "__main__":
    run_erp_pipeline()