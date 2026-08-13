import json

from agent import logger


def test_iteration_logging(
    tmp_path,
    monkeypatch
):

    log_path = (
        tmp_path
        / "agent_trace.jsonl"
    )

    monkeypatch.setattr(
        logger,
        "LOG_PATH",
        log_path
    )

    logger.log_iteration(
        {
            "iteration": 1,
            "plan": {
                "plan_summary":
                    "Return employees."
            },
            "action": {
                "tool":
                    "execute_sql"
            },
            "observation": {
                "status":
                    "success"
            },
            "success": True
        }
    )

    lines = log_path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 1

    record = json.loads(
        lines[0]
    )

    assert (
        record["iteration"]
        == 1
    )

    assert (
        record["success"]
        is True
    )