import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "sample.db"
)


def get_database_schema():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        """
    )

    tables = cursor.fetchall()

    schema = {}

    for table in tables:
        table_name = table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema[table_name] = [
            {
                "name": column[1],
                "type": column[2]
            }
            for column in columns
        ]

    connection.close()

    return schema


if __name__ == "__main__":
    database_schema = get_database_schema()

    print("\n===== DATABASE SCHEMA =====")

    for table_name, columns in database_schema.items():

        print(f"\nTable: {table_name}")

        for column in columns:
            print(
                f"  - {column['name']} "
                f"({column['type']})"
            )