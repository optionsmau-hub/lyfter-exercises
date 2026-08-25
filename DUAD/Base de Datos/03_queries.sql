-- =====================================================================
-- 03_queries.sql
-- The 7 SELECT queries required by the exercise.
-- =====================================================================

-- 1) Get all stored products
SELECT * FROM Products;

-- 2) Get all products with a price greater than 50000
SELECT * FROM Products
WHERE price > 50000;

-- 3) Get all purchases of the same product by id
--    ("purchases" = already-invoiced line items, Invoice_Details)
--    (example: product id = 3, "27" monitor")
SELECT id.*, p.name AS product_name
FROM Invoice_Details id
JOIN Products p ON p.product_id = id.product_id
WHERE id.product_id = 3;

-- 4) Get all purchases grouped by product, showing the total
--    purchased across all purchases
SELECT
    p.product_id                        AS product_id,
    p.name                              AS product_name,
    SUM(id.quantity)                    AS total_quantity_sold,
    ROUND(SUM(id.total_amount), 2)      AS total_amount_sold
FROM Invoice_Details id
JOIN Products p ON p.product_id = id.product_id
GROUP BY p.product_id, p.name;

-- 5) Get all invoices made by the same buyer
--    (example: ana@example.com)
SELECT * FROM Invoices
WHERE buyer_email = 'ana@example.com';

-- 6) Get all invoices ordered by total amount in descending order
SELECT * FROM Invoices
ORDER BY total_amount DESC;

-- 7) Get a single invoice by invoice number
--    (example: INV-1003)
SELECT * FROM Invoices
WHERE invoice_number = 'INV-1003';
