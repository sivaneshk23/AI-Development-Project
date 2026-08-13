from agent.self_correct import self_correct


def test_self_correction_calls_planner(
    monkeypatch
):

    expected = {
        "sql_query":
            "SELECT * FROM employees;",
        "plan_summary":
            "Corrected query."
    }

    monkeypatch.setattr(
        "agent.self_correct.create_plan",
        lambda perception,
        previous_observation=None,
        previous_sql=None:
            expected
    )

    perception = {
        "user_question":
            "Show all employees.",
        "database_schema": {}
    }

    observation = {
        "status": "error",
        "message":
            "no such table: employeez",
        "should_retry": True,
        "has_rows": False
    }

    result = self_correct(
        perception,
        "SELECT * FROM employeez;",
        observation
    )

    assert (
        result
        ==
        expected
    )