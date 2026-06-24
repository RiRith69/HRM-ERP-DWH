EXTRACT_DIM_SHIFT_QUERY = """
    SELECT 
        CAST([No] AS INT) AS shift_id,
        WorkingName as shift_name,
        CAST(StartTime1 AS TIME) AS start_time_1,
        CAST(EndTime1 AS TIME) AS end_time_1,
        CAST(StartTime2 as TIME) AS start_time_2,
        CASR(EndTime2 as TIME) AS end_time_2
    FROM dbo.tblWorkingTime
    WHERE schClassid IS NOT NULL;
"""

EXTRACT_DIM_POSITION_Query = """
    SELECT distinct
        LevelNo as level_no,
        PositionName as position_name,
        LevelType as rank_name
    from dbo.tblPositionList;
"""
#tblPayrollMain
EXTRACT_DIM_PAY_ROLL_COMPONENT_QUERY = """
    SELECT distinct
        ID as component_id,
        Description as component_name,
        [Type] as component_type
    from dbo.tblPayrollDetails
    WHERE [Type] is not null;
"""

EXTRACT_DIM_APPLICANT_Query = """
    SELECT distinct
        ApplicantID as applicant_id,
        Name as applicant_name,
        Gender as gender,
        Nationality as nationality,
        MaritalStatus as marital_status,
        EducationLevel as education_level,
        BirthDate as birth_date
    FROM dbo.tblApplicant;
"""

EXTRACT_DIM_ASSET_QUERY = """
    SELECT DISTINCT
        a.AssetsID AS asset_id,
        a.AssetCode AS asset_code,
        a.AssetsName AS asset_name,
        t.Name AS asset_type,
        m.Name AS asset_make,
        g.AssetGroupName AS asset_group,
        a.ModelNumber AS model_number,
        a.SerialNumber AS serial_number,
        s.Name AS asset_status
    FROM dbo.tblAssets a
    -- Changed these to LEFT JOIN to protect your 26 original records
    LEFT JOIN dbo.tblAssetsType t ON a.AssetTypeID = t.[No]
    LEFT JOIN dbo.tblAssetsMake m ON a.AssetMakeID = m.[No] 
    LEFT JOIN dbo.tblAssetsGroup g ON a.AssetGroupID = g.[AssetGroupNo]
    LEFT JOIN dbo.tblAssetsStatus s ON a.StatusID = s.[No];
"""

EXTRACT_ASSET_LOCATION_QUERY = """
    SELECT distinct
        l.[No] as asset_location_id,
        l.Name as location_name,
        lt.Name as location_type
    FROM dbo.tblAssetsLocation l
    left JOIN dbo.tblAssetsLocationType lt on l.[No] = lt.[No];
"""

# DIM_Asset_Transaction_Type -----------------------------------------------------------
EXTRACT_DIM_ASSET_TRANSACTION_TYPE_QUERY = """
    SELECT 
        CONCAT('DISP-', CAST([No] AS VARCHAR(20))) AS asset_transaction_type_id, 
        COALESCE(TRIM(Name), 'Unknown Disposal') AS asset_transaction_type_name, 
        'Disposal' AS transaction_category
    FROM dbo.tblAssetsDisposalType
    WHERE [No] IS NOT NULL
    UNION ALL
    SELECT 
        CONCAT('MAINT-', CAST([No] AS VARCHAR(20))) AS asset_transaction_type_id, 
        COALESCE(TRIM(Name), 'Unknown Maintenance') AS asset_transaction_type_name, 
        'Maintenance' AS transaction_category FROM dbo.tblAssetsMaintenanceType WHERE [No] IS NOT NULL
    UNION ALL
    SELECT 
        CONCAT('ASTSTAT-', CAST([No] AS VARCHAR(20))) AS asset_transaction_type_id, 
        COALESCE(TRIM(Name), 'Unknown Inventory Status') AS asset_transaction_type_name, 
        'Inventory Status' AS transaction_category 
    FROM dbo.tblAssetsStatus 
    WHERE [No] IS NOT NULL
    UNION ALL
    SELECT 
        CONCAT('EMPSTAT-', CAST([No] AS VARCHAR(20))) AS asset_transaction_type_id, 
        COALESCE(TRIM(Name), 'Unknown Assignment Status') AS asset_transaction_type_name, 
        'Employee Assignment' AS transaction_category 
    FROM dbo.tblAssetsEmployeeStatus 
    WHERE [No] IS NOT NULL;
"""
#KI: KPI Indicator
#KID: KPI Indicatore Detail
#KC: KPI category
EXTRACT_DIM_KPI_QUERY = """
    SELECT 
        ki.IndicatorID as Indicator_id,
        kid.Name as kpi_name,
        kc.CategoryName as kpi_category,
        ki.KPIPeriod as kpi_period,
        ki.KPIDirection as kpi_direction,
        ki.KPIFormulas as kpi_formula
    FROM dbo.tblKPIIndicator ki
    LEFT JOIN dbo.tblKPIIndicatorDetails kid on ki.IndicatorID = kid.IndicatorID
    LEFT JOIN dbo.tblKPICategory kc on try_cast(ki.CategoryNo as int) = kc.[No];
"""
EXTRACT_DIM_LEAVE_TYPE_QUERY = """"
    SELECT distinct
        LeaveId as leave_id,
        LeaveName as leave_name,
        ReportSymbol as report_symbol,
        Color as color_code,
        Unit as unit_type
    FROM dbo.LeaveClass;
"""

EXTRACT_DIM_ORGANIZATION_QUERY = """ 
    SELECT 
        CAST(tor.OrganizationID AS VARCHAR(10))   AS organization_id, 
        COALESCE(TRIM(tor.OrganizationName), 'Unknown Org') AS organization_name,
        TRY_CAST(tor.LevelNo AS INT)              AS level_no,
        CAST(tor.ParentID AS VARCHAR(50))         AS parent_id,
        CAST(td.DepartmentID AS VARCHAR(10))   AS department_id,
        COALESCE(TRIM(td.DepartmentName), 'No Department') AS department_name
    FROM dbo.tblOrganization tor
    LEFT JOIN dbo.tblDepartment td ON tor.OrganizationID = td.OrganizationID;
"""

# Extract query for Dim_Workflow conformed dimension
EXTRACT_DIM_WORKFLOW_QUERY = """
    SELECT DISTINCT
        w.workflow_id,
        w.workflow_code,
        w.workflow_name,
        w.module_name,
        s.step_order,
        s.step_name,
        s.approval_type,
        s.approver_type,
        s.role_code,
        s.sla_hours,
        CAST(s.is_mandatory AS INT) AS is_mandatory -- Converts bit (0/1) to an integer flag
    FROM workflow.approval_workflows w
    INNER JOIN workflow.approval_workflow_steps s 
        ON w.workflow_id = s.workflow_id
    WHERE w.is_active = 1 
      AND s.is_active = 1;
"""

# Extract query for Dim_Absence_Permission conformed dimension
# Highly accurate extraction query matching your exact target DDL
EXTRACT_DIM_ABSENCE_PERMISSION_QUERY = """
    SELECT DISTINCT
        CAST(ap.RequestNo AS VARCHAR(50)) AS permission_id,
        COALESCE(ap.RequestTypeID, 'UNKNOWN') AS request_type_name,
        COALESCE(ap.ReasonDescription, 'No Reason Provided') AS reason_description,
        CASE 
            WHEN ap.Approved = 1 THEN 'Approved'
            WHEN ap.Approved = 0 THEN 'Pending'
            ELSE 'Rejected'
        END AS approval_status,
        -- Maps bit to True/False for your target BOOLEAN column
        CASE 
            WHEN ap.PaidLeave = 1 THEN 1 
            ELSE 0 
        END AS is_paid_leave, 
        CASE 
            WHEN ap.FullDay = 1 THEN 'Full Day'
            WHEN ap.HalfDay = 1 THEN 'Half Day'
            ELSE 'Hourly'
        END AS leave_duration_type,
        COALESCE(ap.ApprovingPersonID, 'System Auto-Approved') AS approving_person
    FROM dbo.tblAbsencePermission ap
    WHERE ap.RequestNo IS NOT NULL;
"""
#It seem like not clear about the interview round that come from phase but what number that phase column hold
EXTRACT_DIM_INTERVIEW_STAGE_QUERY = """
    SELECT DISTINCT 
        i.InterviewID as interview_id,
        i.InterviewRound as interview_round,
        i.InterviewType as interview_type,
        i.InterviewMode as interview_mode,
        ip.[Role] as panel_role,
        if.Recommendation as stage_recommendation
    FROM recruitment.interviews i
    left join recruitment.interview_panels ip on i.InterviewID = ip.InterviewID
    left join recruitment.interview_feedbacks if on i.InterviewID = if.InterviewID;
"""

EXTRACT_DIM_BENEFIT_PROFILE_QUERY = """
    SELECT DISTINCT
        bp.[No] AS benefit_profile_no,
        COALESCE(bp.BenefitProfileName, 'Standard Package') AS benefit_profile_name,
        bpd.BenefitName as benefit_name,
        CASE
            WHEN bpd.DialyBasic = 1 THEN 'Daily'
            WHEN bpd.MonthlyBasic = 1 THEN 'Monthly'
            WHEN bpd.YearlyBasic = 1 THEN 'Annually'
            ELSE 'As-Needed'
        END AS payout_frequency,
        bpd.Amount as amount
    FROM dbo.tblBenefitProfile bp
    JOIN tblBenefitProfileDetails bpd on bp.[No] = bpd.BenefitProfileNo;
"""

# Extraction query combining header and line item detail definitions
EXTRACT_DIM_WORKING_PROFILE_QUERY = """
    SELECT DISTINCT
        CAST(wp.[No] AS VARCHAR(50)) AS working_profile_id,
        COALESCE(TRIM(wp.ShiftName), 'Standard Shift') AS shift_name,
	    COALESCE(TRIM(wp.RosterType), 'Fixed') AS roster_type,          
	    COALESCE(TRIM(ws.ScheduleName), 'Not Assigned') AS schedule_name,
	    COALESCE(TRIM(wpd.WorkingDayName), 'Unknown Day') AS working_day_name,
        CAST(wpd.FromTime AS TIME) AS from_time1,
	    CAST(wpd.ToTime AS TIME) AS to_time1,
	    CAST(wpd.FromTime2 AS TIME) AS from_time2,
	    CAST(wpd.ToTime2 AS TIME) AS to_time2
    FROM tblWorkingProfile wp
    LEFT  join tblWorkingSchedule ws on wp.SheduleNo = ws.ScheduleID
    left join tblWorkingProfileDetails wpd on wp.[No] = wpd.WorkingProfileNo;
"""

EXTRACT_FACT_ATTENDANCE_QUERY = """
    SELECT 
        CAST(staffID AS VARCHAR(50)) AS source_employee_id,
        CAST([Date] AS Date) AS source_date_id,
        CAST(schClassid AS int) AS source_shift_id,
        CAST(LevelNo AS VARCHAR(50)) AS source_position_id,
        CAST(No AS int) AS source_working_profile_id,

        CASE 
            WHEN Absence = 1 THEN 0.0
            WHEN TimeIn IS NOT NULL AND TimeOut IS NOT NULL THEN
                CAST(DATEDIFF(MINUTE, TimeIn, TimeOut) AS DECIMAL(5,2)) / 60.0
            ELSE 0.0 
        END AS work_hours,
        
        CASE 
            WHEN Absence = 1 THEN 0.0
            WHEN CAST(TimeIn as time) > '08:30:00' THEN DATEDIFF(MINUTE, '08:30:00', CAST(TimeIn as TIME))
            ELSE 0
        END AS late_minutes,

        CASE 
            WHEN Absence = 1 THEN 0.0
            WHEN Permission = 1 THEN 'On Leave'
            WHEN CAST(TimeIn as TIME) > '09:00:00' THEN 'Late'
            WHEN status = 0 THEN 'Absence'
            ELSE 'Present'
        END as attendance_status,
        CAST(TimeIn AS TIME) AS check_in_time,
        CAST(TimeOut AS TIME) AS check_out_time,
        OverTime as overtime_hours
    FROM tblAttendance
    WHERE staffID is not null;
"""
