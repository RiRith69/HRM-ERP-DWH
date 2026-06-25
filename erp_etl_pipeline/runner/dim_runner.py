import pandas as pd
from sqlalchemy import text
# dim_runner.py update just this part
def run_dim_etl(registry, source_conn, dw_conn):
    for etl in registry:
        print(f"\nProcessing {etl['target_table']}...")
        try:
            # step 1 — extract
            raw_df = pd.read_sql(etl['extract_query'], source_conn)
            rows_extracted = len(raw_df)
            print(f"  Extracted: {rows_extracted} rows")

            # step 2 — transform
            raw_records    = raw_df.to_dict('records')    
            transformed    = etl['transform_func'](raw_records)  
            transformed_df = pd.DataFrame(transformed)   
            print(f"  Transformed: {len(transformed_df)} rows")

            # step 3 — load
            with dw_conn.begin() as conn:
                for _, row in transformed_df.iterrows():
                    conn.execute(text(etl['insert_query']), row.to_dict())

            print(f"  ✅ {etl['target_table']} loaded successfully")

        except Exception as e:
            print(f"  ❌ {etl['target_table']} failed → {e}")
            raise