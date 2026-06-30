import pandas as pd

def transform_fact_delivery(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # date_key — validate only, replace out of range with -1 ✅
    # merging causes duplicate column since date_key already exists in df
    valid_date_keys = dims['date_key']['df']['date_key'].tolist()
    df['date_key'] = df['date_key'].where(
        df['date_key'].isin(valid_date_keys), -1
    )

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df'].copy()
    df = df.merge(
        dim_customer_df[['customer_id', 'customer_key']], 
        on='customer_id', how='left'
    ).drop(columns=['customer_id'])
    df['customer_key'] = df['customer_key'].fillna(-1)

    # employee_id → employee_key
    dim_employee_df = dims['employee_id']['df'].copy()
    df = df.merge(
        dim_employee_df[['employee_id', 'employee_key']], 
        on='employee_id', how='left'
    ).drop(columns=['employee_id'])
    df['employee_key'] = df['employee_key'].fillna(-1)

    # item_id → item_key
    dim_item_df = dims['item_id']['df'].copy()
    df = df.merge(
        dim_item_df[['item_id', 'item_key']], 
        on='item_id', how='left'
    ).drop(columns=['item_id'])
    df['item_key'] = df['item_key'].fillna(-1)

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df'].copy()
    df = df.merge(
        dim_vendor_df[['vendor_id', 'vendor_key']], 
        on='vendor_id', how='left'
    ).drop(columns=['vendor_id'])
    df['vendor_key'] = df['vendor_key'].fillna(-1)

    # delivery_status → delivery_status_key
    dim_status_df = dims['delivery_no']['df'].copy()
    df = df.merge(
        dim_status_df[['delivery_no', 'delivery_status_key']], 
        on='delivery_no', how='left'
    ).drop(columns=['delivery_no'])
    df['delivery_status_key'] = df['delivery_status_key'].fillna(-1)

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
    df = df.drop_duplicates()
    return df
def transfrom_fact_sale(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    dim_date_df = dims["date_key"]['df']
    df = df.merge(dim_date_df[['date_key']], on='date_key', how='left')

    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    dim_employee_df = dims['employee_id']['df']
    df = df.merge(dim_employee_df[['employee_id', 'employee_key']], on='employee_id',how='left').drop(columns=['employee_id'])

    dim_currency_df = dims['currency_no']['df']
    df = df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])

    fact_columns = [
        'date_key',
        'customer_key',
        'item_key',
        'employee_key',
        'currency_key',
        'sale_order_no',
        'quantity',
        'unit_price',
        'discount',
        'line_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_purchase(raw_df,dims):
    df = raw_df.copy().drop_duplicates()

    dim_date_df = dims["date_key"]['df']
    df = df.merge(dim_date_df[['date_key']], on='date_key', how='left')

    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    dim_employee_df = dims['employee_id']['df']
    df = df.merge(dim_employee_df[['employee_id', 'employee_key']], on='employee_id',how='left').drop(columns=['employee_id'])

    dim_vendor_df = dims['vendor_id']['df']
    df = df.merge(dim_vendor_df[['vendor_id', 'vendor_key']], on='vendor_id', how='left').drop(columns=['vendor_id'])
    
    dim_currency_df = dims['currency_no']["df"]
    df= df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])
    fact_columns = [
        'date_key',
        'item_key',
        'employee_key',
        'vendor_key',
        'currency_key',
        'purchase_order_no',
        'purchase_status',
        'approval_status',
        'quantity',
        'unit_cost',
        'total_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_inventory(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # date_key — validate only, no merge needed
    valid_date_keys = dims['date_key']['df']['date_key'].tolist()
    df['date_key'] = df['date_key'].where(
        df['date_key'].isin(valid_date_keys), -1
    )

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # location_id → location_key
    dim_location_df = dims['location_id']['df'].copy()
    df = df.merge(
        dim_location_df[['location_id', 'location_key']],
        on='location_id', how='left'
    ).drop(columns=['location_id'])
    df['location_key'] = df['location_key'].fillna(-1)

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df'].copy()
    df = df.merge(
        dim_vendor_df[['vendor_id', 'vendor_key']],
        on='vendor_id', how='left'
    ).drop(columns=['vendor_id'])
    df['vendor_key'] = df['vendor_key'].fillna(-1)

    fact_columns = [
        'date_key',
        'item_key',
        'location_key',
        'vendor_key',
        'units_in_stock_snap'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df


def transform_fact_quotation(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # date_key — validate only, no merge needed
    df['date_key'] = df['date_key'].astype('Int64')
    df['authorizing_date_key'] = df['authorizing_date_key'].astype('Int64')

    # 2. date_key — if not valid, assign pd.NA instead of -1
    valid_date_keys = dims['date_key']['df']['date_key'].tolist()
    df['date_key'] = df['date_key'].where(
        df['date_key'].isin(valid_date_keys), pd.NA
    )

    # 3. authorizing_date_key — if not valid, assign pd.NA instead of -1
    valid_auth_date_keys = dims['authorizing_date_key']['df']['date_key'].tolist()
    df['authorizing_date_key'] = df['authorizing_date_key'].where(
        df['authorizing_date_key'].isin(valid_auth_date_keys), pd.NA
    )

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df'].copy()
    df = df.merge(
        dim_customer_df[['customer_id', 'customer_key']],
        on='customer_id', how='left'
    ).drop(columns=['customer_id'])
    df['customer_key'] = df['customer_key'].fillna(-1)

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(
        dim_item_df[['item_id', 'item_key']],
        on='item_id', how='left'
    ).drop(columns=['item_id'])
    df['item_key'] = df['item_key'].fillna(-1)

    # preparing_employee_id → preparing_employee_key
    # use .copy() to prevent pandas from reusing the same dataframe reference
    dim_preparing_emp_df = dims['preparing_employee_id']['df'].copy()
    df = df.merge(
        dim_preparing_emp_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'preparing_employee_id',
            'employee_key': 'preparing_employee_key'
        }),
        on='preparing_employee_id', how='left'
    ).drop(columns=['preparing_employee_id'])
    df['preparing_employee_key'] = df['preparing_employee_key'].fillna(-1)

    # contacting_employee_id → contacting_employee_key
    # fresh .copy() so it does not conflict with preparing merge above
    dim_contacting_emp_df = dims['contacting_employee_id']['df'].copy()
    df = df.merge(
        dim_contacting_emp_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'contacting_employee_id',
            'employee_key': 'contacting_employee_key'
        }),
        on='contacting_employee_id', how='left'
    ).drop(columns=['contacting_employee_id'])
    df['contacting_employee_key'] = df['contacting_employee_key'].fillna(-1)

    # authorizing_employee_id → authorizing_employee_key
    # fresh .copy() so it does not conflict with previous employee merges
    dim_authorizing_emp_df = dims['authorizing_employee_id']['df'].copy()
    df = df.merge(
        dim_authorizing_emp_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'authorizing_employee_id',
            'employee_key': 'authorizing_employee_key'
        }),
        on='authorizing_employee_id', how='left'
    ).drop(columns=['authorizing_employee_id'])
    df['authorizing_employee_key'] = df['authorizing_employee_key'].fillna(-1)

    # authorizing_status → quotation_status_key
    dim_status_df = dims['authorizing_status']['df'].copy()
    df = df.merge(
        dim_status_df[['authorizing_status', 'quotation_status_key']],
        on='authorizing_status', how='left'
    ).drop(columns=['authorizing_status'])
    df['quotation_status_key'] = df['quotation_status_key'].fillna(-1)

    # final column alignment
    fact_columns = [
        'date_key',
        'authorizing_date_key',
        'customer_key',
        'item_key',
        'preparing_employee_key',
        'contacting_employee_key',
        'authorizing_employee_key',
        'quotation_status_key',
        'quotation_no',
        'quotation_detail_no',
        'quantity',
        'unit_price',
        'discount_amount',
        'gross_amount',
        'net_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df
def transform_fact_invoice(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # invoice_date_key → validate against dim_date
    dim_date_df = dims['invoice_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'invoice_date_key'}), on='invoice_date_key', how='left')

    # due_date_key → same dim_date different role
    dim_due_date_df = dims['due_date_key']['df']
    df = df.merge(dim_due_date_df[['date_key']].rename(columns={'date_key': 'due_date_key'}), on='due_date_key', how='left')

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # cashier_employee_id → cashier_employee_key
    dim_emp_df = dims['cashier_employee_id']['df']
    df = df.merge(
        dim_emp_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'cashier_employee_id',
            'employee_key': 'cashier_employee_key'
        }), on='cashier_employee_id', how='left'
    ).drop(columns=['cashier_employee_id'])

    # salesperson_employee_id → salesperson_employee_key
    dim_emp_df = dims['salesperson_employee_id']['df']
    df = df.merge(
        dim_emp_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'salesperson_employee_id',
            'employee_key': 'salesperson_employee_key'
        }), on='salesperson_employee_id', how='left'
    ).drop(columns=['salesperson_employee_id'])

    # location_id → location_key
    dim_location_df = dims['location_id']['df']
    df = df.merge(dim_location_df[['location_id', 'location_key']], on='location_id', how='left').drop(columns=['location_id'])

    # currency_no → currency_key
    dim_currency_df = dims['currency_no']['df']
    df = df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])

    # invoice_no → invoice_key
    dim_invoice_df = dims['invoice_no']['df']
    df = df.merge(dim_invoice_df[['invoice_no', 'invoice_key']], on='invoice_no', how='left').drop(columns=['invoice_no'])

    # final column alignment
    fact_columns = [
        'invoice_date_key',
        'due_date_key',
        'customer_key',
        'item_key',
        'cashier_employee_key',
        'salesperson_employee_key',
        'location_key',
        'currency_key',
        'invoice_key',
        'quantity_billed',
        'unit_price',
        'discount_amount',
        'unit_tax_amount',
        'gross_revenue',
        'net_tax_amount',
        'net_revenue'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    df = df.where(pd.notnull(df), None)
    return df

def transform_fact_expense(raw_df, dims):
    df = raw_df.copy().drop_duplicates()
    # expense_date_key → validate against dim_date
    dim_date_df = dims['expense_date_key']['df']
    df = df.merge(
        dim_date_df[['date_key']].rename(columns={'date_key': 'expense_date_key'}),
        on='expense_date_key', how='left'
    )

    # authorizing_date_key → same dim_date different role
    dim_auth_date_df = dims['authorizing_date_key']['df']
    df = df.merge(
        dim_auth_date_df[['date_key']].rename(columns={'date_key': 'authorizing_date_key'}),
        on='authorizing_date_key', how='left'
    )

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(
        dim_emp_df[['employee_id', 'employee_key']],
        on='employee_id', how='left'
    ).drop(columns=['employee_id'])

    # authorizer_id → authorizer_key (same dim_employee different role)
    dim_auth_df = dims['authorizer_id']['df']
    df = df.merge(
        dim_auth_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'authorizer_id',
            'employee_key': 'authorizer_key'
        }),
        on='authorizer_id', how='left'
    ).drop(columns=['authorizer_id'])

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df']
    df = df.merge(
        dim_vendor_df[['vendor_id', 'vendor_key']],
        on='vendor_id', how='left'
    ).drop(columns=['vendor_id'])

    # currency_no → currency_key
    dim_currency_df = dims['currency_no']['df']
    df = df.merge(
        dim_currency_df[['currency_no', 'currency_key']],
        on='currency_no', how='left'
    ).drop(columns=['currency_no'])

    # department_id → department_key
    dim_dept_df = dims['department_id']['df']
    df = df.merge(
        dim_dept_df[['department_id', 'department_key']],
        on='department_id', how='left'
    ).drop(columns=['department_id'])

    # final column alignment
    fact_columns = [
        'expense_date_key',
        'authorizing_date_key',
        'employee_key',
        'authorizer_key',
        'vendor_key',
        'currency_key',
        'department_key',
        'expense_no',
        'reference',
        'payment_method',
        'tax_option',
        'authorizing_status',
        'is_paid',
        'quantity',
        'unit_price',
        'discount',
        'tax_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    df['quantity'] = df['quantity'].astype('Int64')
    return df

def transform_fact_lead_activity(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # activity_date_key → validate against dim_date
    dim_date_df = dims['activity_date_key']['df']
    df = df.merge(
        dim_date_df[['date_key']].rename(columns={'date_key': 'activity_date_key'}),
        on='activity_date_key',
        how='left'
    )

    # modified_date_key → same dim_date different role
    dim_mod_date_df = dims['modified_date_key']['df']
    df = df.merge(dim_mod_date_df[['date_key']].rename(columns={'date_key': 'modified_date_key'}), on='modified_date_key', how='left')

    # lead_id → lead_key
    dim_lead_df = dims['lead_id']['df']
    df = df.merge(dim_lead_df[['lead_id', 'lead_key']], on='lead_id',how='left').drop(columns=['lead_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # final column alignment
    fact_columns = [
        'lead_key',
        'employee_key',
        'activity_date_key',
        'modified_date_key',
        'activity_type',
        'status'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_receive_payment(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # payment_date_key → validate against dim_date
    dim_date_df = dims['payment_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'payment_date_key'}), on='payment_date_key', how='left')

    # invoice_no → invoice_key
    dim_invoice_df = dims['invoice_no']['df']
    df = df.merge(dim_invoice_df[['invoice_no', 'invoice_key']], on='invoice_no', how='left').drop(columns=['invoice_no'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    # currency_no → currency_key
    dim_currency_df = dims['currency_no']['df']
    df = df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])

    # final column alignment
    fact_columns = [
        'invoice_key',
        'employee_key',
        'payment_date_key',
        'currency_key',
        'customer_key',
        'payment_no',
        'payment_method',
        'station_id',
        'amount_due',
        'amount_paid',
        'cash_in',
        'cash_change'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_receive_item(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # receive_date_key → validate against dim_date
    dim_date_df = dims['receive_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'receive_date_key'}), on='receive_date_key',how='left')

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df']
    df = df.merge(dim_vendor_df[['vendor_id', 'vendor_key']], on='vendor_id', how='left').drop(columns=['vendor_id'])

    # location_id → location_key
    dim_location_df = dims['location_id']['df']
    df = df.merge(dim_location_df[['location_id', 'location_key']], on='location_id', how='left').drop(columns=['location_id'])

    # currency_no → currency_key
    dim_currency_df = dims['currency_no']['df']
    df = df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])

    # final column alignment
    fact_columns = [
        'item_key',
        'receive_date_key',
        'employee_key',
        'vendor_key',
        'currency_key',
        'location_key',
        'receive_no',
        'reference_no',
        'status',
        'quantity_received',
        'unit_cost',
        'line_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    df['receive_date_key'] = df['receive_date_key'].replace(19000101, -1)
    return df

def transform_fact_purchase_request(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # request_date_key → validate against dim_date
    dim_date_df = dims['request_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'request_date_key'}), on='request_date_key', how='left')

    # required_date_key → same dim_date different role
    dim_req_date_df = dims['required_date_key']['df']
    df = df.merge(dim_req_date_df[['date_key']].rename(columns={'date_key': 'required_date_key'}), on='required_date_key', how='left')
    # approval_date_key → same dim_date different role
    dim_app_date_df = dims['approval_date_key']['df']
# normalize approval_date_key to a clean int64 before merging
    df['approval_date_key'] = pd.to_numeric(df['approval_date_key'], errors='coerce')
    df['approval_date_key'] = df['approval_date_key'].fillna(-1).astype('int64')
    df = df.merge(
        dim_app_date_df[['date_key']].rename(columns={'date_key': 'approval_date_key'}),
        on='approval_date_key', how='left'
    )

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # vendor_id → vendor_key
    dim_vendor_df = dims['vendor_id']['df']
    df = df.merge(dim_vendor_df[['vendor_id', 'vendor_key']], on='vendor_id', how='left').drop(columns=['vendor_id'])

    # approver_id → approver_key (same dim_employee different role)
    dim_approver_df = dims['approver_id']['df']
    df = df.merge(dim_approver_df[['employee_id', 'employee_key']].rename(columns={
            'employee_id':  'approver_id',
            'employee_key': 'approver_key'
        }),
        on='approver_id', how='left'
    ).drop(columns=['approver_id'])

    # currency_no → currency_key
    df['currency_no'] = pd.to_numeric(df['currency_no'], errors='coerce')
    df['currency_no'] = df['currency_no'].fillna(-1).astype('int64')
    dim_currency_df = dims['currency_no']['df']
    df = df.merge(dim_currency_df[['currency_no', 'currency_key']], on='currency_no', how='left').drop(columns=['currency_no'])
    
    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    # final column alignment
    fact_columns = [
        'item_key',
        'request_date_key',
        'required_date_key',
        'employee_key',
        'vendor_key',
        'approval_date_key',
        'approver_key',
        'currency_key',
        'customer_key',
        'purchase_request_no',
        'approval_status',
        'delivery_status',
        'quantity_request',
        'unit_cost',
        'estimated_line_amount',
        'delivering_quantity'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_return_item(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # return_date_key → validate against dim_date
    df['return_date_key'] = pd.to_numeric(df['return_date_key'], errors='coerce')
    df['return_date_key'] = df['return_date_key'].fillna(-1).astype('int64')

    dim_date_df = dims['return_date_key']['df']
    valid_dates = set(dim_date_df['date_key'])

    unresolved_count = (~df['return_date_key'].isin(valid_dates)).sum()
    if unresolved_count > 0:
        print(f"  WARNING: {unresolved_count} unresolved rows in return_date_key → will be replaced with -1")

    df['return_date_key'] = df['return_date_key'].where(
        df['return_date_key'].isin(valid_dates), -1
    )

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    fact_columns = [
        'return_date_key',
        'item_key',
        'employee_key',
        'return_no',
        'reference_no',
        'description',
        'quantity_return',
        'return_amount'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_item_used(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # date_key → validate against dim_date
    dim_date_df = dims['date_key']['df']
    df = df.merge(dim_date_df[['date_key']], on='date_key',how='left')

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # location_id → location_key
    dim_location_df = dims['location_id']['df']
    df = df.merge(dim_location_df[['location_id', 'location_key']], on='location_id', how='left').drop(columns=['location_id'])

    # final column alignment
    fact_columns = [
        'date_key',
        'item_key',
        'employee_key',
        'location_key',
        'description',
        'quantity_used',
        'unit_cost'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_issue_item(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # issue_date_key → validate against dim_date
    dim_date_df = dims['issue_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'issue_date_key'}), on='issue_date_key', how='left')

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id', how='left').drop(columns=['employee_id'])

    # final column alignment
    fact_columns = [
        'item_key',
        'issue_date_key',
        'employee_key',
        'team_name',
        'issue_no',
        'box_no',
        'status',
        'quantity_issued',
        'unit_cost',
        'total_issued_amount',
        'location_name'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_warehouse_request(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # request_date_key → validate against dim_date
    dim_date_df = dims['request_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'request_date_key'}), on='request_date_key', how='left')

    # delivery_date_key → same dim_date different role
    dim_del_date_df = dims['delivery_date_key']['df']
    df = df.merge(dim_del_date_df[['date_key']].rename(columns={'date_key': 'delivery_date_key'}), on='delivery_date_key', how='left')

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # request_employee_id → request_employee_key
    dim_emp_df = dims['request_employee_id']['df']
    df = df.merge(
        dim_emp_df[['employee_id', 'employee_key']].rename(columns={'employee_id':  'request_employee_id', 'employee_key': 'request_employee_key'}),
        on='request_employee_id',
        how='left'
    ).drop(columns=['request_employee_id'])

    # approve_employee_id → approve_employee_key
    dim_emp_df = dims['approve_employee_id']['df']
    df = df.merge(
        dim_emp_df[['employee_id', 'employee_key']].rename(columns={'employee_id':  'approve_employee_id', 'employee_key': 'approve_employee_key'}),
        on='approve_employee_id',
        how='left'
    ).drop(columns=['approve_employee_id'])

    # customer_id → customer_key
    dim_customer_df = dims['customer_id']['df']
    df = df.merge(dim_customer_df[['customer_id', 'customer_key']], on='customer_id', how='left').drop(columns=['customer_id'])

    # location_id → location_key
    dim_location_df = dims['location_id']['df']
    df = df.merge(dim_location_df[['location_id', 'location_key']], on='location_id', how='left').drop(columns=['location_id'])

    # final column alignment
    fact_columns = [
        'item_key',
        'request_date_key',
        'delivery_date_key',
        'request_employee_key',
        'approve_employee_key',
        'customer_key',
        'location_key',
        'request_no',
        'ref_sale_order_no',
        'request_type',
        'status',
        'delivery_status',
        'quantity_request'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df

def transform_fact_item_transfer(raw_df, dims):
    df = raw_df.copy().drop_duplicates()

    # transfer_date_key → validate against dim_date
    dim_date_df = dims['transfer_date_key']['df']
    df = df.merge(dim_date_df[['date_key']].rename(columns={'date_key': 'transfer_date_key'}), on='transfer_date_key', how='left')

    # item_id → item_key
    dim_item_df = dims['item_id']['df']
    df = df.merge(dim_item_df[['item_id', 'item_key']], on='item_id', how='left').drop(columns=['item_id'])

    # employee_id → employee_key
    dim_emp_df = dims['employee_id']['df']
    df = df.merge(dim_emp_df[['employee_id', 'employee_key']], on='employee_id',how='left').drop(columns=['employee_id'])

    # source_location_id → source_location_key
    dim_loc_df = dims['source_location_id']['df']
    df = df.merge(dim_loc_df[['location_id', 'location_key']].rename(columns={'location_id':  'source_location_id', 'location_key': 'source_location_key'}),
        on='source_location_id',
        how='left'
    ).drop(columns=['source_location_id'])

    # dest_location_id → dest_location_key
    dim_loc_df = dims['dest_location_id']['df']
    df = df.merge(dim_loc_df[['location_id', 'location_key']].rename(columns={'location_id':  'dest_location_id', 'location_key': 'dest_location_key'}),
        on='dest_location_id',
        how='left'
    ).drop(columns=['dest_location_id'])

    # final column alignment
    fact_columns = [
        'item_key',
        'transfer_date_key',
        'employee_key',
        'source_location_key',
        'dest_location_key',
        'transfer_no',
        'status',
        'quantity_transfer'
    ]
    df = df[fact_columns]
    df = df.drop_duplicates()
    return df
