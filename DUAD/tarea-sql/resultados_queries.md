# Query Results — library.db

Database created and queried with the `sqlite3` CLI (version 3.53.4), from the [setup_library.sql](setup_library.sql) script that generates [library.db](library.db).

---

## 1. All books and their authors (if they have one)

**Why `LEFT JOIN`:** the base table is `Books`, and we want to keep **every** book even if it has no associated author (the one with `Author = NULL`). An `INNER JOIN` would have excluded "The Book of the 5 Rings" since it has no match in `Authors`.

```sql
SELECT Books.Name AS Book, Authors.Name AS Author
FROM Books
LEFT JOIN Authors ON Books.Author = Authors.ID;
```

```
          Book                      Author
-------------------------  -------------------------
Don Quijote                Miguel de Cervantes
La Divina Comedia          Dante Alighieri
Vagabond 1-3                Takehiko Inoue
Dragon Ball 1               Akira Toriyama
The Book of the 5 Rings
```

---

## 2. Books without an author

**Why `LEFT JOIN`:** we start from `Books` (we want to see books) and join with `Authors`. When no match is found, the `Authors` columns come back as `NULL`; filtering on `Authors.ID IS NULL` isolates exactly the books with no author.

```sql
SELECT Books.ID, Books.Name
FROM Books
LEFT JOIN Authors ON Books.Author = Authors.ID
WHERE Authors.ID IS NULL;
```

```
ID           Name
--  -----------------------
 5  The Book of the 5 Rings
```

---

## 3. Authors without books

**Why `LEFT JOIN`:** here the base table switches to `Authors`, since we want to keep every author even without any related book. We filter on `Books.ID IS NULL` to keep only the ones with no match.

```sql
SELECT Authors.ID, Authors.Name
FROM Authors
LEFT JOIN Books ON Books.Author = Authors.ID
WHERE Books.ID IS NULL;
```

```
ID     Name
--  -----------
 5  Walt Disney
```

---

## 4. Books that have been rented at least once

**Why `INNER JOIN`:** only books that **do** have at least one match in `Rents` matter. `INNER JOIN` automatically discards books with no associated rental, which is exactly what we're after. `DISTINCT` is used because a book can have several rentals (e.g. "La Divina Comedia" appears twice in `Rents`), and we don't want duplicates.

```sql
SELECT DISTINCT Books.ID, Books.Name
FROM Books
INNER JOIN Rents ON Books.ID = Rents.BookID;
```

```
ID        Name
--  -----------------
 1  Don Quijote
 2  La Divina Comedia
 3  Vagabond 1-3
```

---

## 5. Books that have never been rented

**Why `LEFT JOIN`:** again we start from `Books` to keep every book, and filter on `Rents.ID IS NULL` to keep only the ones with no match in `Rents`.

```sql
SELECT Books.ID, Books.Name
FROM Books
LEFT JOIN Rents ON Books.ID = Rents.BookID
WHERE Rents.ID IS NULL;
```

```
ID           Name
--  -----------------------
 4  Dragon Ball 1
 5  The Book of the 5 Rings
```

---

## 6. Customers who have never rented a book

**Why `LEFT JOIN`:** we start from `Customers` to keep every customer, and filter on `Rents.ID IS NULL` to keep only those with no rental on record.

```sql
SELECT Customers.ID, Customers.Name
FROM Customers
LEFT JOIN Rents ON Customers.ID = Rents.CustomerID
WHERE Rents.ID IS NULL;
```

```
ID       Name
--  --------------
 3  Luke Skywalker
```

---

## 7. Books rented with state "Overdue"

**Why `INNER JOIN`:** only rentals that exist and additionally have a match in both `Books` and `Customers` are of interest; there's no need to keep unmatched rows, so `INNER JOIN` is enough and more direct. The join with `Customers` is added to show who has the overdue book.

```sql
SELECT Books.Name AS Book, Customers.Name AS Customer, Rents.State
FROM Rents
INNER JOIN Books ON Rents.BookID = Books.ID
INNER JOIN Customers ON Rents.CustomerID = Customers.ID
WHERE Rents.State = 'Overdue';
```

```
        Book                Customer          State
--------------------  --------------------  ----------
La Divina Comedia     Jane Doe              Overdue
```
