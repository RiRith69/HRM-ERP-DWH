EXTRACT_customer_QUERY = """
    SELECT 
        tc.CustomerID as customer_id,
        tc.CustomerName as customer_name,
        tct.CustomerType as customer_type,
        tcc.ContactName as contact_name,
        n.Nationality as nationality,
        tc.Gender as gender,
        tc.Age as age,
        tc.City as city,
        tc.Region as region,
        tc.Country as country
    FROM tblCustomer tc
    LEFT JOIN tblNationality n on tc.NationalityNo = n.[No]
    LEFT JOIN tblCustomerType tct on tc.CustomerTypeID = tct.CustomerTypeID
    LEFT JOIN tblCustomerContact tcc on tc.CustomerID = tcc.CustomerID;
"""

#Position in vendor not position no it data type varchar not int in the tbl position
#In the tblVendor contain position not posittionNo
EXTRACT_vendor_QUERY = """
    SELECT 
        tv.VendorID as vendor_id,
        tv.CompanyName as company_name,
        tv.Position as contact_position,
        tv.Region as region,
        tv.City as city,
        tv.Country as country,
        tv.TypeofBusiness as type_of_business,
        tv.Active as is_active
    FROM tblVendor tv;
"""

EXTRACT_quotation_status_QUERY = """
     SELECT 
        QuotationNo as quotation_id,
        COALESCE(TRIM(Status), 'Unknown') AS quotation_status,
        AuthorizingStatus as authorizing_status,
        CASE 
	        WHEN CustomerApprovalStatus = 1 THEN 'Approved' 
	        WHEN CustomerApprovalStatus = 0 THEN 'Rejected'
	        ELSE 'Pending' 
    	END AS customer_approval_status,
        QuotationType as quotation_type,
        Version as version_label,
        COALESCE(TRIM(StatusDescription), 'No Description') AS status_description
    FROM tblQuotation;
"""

EXTRACT_item_QUERY = """
    SELECT 
        ti.ItemID as item_id,
        tv.CompanyName as vendor_name,
        ti.Description as description_item,
        tib.BrandName as brand_name,
        tc.CategoryName as category_name,
        ti.UnitofMeasurement as unit_of_measurement,
        ti.UnitofMeasurementLevel2 as unit_of_measurement_level2,
        ti.InventoryType as inventory_type,
        ti.Status as item_status,
        ti.AvgCost as average_cost,
        ti.UnitPrice as standard_unit_price,
        ti.PriceLevel2 as price_level2,
        ti.PriceLevel3 as price_level3,
        ti.PriceLevel4 as price_level4,
        ti.PriceLevel5 as price_level5
    FROM tblItem ti
    LEFT JOIN tblVendor tv on ti.VendorID = tv.VendorID
    LEFT JOIN tblItemBrand tib on ti.BrandID = tib.BrandID
    LEFT JOIN tblCategory tc on ti.CategoryID = tc.CategoryID;
"""

# NOt yet done this dim not yet complete ??????????????????????????????
EXTRACT_DIM_LOCATION_QUERY = """
    SELECT 
        CAST(TRIM(LocationID) AS VARCHAR(50)) AS location_id,
        COALESCE(TRIM(LocationName), 'Unknown location') as location_name,
        coalesce(TRIM(Description), 'No Description Provide') as description
    FROM dbo.tblLocation;
"""



EXTRACT_Delivery_Status_QUERY = """
    SELECT 
        DeliveryNo as delivery_no,
        DeliveryStatus as delivery_status,
        CASE 
        		WHEN AuthorizingStatus = 1 THEN 'TRUE'
        		WHEN AuthorizingStatus = 0 THEN 'FALSE'
        		ELSE 'Pending'
        END as authorizing_status,
        CASE
        	WHEN CustomerAcceptanceStatus = 1 THEN 'Accepted'
        	WHEN CustomerAcceptanceStatus = 0 THEN 'Rejected'
        	ELSE 'Unknown'
        END customer_acceptance_status
   FROM tblDeliveryNote;
"""

EXTRACT_DIM_CURRENCY_QUERY = """
    SELECT 
        tcn.CurrencyNo AS currency_no,
        -- 💡 Using the abbreviated column for code and full name as a fallback
        COALESCE(TRIM(tcn.Currency), 'Unknown') AS currency_code,
        COALESCE(TRIM(tcn.Currency), 'Unknown') AS currency_name, 
        COALESCE(TRIM(tcn.[Type]), 'Standard') AS currency_type,
        COALESCE(TRIM(tcn.FormatCurrency), '#,##0.00') AS format_currency,
        CASE 
            WHEN tcn.CurrencyBaseRate = 1.0 THEN CAST(1.0 AS FLOAT)
            ELSE CAST(0.0 AS FLOAT)
        END as is_base_currency
    FROM dbo.tblCurrencyName tcn;
"""

EXTRACT_DIM_DEPARTMENT_QUERY = """
    SELECT 
        DepartmentID as department_id,
        DepartmentName as department_name,
        CASE
            WHEN Active = 1 THEN 'TRUE'
            WHEN Active = 0 THEN 'FALSE'
            ELSE 'Unknown'
        END is_active,
        CreatingPersonID as creating_person_id
    from tblDepartment;
"""

EXTRACT_DIM_LEAD_QUERY = """
    SELECT 
        tl.LeadNo as lead_id,
        tl.Title as lead_name,
        tlt.LeadType as lead_type,
        tls.LeadSource as lead_source,
        tl.LeadOwnerID as lead_owner_id,
        lst.LeadStage as lead_stage,
        tl.Seriosity as seriosity,
        COALESCE(tl.Percentage, 0) AS percentage,
        tl.Status as status,
        tlc.ContactName as contact_name,
        tlc.Phone as contact_phone,
        COALESCE(TRIM(lcp.Competitor), 'None') AS competitor
    FROM tblLead tl 
    LEFT JOIN tblLeadType tlt on tl.LeadTypeNo = tlt.LeadTypeNo
    LEFT JOIN tblLeadSource tls on tl.SourceNo = tls.SourceNo
    LEFT JOIN tblLeadStage lst on tl.StageNo = lst.StageNo
    LEFT JOIN tblLeadContact tlc on tl.LeadNo = tlc.LeadNo
    LEFT JOIN tblLeadCompetitor lcp on tl.LeadNo = lcp.LeadNo;
"""

EXTRACT_DIM_INVOICE_QUERY = """
    SELECT 
        InvoiceNo AS invoice_no,
        COALESCE(TRIM(CashierID), 'Unknown') AS cashier_id,
        COALESCE(TRIM(RefQuotationNo), 'Direct Sale') AS ref_quotation_no,
        COALESCE(TRIM(PONumber), 'None') AS po_number,
        COALESCE(TRIM(taxOption), 'Standard') AS tax_option,
        COALESCE(TRIM(AuthorizingStatus), 'Pending') AS authorizing_status,
        -- 💡 Convert SQL Server BIT (1/0) fields into true Booleans for PostgreSQL
        CASE 
            WHEN Paid = 1 THEN CAST(1 AS BIT)
            ELSE CAST(0 AS BIT)
        END AS is_paid,
        
        CASE 
            WHEN VAT = 1 THEN CAST(1 AS BIT)
            ELSE CAST(0 AS BIT)
        END AS is_vat_applied
    FROM dbo.tblInvoice
    WHERE InvoiceNo IS NOT NULL;
"""

EXTRACT_DIM_EXPENSE_QUERY = """
    SELECT 
        ExpenseTypeID as expense_type_id,
        COALESCE(TRIM(ExpenseType), 'Unknown Title') AS expense_type,
        COALESCE(TRIM(Description), 'No description provided') AS description
    FROM tblExpenseType;
"""

#------------------------- Fact Table -----------------------------

EXTRACT_FACT_DELIVERY_QUERY = """
    SELECT 
        YEAR(dn.DeliveryDate) * 1000 + MONTH(dn.DeliveryDate) * 500 + DAY(dn.DeliveryDate) as date_key,
        dn.CustomerID as customer_id,
        dnd.ItemID as item_id,
        dn.PreparingPersonID as employee_id,
        dnd.VendorID as vendor_id,
        dn.DeliveryNo AS delivery_note,
        dn.RefSaleOrderNo as ref_sale_order_no,
        dnd.Qty as quantity_shipped,
        dnd.UnitPrice as unit_price,
        dnd.Discount as discount_amount,
        (dnd.Qty * dnd.UnitPrice) - ISNULL(dnd.Discount, 0) as gross_delivery_value
    FROM tblDeliveryNote dn
    JOIN tblDeliveryNoteDetails dnd on dn.DeliveryNo = dnd.DeliveryNo;
"""

#tblSaleOrderDetail it seem this table contain the key as same as SaleOrderNo
EXTRACT_FACT_SALE_QUERY = """
    SELECT 
        YEAR(so.[Date]) * 1000 + MONTH(so.[Date]) * 500 + DAY(so.[Date]) as date_key,
        so.SaleOrderNo as sale_order_no,
        sod.SaleOrderNo as sale_order_detail_no,
        so.CustomerID as customer_id,
        sod.ItemID as item_id,
        so.PreparingPersonID as employee_id,
        sod.Qty as quantity,
        sod.UnitPrice as unit_price,
        sod.Discount as discount,
        (sod.Qty * sod.UnitPrice) - ISNULL(sod.DiscountAmount, 0) AS line_amount
    FROM tblSaleOrder so
    LEFT JOIN tblSaleOrderDetails sod on so.SaleOrderNo = so.SaleOrderNo;
"""

# queries.py

EXTRACT_FACT_PURCHASE_QUERY = """
    SELECT 
        YEAR(po.[Date]) * 10000 + MONTH(po.[Date]) * 100 + DAY(po.[Date]) AS date_key,
        po.PurchaseOrderNo AS purchase_order_no,
        pod.PurchaseOrderNo as purchase_order_detail_no,
        po.Status AS purchase_status,        
        po.ApprovalStatus AS approval_status,  
        pod.ItemID AS item_id,
        po.ApprovedByID AS employee_id,            
        po.VendorID AS vendor_id,                  
        po.CustomerID AS customer_id, 
        ISNULL(pod.Qty, 1) AS quantity,
        ISNULL(pod.UnitCost, 0.00) AS unit_cost,
        (ISNULL(pod.Qty, 1) * ISNULL(pod.UnitCost, 0.00)) AS gross_purchase_amount,
        (ISNULL(pod.Qty, 1) * ISNULL(pod.UnitCost, 0.00)) AS net_purchase_amount
    FROM tblPurchaseOrder po
    INNER JOIN tblPurchaseOrderDetails pod ON po.PurchaseOrderNo = pod.PurchaseOrderNo;
"""
#Not yet include employeeID
EXTRACT_Fact_Inventory_QUERY = """
    SELECT 
        YEAR(tih.[Date]) * 10000 + MONTH(tih.[Date]) * 100 + DAY(tih.[Date]) AS date_key,
        tih.ItemID as item_id,
        tih.LocationID as location_id,
        it.VendorID as vendor_id,
        tih.UnitInStock as units_in_stock_snap
    FROM tblInventoryHistory as tih
    JOIN tblItem it on tih.ItemID = it.ItemID;
"""

#It seem like this table is do not have the key that connect with each other
EXTRACT_FACT_QUOTATION_QUERY = """
    SELECT 
        YEAR(tq.[Date]) * 10000 + MONTH(tq.[Date]) * 100 + DAY(tq.[Date]) AS date_key,
        YEAR(tq.AuthorizingDate) * 10000 + MONTH(tq.[Date]) * 100 DAY(tq.[Date]) as authorizing_date_key,
        tq.CustomerID as customer_id,
        tqd.ItemID as item_id,
        tq.PreparingPersonID as employee_id,
        tq.ContactingPersonID as employee_id,
        tq.AuthorizingPersonID as employee_id,
        ISNULL(tq.AuthorizingStatus, 'Unknown') AS source_authorizing_status,
        tq.QuotationNo as quotation_no,
        tqd.QuotationNo as quotation_detail_no,
        tqd.Qty as quantity,
        tqd.UnitPrice as unit_price,
        tqd.Discount as discount_amount,
        tqd.Qty * tqd.UnitPrice as gross_amount,
        (tqd.Qty * tqd.UnitPrice) - tqd.Discount as net_amount
    FROM tblQuotation tq
    JOIN tblQuotationDetails tqd on tq.
"""

EXTRACT_FACT_INVOICE_QUERY = """
    SELECT 
        ti.InvoiceNo as invoice_no,
        tid.InvoiceDetailsNo as invoice_detail_no,
        ti.RefQuotationNo as ref_quotation_no,
        ti.PONumber as po_number,
        ti.taxOption as tax_option,
        ti.AuthorizingStatus as authorizing_status,
        ti.Paid as is_paid,
        ti.VAT as vat_applied,
        ISNULL(YEAR(ti.[Date]) * 10000 + MONTH(ti.[Date]) * 100 + DAY(ti.[Date]), -1) AS invoice_date_key,
        ISNULL(YEAR(ISNULL(ti.DueDate, ti.[Date])) * 10000 + MONTH(ISNULL(ti.DueDate, ti.[Date])) * 100 + DAY(ISNULL(ti.DueDate, ti.[Date])), -1) AS due_date_key,
        ti.CustomerID AS customer_id,
        tid.ItemID AS item_id,
        ti.CashierID as cashier_employee_id,
        ti.SalePersonID AS salesperson_employee_id,
        tid.Qty as quantity_billed,
        tid.Price as unit_price,
        tid.Discount as discount_amount,
        tid.Qty * tid.Price as gross_amount,
        (tid.Qty * tid.Price) - tid.Discount as net_amount,
        (((tid.Qty * tid.Price) - tid.Discount) / ti.OriginalAmount) * ti.VATAmount AS total_tax_amount,
        ((tid.Qty * tid.Price) - tid.Discount) + ((((tid.Qty * tid.Price) - tid.Discount) / ti.OriginalAmount) * ti.VATAmount) AS net_revenue_collected
    FROM tblInvoice ti
    LEFT JOIN tblInvoiceDetails tid on ti.InvoiceNo = tid.InvoiceDetailsNo;
"""

EXTRACT_FACT_FINANCE_QUERY = """
    SELECT 
        (YEAR(i.[Date]) * 10000 + MONTH(i.[Date]) * 100 + DAY(i.[Date])) AS date_key,
        i.InvoiceNo AS transaction_no,
        'Collection' AS transaction_type,               
        'Cash' AS payment_method, 
        i.CashierID AS cashier_employee_id,           
        i.CustomerID AS customer_id,
        CAST(NULL AS INT) AS vendor_id, 
        i.StationID AS station_id,
        s.Description AS station_description,           
        s.ComputerName AS station_computer_name,  
        i.CashIn AS amount_paid,                        
        (i.CashIn - i.ChangeCash) AS net_cash_flow      
    FROM tblInvoice i
    LEFT JOIN tblStation s ON i.StationID = s.StationID;
"""