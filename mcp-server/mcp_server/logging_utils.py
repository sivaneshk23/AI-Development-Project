from __future__ import annotations

import json

from datetime import datetime, timezone
from pathlib import Path


LOG_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "logs"
)

LOG_FILE = (
    LOG_DIRECTORY
    / "mcp_invocations.jsonl"
)


def log_invocation(
    tool_name: str,
    arguments: dict,
    success: bool,
    error: str | None = None
) -> None:

    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    sanitized_arguments = {
        str(key): str(value)
        for key, value in arguments.items()
    }

    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "tool": tool_name,

        "arguments": sanitized_arguments,

        "success": success,

        "error": error
    }

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                record,
                ensure_ascii=False
            )
            + "\n"
        )