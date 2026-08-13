from __future__ import annotations

import re

from agent.llm import call_llm


SYSTEM_PROMPT = """
You are the SQL planning component of a self-correcting SQL agent.

Your job is to convert the user's natural-language database request
into exactly one read-only SQLite SELECT statement.

STRICT RULES:

1. Use ONLY tables and columns present in the supplied schema.
2. Never invent a table or column.
3. Generate exactly one SELECT statement.
4. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   PRAGMA, ATTACH, or other write/destructive statements.
5. If a previous SQL attempt failed, use the observed error to correct it.
6. If a previous SQL attempt returned zero rows, revise the query
   to produce a useful non-empty result while staying as close as
   possible to the user's request.
7. Return JSON only.
8. Do not return Markdown.
9. Do not return code fences.
10. Return exactly these keys:

{
  "sql_query": "...",
  "plan_summary": "short explanation"
}
"""


def _validate_sql(
    sql_query: str
) -> str:

    sql = sql_query.strip()

    sql = re.sub(
        r"^```(?:sql)?\s*|\s*```$",
        "",
        sql,
        flags=re.IGNORECASE | re.DOTALL
    ).strip()

    if not re.match(
        r"^SELECT\b",
        sql,
        flags=re.IGNORECASE
    ):

        raise ValueError(
            "The LLM must generate a read-only SELECT statement."
        )

    return sql


def create_plan(
    perception: dict,
    previous_observation: dict | None = None,
    previous_sql: str | None = None
) -> dict:

    schema = perception[
        "database_schema"
    ]

    user_question = perception[
        "user_question"
    ]

    prompt = {
        "user_question": user_question,
        "database_schema": schema,
        "previous_sql": previous_sql,
        "previous_observation": previous_observation
    }

    response = call_llm(
        SYSTEM_PROMPT,
        str(prompt)
    )

    sql_query = response.get(
        "sql_query"
    )

    plan_summary = response.get(
        "plan_summary"
    )

    if (
        not isinstance(
            sql_query,
            str
        )
        or not sql_query.strip()
    ):

        raise RuntimeError(
            "LLM response did not contain a valid sql_query."
        )

    if not isinstance(
        plan_summary,
        str
    ):

        plan_summary = (
            "Generate SQL from the supplied "
            "request and database schema."
        )

    return {
        "sql_query": _validate_sql(
            sql_query
        ),
        "plan_summary": plan_summary.strip()
    }


def display_plan(
    plan: dict
) -> None:

    print(
        "\n===== PLAN ====="
    )

    print(
        "Plan summary:",
        plan["plan_summary"]
    )

    print(
        "SQL query:",
        plan["sql_query"]
    )


if __name__ == "__main__":

    from agent.perceive import perceive

    question = input(
        "Enter your database question: "
    )

    perception = perceive(
        question
    )

    plan = create_plan(
        perception
    )

    display_plan(
        plan
    )