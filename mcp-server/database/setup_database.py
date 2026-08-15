from __future__ import annotations

import sqlite3

from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent
    / "ecommerce.db"
)


def create_database() -> None:

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS returns;

        DROP TABLE IF EXISTS orders;

        DROP TABLE IF EXISTS products;


        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
        );


        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            order_status TEXT NOT NULL,
            tracking_number TEXT,
            FOREIGN KEY (
                product_id
            )
            REFERENCES products(product_id)
        );


        CREATE TABLE returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (
                order_id
            )
            REFERENCES orders(order_id)
        );
        """
    )

    products = [
        (
            "P1001",
            "Wireless Keyboard",
            "Electronics",
            1499.00,
            25
        ),
        (
            "P1002",
            "Wireless Mouse",
            "Electronics",
            799.00,
            40
        ),
        (
            "P1003",
            "USB-C Hub",
            "Accessories",
            1299.00,
            12
        ),
        (
            "P1004",
            "Laptop Stand",
            "Accessories",
            999.00,
            0
        ),
        (
            "P1005",
            "Webcam",
            "Electronics",
            2499.00,
            8
        )
    ]

    cursor.executemany(
        """
        INSERT INTO products (
            product_id,
            name,
            category,
            price,
            stock_quantity
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        products
    )

    orders = [
        (
            "ORD1001",
            "Arun",
            "P1001",
            1,
            "Shipped",
            "TRK100001"
        ),
        (
            "ORD1002",
            "Priya",
            "P1003",
            2,
            "Delivered",
            "TRK100002"
        ),
        (
            "ORD1003",
            "Rahul",
            "P1004",
            1,
            "Processing",
            None
        ),
        (
            "ORD1004",
            "Divya",
            "P1005",
            1,
            "Shipped",
            "TRK100004"
        )
    ]

    cursor.executemany(
        """
        INSERT INTO orders (
            order_id,
            customer_name,
            product_id,
            quantity,
            order_status,
            tracking_number
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        orders
    )

    connection.commit()
    connection.close()

    print(
        f"Database created: {DATABASE_PATH}"
    )


if __name__ == "__main__":
    create_database()