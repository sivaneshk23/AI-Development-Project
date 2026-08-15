from __future__ import annotations

from typing import Any

from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict, Field


try:

    from mcp_server.database import (
        create_return,
        get_dataset_summary,
        get_order,
        get_product,
    )

    from mcp_server.logging_utils import (
        log_invocation,
    )

except ModuleNotFoundError:

    from database import (
        create_return,
        get_dataset_summary,
        get_order,
        get_product,
    )

    from logging_utils import (
        log_invocation,
    )


mcp = MCPServer(
    name="ecommerce-order-server"
)


class OrderData(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    order_id: str
    customer_name: str
    product_id: str
    product_name: str
    quantity: int
    order_status: str
    tracking_number: str


class TrackOrderOutput(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    success: bool
    order: OrderData | None = None
    error: str | None = None


class ProductData(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    product_id: str
    name: str
    category: str
    price: float
    stock_quantity: int


class CheckStockOutput(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    success: bool
    product: ProductData | None = None
    error: str | None = None


class ReturnData(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    return_id: int
    order_id: str
    reason: str
    status: str


class InitiateReturnOutput(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    success: bool
    return_data: ReturnData | None = Field(
        default=None,
        alias="return"
    )
    error: str | None = None


@mcp.tool()
def track_order(
    order_id: str,
) -> TrackOrderOutput:
    """
    Retrieve the current status and tracking
    information for an e-commerce order.
    """

    try:

        order = get_order(
            order_id
        )

        if order is None:

            raise ValueError(
                f"Order not found: {order_id}"
            )

        result = TrackOrderOutput(
            success=True,
            order=OrderData(
                **order
            ),
        )

        log_invocation(
            tool_name="track_order",
            arguments={
                "order_id": order_id,
            },
            success=True,
        )

        return result

    except Exception as error:

        log_invocation(
            tool_name="track_order",
            arguments={
                "order_id": order_id,
            },
            success=False,
            error=str(error),
        )

        return TrackOrderOutput(
            success=False,
            error=str(error),
        )


@mcp.tool()
def check_stock(
    product_id: str,
) -> CheckStockOutput:
    """
    Retrieve product details and current
    available stock quantity.
    """

    try:

        product = get_product(
            product_id
        )

        if product is None:

            raise ValueError(
                f"Product not found: {product_id}"
            )

        result = CheckStockOutput(
            success=True,
            product=ProductData(
                **product
            ),
        )

        log_invocation(
            tool_name="check_stock",
            arguments={
                "product_id": product_id,
            },
            success=True,
        )

        return result

    except Exception as error:

        log_invocation(
            tool_name="check_stock",
            arguments={
                "product_id": product_id,
            },
            success=False,
            error=str(error),
        )

        return CheckStockOutput(
            success=False,
            error=str(error),
        )


@mcp.tool()
def initiate_return(
    order_id: str,
    reason: str,
) -> InitiateReturnOutput:
    """
    Initiate a return request for an eligible
    delivered e-commerce order.
    """

    try:

        cleaned_reason = reason.strip()

        if not cleaned_reason:

            raise ValueError(
                "Return reason cannot be empty."
            )

        result = create_return(
            order_id=order_id,
            reason=cleaned_reason,
        )

        response = InitiateReturnOutput(
    success=True,
    return_data=ReturnData(
        **result
    ),
)

        log_invocation(
            tool_name="initiate_return",
            arguments={
                "order_id": order_id,
                "reason": cleaned_reason,
            },
            success=True,
        )

        return response

    except Exception as error:

        log_invocation(
            tool_name="initiate_return",
            arguments={
                "order_id": order_id,
                "reason": reason,
            },
            success=False,
            error=str(error),
        )

        return InitiateReturnOutput(
            success=False,
            error=str(error),
        )


@mcp.resource(
    "ecommerce://summary"
)
def ecommerce_summary() -> str:
    """
    Return a read-only summary of the
    e-commerce dataset.
    """

    summary = get_dataset_summary()

    return (
        "E-Commerce Dataset Summary\n"
        f"Database: {summary['database']}\n"
        f"Products: {summary['products']}\n"
        f"Orders: {summary['orders']}\n"
        f"Returns: {summary['returns']}"
    )


if __name__ == "__main__":

    mcp.run()