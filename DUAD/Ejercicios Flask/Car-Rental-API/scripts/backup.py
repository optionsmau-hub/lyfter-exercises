"""
Exports users, cars and rentals to CSV files under db_backups/, one file
per table, named with today's date (e.g. backup_2026-11-07_users.csv).

Run from anywhere:
    python scripts/backup.py
"""

import csv
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api"))

import psycopg2.extras

from db import get_connection

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "db_backups")
TABLES = ["users", "cars", "rentals"]


def export_table(cur, table, date_str):
    cur.execute(f"SELECT * FROM {table} ORDER BY id")
    columns = [column.name for column in cur.description]
    rows = cur.fetchall()

    file_path = os.path.join(BACKUP_DIR, f"backup_{date_str}_{table}.csv")
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    return file_path, len(rows)


def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    date_str = date.today().isoformat()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            for table in TABLES:
                file_path, row_count = export_table(cur, table, date_str)
                print(f"{table}: {row_count} filas -> {file_path}")


if __name__ == "__main__":
    main()
