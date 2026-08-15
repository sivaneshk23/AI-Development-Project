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


# ============================================================
# Structured output models
# ============================================================


class OrderData(BaseModel):
    order_id: str
    customer_name: str
    product_id: str
    product_name: str
    quantity: int
    order_status: str
    tracking_number: str


class ProductData(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    stock_quantity: int


class ReturnData(BaseModel):
    return_id: int
    order_id: str
    reason: str
    status: str


class TrackOrderOutput(BaseModel):
    success: bool
    order: OrderData | None = None
    error: str | None = None


class CheckStockOutput(BaseModel):
    success: bool
    product: ProductData | None = None
    error: str | None = None


class InitiateReturnOutput(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    success: bool

    return_data: ReturnData | None = Field(
        default=None,
        alias="return",
    )

    error: str | None = None


# ============================================================
# Explicit model rebuild
# ============================================================

OrderData.model_rebuild()
ProductData.model_rebuild()
ReturnData.model_rebuild()

TrackOrderOutput.model_rebuild()
CheckStockOutput.model_rebuild()
InitiateReturnOutput.model_rebuild()


# ============================================================
# MCP server
# ============================================================


mcp = MCPServer(
    name="ecommerce-order-server"
)


# ============================================================
# Tool 1: Track Order
# ============================================================


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

        order_data = OrderData(
            order_id=order["order_id"],
            customer_name=order["customer_name"],
            product_id=order["product_id"],
            product_name=order["product_name"],
            quantity=order["quantity"],
            order_status=order["order_status"],
            tracking_number=order["tracking_number"],
        )

        result = TrackOrderOutput(
            success=True,
            order=order_data,
            error=None,
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
            order=None,
            error=str(error),
        )


# ============================================================
# Tool 2: Check Stock
# ============================================================


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

        product_data = ProductData(
            product_id=product["product_id"],
            name=product["name"],
            category=product["category"],
            price=product["price"],
            stock_quantity=product["stock_quantity"],
        )

        result = CheckStockOutput(
            success=True,
            product=product_data,
            error=None,
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
            product=None,
            error=str(error),
        )


# ============================================================
# Tool 3: Initiate Return
# ============================================================


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

        return_record = create_return(
            order_id=order_id,
            reason=cleaned_reason,
        )

        return_data = ReturnData(
            return_id=return_record["return_id"],
            order_id=return_record["order_id"],
            reason=return_record["reason"],
            status=return_record["status"],
        )

        result = InitiateReturnOutput(
            success=True,
            return_data=return_data,
            error=None,
        )

        log_invocation(
            tool_name="initiate_return",
            arguments={
                "order_id": order_id,
                "reason": cleaned_reason,
            },
            success=True,
        )

        return result

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
            return_data=None,
            error=str(error),
        )


# ============================================================
# MCP Resource
# ============================================================


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


# ============================================================
# Server entry point
# ============================================================


if __name__ == "__main__":
    mcp.run()