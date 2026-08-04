from agent.act import act


def test_successful_query():
    action = act(
        "SELECT * FROM employees "
        "WHERE department = 'IT';"
    )

    result = action["result"]

    assert action["tool"] == "execute_sql"
    assert result["success"] is True
    assert len(result["rows"]) == 2


def test_salary_query():
    action = act(
        "SELECT name, salary "
        "FROM employees "
        "ORDER BY salary DESC;"
    )

    result = action["result"]

    assert result["success"] is True
    assert len(result["rows"]) == 5

    assert result["rows"][0][0] == "Kumar"
    assert result["rows"][0][1] == 60000.0


def test_invalid_table():
    action = act(
        "SELECT * FROM employeez;"
    )

    result = action["result"]

    assert result["success"] is False
    assert result["error"] is not None


def test_zero_rows():
    action = act(
        "SELECT * FROM employees "
        "WHERE department = 'Space Research';"
    )

    result = action["result"]

    assert result["success"] is True
    assert len(result["rows"]) == 0


if __name__ == "__main__":
    tests = [
        (
            "Successful SQL execution",
            test_successful_query
        ),
        (
            "Salary query execution",
            test_salary_query
        ),
        (
            "SQL tool failure handling",
            test_invalid_table
        ),
        (
            "Zero-row handling",
            test_zero_rows
        )
    ]

    print("\n===== ACT STAGE TESTS =====\n")

    passed = 0

    for name, test_function in tests:
        try:
            test_function()

            print(
                f"{name}: PASS"
            )

            passed += 1

        except Exception as error:
            print(
                f"{name}: FAIL"
            )

            print(
                "  Error:",
                error
            )

    print(
        f"\nResult: {passed}/{len(tests)} tests passed."
    )