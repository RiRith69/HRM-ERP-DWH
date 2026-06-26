import pandas as pd
import numpy as np
from sqlalchemy import text


def clean_row(row_dict):
    """convert all NaN and float integers to proper Python types"""
    cleaned = {}
    for key, val in row_dict.items():
        if isinstance(val, float) and np.isnan(val):
            cleaned[key] = None          
        elif isinstance(val, float) and val == int(val):
            cleaned[key] = int(val)      
        else:
            cleaned[key] = val
    return cleaned


def run_conformed_etl(registry, hrm_conn, erp_conn, dw_conn):
    print("\n=== START: Conformed Dimension ETL ===")

    for dim_name, etl in registry.items():
        print(f"\nProcessing public.{dim_name}...")

        try:
            # step 1 — extract from both systems
            hrm_df = pd.read_sql(etl['hrm_query'], hrm_conn)
            erp_df = pd.read_sql(etl['erp_query'], erp_conn)
            print(f"  HRM extracted: {len(hrm_df)} rows")
            print(f"  ERP extracted: {len(erp_df)} rows")

            # step 2 — merge HRM + ERP
            merged_df = pd.concat([hrm_df, erp_df], ignore_index=True)
            merged_df = merged_df.drop_duplicates(
                subset=['employee_id'], keep='first'
            )
            print(f"  Merged unique rows: {len(merged_df)}")

            # step 3 — replace NaN with None BEFORE transform
            merged_df = merged_df.where(pd.notna(merged_df), None)   

            # step 4 — transform
            raw_records    = merged_df.to_dict('records')
            transformed    = etl['transform_func'](raw_records)
            transformed_df = pd.DataFrame(transformed)

            # step 5 — replace NaN with None AFTER transform
            transformed_df = transformed_df.where(                   
                pd.notna(transformed_df), None
            )
            print(f"  Transformed: {len(transformed_df)} rows")

            # step 6 — load with clean_row
            with dw_conn.begin() as conn:
                for _, row in transformed_df.iterrows():
                    cleaned = clean_row(row.to_dict())                
                    conn.execute(text(etl['insert_query']), cleaned)

            print(f"  ✅ public.{dim_name} loaded successfully")

        except Exception as e:
            print(f"  ❌ public.{dim_name} failed → {e}")
            raise

    print("\n=== DONE: Conformed Dimension ETL ===")