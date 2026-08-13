from agent.act import act
from agent.observe import observe


def test_success_observation():
    action = act(
        "SELECT * FROM employees "
        "WHERE department = 'IT';"
    )

    observation = observe(action)

    assert observation["status"] == "success"
    assert observation["should_retry"] is False


def test_error_observation():
    action = act(
        "SELECT * FROM employeez;"
    )

    observation = observe(action)

    assert observation["status"] == "error"
    assert observation["should_retry"] is True

    assert observation["message"] is not None


def test_zero_rows_observation():
    action = act(
        "SELECT * FROM employees "
        "WHERE department = 'Space Research';"
    )

    observation = observe(action)

    assert observation["status"] == "zero_rows"
    assert observation["should_retry"] is True


def run_tests():

    tests = [
        (
            "Successful result observation",
            test_success_observation
        ),
        (
            "SQL error observation",
            test_error_observation
        ),
        (
            "Zero-row observation",
            test_zero_rows_observation
        )
    ]

    print(
        "\n===== OBSERVE STAGE TESTS =====\n"
    )

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
                repr(error)
            )

    print(
        f"\nResult: {passed}/{len(tests)} "
        "tests passed."
    )


if __name__ == "__main__":
    run_tests()