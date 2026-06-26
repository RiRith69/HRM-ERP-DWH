import pandas as pd
import math

def trans_employee(raw_records):
    transformed = []
    for row in raw_records:

        # helper to safely convert to int
        def safe_int(val):
            try:
                if val is None:
                    return None
                if isinstance(val, float) and math.isnan(val):
                    return None
                return int(val)
            except (ValueError, TypeError):
                return None

        transformed.append({
            "employee_id":              str(row["employee_id"]).strip() if row["employee_id"] else None,
            "name":                     row["name"]             if row["name"]             else "Unknown",
            "gender":                   row["gender"]           if row["gender"]           else "Unknown",
            "nationality":              row["nationality"]      if row["nationality"]      else None,
            "marital_status":           row["marital_status"]   if row["marital_status"]   else None,
            "birth_date":               row["birth_date"],
            "hiring_date":              row["hiring_date"],
            "getting_position_date":    row["getting_position_date"],
            "contract_type":            row["contract_type"]    if row["contract_type"]    else "Unknown",
            "contract_end_date":        row["contract_end_date"],
            "site_name":                row["site_name"]        if row["site_name"]        else None,
            "supervisor_id":            safe_int(row["supervisor_id"]),  
            "supervisor_key":           None,
            "is_active":                bool(row["is_active"])  if row["is_active"] is not None else False,
            "position_name":            row["position_name"]    if row["position_name"]    else None,
            "position_type":            None,
            "position_level":           safe_int(row["position_level"]), 
            "team_name":                None,
            "team_description":         None,
            "education":                row["education"]        if row["education"]        else None,
            "school":                   row["school"]           if row["school"]           else None,
            "previous_position":        row["previous_position"],
            "changing_position":        row["changing_position"],
            "resign_request_date":      row["resign_request_date"],
            "resign_leave_date":        row["resign_leave_date"],
            "approve_by":               safe_int(row["approve_by"]),     
            "source_system":            row["source_system"],
        })
    return transformed