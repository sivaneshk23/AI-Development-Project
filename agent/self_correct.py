from agent.planner import create_plan


def self_correct(
    perception: dict,
    sql_query: str,
    observation: dict
) -> dict:

    return create_plan(
        perception,
        previous_observation=observation,
        previous_sql=sql_query
    )