import pandas as pd

def transform_fact_delivery(raw_df, dims):
    df = raw_df.copy()

    # date_key already YYYYMMDD → directly matches dim_date SK
    dim_date_df = dims['date_key']['df']
    df = df.merge(dim_date_df[['date_key']], on='date_key', how='left')

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    # employee_id → employee_key
    dim_employee_df = dims['employee_id']['df']
    df = df.merge(dim_employee_df[['employee_id', 'employee_key']], on='employee_id',how='left').drop(columns=['employee_id'])

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df']
    df = df.merge(dim_vendor_df[['vendor_id', 'vendor_key']], on='vendor_id', how='left').drop(columns=['vendor_id'])

    # delivery_status → delivery_status_key
    dim_status_df = dims['delivery_status']['df']
    df = df.merge(dim_status_df[['delivery_status', 'delivery_status_key']], on='delivery_status', how='left').drop(columns=['delivery_status'])

    fact_columns = [
        'date_key',
        'customer_key',
        'item_key',
        'employee_key',
        'vendor_key',
        'delivery_status_key',
        'delivery_note',
        'ref_sale_order_no',
        'quantity_shipped',
        'unit_price',
        'discount_amount',
        'gross_delivery_value'
    ]
    df = df[fact_columns]
    return df

def transfrom_fact_sale(raw_df, dims):
    df = raw_df.copy()