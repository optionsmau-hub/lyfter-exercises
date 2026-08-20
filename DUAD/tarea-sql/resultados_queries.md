# Resultados de Queries — library.db

Base de datos creada e interrogada con el CLI `sqlite3` (versión 3.53.4), a partir del script [setup_library.sql](setup_library.sql) que genera [library.db](library.db).

---

## 1. Todos los libros y sus autores (si los tienen)

**Por qué `LEFT JOIN`:** la tabla base es `Books`, y queremos conservar **todos** los libros aunque no tengan autor asociado (el libro con `Author = NULL`). Un `INNER JOIN` habría excluido "The Book of the 5 Rings" porque no tiene coincidencia en `Authors`.

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

## 2. Libros sin autor

**Por qué `LEFT JOIN`:** partimos de `Books` (queremos ver libros) y unimos con `Authors`. Al no encontrar coincidencia, las columnas de `Authors` quedan en `NULL`; filtrando por `Authors.ID IS NULL` aislamos justamente los libros huérfanos de autor.

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

## 3. Autores sin libros

**Por qué `LEFT JOIN`:** aquí la tabla base cambia a `Authors`, porque queremos conservar todos los autores aunque no tengan ningún libro relacionado. Filtramos por `Books.ID IS NULL` para quedarnos solo con los que no encontraron coincidencia.

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

## 4. Libros que han sido rentados alguna vez

**Por qué `INNER JOIN`:** solo interesan los libros que **sí** tienen al menos una coincidencia en `Rents`. `INNER JOIN` descarta automáticamente los libros sin ninguna renta asociada, que es exactamente lo que buscamos. Se usa `DISTINCT` porque un libro puede tener varias rentas (por ejemplo, "La Divina Comedia" aparece dos veces en `Rents`) y no queremos duplicados.

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

## 5. Libros que nunca han sido rentados

**Por qué `LEFT JOIN`:** de nuevo partimos de `Books` para conservar todos los libros, y filtramos por `Rents.ID IS NULL` para quedarnos solo con los que no encontraron ninguna coincidencia en `Rents`.

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

## 6. Clientes que nunca han rentado un libro

**Por qué `LEFT JOIN`:** partimos de `Customers` para conservar todos los clientes, y filtramos por `Rents.ID IS NULL` para quedarnos solo con quienes no tienen ninguna renta registrada.

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

## 7. Libros rentados en estado "Overdue"

**Por qué `INNER JOIN`:** solo interesan rentas que existen y que además tienen coincidencia tanto en `Books` como en `Customers`; no hay necesidad de conservar filas sin match, así que `INNER JOIN` es suficiente y más directo. Se agrega el join con `Customers` para mostrar quién tiene el libro atrasado.

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
