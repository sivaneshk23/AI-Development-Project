# Cycle 2 — Requirements

## Selected Use Case

UC4 — E-Commerce Order MCP Server

## Mandatory MCP Tools

### 1. track_order

Input:

- `order_id: string`

Output:

- success status
- order information or error

Purpose:

Retrieve the current status and tracking information for an order.

---

### 2. check_stock

Input:

- `product_id: string`

Output:

- success status
- product information
- stock quantity
- error when the product does not exist

Purpose:

Retrieve product and inventory information.

---

### 3. initiate_return

Input:

- `order_id: string`
- `reason: string`

Output:

- success status
- return information or error

Purpose:

Create a return request for an eligible delivered order.

---

## Resource

Resource URI:

`ecommerce://summary`

Purpose:

Expose a read-only summary of the e-commerce dataset.

---

## Transport

The server uses:

`stdio`

for local MCP client communication.

---

## Database

SQLite.

Tables:

- products
- orders
- returns

---

## Invocation Logging

Every tool invocation records:

- UTC timestamp
- tool name
- sanitized arguments
- success/failure
- error when applicable

Log:

`logs/mcp_invocations.jsonl`

---

## Verification Requirements

The completed cycle must be verified using:

1. MCP Inspector
2. A real MCP client
3. Live end-to-end tool invocation
4. Automated tests
5. Error-case testing

---

## Security

No secrets or credentials are required by the local server.

Runtime logs and local database files are development artifacts and should not expose sensitive customer information.