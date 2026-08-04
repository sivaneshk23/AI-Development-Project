from tools.sql_tool import execute_sql


def act(sql_query):
    """
    Execute a SQL query using the SQL execution tool.

    The ACT stage does not generate SQL.
    It receives SQL produced by the planning/reasoning
    stage and delegates execution to the SQL tool.
    """

    result = execute_sql(sql_query)

    action = {
        "tool": "execute_sql",
        "sql_query": sql_query,
        "result": result
    }

    return action


def display_action(action):
    print("\n===== ACT =====")

    print("\nTool:")
    print(action["tool"])

    print("\nSQL Query:")
    print(action["sql_query"])

    result = action["result"]

    if result["success"]:
        print("\nExecution Status: SUCCESS")

        if result["columns"]:
            print(
                "Columns:",
                result["columns"]
            )

        if result["rows"]:
            print("\nResults:")

            for row in result["rows"]:
                print(row)

        elif result["columns"]:
            print("\nNo records found.")

    else:
        print("\nExecution Status: FAILED")
        print("Error:", result["error"])


if __name__ == "__main__":
    query = input(
        "Enter SQL query for ACT stage: "
    )

    action_result = act(query)

    display_action(action_result)