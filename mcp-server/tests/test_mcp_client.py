from __future__ import annotations

import asyncio
import sys

from pathlib import Path

from mcp import (
    Client,
    StdioServerParameters,
)

from mcp.client.stdio import (
    stdio_client,
)


PROJECT_DIRECTORY = (
    Path(__file__).resolve().parent.parent
)

SERVER_FILE = (
    PROJECT_DIRECTORY
    / "mcp_server"
    / "server.py"
)


async def verify_mcp_client() -> None:

    server_parameters = (
        StdioServerParameters(
            command=sys.executable,
            args=[
                str(SERVER_FILE)
            ],
            cwd=str(PROJECT_DIRECTORY),
        )
    )

    async with Client(
        stdio_client(server_parameters)
    ) as client:

        tools = await client.list_tools()

        tool_names = {
            tool.name
            for tool in tools.tools
        }

        assert tool_names == {
            "track_order",
            "check_stock",
            "initiate_return",
        }

        for tool in tools.tools:

            assert tool.input_schema is not None
            assert tool.output_schema is not None

        resources = (
            await client.list_resources()
        )

        resource_names = {
            str(resource.uri)
            for resource in resources.resources
        }

        assert (
            "ecommerce://summary"
            in resource_names
        )

        resource_result = (
            await client.read_resource(
                "ecommerce://summary"
            )
        )

        assert resource_result is not None

        track_result = await client.call_tool(
            "track_order",
            {
                "order_id": "ORD1001"
            },
        )

        assert not track_result.is_error

        stock_result = await client.call_tool(
            "check_stock",
            {
                "product_id": "P1001"
            },
        )

        assert not stock_result.is_error

        return_result = await client.call_tool(
            "initiate_return",
            {
                "order_id": "ORD1002",
                "reason": "Product damaged",
            },
        )

        assert not return_result.is_error

        error_result = await client.call_tool(
            "track_order",
            {
                "order_id": "ORD9999"
            },
        )

        assert not error_result.is_error

        assert error_result.content is not None


def test_real_mcp_client_connection() -> None:

    asyncio.run(
        verify_mcp_client()
    )