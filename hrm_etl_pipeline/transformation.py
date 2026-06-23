# transformations.py

def clean_shift(raw_records):
    """Cleans raw shift data records from SQL Server."""
    transformed = []
    for row in raw_records:
        transformed.append({
            "shift_id": row["shift_id"],
            "shift_name": row["shift_name"].strip() if row["shift_name"] else "Standard Shift",
            "start_time": row["start_time"],
            "end_time": row["end_time"],
            "work_minutes": row["work_minutes"],
            "late_minutes": row["late_minutes"],
            "early_minutes": row["early_minutes"]
        })
    return transformed

def trans_position(raw_records):
    """Cleans raw position records from SQL Server."""
    transformed = []
    for row in raw_records:
        transformed.append({
            "level_no": str(row["level_no"]).strip(),
            "position_name": row["position_name"].strip() if row["position_name"] else "Unknown Position",
            "rank_name": row["rank_name"].strip() if row["rank_name"] else "General"
        })
    return transformed

def trans_payroll_component(raw_records):
    """Cleans raw payroll components from SQL Server."""
    transformed = []
    for row in raw_records:
        transformed.append({
            "component_id": row["component_id"],
            "component_name": row["component_name"].strip() if row["component_name"] else "Generic Component",
            "component_type": row["component_type"].strip() if row["component_type"] else "Allowance"
        })
    return transformed 

def trans_applicant(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "applicant_id": row["applicant_id"],
            "applicant_name": row["applicant_name"].strip() if row["applicant_name"] else "Unknown applicant name",
            "gender": row["gender"],
            "nationality": row["nationality"].strip() if row["nationality"] else "Unknown nationality",
            "marital_status": row["marital_status"].strip() if row["marital_status"] else "Single",
            "education_level": row["education_level"].strip() if row["education_level"] else "Bachelor Degree",
            "birth_date": row["birth_date"]
        })
    return transformed

def trans_asset(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "asset_id": row["asset_id"],
            "asset_code": row["asset_code"].strip() if row["asset_code"] else "Unknown Code",
            "asset_name": row["asset_name"].strip() if row["asset_name"] else "Unknown Asset Name",
            "asset_type": row["asset_type"].strip() if row["asset_type"] else "Unknown asset type",
            "asset_make": row["asset_make"].strip() if row["asset_make"] else "Unknown asset make",
            "asset_group": row["asset_group"].strip() if row["asset_group"] else "Unknown asset group",
            "model_number": row["model_number"].strip() if row["model_number"] else "Unknown model number",
            "serial_number": row["serial_number"].strip() if row["serial_number"] else "Unknown serial number",
            "asset_status": row["asset_status"].strip() if row["asset_status"] else "Unknown asset status"
        })
    return trans_asset
def trans_asset_location(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "asset_location_id": row["asset_location_id"],
            "location_name": row["location_name"].strip() if row["location_name"] else "Unknown location",
            "location_type": row["location_type"].strip() if row["location_type"] else "Unknown"
        })
    return transformed

def trans_asset_transaction_type(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Cleans up any accidental spaces from string conversion or concatenation
            "asset_transaction_type_id": str(row["asset_transaction_type_id"]).strip(),
            "asset_transaction_type_name": row["asset_transaction_type_name"].strip() if row["asset_transaction_type_name"] else "Unknown Type",
            "transaction_category": row["transaction_category"].strip() if row["transaction_category"] else "Uncategorized"
        })
    return transformed

def trans_kpi(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "indicator_id": row["indicator_id"],
            "kpi_name": row["kpi_name"].strip() if row["kpi_name"] else "Unknown",
            "kpi_category": row["kpi_category"].strip() if row["kpi_category"] else "Unknown Category",
            "kpi_period": row["kpi_period"].strip() if row["kpi_period"] else "Unknown",
            "kpi_direction": row["kpi_direction"].strip() if row["kpi_direction"] else "Unknown",
            "kpi_formula": row["kpi_formula"].strip() if row["kpi_formula"] else "No formula provide"
        })
    return transformed

def trans_leave_type(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Standardizing the ID to a clean string format
            "leave_id": str(row["leave_id"]).strip() if row["leave_id"] else None,
            # Cleaning the descriptive text fields
            "leave_name": row["leave_name"].strip() if row["leave_name"] else "Unknown Leave Type",
            # Report symbol (e.g., 'AL' for Annual Leave, 'SL' for Sick Leave)
            "report_symbol": str(row["report_symbol"]).strip() if row["report_symbol"] else "-",
            # Color hex code or name used for calendar dashboards (e.g., '#FF0000' or 'Red')
            "color_code": str(row["color_code"]).strip() if row["color_code"] else "#FFFFFF",
            # Unit type (e.g., 'Days', 'Hours')
            "unit_type": row["unit_type"].strip() if row["unit_type"] else "Days"
        })
    return transformed
def trans_organization(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "organization_id": str(row["organization_id"]).strip() if row["organization_id"] else None,
            
            # Cleaning organization/department descriptive names
            "organization_name": row["organization_name"].strip() if row["organization_name"] else "Unknown Unit",
            
            "level_no": int(row["level_no"]) if row["level_no"] is not None else 0,
            
            "parent_id": str(row["parent_id"]).strip() if row["parent_id"] else None,
            "department_name": row["department_name"] if row["department_name"] else "No Department"
        })
    return transformed
def trans_workflow(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Base Workflow Details
            "workflow_id": str(row["workflow_id"]).strip() if row["workflow_id"] else None,
            "workflow_code": str(row["workflow_code"]).strip() if row["workflow_code"] else "UNKNOWN",
            "workflow_name": row["workflow_name"].strip() if row["workflow_name"] else "Unknown Workflow",
            "module_name": row["module_name"].strip() if row["module_name"] else "General System",
            
            # Workflow Step Details
            "step_order": int(row["step_order"]) if row["step_order"] is not None else 0,
            "step_name": row["step_name"].strip() if row["step_name"] else f"Step {row['step_order']}",
            "approval_type": row["approval_type"].strip() if row["approval_type"] else "Standard",
            "approver_type": row["approver_type"].strip() if row["approver_type"] else "Manager",
            "role_code": str(row["role_code"]).strip() if row["role_code"] else "DEFAULT_ROLE",
            
            # Numeric SLA Hours Metric
            "sla_hours": float(row["sla_hours"]) if row["sla_hours"] is not None else 0.0,
            
            # Convert the integer flag (0/1) from your SQL CAST to a clean Python Boolean (True/False)
            "is_mandatory": True if row["is_mandatory"] == 1 else False
        })
    return transformed
def trans_absence_permission(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            "permission_id": str(row["permission_id"]).strip(),
            "request_type_name": row["request_type_name"].strip() if row["request_type_name"] else "UNKNOWN",
            "reason_description": row["reason_description"].strip() if row["reason_description"] else "No Reason Provided",
            "approval_status": row["approval_status"].strip() if row["approval_status"] else "Rejected",
            
            # Ensures it treats 1 as True and 0 as False for a PostgreSQL BOOLEAN target column
            "is_paid_leave": True if row["is_paid_leave"] == 1 else False,
            
            "leave_duration_type": row["leave_duration_type"].strip() if row["leave_duration_type"] else "Hourly",
            "approving_person": row["approving_person"].strip() if row["approving_person"] else "System Auto-Approved"
        })
    return transformed

def trans_interview_stage(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Base Interview Core Details
            "interview_id": str(row["interview_id"]).strip() if row["interview_id"] else None,
            "interview_round": int(row["interview_round"]) if row["interview_round"] is not None else 1,
            "interview_type": row["interview_type"].strip() if row["interview_type"] else "Technical",
            "interview_mode": row["interview_mode"].strip() if row["interview_mode"] else "Online",
            
            # Panel & Feedback Flattened Attributes
            "panel_role": row["panel_role"].strip() if row["panel_role"] else "Interviewer",
            "stage_recommendation": row["stage_recommendation"].strip() if row["stage_recommendation"] else "Pending"
        })
    return transformed

def trans_benefit_profile(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Standardizing IDs to strings
            "benefit_profile_no": str(row["benefit_profile_no"]).strip() if row["benefit_profile_no"] else None,
            "benefit_profile_name": row["benefit_profile_name"].strip() if row["benefit_profile_name"] else "Standard Package",
            "benefit_name": row["benefit_name"].strip() if row["benefit_name"] else "General Benefit",
            "payout_frequency": row["payout_frequency"].strip() if row["payout_frequency"] else "As-Needed",
            
            # Ensuring numeric amount is cast cleanly to a float for decimal columns
            "amount": float(row["amount"]) if row["amount"] is not None else 0.0
        })
    return transformed


def trans_working_profile(raw_records):
    transformed = []
    for row in raw_records:
        transformed.append({
            # Base Profile Configurations
            "working_profile_id": str(row["working_profile_id"]).strip() if row["working_profile_id"] else None,
            "shift_name": row["shift_name"].strip() if row["shift_name"] else "Standard Shift",
            "roster_type": row["roster_type"].strip() if row["roster_type"] else "Fixed",
            "schedule_name": row["schedule_name"].strip() if row["schedule_name"] else "Not Assigned",
            
            # Schedule Line Details
            "working_day_name": row["working_day_name"].strip() if row["working_day_name"] else "Unknown Day",
            
            # Handle Time values cleanly (keep as string or pass None if missing)
            "from_time1": str(row["from_time1"]) if row["from_time1"] else None,
            "to_time1": str(row["to_time1"]) if row["to_time1"] else None,
            "from_time2": str(row["from_time2"]) if row["from_time2"] else None,
            "to_time2": str(row["to_time2"]) if row["to_time2"] else None
        })
    return transformed