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
            ("SELECT delivery_no, delivery_status_key FROM dim_delivery_status",     "delivery_no", "delivery_status_key"),
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
        "transform_func": transfrom_fact_sale,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date", "date_key", "date_key"),
            ("SELECT customer_id, customer_key FROM dim_customer", "customer_id", "customer_key"),
            ("SELECT employee_id, employee_key FROM dim_employee", "employee_id", "employee_key"),
            ("SELECT item_id, item_key FROM dim_item", "item_id", "item_key"),
            ("SELECT currency_no, currency_key FROM dim_currency", "currency_no", "currency_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_sale (date_key, customer_key, employee_key, item_key, currency_key, sale_order_no, quantity, unit_price, discount, line_amount)
            VALUES (:date_key, :customer_key, :employee_key, :item_key, :currency_key, :sale_order_no, :quantity, :unit_price, :discount, :line_amount)
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_purchase",
        "extract_query": EXTRACT_FACT_PURCHASE_QUERY,
        "transform_func": transform_fact_purchase,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date", "date_key", "date_key"),
            ("SELECT item_id, item_key FROM dim_item", "item_id", "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee", "employee_id", "employee_key"),
            ("SELECT vendor_id, vendor_key FROM dim_vendor", "vendor_id", "vendor_key"),
            ("SELECT customer_id, customer_key FROM dim_customer", "customer_id", "customer_key"),
            ("SELECT currency_no, currency_key FROM dim_currency", "currency_no", "currency_key")
        ],
        "insert_query": """
            INSERT INTO public.fact_purchase (date_key, item_key, employee_key, vendor_key, customer_key, currency_key, purchase_order_no, purchase_status, approval_status, quantity, unit_cost, total_amount)
            VALUES (:date_key, :item_key, :employee_key, :vendor_key, :customer_key, :currency_key, :purchase_order_no, :purchase_status, :approval_status, :quantity, :unit_cost, :total_amount)
            ON CONFLict NOTHING;
        """
    },
    {
        "target_table": "public.fact_inventory",
        "extract_query": EXTRACT_Fact_Inventory_QUERY,
        "transform_func": transform_fact_inventory,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date", "date_key", "date_key"),
            ("SELECT item_id, item_key FROM dim_item", "item_id", "item_key"),
            ("SELECT location_id, location_key FROM dim_location", "location_id", "location_key"),
            ("SELECT vendor_id, vendor_key FROM dim_vendor", "vendor_id", "vendor_key")
        ],
        "insert_query": """
            INSERT INTO public.fact_inventory (
                date_key, item_key, location_key,
                vendor_key, units_in_stock_snap
            )
            VALUES (
                :date_key, :item_key, :location_key,
                :vendor_key, :units_in_stock_snap
            )
            ON CONFLICT NOTHING;
        """
    },

    {
        "target_table": "public.fact_quotation",
        "extract_query": EXTRACT_FACT_QUOTATION_QUERY,
        "transform_func": transform_fact_quotation,
        "dim_lookups": [
            # date keys
            ("SELECT date_key FROM dim_date", "date_key", "date_key"),
            ("SELECT date_key FROM dim_date", "authorizing_date_key", "authorizing_date_key"),

            # customer
            ("SELECT customer_id, customer_key FROM dim_customer", "customer_id", "customer_key"),

            # item
            ("SELECT item_id, item_key FROM dim_item", "item_id", "item_key"),

            # 3 separate employee lookups
            ("SELECT employee_id, employee_key FROM dim_employee", "preparing_employee_id", "preparing_employee_key"),
            ("SELECT employee_id, employee_key FROM dim_employee", "contacting_employee_id", "contacting_employee_key"),
            ("SELECT employee_id, employee_key FROM dim_employee", "authorizing_employee_id","authorizing_employee_key"),

            # quotation status
            ("SELECT authorizing_status, quotation_status_key FROM dim_quotation_status", "authorizing_status", "quotation_status_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_quotation (
                date_key, authorizing_date_key, customer_key, item_key,
                preparing_employee_key, contacting_employee_key, authorizing_employee_key,
                quotation_status_key, quotation_no, quotation_detail_no,
                quantity, unit_price, discount_amount, gross_amount, net_amount
            )
            VALUES (
                :date_key, :authorizing_date_key, :customer_key, :item_key,
                :preparing_employee_key, :contacting_employee_key, :authorizing_employee_key,
                :quotation_status_key, :quotation_no, :quotation_detail_no,
                :quantity, :unit_price, :discount_amount, :gross_amount, :net_amount
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_invoice",
        "extract_query": EXTRACT_FACT_INVOICE_QUERY,
        "transform_func": transform_fact_invoice,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "invoice_date_key",         "invoice_date_key"),
            ("SELECT date_key FROM dim_date",                          "due_date_key",             "due_date_key"),
            ("SELECT customer_id, customer_key FROM dim_customer",     "customer_id",              "customer_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",                  "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "cashier_employee_id",      "cashier_employee_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "salesperson_employee_id",  "salesperson_employee_key"),
            ("SELECT location_id, location_key FROM dim_location",     "location_id",              "location_key"),
            ("SELECT currency_no, currency_key FROM dim_currency",     "currency_no",              "currency_key"),
            ("SELECT invoice_id, invoice_key FROM dim_invoice",        "invoice_id",               "invoice_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_invoice (
                invoice_date_key, due_date_key,
                customer_key, item_key,
                cashier_employee_key, salesperson_employee_key,
                location_key, currency_key, invoice_key,
                quantity_billed, unit_price, discount_amount,
                unit_tax_amount, gross_revenue,
                net_tax_amount, net_revenue
            )
            VALUES (
                :invoice_date_key, :due_date_key,
                :customer_key, :item_key,
                :cashier_employee_key, :salesperson_employee_key,
                :location_key, :currency_key, :invoice_key,
                :quantity_billed, :unit_price, :discount_amount,
                :unit_tax_amount, :gross_revenue,
                :net_tax_amount, :net_revenue
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_expense",
        "extract_query": EXTRACT_FACT_EXPENSE_QUERY,
        "transform_func": transform_fact_expense,
        "dim_lookups": [
            # date keys
            ("SELECT date_key FROM dim_date",                          "expense_date_key",      "expense_date_key"),
            ("SELECT date_key FROM dim_date",                          "authorizing_date_key",  "authorizing_date_key"),

            # employee (2 roles from same dim)
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",           "employee_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "authorizer_id",         "authorizer_key"),

            # vendor
            ("SELECT vendor_id, vendor_key FROM dim_vendor",           "vendor_id",             "vendor_key"),

            # currency
            ("SELECT currency_no, currency_key FROM dim_currency",     "currency_no",           "currency_key"),

            # department
            ("SELECT department_id, department_key FROM dim_department","department_id",         "department_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_expense (
                expense_date_key, authorizing_date_key,
                employee_key, authorizer_key,
                vendor_key, currency_key, department_key,
                expense_no, reference, payment_method,
                tax_option, authorizing_status, is_paid,
                quantity, unit_price, discount, tax_amount
            )
            VALUES (
                :expense_date_key, :authorizing_date_key,
                :employee_key, :authorizer_key,
                :vendor_key, :currency_key, :department_key,
                :expense_no, :reference, :payment_method,
                :tax_option, :authorizing_status, :is_paid,
                :quantity, :unit_price, :discount, :tax_amount
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_lead_activity",
        "extract_query": EXTRACT_FACT_LEAD_ACTIVITY_QUERY,
        "transform_func": transform_fact_lead_activity,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                      "activity_date_key", "activity_date_key"),
            ("SELECT date_key FROM dim_date",                      "modified_date_key", "modified_date_key"),
            ("SELECT lead_no, lead_key FROM dim_lead",             "lead_no",           "lead_key"),
            ("SELECT employee_id, employee_key FROM dim_employee", "employee_id",       "employee_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_lead_activity (
                lead_key, employee_key,
                activity_date_key, modified_date_key,
                activity_type, status
            )
            VALUES (
                :lead_key, :employee_key,
                :activity_date_key, :modified_date_key,
                :activity_type, :status
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_receive_payment",
        "extract_query": EXTRACT_FACT_RECEIVE_PAYMENT_QUERY,
        "transform_func": transform_fact_receive_payment,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "payment_date_key", "payment_date_key"),
            ("SELECT invoice_id, invoice_key FROM dim_invoice",        "invoice_id",       "invoice_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",      "employee_key"),
            ("SELECT customer_id, customer_key FROM dim_customer",     "customer_id",      "customer_key"),
            ("SELECT currency_no, currency_key FROM dim_currency",     "currency_no",      "currency_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_receive_payment (
                invoice_key, employee_key, payment_date_key,
                currency_key, customer_key,
                payment_no, payment_method, station_id,
                amount_due, amount_paid, cash_in, cash_change
            )
            VALUES (
                :invoice_key, :employee_key, :payment_date_key,
                :currency_key, :customer_key,
                :payment_no, :payment_method, :station_id,
                :amount_due, :amount_paid, :cash_in, :cash_change
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_receive_item",
        "extract_query": EXTRACT_FACT_RECEIVE_ITEM_QUERY,
        "transform_func": transform_fact_receive_item,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "receive_date_key", "receive_date_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",          "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",      "employee_key"),
            ("SELECT vendor_id, vendor_key FROM dim_vendor",           "vendor_id",        "vendor_key"),
            ("SELECT location_id, location_key FROM dim_location",     "location_id",      "location_key"),
            ("SELECT currency_no, currency_key FROM dim_currency",     "currency_no",      "currency_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_receive_item (
                item_key, receive_date_key, employee_key,
                vendor_key, currency_key, location_key,
                receive_no, reference_no, status,
                quantity_received, unit_cost, line_amount
            )
            VALUES (
                :item_key, :receive_date_key, :employee_key,
                :vendor_key, :currency_key, :location_key,
                :receive_no, :reference_no, :status,
                :quantity_received, :unit_cost, :line_amount
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_purchase_request",
        "extract_query": EXTRACT_FACT_PURCHASE_REQUEST_QUERY,
        "transform_func": transform_fact_purchase_request,
        "dim_lookups": [
            # date keys
            ("SELECT date_key FROM dim_date",                           "request_date_key",  "request_date_key"),
            ("SELECT date_key FROM dim_date",                           "required_date_key", "required_date_key"),
            ("SELECT date_key FROM dim_date",                           "approval_date_key", "approval_date_key"),

            # dimensions
            ("SELECT item_id, item_key FROM dim_item",                  "item_id",           "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",      "employee_id",       "employee_key"),
            ("SELECT vendor_id, vendor_key FROM dim_vendor",            "vendor_id",         "vendor_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",      "approver_id",       "approver_key"),
            ("SELECT currency_no, currency_key FROM dim_currency",      "currency_no",       "currency_key"),
            ("SELECT customer_id, customer_key FROM dim_customer",      "customer_id",       "customer_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_purchase_request (
                item_key, request_date_key, required_date_key,
                employee_key, vendor_key, approval_date_key,
                approver_key, currency_key, customer_key,
                purchase_request_no, approval_status, delivery_status,
                quantity_request, unit_cost,
                estimated_line_amount, delivering_quantity
            )
            VALUES (
                :item_key, :request_date_key, :required_date_key,
                :employee_key, :vendor_key, :approval_date_key,
                :approver_key, :currency_key, :customer_key,
                :purchase_request_no, :approval_status, :delivery_status,
                :quantity_request, :unit_cost,
                :estimated_line_amount, :delivering_quantity
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_return_item",
        "extract_query": EXTRACT_FACT_RETURN_ITEM_QUERY,
        "transform_func": transform_fact_return_item,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "return_date_key", "return_date_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",         "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",     "employee_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_return_item (
                return_date_key, item_key, employee_key,
                return_no, reference_no, description,
                quantity_return, return_amount
            )
            VALUES (
                :return_date_key, :item_key, :employee_key,
                :return_no, :reference_no, :description,
                :quantity_return, :return_amount
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_item_used",
        "extract_query": EXTRACT_FACT_ITEM_USED_QUERY,
        "transform_func": transform_fact_item_used,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "date_key",    "date_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",     "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id", "employee_key"),
            ("SELECT location_id, location_key FROM dim_location",     "location_id", "location_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_item_used (
                date_key, item_key, employee_key, location_key,
                description, quantity_used, unit_cost
            )
            VALUES (
                :date_key, :item_key, :employee_key, :location_key,
                :description, :quantity_used, :unit_cost
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_issue_item",
        "extract_query": EXTRACT_FACT_ISSUE_ITEM_QUERY,
        "transform_func": transform_fact_issue_item,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "issue_date_key", "issue_date_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",        "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",    "employee_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_issue_item (
                item_key, issue_date_key, employee_key,
                team_name, issue_no, box_no, status,
                quantity_issued, unit_cost, total_issued_amount, location_name
            )
            VALUES (
                :item_key, :issue_date_key, :employee_key,
                :team_name, :issue_no, :box_no, :status,
                :quantity_issued, :unit_cost, :total_issued_amount, :location_name
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_warehouse_request",
        "extract_query": EXTRACT_FACT_WAREHOUSE_REQUEST_QUERY,
        "transform_func": transform_fact_warehouse_request,
        "dim_lookups": [
            # date keys
            ("SELECT date_key FROM dim_date",                           "request_date_key",     "request_date_key"),
            ("SELECT date_key FROM dim_date",                           "delivery_date_key",    "delivery_date_key"),

            # dimensions
            ("SELECT item_id, item_key FROM dim_item",                  "item_id",              "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",      "request_employee_id",  "request_employee_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",      "approve_employee_id",  "approve_employee_key"),
            ("SELECT customer_id, customer_key FROM dim_customer",      "customer_id",          "customer_key"),
            ("SELECT location_id, location_key FROM dim_location",      "location_id",          "location_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_warehouse_request (
                item_key, request_date_key, delivery_date_key,
                request_employee_key, approve_employee_key,
                customer_key, location_key,
                request_no, ref_sale_order_no,
                request_type, status, delivery_status,
                quantity_request
            )
            VALUES (
                :item_key, :request_date_key, :delivery_date_key,
                :request_employee_key, :approve_employee_key,
                :customer_key, :location_key,
                :request_no, :ref_sale_order_no,
                :request_type, :status, :delivery_status,
                :quantity_request
            )
            ON CONFLICT NOTHING;
        """
    },
    {
        "target_table": "public.fact_item_transfer",
        "extract_query": EXTRACT_FACT_ITEM_TRANSFER_QUERY,
        "transform_func": transform_fact_item_transfer,
        "dim_lookups": [
            ("SELECT date_key FROM dim_date",                          "transfer_date_key",  "transfer_date_key"),
            ("SELECT item_id, item_key FROM dim_item",                 "item_id",            "item_key"),
            ("SELECT employee_id, employee_key FROM dim_employee",     "employee_id",        "employee_key"),
            ("SELECT location_id, location_key FROM dim_location",     "source_location_id", "source_location_key"),
            ("SELECT location_id, location_key FROM dim_location",     "dest_location_id",   "dest_location_key"),
        ],
        "insert_query": """
            INSERT INTO public.fact_item_transfer (
                item_key, transfer_date_key, employee_key,
                source_location_key, dest_location_key,
                transfer_no, status,
                quantity_transfer
            )
            VALUES (
                :item_key, :transfer_date_key, :employee_key,
                :source_location_key, :dest_location_key,
                :transfer_no, :status,
                :quantity_transfer
            )
            ON CONFLICT NOTHING;
        """
    }
]