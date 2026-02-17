examples = [
    {
        "question": "List all customers",
        "sql": 'SELECT * FROM "Customer" LIMIT 20;'
    },
    {
        "question": "Count total invoices",
        "sql": 'SELECT COUNT(*) AS "TotalInvoices" FROM "Invoice";'
    },
    {
        "question": "Top 5 best selling tracks",
        "sql": 'SELECT "InvoiceLine"."TrackId", SUM("InvoiceLine"."Quantity") AS "TotalSold" FROM "InvoiceLine" GROUP BY "InvoiceLine"."TrackId" ORDER BY SUM("InvoiceLine"."Quantity") DESC LIMIT 5;'
    },
    {
        "question": "Total revenue",
        "sql": 'SELECT SUM("Invoice"."Total") AS "TotalRevenue" FROM "Invoice";'
    },
]
