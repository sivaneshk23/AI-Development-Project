import sqlite3


connection = sqlite3.connect("database/sample.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT name, department, salary
    FROM employees
    WHERE department = 'IT'
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()