from __future__ import annotations

from mcp_server.server import (
    CheckStockOutput,
    InitiateReturnOutput,
    TrackOrderOutput,
)


def test_track_order_output_schema() -> None:

    schema = (
        TrackOrderOutput.model_json_schema()
    )

    properties = schema["properties"]

    assert "success" in properties
    assert "order" in properties
    assert "error" in properties


def test_check_stock_output_schema() -> None:

    schema = (
        CheckStockOutput.model_json_schema()
    )

    properties = schema["properties"]

    assert "success" in properties
    assert "product" in properties
    assert "error" in properties


def test_initiate_return_output_schema() -> None:

    schema = (
        InitiateReturnOutput.model_json_schema()
    )

    properties = schema["properties"]

    assert "success" in properties
    assert "return" in properties
    assert "error" in properties

    assert "return_data" not in properties