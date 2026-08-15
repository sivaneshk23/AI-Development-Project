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


async def run_client() -> None:

    server_parameters = (
        StdioServerParameters(
            command=sys.executable,
            args=[
                str(SERVER_FILE)
            ],
            cwd=str(PROJECT_DIRECTORY),
        )
    )

    print(
        "Python executable:",
        sys.executable
    )

    print(
        "Server file:",
        SERVER_FILE
    )

    async with Client(
        stdio_client(server_parameters)
    ) as client:

        print(
            "\n=== MCP CLIENT CONNECTED ==="
        )

        print(
            "Protocol:",
            client.protocol_version
        )

        print(
            "Server:",
            client.server_info
        )

        print(
            "\n=== TOOLS ==="
        )

        tools = await client.list_tools()

        tool_names = [
            tool.name
            for tool in tools.tools
        ]

        print(
            tool_names
        )

        expected_tools = {
            "track_order",
            "check_stock",
            "initiate_return",
        }

        missing_tools = (
            expected_tools
            - set(tool_names)
        )

        if missing_tools:

            raise RuntimeError(
                "Missing MCP tools: "
                f"{sorted(missing_tools)}"
            )

        print(
            "All required tools discovered."
        )

        print(
            "\n=== TOOL SCHEMAS ==="
        )

        for tool in tools.tools:

            print(
                f"\n{tool.name}"
            )

            print(
            "Input schema:",
            tool.input_schema
            )

            print(
            "Output schema:",
            tool.output_schema
)

        print(
            "\n=== RESOURCES ==="
        )

        resources = (
            await client.list_resources()
        )

        resource_uris = [
            str(resource.uri)
            for resource in resources.resources
        ]

        print(
            resource_uris
        )

        expected_resource = (
            "ecommerce://summary"
        )

        if expected_resource not in (
            resource_uris
        ):

            raise RuntimeError(
                "Required resource was not discovered."
            )

        print(
            "Required resource discovered."
        )

        print(
            "\n=== RESOURCE READ ==="
        )

        resource_result = (
            await client.read_resource(
                expected_resource
            )
        )

        print(
            resource_result
        )

        print(
            "\n=== TRACK ORDER ==="
        )

        track_result = await client.call_tool(
            "track_order",
            {
                "order_id": "ORD1001"
            },
        )

        print(
            track_result
        )

        if track_result.is_error:

            raise RuntimeError(
                "track_order returned an error."
            )

        print(
            "track_order succeeded."
        )

        print(
            "\n=== CHECK STOCK ==="
        )

        stock_result = await client.call_tool(
            "check_stock",
            {
                "product_id": "P1001"
            },
        )

        print(
            stock_result
        )

        if stock_result.is_error:

            raise RuntimeError(
                "check_stock returned an error."
            )

        print(
            "check_stock succeeded."
        )

        print(
            "\n=== INITIATE RETURN ==="
        )

        return_result = await client.call_tool(
            "initiate_return",
            {
                "order_id": "ORD1002",
                "reason": "Product damaged",
            },
        )

        print(
            return_result
        )

        if return_result.is_error:

            raise RuntimeError(
                "initiate_return returned an error."
            )

        print(
            "initiate_return succeeded."
        )

        print(
            "\n=== ERROR CASE ==="
        )

        error_result = await client.call_tool(
            "track_order",
            {
                "order_id": "ORD9999"
            },
        )

        print(
            error_result
        )

        if error_result.is_error:

            print(
                "MCP protocol error received."
            )

        else:

            print(
                "Structured business error received."
            )

        print(
            "\n=== CLIENT VERIFICATION COMPLETE ==="
        )


def main() -> None:

    asyncio.run(
        run_client()
    )


if __name__ == "__main__":

    main()