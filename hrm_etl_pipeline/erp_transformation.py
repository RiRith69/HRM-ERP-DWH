def trans_customer(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"] if row["customer_name"] else "Unknow customer",
            "customer_type": row["customer_type"] if row["customer_type"] else "Unknown Type",
            "contact_name": row["contact_name"] if row["contact_name"] else "Not provide",
            "nationality": row["nationality"] if row["nationality"] else "Unknown",
            "gender": row["gender"] if row["gender"] else "Not provide",
            "age": row.get("age"),
            "region": row["region"] if row["region"] else "Not provide",
            "country": row["country"] if row["country"] else "Not provide"
        })
    return transformed
