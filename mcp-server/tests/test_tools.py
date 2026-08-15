from __future__ import annotations

from mcp_server.server import (
    check_stock,
    initiate_return,
    track_order,
)


def test_track_order_success() -> None:

    result = track_order(
        "ORD1001"
    )

    assert result.success is True
    assert result.order is not None
    assert result.order.order_id == "ORD1001"
    assert result.order.customer_name == "Arun"
    assert result.order.product_id == "P1001"
    assert result.order.product_name == "Wireless Keyboard"
    assert result.order.order_status == "Shipped"
    assert result.order.tracking_number == "TRK100001"
    assert result.error is None


def test_track_order_not_found() -> None:

    result = track_order(
        "ORD9999"
    )

    assert result.success is False
    assert result.order is None
    assert result.error == (
        "Order not found: ORD9999"
    )


def test_check_stock_success() -> None:

    result = check_stock(
        "P1001"
    )

    assert result.success is True
    assert result.product is not None
    assert result.product.product_id == "P1001"
    assert result.product.name == "Wireless Keyboard"
    assert result.product.stock_quantity == 25
    assert result.error is None


def test_check_stock_not_found() -> None:

    result = check_stock(
        "P9999"
    )

    assert result.success is False
    assert result.product is None
    assert result.error == (
        "Product not found: P9999"
    )


def test_initiate_return_success() -> None:

    result = initiate_return(
        "ORD1002",
        "Product damaged",
    )

    assert result.success is True
    assert result.return_data is not None
    assert result.return_data.order_id == "ORD1002"
    assert result.return_data.reason == (
        "Product damaged"
    )
    assert result.return_data.status == "Requested"
    assert result.error is None


def test_initiate_return_rejects_empty_reason() -> None:

    result = initiate_return(
        "ORD1002",
        "   ",
    )

    assert result.success is False
    assert result.return_data is None
    assert result.error == (
        "Return reason cannot be empty."
    )