from agent.loop import run_agent


def test_successful_query():
    result = run_agent(
        "Show all employees."
    )

    assert result["status"] == "success"
    assert result["observation"]["status"] == "success"


def test_zero_result_query():
    result = run_agent(
        "Show employees from Space Research."
    )

    assert result["status"] == "no_results"
    assert result["observation"]["status"] == "zero_rows"

def test_sql_error_recovery():
    result = run_agent(
        "Show all employees.",
        initial_query="SELECT * FROM employeez;"
    )

    assert result["status"] == "success"
    assert result["observation"]["status"] == "success"

try:
    test_sql_error_recovery()
    print("SQL error recovery: PASS")
except Exception as error:
    print("SQL error recovery: FAIL")
    print("Error:", error)

print("\n===== AGENT LOOP TESTS =====")

try:
    test_successful_query()
    print("Successful agent loop: PASS")
except Exception as error:
    print("Successful agent loop: FAIL")
    print("Error:", error)

try:
    test_zero_result_query()
    print("Zero-result handling: PASS")
except Exception as error:
    print("Zero-result handling: FAIL")
    print("Error:", error)

print("\nAgent loop tests completed.")