from tools.schema_tool import (
    get_database_schema
)

from tools.sql_tool import (
    execute_sql
)


def act(
    sql_query: str
) -> dict:

    try:

        schema = get_database_schema()

        schema_tool = {
            "tool": "inspect_database_schema",
            "success": True,
            "result": schema,
            "error": None
        }

    except Exception as error:

        schema_tool = {
            "tool": "inspect_database_schema",
            "success": False,
            "result": {},
            "error": str(error)
        }

    if not schema_tool["success"]:

        return {
            "tools_called": [
                schema_tool
            ],
            "tool": "inspect_database_schema",
            "sql_query": sql_query,
            "result": {
                "success": False,
                "columns": [],
                "rows": [],
                "error": schema_tool["error"]
            }
        }

    sql_result = execute_sql(
        sql_query
    )

    sql_tool = {
        "tool": "execute_sql",
        "success": sql_result["success"],
        "result": sql_result,
        "error": sql_result["error"]
    }

    return {
        "tools_called": [
            schema_tool,
            sql_tool
        ],
        "tool": "execute_sql",
        "sql_query": sql_query,
        "result": sql_result
    }