import pandas as pd
from sqlalchemy import text

def validate_fact(df, dims):
    """validate all SK columns have no nulls"""
    sk_columns = [info['sk_col'] for info in dims.values()]

    for col in sk_columns:
        nulls = df[col].isna().sum()
        if nulls > 0:
            print(f"  WARNING: {nulls} unresolved rows in {col} → will be dropped")

    df = df.dropna(subset=sk_columns)
    return df

def run_fact_etl(registry, source_conn, dw_conn):
    print("\n=== START: Fact ETL ===")

    for etl in registry:
        print(f"\nProcessing {etl['target_table']}...")

        try:
            # step 1 — extract
            raw_df = pd.read_sql(etl['extract_query'], source_conn)
            rows_extracted = len(raw_df)
            print(f"  Extracted: {rows_extracted} rows")

            # step 2 — load dim SKs from DW
            dims = {}
            for dim_query, source_col, sk_col in etl['dim_lookups']:
                dims[source_col] = {
                    'df':     pd.read_sql(dim_query, dw_conn),
                    'sk_col': sk_col
                }
            print(f"  Loaded: {len(dims)} dim lookups")

            # step 3 — transform
            transformed_df = etl['transform_func'](raw_df, dims)
            print(f"  Transformed: {len(transformed_df)} rows")

            # step 4 — validate
            validated_df  = validate_fact(transformed_df, dims)
            rows_loaded   = len(validated_df)
            rows_rejected = rows_extracted - rows_loaded
            print(f"  Validated: {rows_loaded} passed, {rows_rejected} rejected")

            # step 5 — load
            with dw_conn.begin() as conn:
                for _, row in validated_df.iterrows():
                    conn.execute(text(etl['insert_query']), row.to_dict())

            print(f"  ✅ {etl['target_table']} loaded successfully")

        except Exception as e:
            print(f"  ❌ {etl['target_table']} failed → {e}")
            raise

    print("\n=== DONE: Fact ETL ===")