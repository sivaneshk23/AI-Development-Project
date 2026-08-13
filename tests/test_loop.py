from agent.loop import run_agent


def fake_planner(
    perception,
    previous_observation=None,
    previous_sql=None
):

    if previous_observation is None:

        return {
            "sql_query":
                "SELECT * FROM employeez;",
            "plan_summary":
                "Deliberately invalid SQL "
                "for failure-recovery testing."
        }

    return {
        "sql_query":
            "SELECT * FROM employees;",
        "plan_summary":
            "Correct the failed query using "
            "the observed database error."
    }


def test_sql_error_recovery():

    result = run_agent(
        "Show all employees.",
        planner=fake_planner
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["observation"]["status"]
        == "success"
    )

    assert (
        result["iterations"]
        == 2
    )


def test_successful_agent_loop():

    def successful_planner(
        perception,
        previous_observation=None,
        previous_sql=None
    ):

        return {
            "sql_query":
                "SELECT * FROM employees;",
            "plan_summary":
                "Return all employee records."
        }

    result = run_agent(
        "Show all employees.",
        planner=successful_planner
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["iterations"]
        == 1
    )