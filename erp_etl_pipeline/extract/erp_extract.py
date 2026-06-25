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
        coalesce(TRIM(Description), 'No Description Provide') as description,
        CASE 
            WHEN [POS Location] = 1 THEN 'TRUE'
            ELSE 'FALSE'
        END AS pos_location
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
            WHEN Paid = 1 THEN 1
            ELSE 0
        END AS is_paid,
        CASE 
            WHEN VAT = 1 THEN 1
            ELSE 0
        END AS is_vat_applied
    FROM dbo.tblInvoice
    WHERE InvoiceNo IS NOT NULL;
"""

EXTRACT_DIM_EXPENSE_TYPE_QUERY = """
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
        dn.DeliveryNo as delivery_no, 
        dn.Remark AS delivery_note,
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
        so.CustomerID as customer_id,
        sod.ItemID as item_id,
        so.PreparingPersonID as employee_id,
        sod.CurrencyNo as currency_id,
        so.SaleOrderNo as sale_order_no,
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
        pod.ItemID AS item_id,
        po.ApprovedByID AS employee_id,            
        po.VendorID AS vendor_id,                  
        po.CustomerID AS customer_id, 
        pod.CurrencyNo AS currency_id,
        po.PurchaseOrderNo AS purchase_order_no,
        po.Status AS purchase_status,        
        po.ApprovalStatus AS approval_status,  
        ISNULL(pod.Qty, 1) AS quantity,
        ISNULL(pod.UnitCost, 0.00) AS unit_cost,
        (pod.Qty * pod.UnitCost) AS total_amount
    FROM tblPurchaseOrder po
    LEFT JOIN tblPurchaseOrderDetails pod ON po.PurchaseOrderNo = pod.PurchaseOrderNo;
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
        YEAR(tq.AuthorizingDate) * 10000 + MONTH(tq.AuthorizingDate) * 100 + DAY(tq.AuthorizingDate) as authorizing_date_key,
        tq.CustomerID as customer_id,
        tqd.ItemID as item_id,
        tq.PreparingPersonID   as preparing_employee_id,
        tq.ContactingPersonID  as contacting_employee_id,
        tq.AuthorizingPersonID as authorizing_employee_id,
        ISNULL(tq.AuthorizingStatus, 'Unknown') AS authorizing_status,
        tq.QuotationNo as quotation_no,
        tqd.QuotationNo as quotation_detail_no,
        tqd.Qty as quantity,
        tqd.UnitPrice as unit_price,
        tqd.Discount as discount_amount,
        tqd.Qty * tqd.UnitPrice as gross_amount,
        (tqd.Qty * tqd.UnitPrice) - tqd.Discount as net_amount
    FROM tblQuotation tq
    JOIN tblQuotationDetails tqd ON tq.QuotationNo = tqd.QuotationNo;
"""

EXTRACT_FACT_INVOICE_QUERY = """
    SELECT
        ISNULL(
            YEAR(ti.[Date]) * 10000 + MONTH(ti.[Date]) * 100 + DAY(ti.[Date]), -1) AS invoice_date_key,
        ISNULL(YEAR(ISNULL(ti.DueDate, ti.[Date])) * 10000 + MONTH(ISNULL(ti.DueDate, ti.[Date])) * 100 + DAY(ISNULL(ti.DueDate, ti.[Date])), -1) AS due_date_key,
        ti.CustomerID       AS customer_id,
        tid.ItemID          AS item_id,
        ti.CashierID        AS cashier_employee_id,
        ti.SalePersonID     AS salesperson_employee_id,
        ti.POSLocationID    AS location_id,
        tid.CurrencyNo      AS currency_id,
        ti.InvoiceNo        AS invoice_id,
        tid.Qty                         AS quantity_billed,
        tid.Price                       AS unit_price,
        ISNULL(tid.Discount, 0)         AS discount_amount,
        ISNULL(tid.UnitTax, 0)          AS unit_tax_amount,
        (tid.Qty * tid.Price)           AS gross_revenue,
        (((tid.Qty * tid.Price) - ISNULL(tid.Discount, 0)) / NULLIF(ti.OriginalAmount, 0)) * ti.VATAmount AS net_tax_amount,
        ((tid.Qty * tid.Price) - ISNULL(tid.Discount, 0)) + ((((tid.Qty * tid.Price) - ISNULL(tid.Discount, 0)) / NULLIF(ti.OriginalAmount, 0)) * ti.VATAmount) AS net_revenue
    FROM tblInvoice ti
    LEFT JOIN tblInvoiceDetails tid ON ti.InvoiceNo = tid.InvoiceNo
    LEFT JOIN tblLocation tl on ti.POSLocationID = tl.LocationID;
"""

EXTRACT_FACT_EXPENSE_QUERY = """
    SELECT
        YEAR(te.[Date]) * 10000 + MONTH(te.[Date]) * 100 + DAY(te.[Date]) AS expense_date_key,
        YEAR(te.AuthorizingDate) * 10000 + MONTH(te.AuthorizingDate) * 100 + DAY(te.AuthorizingDate) AS authorizing_date_key,
        te.PreparingPersonID    AS employee_id,
        te.AuthorizingPersonID  AS authorizer_id,
        te.VendorID             AS vendor_id,
        te.DepartmentID         AS department_id,
        ted.CurrencyNo          AS currency_id,
        te.ExpenseNo            AS expense_no,
        te.Reference            AS reference,
        te.PaymentMethod        AS payment_method,
        te.TaxOption            AS tax_option,
        te.AuthorizingStatus    AS authorizing_status,
        te.Paid                 AS is_paid,
        ted.Qty                 AS quantity,
        ted.UnitPrice           AS unit_price,
        ISNULL(ted.Discount, 0) AS discount,
        ISNULL(ted.TaxAmount,0) AS tax_amount
    FROM tblExpense te
    LEFT JOIN tblExpenseDetails ted ON te.ExpenseNo = ted.ExpenseNo
"""

EXTRACT_FACT_LEAD_ACTIVITY_QUERY = """
    SELECT
        YEAR(la.[Date]) * 10000 + MONTH(la.[Date]) * 100 + DAY(la.[Date]) AS activity_date_key,
        YEAR(la.ModifyingDate) * 10000 + MONTH(la.ModifyingDate) * 100 + DAY(la.ModifyingDate) AS modified_date_key,
        la.LeadNo AS lead_no,
        la.StaffID AS employee_id,
        lat.ActivityType AS activity_type,
        la.Status           AS status
    FROM tblLeadActivity la
    LEFT JOIN tblLeadActivityType lat ON la.ActivityTypeNo = lat.ActivityTypeNo;
"""

EXTRACT_FACT_RECEIVE_PAYMENT_QUERY = """
    SELECT
        YEAR(rp.[Date]) * 10000 + MONTH(rp.[Date]) * 100 + DAY(rp.[Date]) AS payment_date_key,
        rp.InvoiceNo            AS invoice_id,
        rp.ReceivePersonID      AS employee_id,
        ti.CustomerID           AS customer_id,      -- from tblInvoice join
        rpd.CurrencyNo          AS currency_id,
        rp.PaymentNo            AS payment_no,
        rpd.[Payment Method]    AS payment_method,
        rp.StationID            AS station_id,
        ISNULL(rp.AmountDue, 0)     AS amount_due,
        ISNULL(rp.AmountPaid, 0)    AS amount_paid,
        ISNULL(rp.CashIn, 0)        AS cash_in,
        ISNULL(rp.CashChange, 0)    AS cash_change
    FROM tblReceivePayment rp
    LEFT JOIN tblReceivePaymentDetails rpd
        ON rp.InvoiceNo = rpd.InvoiceNo
        AND rp.PaymentNo = rpd.PaymentNo
    LEFT JOIN tblInvoice ti
        ON rp.InvoiceNo = ti.InvoiceNo;
"""

EXTRACT_FACT_RECEIVE_ITEM_QUERY = """
    SELECT
        YEAR(ri.ReceivingDate) * 10000 + MONTH(ri.ReceivingDate) * 100 + DAY(ri.ReceivingDate) AS receive_date_key,
        rid.ItemID              AS item_id,
        ri.ReceivingPersonID    AS employee_id,
        ri.VendorID             AS vendor_id,
        ri.LocationID           AS location_id,
        rid.CurrencyNo          AS currency_id,
        ri.ReceiveNo            AS receive_no,
        ri.ReferenceNo          AS reference_no,
        ri.Status               AS status,
        ISNULL(rid.Qty, 0)              AS quantity_received,
        ISNULL(rid.Cost, 0)             AS unit_cost,
        ISNULL(rid.Qty, 0) * ISNULL(rid.Cost, 0) AS line_amount
    FROM tblReceiveItem ri
    LEFT JOIN tblReceiveItemDetails rid ON ri.ReceiveNo = rid.ReceiveNo;
"""

EXTRACT_FACT_PURCHASE_REQUEST_QUERY = """
    SELECT
        -- date keys
        YEAR(pr.[Date]) * 10000 + MONTH(pr.[Date]) * 100 + DAY(pr.[Date]) AS request_date_key,
        YEAR(pr.DateRequired) * 10000 + MONTH(pr.DateRequired) * 100 + DAY(pr.DateRequired) AS required_date_key,
        YEAR(pr.ApprovalDate) * 10000 + MONTH(pr.ApprovalDate) * 100 + DAY(pr.ApprovalDate) AS approval_date_key,
        prd.ItemID              AS item_id,
        pr.ModifyingPersonID    AS employee_id,
        pr.VendorID             AS vendor_id,
        pr.ApprovedByID         AS approver_id,
        prd.CurrencyNo          AS currency_id,
        pr.CustomerID           AS customer_id,
        pr.PurchaseRequestNo    AS purchase_request_no,
        pr.ApprovalStatus       AS approval_status,
        pr.DeliveryStatus       AS delivery_status,
        ISNULL(prd.Qty, 0)                              AS quantity_request,
        ISNULL(prd.UnitCost, 0)                         AS unit_cost,
        ISNULL(prd.Qty, 0) * ISNULL(prd.UnitCost, 0)   AS estimated_line_amount,
        ISNULL(prd.DeliveringQty, 0)                    AS delivering_quantity
    FROM tblPurchaseRequest pr
    LEFT JOIN tblPurchaseRequestDetails prd
        ON pr.PurchaseRequestNo = prd.PurchaseRequestNo;
"""

EXTRACT_FACT_RETURN_ITEM_QUERY = """
    SELECT
        YEAR(ri.ReturnDate) * 10000 + MONTH(ri.ReturnDate) * 100 + DAY(ri.ReturnDate) AS return_date_key,
        rid.ItemID          AS item_id,
        ri.StaffID          AS employee_id,
        ri.ReturnNo         AS return_no,
        ri.ReferenceNo      AS reference_no,
        ri.Description      AS description,
        ISNULL(rid.Qty, 0)      AS quantity_return,
        ISNULL(rid.Amount, 0)   AS return_amount
    FROM tblReturnItem ri
    LEFT JOIN tblReturnItemDetails rid ON ri.ReturnNo = rid.ReturnNo;
"""

EXTRACT_FACT_ITEM_USED_QUERY = """
    SELECT
        -- date key
        YEAR(iu.[Date]) * 10000 + MONTH(iu.[Date]) * 100 + DAY(iu.[Date]) AS date_key,
        iu.ItemID       AS item_id,
        iu.StaffID      AS employee_id,
        iu.LocationID   AS location_id,
        iu.Description  AS description,
        ISNULL(iu.Qty, 0)       AS quantity_used,
        ISNULL(iu.UnitCost, 0)  AS unit_cost
    FROM tblItemUsed iu;
"""

EXTRACT_FACT_ISSUE_ITEM_QUERY = """
    SELECT
        YEAR(ii.IssuingDate) * 10000 + MONTH(ii.IssuingDate) * 100 + DAY(ii.IssuingDate) AS issue_date_key,
        iid.ItemID              AS item_id,
        ii.IssuingPersonID      AS employee_id,
        tt.TeamName              AS team_name,
        ii.IssueNo              AS issue_no,
        ii.BoxNo                AS box_no,
        ii.Status               AS status,
        ISNULL(iid.Qty, 0)                              AS quantity_issued,
        ISNULL(iid.Cost, 0)                             AS unit_cost,
        ISNULL(iid.Qty, 0) * ISNULL(iid.Cost, 0)       AS total_issued_amount,
        ii.location as location_name
    FROM tblIssueItem ii
    LEFT JOIN tblIssueItemDetails iid ON ii.IssueNo = iid.IssueNo
    LEFT JOIN tblTeam tt on ii.TeamID = tt.TeamID;
"""

EXTRACT_FACT_WAREHOUSE_REQUEST_QUERY = """
    SELECT
        YEAR(wr.[Date]) * 10000 + MONTH(wr.[Date]) * 100 + DAY(wr.[Date]) AS request_date_key,
        YEAR(wr.DeliveryDate) * 10000 + MONTH(wr.DeliveryDate) * 100 + DAY(wr.DeliveryDate) AS delivery_date_key,
        wrd.ItemID                  AS item_id,
        wr.RequestingPersonID       AS request_employee_id,
        wr.ApprovedByID             AS approve_employee_id,
        wr.CustomerID               AS customer_id,
        wr.LocationID               AS location_id,
        wr.RequestNo                AS request_no,
        wr.RefSaleOrderNo           AS ref_sale_order_no,
        wr.RequestType              AS request_type,
        wr.Status                   AS status,
        wr.DeliveryStatus           AS delivery_status,
        ISNULL(wrd.Qty, 0)          AS quantity_request
    FROM tblWarehouseRequest wr
    LEFT JOIN tblWarehouseRequestDetails wrd ON wr.RequestNo = wrd.RequestNo
"""

EXTRACT_FACT_ITEM_TRANSFER_QUERY = """
    SELECT
        YEAR(t.TransferingDate) * 10000 + MONTH(t.TransferingDate) * 100 + DAY(t.TransferingDate) AS transfer_date_key,
        td.ItemID               AS item_id,
        t.TransferingPersonID   AS employee_id,
        t.FromLocationID        AS source_location_id,
        t.ToLocationID          AS dest_location_id,
        t.TransferNo            AS transfer_no,
        t.Status                AS status,
        ISNULL(td.Qty, 0)       AS quantity_transfer
    FROM tblTransfer t
    LEFT JOIN tblTransferDetails td ON t.TransferNo = td.TransferNo;
"""