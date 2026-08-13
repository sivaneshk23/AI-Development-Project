import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "sample.db"
)


def execute_sql(query):
    connection = None

    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(query)

        if cursor.description is not None:
            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "error": None
            }

        connection.commit()

        return {
            "success": True,
            "columns": [],
            "rows": [],
            "error": None
        }

    except sqlite3.Error as error:

        return {
            "success": False,
            "columns": [],
            "rows": [],
            "error": str(error)
        }

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":

    print("\n===== SQL EXECUTION TOOL =====")

    query = input("Enter SQL query: ")

    result = execute_sql(query)

    if result["success"]:

        print("\nQuery executed successfully.")

        if result["columns"]:
            print("Columns:", result["columns"])

        if result["rows"]:

            print("\nResults:")

            for row in result["rows"]:
                print(row)

        elif result["columns"]:
            print("No records found.")

    else:

        print("\nQuery failed.")
        print("Error:", result["error"])