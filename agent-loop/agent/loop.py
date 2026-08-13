from __future__ import annotations

import os

from agent.perceive import perceive
from agent.planner import create_plan
from agent.act import act
from agent.observe import observe
from agent.logger import (
    log_iteration,
    utc_timestamp
)


MAX_ITERATIONS = int(
    os.getenv(
        "MAX_ITERATIONS",
        "3"
    )
)


def run_agent(
    question: str,
    initial_query: str | None = None,
    planner=create_plan
) -> dict:

    print(
        "\n===== AGENT LOOP ====="
    )

    previous_observation = None
    previous_sql = None

    for iteration in range(
        1,
        MAX_ITERATIONS + 1
    ):

        print(
            f"\n===== ITERATION "
            f"{iteration}/{MAX_ITERATIONS} ====="
        )

        # =========================
        # PERCEIVE
        # =========================

        perception = perceive(
            question
        )

        print(
            "\n===== PERCEIVE ====="
        )

        print(
            "User Question:",
            perception["user_question"]
        )

        print(
            "Database Schema:",
            perception["database_schema"]
        )

        # =========================
        # PLAN
        # =========================

        plan = planner(
            perception,
            previous_observation=(
                previous_observation
            ),
            previous_sql=previous_sql
        )

        sql_query = (
            initial_query
            if (
                iteration == 1
                and initial_query
            )
            else plan["sql_query"]
        )

        print(
            "\n===== PLAN ====="
        )

        print(
            "Plan summary:",
            plan["plan_summary"]
        )

        print(
            "SQL query:",
            sql_query
        )

        # =========================
        # ACT
        # =========================

        action = act(
            sql_query
        )

        print(
            "\n===== ACT ====="
        )

        print(
            "Tools called:",
            [
                item["tool"]
                for item in action[
                    "tools_called"
                ]
            ]
        )

        print(
            "SQL query:",
            sql_query
        )

        print(
            "SQL result:",
            action["result"]
        )

        # =========================
        # OBSERVE
        # =========================

        observation = observe(
            action
        )

        success = (
            observation["status"]
            == "success"
            and observation["has_rows"]
        )

        print(
            "\n===== OBSERVE ====="
        )

        print(
            "Status:",
            observation["status"]
        )

        print(
            "Message:",
            observation["message"]
        )

        print(
            "Should retry:",
            observation["should_retry"]
        )

        # =========================
        # LOG ITERATION
        # =========================

        log_iteration(
            {
                "timestamp": utc_timestamp(),
                "iteration": iteration,

                "perceive": perception,

                "plan": {
                    "plan_summary": (
                        plan["plan_summary"]
                    ),
                    "sql_query": sql_query
                },

                "action": action,

                "observation": observation,

                "success": success
            }
        )

        # =========================
        # SUCCESS CONDITION
        # =========================

        if success:

            print(
                "\n===== AGENT COMPLETED ====="
            )

            return {
                "status": "success",
                "query": sql_query,
                "observation": observation,
                "iterations": iteration
            }

        previous_observation = (
            observation
        )

        previous_sql = (
            sql_query
        )

        # =========================
        # RETRY DECISION
        # =========================

        if not observation[
            "should_retry"
        ]:

            break

    print(
        "\n===== AGENT STOPPED ====="
    )

    if (
        previous_observation
        and previous_observation[
            "status"
        ] == "zero_rows"
    ):

        final_status = "no_results"

    else:

        final_status = "failed"

    return {
        "status": final_status,
        "query": previous_sql,
        "observation": previous_observation,
        "iterations": MAX_ITERATIONS
    }


if __name__ == "__main__":

    question = input(
        "Enter your database question: "
    )

    result = run_agent(
        question
    )

    print(
        "\n===== FINAL RESULT ====="
    )

    print(
        result
    )