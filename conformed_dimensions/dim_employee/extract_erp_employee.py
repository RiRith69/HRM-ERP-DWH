EXTRACT_ERP_EMPLOYEE_QUERY = """
    SELECT 
        TRIM(CAST(ts.StaffID AS VARCHAR(50))) AS staff_id,
        ts.Name as name,
        ts.Gender as gender,
        'Cambodian' AS nationality,                          
        'Single' AS marital_status,
        ts.DOB as birth_date,
        ts.HiringDate as hiring_date,
        NULL AS getting_position_date,                       
        'Undetermined' AS contract_type,                     
        NULL AS contract_end_date,                           
        'ERP Operations' AS site_name,
        NULL AS supervisor_id,                               
        NULL AS supervisor_key,
        'Unknown' as is_active,
        tp.[Position] as position_name,
        CAST(tp.[Level] AS VARCHAR(50)) AS position_level,
        'Unknown' as team_name,
        'Unknown' as team_description,
        NULL AS education,                                   
        NULL AS school,                                      
        NULL AS previous_position,                           
        NULL AS changing_position,                           
        NULL AS resign_request_date,                         
        NULL AS resign_leave_date,                           
        NULL AS approve_by,
        'ERP' AS source_system
    FROM tblStaff ts
    LEFT JOIN tblPosition tp on ts.PositionNo = tp.PositionNo;
"""