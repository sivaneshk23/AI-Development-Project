import sqlite3


DATABASE_PATH = "database/sample.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    cursor.execute("DELETE FROM employees")

    employees = [
        ("Arun", "IT", 50000),
        ("Priya", "HR", 40000),
        ("Kumar", "IT", 60000),
        ("Meena", "Finance", 55000),
        ("Rahul", "Sales", 45000)
    ]

    cursor.executemany(
        """
        INSERT INTO employees (name, department, salary)
        VALUES (?, ?, ?)
        """,
        employees
    )

    connection.commit()
    connection.close()

    print("Sample database created successfully.")


if __name__ == "__main__":
    create_database()