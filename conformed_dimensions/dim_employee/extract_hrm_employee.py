EXTRACT_HRM_EMPLOYEE_QUERY = """
    SELECT 
        TRIM(CAST(ts.StaffID AS VARCHAR(50))) AS staff_id,
        COALESCE(TRIM(ts.Name), 'Unknown Employee') AS name,
        TRIM(ts.Gender) as gender,
        COALESCE(TRIM(ts.Nationality), 'Cambodian') AS nationality,
        COALESCE(TRIM(ts.MaritalStatus), 'Single') AS marital_status,
        CAST(ts.BirthDate AS DATE) AS birth_date,
        CAST(ts.HiringDate AS DATE) AS hiring_date,
        ts.GettingPositionDate as getting_position_date,
        COALESCE(TRIM(tct.ContractType), 'Undetermined') AS contract_type,
        CAST(ts.ContractEndDate AS DATE) AS contract_end_date,
        tsi.SiteName as site_name,
        ts.SupervisorID as supervisor_id,
        NULL as supervisor_key,
        ts.IsActive as is_active,
        COALESCE(TRIM(tpl.PositionName), 'Unmapped Position') AS position_name,
        CAST(TRIM(tpl.LevelType) AS varchar(50)) AS position_level,
        'Unknown Team' AS team_name,
        'No Description Available' AS team_description,
        TRIM(ts.Education) AS education,
        TRIM(tse.School) AS school,
        TRIM(tpp.PreviousPosition) AS previous_position,      
        TRIM(tpp.ChangingPosition) AS changing_position,
        tsr.RequestDate as resign_request_date,
        tsr.LeaveDate as resign_leave_date,
        tsr.ApprovedBy as approve_by,
        'HRM' AS source_system
    FROM dbo.tblStaff ts
    LEFT JOIN tblContractType tct ON TRIM(CAST(ts.ContractTypeNo AS VARCHAR(50))) = TRIM(CAST(tct.[No] AS VARCHAR(50)))
    LEFT JOIN tblPositionList tpl ON TRIM(CAST(ts.[Position] AS VARCHAR(50))) = TRIM(CAST(tpl.LevelNo AS VARCHAR(50)))
    LEFT JOIN tblStaffEducation tse ON TRIM(CAST(ts.StaffID AS VARCHAR(50))) = TRIM(CAST(tse.StaffID AS VARCHAR(50)))
    LEFT JOIN tblPositionPromotion tpp ON TRIM(CAST(ts.StaffID AS VARCHAR(50))) = TRIM(CAST(tpp.StaffID AS VARCHAR(50)))
    LEFT JOIN tblSite tsi ON TRIM(CAST(ts.SiteID AS VARCHAR(50))) = TRIM(CAST(tsi.SiteID AS VARCHAR(50)))
    LEFT JOIN tblStaffResign tsr ON TRIM(CAST(ts.StaffID AS VARCHAR(50))) = TRIM(CAST(tsr.StaffID AS VARCHAR(50)))
    WHERE ts.StaffID IS NOT NULL;

"""