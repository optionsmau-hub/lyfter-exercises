# SQL SELECT Research: ORDER BY, LIMIT, GROUP BY, and JOIN Types

This document summarizes documentation research on the main clauses used
with `SELECT` statements (`ORDER BY`, `LIMIT`, `GROUP BY`) and three types
of `JOIN`. Sources are listed at the end.

## What each clause does

**ORDER BY** sorts the rows returned by a query, either in ascending order
(`ASC`, the default) or descending order (`DESC`). It can sort by one or
multiple columns, and sorting by a later column only matters when earlier
columns have tied values.

**LIMIT** restricts the number of rows a query returns. It is commonly used
together with `ORDER BY` to answer questions like "top 5 highest sales" or
to build pagination. (Some database engines, such as SQL Server, use `TOP`
or `OFFSET/FETCH` instead of `LIMIT`, but the concept is the same.)

**GROUP BY** collapses multiple rows that share the same value in one or
more columns into a single summary row. It is almost always used together
with an aggregate function (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) to produce
per-group totals, and it can be filtered afterward with `HAVING` (unlike
`WHERE`, which filters rows before grouping).

**JOIN** combines rows from two or more tables based on a related column
between them (usually a foreign key). The type of join determines which
rows are kept when a match does not exist on one side.

- **INNER JOIN** returns only the rows that have a match in **both**
  tables. Rows without a matching row on the other side are excluded
  entirely.
- **LEFT JOIN** (or `LEFT OUTER JOIN`) returns **all** rows from the left
  (first) table, plus the matching rows from the right table. When there is
  no match, the columns from the right table are filled with `NULL`.
- **RIGHT JOIN** (or `RIGHT OUTER JOIN`) is the mirror image of `LEFT JOIN`:
  it returns **all** rows from the right table, plus the matching rows from
  the left table, filling unmatched left-side columns with `NULL`.
- (A fourth type, **FULL JOIN** / `FULL OUTER JOIN`, keeps all rows from
  both tables, matched or not — mentioned here for context, since it is the
  natural counterpart of the other three, even though only three types were
  requested.)

## Informative table (not SQL code)

| Clause / Join    | Purpose                                                        | Typical use case                                           | Key detail                                                                 |
|-------------------|-----------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------------|
| ORDER BY          | Sorts the result set                                            | Show customers sorted alphabetically, or sales from highest to lowest | Default direction is ascending (`ASC`); use `DESC` for descending; can sort by several columns at once |
| LIMIT             | Caps the number of rows returned                                 | Get only the "top 10" results, or paginate a table listing   | Usually combined with `ORDER BY` so the "top" rows are meaningful; some engines use `TOP`/`FETCH` instead |
| GROUP BY          | Groups rows that share a value so they can be summarized         | Count how many books each author has written                 | Needs an aggregate function to be useful; filter groups with `HAVING`, not `WHERE` |
| INNER JOIN        | Keeps only rows that match in both tables                        | List books together with their authors, only if the author is known | Rows without a match on either side are dropped                                |
| LEFT JOIN         | Keeps all rows from the left table, matched or not                | List every book, even the ones without an author              | Unmatched right-side columns come back as `NULL`                              |
| RIGHT JOIN        | Keeps all rows from the right table, matched or not                | List every author, even the ones with no books written yet    | Unmatched left-side columns come back as `NULL`; equivalent to a `LEFT JOIN` with the tables swapped |

## Sources

- [SQL JOIN — W3Schools](https://www.w3schools.com/sql/sql_join.asp)
- [SQL INNER JOIN — W3Schools](https://www.w3schools.com/sql/sql_join_inner.asp)
- [SQL GROUP BY Statement — W3Schools](https://www.w3schools.com/sql/sql_groupby.asp)
- [SQL Server LEFT JOIN — sqlservertutorial.net](https://www.sqlservertutorial.net/sql-server-basics/sql-server-left-join/)
- [SQL Joins (Inner, Left, Right and Full Join) — GeeksforGeeks](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/)
