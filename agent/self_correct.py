from agent.act import act
from agent.observe import observe


def self_correct(sql_query):
    """
    Execute one agent cycle.

    This component decides whether another
    planning iteration should be attempted.
    """

    action = act(sql_query)

    observation = observe(action)

    decision = {
        "sql_query": sql_query,
        "status": observation["status"],
        "retry": observation["should_retry"],
        "message": observation["message"]
    }

    return decision


def display_decision(decision):

    print("\n===== SELF CORRECTION =====")

    print(
        "SQL:",
        decision["sql_query"]
    )

    print(
        "Status:",
        decision["status"]
    )

    print(
        "Retry:",
        decision["retry"]
    )

    print(
        "Message:",
        decision["message"]
    )


if __name__ == "__main__":

    query = input(
        "Enter SQL query: "
    )

    decision = self_correct(query)

    display_decision(decision)