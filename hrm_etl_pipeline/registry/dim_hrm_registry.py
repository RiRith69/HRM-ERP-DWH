from extract.hrm_extract import *
from transform.dim_hrm_transform import *
ETL_Registry = [
    {
        "target_table": "public.dim_shift",
        "extract_query": EXTRACT_DIM_SHIFT_QUERY,
        "transform_func": trans_shift,
        "insert_query": """
            INSERT INTO public.dim_shift (shift_id, shift_name, start_time_1, end_time_1, start_time_2, end_time_2)
            VALUES (:shift_id, :shift_name, :start_time_1, :end_time_1, :start_time_2, :end_time_2)
            ON CONFLICT (shift_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_position",
        "extract_query": EXTRACT_DIM_POSITION_Query,
        "transform_func": trans_position,
        "insert_query": """
            INSERT INTO public.dim_position (level_no, position_name, rank_name)
            VALUES (:level_no, :position_name, :rank_name)
            ON CONFLICT (level_no) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_payroll_component",
        "extract_query": EXTRACT_DIM_PAY_ROLL_COMPONENT_QUERY,
        "transform_func": trans_payroll_component,
        "insert_query": """
            INSERT INTO public.dim_payroll_component (component_id, component_name, component_type)
            VALUES (:component_id, :component_name, :component_type)
            ON CONFLICT (component_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_applicant",
        "extract_query": EXTRACT_DIM_APPLICANT_Query,
        "trans_func": trans_applicant,
        "insert_query": """
            INSERT INTO public.dim_applicant (applicant_id, applicant_name, gender, nationality, marital_status, education_level, birth_date)
            VALUES (:applicant_id, :applicant_name, :gender, :nationality, :marital_status, :education_level, :birth_date)
            ON CONFLICT (applicant_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_asset",
        "extract_query": EXTRACT_DIM_ASSET_QUERY,
        "trans_func": trans_asset,
        "insert_query": """
            INSERT INTO public.dim_asset (asset_id, asset_code, asset_name, asset_type, asset_make, asset_group, model_number, serial_number, status)
            VALUES (:asset_id, :asset_code, :asset_name, :asset_type, :asset_make, :asset_group, :model_number, :serial_number, :status)
            ON CONFLCIT (asset_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_asset_location",
        "extract_query": EXTRACT_ASSET_LOCATION_QUERY,
        "trans_func": trans_asset_location,
        "insert_query": """
            INSERT INTO public.dim_asset_location (asset_location_id, location_name, location_type)
            VALUES (:asset_location_id, :location_name, :location_type)
            ON CONFLICT (asset_location_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_asset_transaction_type",
        "extract_query": EXTRACT_DIM_ASSET_TRANSACTION_TYPE_QUERY,
        "trans_func": trans_asset_transaction_type,
        "insert_query": """
            INSERT INTO public.dim_asset_transaction_type (asset_transaction_type_id, asset_transaction_type_name, transaction_category)
            VALUES (:asset_transaction_type_id, :asset_transaction_type_name, :transaction_category)
            ON CONFLICT (asset_transaction_type_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_kpi",
        "extract_query": EXTRACT_DIM_KPI_QUERY,
        "trans_func": trans_kpi,
        "insert_query": """
            INSERT INTO (indicator_id, kpi_name, kpi_category, kpi_period, kpi_direction, kpi_formula)
            VALUES (:indicator_id, :kpi_name, :kpi_category, :kpi_period, :kpi_direction, :kpi_formula)
            ON CONFLICT (indicator_id) DO NOTHING;
        """
    },

    {
        "target_table": "public.dim_leave_type",
        "extract_query": EXTRACT_DIM_LEAVE_TYPE_QUERY,
        "trans_func": trans_leave_type,
        "insert_query": """
            INSERT INTO (leave_id, leave_name, report_symbol, color_code, unit_type)
            VALUES (:leave_id, :leave_name, :report_symbol, :color_code, :unit_type)
            ON CONFLICT (leave_id) DO NOTHING;
        """
    },

    {
        "target_table": "public.dim_organization",
        "extract_query": EXTRACT_DIM_ORGANIZATION_QUERY,
        "trans_func": trans_organization,
        "insert_query": """
            INSERT INTO (organization_id, organization_name, level_no, parent_id, department_id, department_name)
            VALUES (:organization_id, :organization_name, :level_no, :parent_id, :department_id, :department_name)
            ON CONFLICT (organization_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_workflow",
        "extract_query": EXTRACT_DIM_WORKFLOW_QUERY,
        "trans_func": trans_workflow,
        "insert_query": """
            INSERT INTO (workflow_id, workflow_code, workflow_name, module_name, step_order, step_name, approval_type, approver_type, role_code, sla_hours, is_mandatory)
            VALUES (:workflow_id, :workflow_code, :workflow_name, :module_name, :step_order, :step_name, :approval_type, :approver_type, :role_code, :sla_hours, :is_mandatory)
            ON CONFLICT (workflow_id) DO NOTHING;
        """
    },

    {
        "target_table": "public.dim_absence_permission",
        "extract_query": EXTRACT_DIM_ABSENCE_PERMISSION_QUERY,
        "transform_func": trans_absence_permission,  # Passing the function pointer tool
        "insert_query": """
            INSERT INTO public.dim_absence_permission (permission_id, request_type_name, reason_description, approval_status, is_paid_leave, leave_duration_type, approving_person)
            VALUES (:permission_id, :request_type_name, :reason_description, :approval_status, :is_paid_leave, :leave_duration_type, :approving_person)
            ON CONFLICT (permission_id) DO UPDATE 
            SET 
                request_type_name = EXCLUDED.request_type_name,
                reason_description = EXCLUDED.reason_description,
                approval_status = EXCLUDED.approval_status,
                is_paid_leave = EXCLUDED.is_paid_leave,
                leave_duration_type = EXCLUDED.leave_duration_type,
                approving_person = EXCLUDED.approving_person;
        """
    },
    {
        "target_table": "public.dim_interview_stage",
        "extract_query": EXTRACT_DIM_INTERVIEW_STAGE_QUERY,
        "trans_func": trans_interview_stage,
        "insert_query": """
            INSERT INTO public.dim_interview_stage (interview_id, interview_round, interview_type, interview_mode, panel_role, stage_recommendation)
            VALUES (:interview_id, :interview_round, :interview_type, :interview_mode, :panel_role, :stage_recommendation)
            ON CONFLICT (interview_id) DO UPDATE
            SET 
                stage_recommendation = EXCLUDED.stage_recommendation;   
        """
    },

    {
        "target_table": "public.dim_benefit_profile",
        "extract_query": EXTRACT_DIM_BENEFIT_PROFILE_QUERY,
        "trans_func": trans_benefit_profile,
        "insert_query": """
            INSERT INTO public.dim_benefit_profile (benefit_profile_id, benefit_profile_name, benefit_name, payout_frequency, amount)
            VALUES (:benefit_profile_id, :benefit_profile_name, :benefit_name, :payout_frequency, :amount)
            ON CONFLICT (benefit_profile_id) DO NOTHING;
        """
    },
    {
        "target_table": "public.dim_working_profile",
        "extract_query": EXTRACT_DIM_WORKING_PROFILE_QUERY,
        "trans_func": trans_working_profile,
        "insert_query": """
            INSERT INTO public.dim_working_profile (working_profile_id, shift_name, roster_type, schedule_name, working_day_name, from_time1, to_time1, from_time2, to_time2)
            VALUES (:working_profile_id, :shift_name, :roster_type, :schedule_name, :working_day_name, :from_time1, :to_time1, :from_time2, :to_time2)
            ON CONFLICT (working_profile_id) DO NOTHING;
        """
    }
]