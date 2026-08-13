from agent.planner import create_plan


def test_planner_uses_llm_response(
    monkeypatch
):

    fake_response = {
        "sql_query": (
            "SELECT name, salary "
            "FROM employees "
            "ORDER BY salary DESC;"
        ),
        "plan_summary": (
            "Return employee salaries "
            "ordered from highest to lowest."
        )
    }

    monkeypatch.setattr(
        "agent.planner.call_llm",
        lambda system_prompt, user_prompt:
            fake_response
    )

    perception = {
        "user_question":
            "Who earns the highest salary?",
        "database_schema": {
            "employees": [
                {
                    "name": "id",
                    "type": "INTEGER"
                },
                {
                    "name": "name",
                    "type": "TEXT"
                },
                {
                    "name": "department",
                    "type": "TEXT"
                },
                {
                    "name": "salary",
                    "type": "REAL"
                }
            ]
        }
    }

    plan = create_plan(
        perception
    )

    assert (
        plan["sql_query"]
        ==
        "SELECT name, salary "
        "FROM employees "
        "ORDER BY salary DESC;"
    )

    assert (
        "salar"
        in plan["plan_summary"].lower()
    )


def test_planner_rejects_non_select(
    monkeypatch
):

    monkeypatch.setattr(
        "agent.planner.call_llm",
        lambda system_prompt, user_prompt: {
            "sql_query":
                "DELETE FROM employees;",
            "plan_summary":
                "Delete employees."
        }
    )

    perception = {
        "user_question":
            "Delete employees.",
        "database_schema": {}
    }

    try:

        create_plan(
            perception
        )

        assert False, (
            "Non-SELECT SQL should be rejected."
        )

    except ValueError as error:

        assert (
            "SELECT"
            in str(error)
        )