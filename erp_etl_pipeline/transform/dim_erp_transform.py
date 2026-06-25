from config.db_config import get_engine
def trans_customer(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"] if row["customer_name"] else "Unknown customer",
            "customer_type": row["customer_type"] if row["customer_type"] else "Unknown Type",
            "contact_name": row["contact_name"] if row["contact_name"] else "Not provided",
            "nationality": row["nationality"] if row["nationality"] else "Unknown",
            "gender": row["gender"] if row["gender"] else "Not provided",
            "age": row.get("age"),
            "region": row["region"] if row["region"] else "Not provided",
            "country": row["country"] if row["country"] else "Not provided"
        })
    return transformed

def trans_vendor(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "vendor_id": row["vendor_id"],
            "company_name": row["company_name"] if row["company_name"] else "Unknown Vendor",
            "contact_position": row["contact_position"] if row["contact_position"] else "Not Provided",
            "region": row["region"] if row["region"] else "Unknown Region",
            "city": row["city"] if row["city"] else "Unknown City",
            "country": row["country"] if row["country"] else "Unknown Country",
            "type_of_business": row["type_of_business"] if row["type_of_business"] else "Unknown",
            "is_active": int(row["is_active"]) if row["is_active"] is not None else 0                         # Already correct — kept as-is
        })
    return transformed
 
 
def trans_quotation_status(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "quotation_id": row["quotation_id"],
            "quotation_status": row["quotation_status"] if row["quotation_status"] else "Unknown",
            "authorizing_status": row["authorizing_status"] if row["authorizing_status"] else "Pending",
            "customer_approval_status": row["customer_approval_status"] if row["customer_approval_status"] else "Pending",
            "quotation_type": row["quotation_type"] if row["quotation_type"] else "Standard",
            "version_label": row["version_label"] if row["version_label"] else "v1",
            "status_description": row["status_description"] if row["status_description"] else "No Description"
        })
    return transformed
 
 
def trans_item(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "item_id": row["item_id"],
            "vendor_name": row["vendor_name"] if row["vendor_name"] else "Unknown Vendor",
            "description_item": row["description_item"] if row["description_item"] else "No Description",
            "brand_name": row["brand_name"] if row["brand_name"] else "Generic / No Brand",
            "category_name": row["category_name"] if row["category_name"] else "Uncategorized",
            "unit_of_measurement": row["unit_of_measurement"] if row["unit_of_measurement"] else "Pcs",
            "unit_of_measurement_level2": row["unit_of_measurement_level2"] if row["unit_of_measurement_level2"] else "N/A",
            "inventory_type": row["inventory_type"] if row["inventory_type"] else "Standard",
            "item_status": row["item_status"] if row["item_status"] else "Active",
            # Fix: use "is not None" to safely handle 0.0 values (falsy but valid)
            "average_cost": round(float(row["average_cost"]), 2) if row["average_cost"] is not None else 0.0,
            "standard_unit_price": round(float(row["standard_unit_price"]), 2) if row["standard_unit_price"] is not None else 0.0,
            "price_level2": round(float(row["price_level2"]), 2) if row["price_level2"] is not None else 0.0,
            "price_level3": round(float(row["price_level3"]), 2) if row["price_level3"] is not None else 0.0,
            "price_level4": round(float(row["price_level4"]), 2) if row["price_level4"] is not None else 0.0,
            "price_level5": round(float(row["price_level5"]), 2) if row["price_level5"] is not None else 0.0
        })
    return transformed
 
 
def trans_location(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "location_id": row["location_id"],
            "location_name": row["location_name"] if row["location_name"] else "Unknown Location",       # Fix: "Unknown location" → "Unknown Location"
            "description": row["description"] if row["description"] else "No Description Provided",   # Fix: "Provide" → "Provided"
            "pos_location": row["pos_location"]
        })
    return transformed

def trans_delivery_status(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "delivery_no": row["delivery_no"],
            "delivery_status": row["delivery_status"] if row["delivery_status"] else "Unknown",
            "authorizing_status": row["authorizing_status"] if row["authorizing_status"] else "Pending",
            "customer_acceptance_status": row["customer_acceptance_status"] if row["customer_acceptance_status"] else "Unknown"
        })
    return transformed
 
 
def trans_currency(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "currency_no": row["currency_no"],
            "currency_code": row["currency_code"] if row["currency_code"] else "Unknown",
            "currency_name": row["currency_name"] if row["currency_name"] else "Unknown",
            "currency_type": row["currency_type"] if row["currency_type"] else "Standard",
            "format_currency": row["format_currency"] if row["format_currency"] else "#,##0.00",
            # is_base_currency comes as FLOAT (1.0 or 0.0) from SQL — keep as float
            "is_base_currency": float(row["is_base_currency"]) if row["is_base_currency"] is not None else 0.0
        })
    return transformed
 
 
def trans_department(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "department_id": row["department_id"],
            "department_name": row["department_name"] if row["department_name"] else "Unknown Department",
            "is_active": row["is_active"] if row["is_active"] else "Unknown",
            "creating_person_id": row["creating_person_id"] if row["creating_person_id"] is not None else None
        })
    return transformed
 
 
def trans_lead(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "lead_id": row["lead_id"],
            "lead_name": row["lead_name"] if row["lead_name"] else "Unknown Lead",
            "lead_type": row["lead_type"] if row["lead_type"] else "Unknown Type",
            "lead_source": row["lead_source"] if row["lead_source"] else "Unknown Source",
            "lead_owner_id": row["lead_owner_id"] if row["lead_owner_id"] is not None else None,
            "lead_stage": row["lead_stage"] if row["lead_stage"] else "Unknown Stage",
            "seriosity": row["seriosity"] if row["seriosity"] else "Unknown",
            # percentage comes with COALESCE(0) in SQL, safe to cast directly
            "percentage": float(row["percentage"]) if row["percentage"] is not None else 0.0,
            "status": row["status"] if row["status"] else "Unknown",
            "contact_name": row["contact_name"] if row["contact_name"] else "Not Provided",
            "contact_phone": row["contact_phone"] if row["contact_phone"] else "Not Provided",
            "competitor": row["competitor"] if row["competitor"] else "None"
        })
    return transformed
 
 
def trans_invoice(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "invoice_no": row["invoice_no"],
            "cashier_id": row["cashier_id"] if row["cashier_id"] else "Unknown",
            "ref_quotation_no": row["ref_quotation_no"] if row["ref_quotation_no"] else "Direct Sale",
            "po_number": row["po_number"] if row["po_number"] else "None",
            "tax_option": row["tax_option"] if row["tax_option"] else "Standard",
            "authorizing_status": row["authorizing_status"] if row["authorizing_status"] else "Pending",
            # BIT fields (1/0) from SQL — cast to int for consistency
            "is_paid": bool(row["is_paid"]) if row["is_paid"] is not None else 0,
            "is_vat_applied": bool(row["is_vat_applied"]) if row["is_vat_applied"] is not None else 0
        })
    return transformed
 
 
def trans_expense_type(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "expense_type_id": row["expense_type_id"],
            "expense_type": row["expense_type"] if row["expense_type"] else "Unknown Title",
            "description": row["description"] if row["description"] else "No Description Provided"
        })
    return transformed
 
 