from agent.perceive import perceive
from agent.planner import create_plan
from agent.act import act
from agent.observe import observe
from agent.self_correct import self_correct


MAX_RETRIES = 2


def run_agent(question, initial_query=None):
    print("\n===== AGENT LOOP =====")

    perception = perceive(question)

    print("\n===== PERCEIVE =====")
    print("User Question:")
    print(perception["user_question"])

    print("\nAvailable Database Schema:")

    for table_name, columns in perception["database_schema"].items():
        print(f"\nTable: {table_name}")

        for column in columns:
            print(
                f"  - {column['name']} "
                f"({column['type']})"
            )

    current_query = None

    for attempt in range(MAX_RETRIES + 1):

        print(
            f"\n===== ITERATION {attempt + 1} ====="
        )

        plan = create_plan(perception)

        print("\n===== PLAN =====")

        for number, step in enumerate(
            plan,
            start=1
        ):
            print(
                f"{number}. {step}"
            )

        if current_query is None:
            if initial_query is not None:
                current_query = initial_query
            else:
                current_query = generate_initial_query(question)

        print("\nGenerated SQL:")
        print(current_query)

        action = act(current_query)

        print("\n===== ACT =====")

        if action["result"]["success"]:
            print("Execution Status: SUCCESS")

            if action["result"]["rows"]:
                print("\nResults:")

                for row in action["result"]["rows"]:
                    print(row)

            elif action["result"]["columns"]:
                print("No records found.")

        else:
            print("Execution Status: FAILED")
            print(
                "Error:",
                action["result"]["error"]
            )

        observation = observe(action)

        print("\n===== OBSERVE =====")
        print("Status:", observation["status"])
        print("Message:", observation["message"])
        print(
            "Should Retry:",
            observation["should_retry"]
        )

        if not observation["should_retry"]:
            print("\n===== AGENT COMPLETED =====")
            return {
                "status": "success",
                "query": current_query,
                "observation": observation
            }

        if attempt >= MAX_RETRIES:
            break

        correction = self_correct(
            current_query
        )

        print("\n===== SELF-CORRECT =====")
        print(
            "Retry required:",
            correction["retry"]
        )

        print(
            "Reason:",
            correction["message"]
        )

        print(
            "Replanning for next iteration..."
        )

        current_query = correct_query(
        current_query,
        observation,
        perception
        )

    if current_query is None:
        print("\nNo matching records were found.")

        return{
        "status": "no_results",
        "query": action["sql_query"],
        "observation": observation
        }

    print("\n===== AGENT STOPPED =====")

    if observation["status"] == "zero_rows":
        final_status = "no_results"
    else:
        final_status = "failed"

    return {
    "status": final_status,
    "query": current_query,
    "observation": observation
    }


def generate_initial_query(question):
    question_lower = question.lower()

    if "salary" in question_lower:
        return "SELECT name, salary FROM employees;"

    if "department" in question_lower:
        if "it" in question_lower:
            return (
                "SELECT * FROM employees "
                "WHERE department = 'IT';"
            )

        if "hr" in question_lower:
            return (
                "SELECT * FROM employees "
                "WHERE department = 'HR';"
            )

        if "finance" in question_lower:
            return (
                "SELECT * FROM employees "
                "WHERE department = 'Finance';"
            )

        if "sales" in question_lower:
            return (
                "SELECT * FROM employees "
                "WHERE department = 'Sales';"
            )

    if "from" in question_lower:
        department = extract_department(question)

        if department:
            return (
                "SELECT * FROM employees "
                f"WHERE department = '{department}';"
            )

    if (
        "all employees" in question_lower
        or "show employees" in question_lower
        or "list employees" in question_lower
    ):
        return "SELECT * FROM employees;"

    return "SELECT * FROM employees;"

def extract_department(question):
    question_lower = question.lower()

    known_departments = [
        "it",
        "hr",
        "finance",
        "sales",
        "space research"
    ]

    for department in known_departments:
        if department in question_lower:
            if department == "it":
                return "IT"

            if department == "hr":
                return "HR"

            if department == "finance":
                return "Finance"

            if department == "sales":
                return "Sales"

            if department == "space research":
                return "Space Research"

    return None


def correct_query(
    query,
    observation,
    perception
):
    if observation["status"] == "error":

        error_message = observation["message"].lower()

        if "no such table" in error_message:
            return "SELECT * FROM employees;"

    if observation["status"] == "zero_rows":
        return None

    return query


if __name__ == "__main__":

    question = input(
        "Enter your database question: "
    )

    result = run_agent(question)

    print("\n===== FINAL RESULT =====")
    print(result)