def observe(
    action: dict
) -> dict:

    schema_tool = (
        action["tools_called"][0]
    )

    if not schema_tool["success"]:

        return {
            "status": "error",
            "message": schema_tool["error"],
            "should_retry": True,
            "has_rows": False
        }

    result = action[
        "result"
    ]

    if not result["success"]:

        return {
            "status": "error",
            "message": result["error"],
            "should_retry": True,
            "has_rows": False
        }

    if (
        result["columns"]
        and not result["rows"]
    ):

        return {
            "status": "zero_rows",
            "message": (
                "Query executed successfully "
                "but returned no rows."
            ),
            "should_retry": True,
            "has_rows": False
        }

    return {
        "status": "success",
        "message": (
            "Query executed successfully "
            "with a non-empty result."
        ),
        "should_retry": False,
        "has_rows": True
    }