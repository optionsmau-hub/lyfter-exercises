-- =====================================================================
-- 02_seed_data.sql
-- Sample data so the required SELECT queries return meaningful results.
-- =====================================================================

INSERT INTO Products (code, name, price, entry_date, brand, stock_available) VALUES
    ('P-001', 'Laptop 14"',       75000.00, '2026-01-10', 'TechCo',    15),
    ('P-002', 'Wireless mouse',    1500.50, '2026-01-12', 'TechCo',    80),
    ('P-003', '27" monitor',      60000.00, '2026-02-01', 'VisionX',   20),
    ('P-004', 'Mechanical keyboard', 4500.00, '2026-02-05', 'KeyMaster', 40),
    ('P-005', 'Ergonomic chair',   48000.00, '2026-02-20', 'SitWell',   10);

INSERT INTO Invoices (invoice_number, purchase_date, buyer_email, total_amount) VALUES
    ('INV-1001', '2026-03-01 10:15:00', 'ana@example.com',    76500.50),
    ('INV-1002', '2026-03-03 12:00:00', 'ana@example.com',     4500.00),
    ('INV-1003', '2026-03-05 09:30:00', 'carlos@example.com', 108000.00),
    ('INV-1004', '2026-03-06 16:45:00', 'maria@example.com',   60000.00);

INSERT INTO Invoice_Details (invoice_id, product_id, quantity, total_amount) VALUES
    (1, 1, 1, 75000.00),   -- Ana buys 1 laptop
    (1, 2, 1, 1500.50),    -- Ana buys 1 mouse (same invoice)
    (2, 4, 1, 4500.00),    -- Ana buys 1 keyboard (different invoice)
    (3, 3, 1, 60000.00),   -- Carlos buys 1 monitor
    (3, 5, 1, 48000.00),   -- Carlos buys 1 chair (same invoice)
    (4, 3, 1, 60000.00);   -- Maria buys 1 monitor

INSERT INTO Shopping_Cart (buyer_email) VALUES
    ('luis@example.com'),
    ('sofia@example.com');

INSERT INTO Cart_Details (product_id, quantity, cart_id) VALUES
    (2, 3, 1),  -- Luis has 3 mice in his cart
    (4, 1, 1),  -- Luis has 1 keyboard in his cart
    (5, 1, 2);  -- Sofia has 1 chair in her cart

-- Fill in the columns added by the ALTER TABLE with sample data
UPDATE Invoices SET buyer_phone = '8888-1111', cashier_employee_code = 'EMP-01' WHERE invoice_id = 1;
UPDATE Invoices SET buyer_phone = '8888-1111', cashier_employee_code = 'EMP-02' WHERE invoice_id = 2;
UPDATE Invoices SET buyer_phone = '8888-2222', cashier_employee_code = 'EMP-01' WHERE invoice_id = 3;
UPDATE Invoices SET buyer_phone = '8888-3333', cashier_employee_code = 'EMP-03' WHERE invoice_id = 4;
