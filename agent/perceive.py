from tools.schema_tool import get_database_schema


def perceive(user_question):
    schema = get_database_schema()

    perception = {
        "user_question": user_question,
        "database_schema": schema
    }

    return perception


def display_perception(perception):
    print("\n===== PERCEIVE =====")

    print("\nUser Question:")
    print(perception["user_question"])

    print("\nAvailable Database Schema:")

    schema = perception["database_schema"]

    for table_name, columns in schema.items():
        print(f"\nTable: {table_name}")

        for column in columns:
            print(
                f"  - {column['name']} "
                f"({column['type']})"
            )


if __name__ == "__main__":
    question = input(
        "Enter your database question: "
    )

    result = perceive(question)

    display_perception(result)