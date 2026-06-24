EXTRACT_EMPLOYEE_QUERY = """
SELECT 
    ts.StaffID AS employee_id,
    ts.Name AS name,
    ts.Gender AS gender,
    ts.Nationality AS nationality,
    ts.MaritalStatus AS marital_status,
    CAST(e.BirthDate AS DATE) AS birth_date,
    CAST(e.HiringDate AS DATE) AS hiring_date,
    e.ContractNumber AS contact_type_no,            
    CAST(e.ContractEndDate AS DATE) AS contract_end_date,
    e.BranchID AS site_id,                   
FROM hrm_tblEmployee e
LEFT JOIN hrm_tblPosition p ON e.PositionID = p.PositionID;
"""