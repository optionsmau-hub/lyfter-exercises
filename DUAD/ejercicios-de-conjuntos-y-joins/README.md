# Set Theory & SQL Exercises

This folder contains all the deliverables for the assignment.

- `01-set-theory.md` — Set operations (Union, Intersection, Difference,
  Complement) using the sets `All`, `Even`, and `Odd`.
- `02-sql-select-research.md` — Documentation research on `ORDER BY`,
  `LIMIT`, `GROUP BY`, and three `JOIN` types (`INNER`, `LEFT`, `RIGHT`),
  plus an informative summary table and sources.
- `sql-exercise/` — The `Books` / `Authors` / `Customers` / `Rents`
  database exercise:
  - `schema.sql` — table definitions.
  - `seed_data.sql` — sample data (matches the assignment's tables).
  - `queries.sql` — the 7 required queries, labeled.
  - `library.db` — the actual SQLite database built from the two scripts
    above (open it with any SQLite client, e.g. the "SQLite Viewer"
    extension in VS Code, or `python3 -c "import sqlite3"`).
  - `run_queries.py` — the script that builds the database, runs every
    query, and generates the screenshots in `screenshots/`.
  - `results.md` — each query with its SQL and a screenshot of the
    actual result (open this file to review everything at once).
  - `screenshots/` — one PNG per query, showing the query and its result
    table.
