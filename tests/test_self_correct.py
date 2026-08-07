from agent.self_correct import self_correct


def test_success():

    result = self_correct(
        "SELECT * FROM employees "
        "WHERE department='IT';"
    )

    assert result["status"] == "success"
    assert result["retry"] is False


def test_sql_error():

    result = self_correct(
        "SELECT * FROM employeez;"
    )

    assert result["status"] == "error"
    assert result["retry"] is True


def test_zero_rows():

    result = self_correct(
        "SELECT * FROM employees "
        "WHERE department='Space Research';"
    )

    assert result["status"] == "zero_rows"
    assert result["retry"] is True


if __name__ == "__main__":

    tests = [
        test_success,
        test_sql_error,
        test_zero_rows
    ]

    passed = 0

    print("\n===== SELF CORRECTION TESTS =====\n")

    for test in tests:

        try:
            test()

            print(
                f"{test.__name__}: PASS"
            )

            passed += 1

        except Exception as error:

            print(
                f"{test.__name__}: FAIL"
            )

            print(error)

    print(
        f"\nResult: {passed}/{len(tests)} tests passed."
    )