from __future__ import annotations

import json

from datetime import (
    datetime,
    timezone
)

from pathlib import Path


LOG_PATH = (
    Path(__file__).resolve().parent.parent
    / "logs"
    / "agent_trace.jsonl"
)


def utc_timestamp() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def log_iteration(
    entry: dict
) -> None:

    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with LOG_PATH.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                entry,
                ensure_ascii=False,
                default=str
            )
            + "\n"
        )