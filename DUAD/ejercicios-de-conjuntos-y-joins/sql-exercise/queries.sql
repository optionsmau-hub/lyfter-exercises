-- ============================================================
-- Query 1: Get all books and their authors (if they have one)
-- ============================================================
SELECT
    Books.ID          AS BookID,
    Books.Name         AS BookName,
    Authors.Name       AS AuthorName
FROM Books
LEFT JOIN Authors ON Books.Author = Authors.ID
ORDER BY Books.ID;


-- ============================================================
-- Query 2: Get all books that have no author
-- ============================================================
SELECT
    Books.ID   AS BookID,
    Books.Name AS BookName
FROM Books
WHERE Books.Author IS NULL;


-- ============================================================
-- Query 3: Get all authors that have no books
-- ============================================================
SELECT
    Authors.ID   AS AuthorID,
    Authors.Name AS AuthorName
FROM Authors
LEFT JOIN Books ON Books.Author = Authors.ID
WHERE Books.ID IS NULL;


-- ============================================================
-- Query 4: Get all books that have been rented at some point
-- ============================================================
SELECT DISTINCT
    Books.ID   AS BookID,
    Books.Name AS BookName
FROM Books
INNER JOIN Rents ON Rents.BookID = Books.ID
ORDER BY Books.ID;


-- ============================================================
-- Query 5: Get all books that have never been rented
-- ============================================================
SELECT
    Books.ID   AS BookID,
    Books.Name AS BookName
FROM Books
LEFT JOIN Rents ON Rents.BookID = Books.ID
WHERE Rents.ID IS NULL;


-- ============================================================
-- Query 6: Get all customers that have never rented a book
-- ============================================================
SELECT
    Customers.ID   AS CustomerID,
    Customers.Name AS CustomerName
FROM Customers
LEFT JOIN Rents ON Rents.CustomerID = Customers.ID
WHERE Rents.ID IS NULL;


-- ============================================================
-- Query 7: Get all books that have been rented and are "Overdue"
-- ============================================================
SELECT
    Books.ID     AS BookID,
    Books.Name   AS BookName,
    Rents.State  AS RentState
FROM Books
INNER JOIN Rents ON Rents.BookID = Books.ID
WHERE Rents.State = 'Overdue';
