from __future__ import annotations

import sqlite3

from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "ecommerce.db"
)


def get_connection() -> sqlite3.Connection:

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


def get_product(
    product_id: str
) -> dict | None:

    connection = get_connection()

    try:

        row = connection.execute(
            """
            SELECT
                product_id,
                name,
                category,
                price,
                stock_quantity
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()


def get_order(
    order_id: str
) -> dict | None:

    connection = get_connection()

    try:

        row = connection.execute(
            """
            SELECT
                o.order_id,
                o.customer_name,
                o.product_id,
                p.name AS product_name,
                o.quantity,
                o.order_status,
                o.tracking_number
            FROM orders o
            JOIN products p
                ON p.product_id = o.product_id
            WHERE o.order_id = ?
            """,
            (order_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()


def create_return(
    order_id: str,
    reason: str
) -> dict:

    connection = get_connection()

    try:

        order = connection.execute(
            """
            SELECT
                order_id,
                order_status
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        ).fetchone()

        if order is None:

            raise ValueError(
                f"Order not found: {order_id}"
            )

        if order["order_status"] != "Delivered":

            raise ValueError(
                "Return can only be initiated "
                "for delivered orders."
            )

        cursor = connection.execute(
            """
            INSERT INTO returns (
                order_id,
                reason,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                order_id,
                reason,
                "Requested"
            )
        )

        connection.commit()

        return {
            "return_id": cursor.lastrowid,
            "order_id": order_id,
            "reason": reason,
            "status": "Requested"
        }

    finally:

        connection.close()


def get_dataset_summary() -> dict:

    connection = get_connection()

    try:

        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        order_count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        return_count = connection.execute(
            "SELECT COUNT(*) FROM returns"
        ).fetchone()[0]

        return {
            "database": "SQLite",
            "products": product_count,
            "orders": order_count,
            "returns": return_count
        }

    finally:

        connection.close()