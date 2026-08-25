-- =====================================================================
-- SQL Exercises - Databases (Lyfter)
-- File: 01_schema.sql
-- Replicates the DrawSQL diagram: Products, Invoices, Invoice_Details,
-- Shopping_Cart, Cart_Details.
-- Content: table creation + ALTER TABLE on Invoices.
-- =====================================================================
--
-- NOTES / SQLITE LIMITATIONS (documented as requested):
--
-- 1) Auto-incrementing PKs:
--    SQLite automatically generates primary key values when a column
--    is declared as "INTEGER PRIMARY KEY". It assigns the next
--    available integer on every INSERT. AUTOINCREMENT is added so
--    that ids are never reused, even if rows are deleted.
--
-- 2) Type mapping from the diagram (MySQL/DrawSQL) to SQLite:
--    - bigint   -> INTEGER   (SQLite already handles 8-byte integers
--                  with INTEGER affinity; there is no separate bigint
--                  type)
--    - varchar  -> TEXT      (SQLite does not enforce a length limit)
--    - decimal  -> DECIMAL/NUMERIC (see note 4 about precision)
--    - date     -> DATE      (stored as TEXT in ISO-8601 format)
--    - datetime -> DATETIME  (same, TEXT in ISO-8601 format)
--    - int      -> INTEGER
--
-- 3) Foreign Keys:
--    SQLite has FKs DISABLED by default even if they are declared in
--    the CREATE TABLE. They must be turned on for every connection
--    with "PRAGMA foreign_keys = ON;" (see below).
--
-- 4) DECIMAL types / money:
--    SQLite has no real fixed-point DECIMAL type; any DECIMAL(10,2)
--    column gets "NUMERIC affinity" and is stored as REAL (floating
--    point), which can cause small rounding errors when repeatedly
--    summing money. This limitation is documented and handled by
--    using ROUND(value, 2) in the queries that sum amounts. Side
--    note: in the original diagram, "total_amount" in Invoice_Details
--    was typed as bigint (integer), which would truncate cents. To
--    avoid losing monetary precision it was corrected here to
--    DECIMAL(10,2), matching Invoices — this change from the original
--    diagram is documented here.
--
-- 5) ALTER TABLE:
--    SQLite only allows ONE operation per ALTER TABLE statement (you
--    cannot add two columns in a single ALTER TABLE). That's why the
--    ALTER on Invoices is done in two separate statements.
--
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- 1. Products table
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Products (
    product_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    code             TEXT NOT NULL UNIQUE,
    name             TEXT NOT NULL,
    price            DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    entry_date       DATE NOT NULL,
    brand            TEXT,
    stock_available  INTEGER NOT NULL DEFAULT 0 CHECK (stock_available >= 0)
);

-- ---------------------------------------------------------------------
-- 2. Invoices table
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL UNIQUE,
    purchase_date  DATETIME NOT NULL,
    buyer_email    TEXT NOT NULL,
    total_amount   DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0)
);

-- ---------------------------------------------------------------------
-- 3. Invoice_Details table (product line items per invoice)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Invoice_Details (
    invoice_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id        INTEGER NOT NULL,
    product_id        INTEGER NOT NULL,
    quantity          INTEGER NOT NULL CHECK (quantity > 0),
    total_amount      DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    FOREIGN KEY (invoice_id) REFERENCES Invoices (invoice_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products (product_id) ON DELETE RESTRICT
);

-- ---------------------------------------------------------------------
-- 4. Shopping_Cart table (cart header per buyer)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Shopping_Cart (
    cart_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_email TEXT NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- 5. Cart_Details table (product line items inside each cart)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Cart_Details (
    cart_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id     INTEGER NOT NULL,
    quantity       INTEGER NOT NULL CHECK (quantity > 0),
    cart_id        INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products (product_id) ON DELETE RESTRICT,
    FOREIGN KEY (cart_id) REFERENCES Shopping_Cart (cart_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- ALTER TABLE: add buyer phone number and cashier employee code
-- (two statements because SQLite cannot add 2 columns at once)
-- ---------------------------------------------------------------------
ALTER TABLE Invoices ADD COLUMN buyer_phone TEXT;
ALTER TABLE Invoices ADD COLUMN cashier_employee_code TEXT;
