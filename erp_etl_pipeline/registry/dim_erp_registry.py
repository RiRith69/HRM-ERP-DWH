from erp_etl_pipeline.extract.erp_extract import *
from erp_etl_pipeline.transform.dim_erp_transform import *
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
    },
    {
        "target_table": "public.dim_vendor",
        "extract_query": EXTRACT_vendor_QUERY,
        "transform_func": trans_vendor,
        "insert_query": """
            INSERT INTO public.dim_vendor (vendor_id, company_name, contact_position, region, city, country, type_of_business, is_active)
            VALUES (:vendor_id, :company_name, :contact_position, :region, :city, :country, :type_of_business, :is_active)
            ON CONFLICT (vendor_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_quotation_status",
        "extract_query": EXTRACT_quotation_status_QUERY,
        "transform_func": trans_quotation_status,
        "insert_query": """
            INSERT INTO public.dim_quotation_status (quotation_id, quotation_status, authorizing_status, customer_approval_status, quotation_type, version_label, status_description)
            VALUES (:quotation_id, :quotation_status, :authorizing_status, :customer_approval_status, :quotation_type, :version_label, :status_description)
            ON CONFLICT (quotation_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_item",
        "extract_query": EXTRACT_item_QUERY,
        "transform_func": trans_item,
        "insert_query": """
            INSERT INTO public.dim_item (item_id, vendor_name, description, brand_name, category_name, unit_of_measurement, unit_of_measurement_level2, inventory_type, item_status, average_cost, standard_unit_price, price_level2, price_level3, price_level4, price_level5)
            VALUES (:item_id, :vendor_name, :description, :brand_name, :category_name, :unit_of_measurement, :unit_of_measurement_level2, :inventory_type, :item_status, :average_cost, :standard_unit_price, :price_level2, :price_level3, :price_level4, :price_level5)
            ON CONFLICT (item_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_location",
        "extract_query": EXTRACT_DIM_LOCATION_QUERY,
        "transform_func": trans_location,
        "insert_query": """
            INSERT INTO public.dim_locations (location_id, location_name, description)
            VALUES (:location_id, :location_name, :description)
            ON CONFLICT (location_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_delivery_status",
        "extract_query": EXTRACT_Delivery_Status_QUERY,
        "transform_func": trans_delivery_status,
        "insert_query": """
            INSERT INTO public.dim_delivery_status (delivery_no, delivery_status, authorizing_status, customer_acceptance_status)
            VALUES (:delivery_no, :delivery_status, :authorizing_status, :customer_acceptance_status)
            ON CONFLICT (delivery_no) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_currency",
        "extract_query": EXTRACT_DIM_CURRENCY_QUERY,
        "transform_func": trans_currency,
        "insert_query": """
            INSERT INTO public.dim_currency (currency_no, currency_code, currency_name, currency_type, format_currency, is_base_currency)
            VALUES (:currency_no, :currency_code, :currency_name, :currency_type, :format_currency, :is_base_currency)
            ON CONFLICT (currency_no) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_department",
        "extract_query": EXTRACT_DIM_DEPARTMENT_QUERY,
        "transform_func":trans_department,
        "insert_query": """
            INSERT INTO public.dim_currency (department_id, department_name, is_active, creating_person_id)
            VALUES (:department_id, :department_name, :is_active, :creating_person_id)
            ON CONFLICT (department_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_lead",
        "extract_query": EXTRACT_DIM_LEAD_QUERY,
        "transform_func":trans_lead,
        "insert_query": """
            INSERT INTO public.dim_lead (lead_id, lead_name, lead_type, lead_source, lead_owner_id, lead_stage, seriosity, percentage, status, contact_name, contact_phone, competitor)
            VALUES (:lead_id, :lead_name, :lead_type, :lead_source, :lead_owner_id, :lead_stage, :seriosity, :percentage, :status, :contact_name, :contact_phone, :competitor)
            ON CONFLICT (lead_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_invoice",
        "extract_query": EXTRACT_DIM_INVOICE_QUERY,
        "transform_func":trans_invoice,
        "insert_query": """
            INSERT INTO public.dim_invoice (invoice_no, cashier_id, ref_quotation_no, po_number, tax_option, authorizing_status, is_paid, is_vat_applied)
            VALUES (:invoice_no, :cashier_id, :ref_quotation_no, :po_number, :tax_option, :authorizing_status, :is_paid, :is_vat_applied)
            ON CONFLICT (invoice_no) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_expense_type",
        "extract_query": EXTRACT_DIM_EXPENSE_TYPE_QUERY,
        "transform_func":trans_expense_type,
        "insert_query": """
            INSERT INTO public.dim_expense_type (expense_type_id, expense_type, description)
            VALUES (:expense_type_id, :expense_type, :description)
            ON CONFLICT (expense_type_id) DO NOTHING;
        """
    },

]