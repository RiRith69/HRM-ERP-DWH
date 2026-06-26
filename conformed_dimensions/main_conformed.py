from config.db_config import get_engine
from conformed_dimensions.registry.conformed_registry import ETL_Conformed_Registry
from conformed_dimensions.runner.conformed_runner import run_conformed_etl

def run_conformed_pipeline():
    print("================================")
    print("=== START: Conformed Dims    ===")
    print("================================")

    hrm_conn = get_engine("hrm")
    erp_conn = get_engine("erp")
    dw_conn  = get_engine("postgres")

    try:
        run_conformed_etl(
            ETL_Conformed_Registry,
            hrm_conn,
            erp_conn,
            dw_conn
        )

        print("================================")
        print("=== DONE: Conformed Dims     ===")
        print("================================")

    except Exception as e:
        print(f"=== FAILED: Conformed → {e} ===")
        raise

if __name__ == "__main__":
    run_conformed_pipeline()