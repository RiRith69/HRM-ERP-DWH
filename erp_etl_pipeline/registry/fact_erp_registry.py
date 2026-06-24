from erp_etl_pipeline.extract.erp_extract import *
from erp_etl_pipeline.transform.fact_erp_transform import *

ETL_Fact_Registry = [
    {
        "target_table": "public.fact_delivery",
        "extract_query": EXTRACT_FACT_DELIVERY_QUERY,
        "transform_func": transform_fact_delivery,
        "dim_lookups": [
            # (dim_query, source_col, sk_col)
            ("SELECT date_key FROM dim_date",                                   "date_key",        "date_key"),
            ("SELECT customer_id, customer_key FROM dim_customer",              "customer_id",     "customer_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",              "employee_id",     "employee_key"),
            ("SELECT item_id, item_key FROM dim_item",                          "item_id",         "item_key"),
            ("SELECT vendor_id, vendor_key FROM dim_vendor",                    "vendor_id",       "vendor_key"),
            ("SELECT delivery_status, delivery_status_key FROM dim_delivery_status", "delivery_status", "delivery_status_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_delivery (
                date_key, customer_key, item_key, employee_key,
                vendor_key, delivery_status_key, delivery_note,
                ref_sale_order_no, quantity_shipped, unit_price,
                discount_amount, gross_delivery_value
            )
            VALUES (
                :date_key, :customer_key, :item_key, :employee_key,
                :vendor_key, :delivery_status_key, :delivery_note,
                :ref_sale_order_no, :quantity_shipped, :unit_price,
                :discount_amount, :gross_delivery_value
            )
            ON CONFLICT DO NOTHING;
        """
    },
    {
        "target_table": "public.fact_sale",
        "extract_query": EXTRACT_FACT_SALE_QUERY,
        "transform_func": ;
    }
]