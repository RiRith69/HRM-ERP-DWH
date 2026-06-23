from queries.erp_queries import *
from hrm_etl_pipeline.erp_transformation import *
ETL_Registry = [
    {
        "target_table": "public.dim_customer",
        "extract_query": EXTRACT_customer_QUERY,
        "transform_func": trans_customer,
        "insert_query": """
            INSERT INTO public.dim_customer (customer_id, customer_name, customer_type, contact_name, nationality, gender, age, region, country)
            VALUES (:customer_id, :customer_name, :customer_type, :contact_name, :nationality, :gender, :age, :region, :country)
            ON CONFLICT (customer_id) DO NOTHING;
        """
    }
]