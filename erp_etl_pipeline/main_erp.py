from config.db_config import get_engine
from erp_etl_pipeline.registry.dim_erp_registry import ETL_Registry
from erp_etl_pipeline.registry.fact_erp_registry import ETL_Fact_Registry
from erp_etl_pipeline.runner.dim_runner import run_dim_etl
from erp_etl_pipeline.runner.fact_runner import run_fact_etl

def run_erp_pipeline():
    print("=============================")
    print("=== START: ERP Pipeline   ===")
    print("=============================")

    source_conn = get_engine("erp")      
    dw_conn     = get_engine("postgres")  

    try:
        print("=== Loading Dimensions ===")
        run_dim_etl(ETL_Registry, source_conn, dw_conn)

        print("=== Loading Facts ===")
        run_fact_etl(ETL_Fact_Registry, source_conn, dw_conn)

        print("=============================")
        print("=== DONE: ERP Pipeline    ===")
        print("=============================")

    except Exception as e:
        print(f"=== FAILED: ERP Pipeline → {e} ===")
        raise

if __name__ == "__main__":
    run_erp_pipeline()