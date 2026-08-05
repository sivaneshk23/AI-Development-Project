from agent.act import act


def observe(action):
    """
    Analyze the result produced by the ACT stage.

    Possible observation states:
    - success
    - zero_rows
    - error
    """

    result = action["result"]

    if not result["success"]:
        return {
            "status": "error",
            "message": result["error"],
            "should_retry": True
        }

    if (
        result["columns"]
        and len(result["rows"]) == 0
    ):
        return {
            "status": "zero_rows",
            "message": "Query executed successfully but returned no rows.",
            "should_retry": True
        }

    return {
        "status": "success",
        "message": "Query executed successfully.",
        "should_retry": False
    }


def display_observation(observation):
    print("\n===== OBSERVE =====")

    print(
        "Status:",
        observation["status"]
    )

    print(
        "Message:",
        observation["message"]
    )

    print(
        "Should Retry:",
        observation["should_retry"]
    )


if __name__ == "__main__":
    query = input(
        "Enter SQL query: "
    )

    action = act(query)

    observation = observe(action)

    display_observation(
        observation
    )