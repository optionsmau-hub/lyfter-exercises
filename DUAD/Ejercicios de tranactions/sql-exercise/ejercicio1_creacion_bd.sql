-- ============================================================
-- Exercise 1: Database creation
-- Entities: Users, Products, Bills (+ BillDetails as a cross table)
-- ============================================================

DROP TABLE IF EXISTS BillDetails;
DROP TABLE IF EXISTS Bills;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    ID    SERIAL PRIMARY KEY,
    Name  TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE
);

CREATE TABLE Products (
    ID    SERIAL PRIMARY KEY,
    Name  TEXT NOT NULL,
    Price NUMERIC(10, 2) NOT NULL CHECK (Price >= 0),
    Stock INTEGER NOT NULL CHECK (Stock >= 0)
);

CREATE TABLE Bills (
    ID       SERIAL PRIMARY KEY,
    UserID   INTEGER NOT NULL,
    BillDate TIMESTAMP NOT NULL DEFAULT NOW(),
    State    TEXT NOT NULL DEFAULT 'Completed' CHECK (State IN ('Completed', 'Returned')),
    FOREIGN KEY (UserID) REFERENCES Users(ID)
);

-- Cross table: line items (product + quantity) for each bill
CREATE TABLE BillDetails (
    ID        SERIAL PRIMARY KEY,
    BillID    INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity  INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice NUMERIC(10, 2) NOT NULL,            -- price captured at purchase time
    FOREIGN KEY (BillID) REFERENCES Bills(ID),
    FOREIGN KEY (ProductID) REFERENCES Products(ID)
);


-- ============================================================
-- Sample data
-- ============================================================

INSERT INTO Users (Name, Email) VALUES
    ('John Doe', 'j.doe@email.com'),
    ('Jane Doe', 'jane@doe.com'),
    ('Luke Skywalker', 'darth.son@email.com');

INSERT INTO Products (Name, Price, Stock) VALUES
    ('Wireless Mouse', 15.99, 50),
    ('Mechanical Keyboard', 79.99, 20),
    ('USB-C Cable', 6.50, 100),
    ('27" Monitor', 249.00, 8),
    ('Webcam HD', 45.00, 0);
