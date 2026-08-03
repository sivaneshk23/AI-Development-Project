from agent.perceive import (
    perceive,
    display_perception
)


def create_plan(perception):
    question = perception[
        "user_question"
    ].lower()

    schema = perception[
        "database_schema"
    ]

    plan = []

    if "employees" not in schema:
        plan.append(
            "Verify which available table contains "
            "employee information."
        )

        return plan

    plan.append(
        "Use the employees table."
    )

    if "department" in question:
        plan.append(
            "Use the department column to filter "
            "employee records."
        )

    if "salary" in question:
        plan.append(
            "Use the salary column for the requested "
            "salary-related operation."
        )

    if (
        "all employees" in question
        or "show" in question
        or "list" in question
    ):
        plan.append(
            "Retrieve the employee records that "
            "match the request."
        )

    if len(plan) == 1:
        plan.append(
            "Determine the required columns and "
            "conditions from the user question."
        )

    return plan


def display_plan(plan):
    print("\n===== PLAN =====")

    for number, step in enumerate(
        plan,
        start=1
    ):
        print(
            f"{number}. {step}"
        )


if __name__ == "__main__":
    question = input(
        "Enter your database question: "
    )

    perception = perceive(question)

    display_perception(perception)

    plan = create_plan(perception)

    display_plan(plan)