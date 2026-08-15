# Cycle 2 — MCP Server

## Selected Use Case

UC4 — E-Commerce Order MCP Server

## Topic

MCP Server

## Cycle

Day 16 – Day 30

## Official Deadline

27 August 2026

## Objective

Build a working local MCP server that exposes e-commerce order and
inventory capabilities through standardized MCP tools and a resource.

## Mandatory Tools

### track_order

Retrieve order status and tracking information for a supplied order ID.

### check_stock

Retrieve product information and current stock quantity for a supplied
product ID.

### initiate_return

Create a return request for an eligible order using a supplied reason.

## Mandatory Resource

Expose a read-only e-commerce data resource that allows an MCP client
to retrieve a useful summary of the available products/orders dataset.

## Transport

stdio for local testing.

## Database

SQLite mock e-commerce database.

## Verification

MCP Inspector.

## MCP Client

A real MCP client or custom MCP client script will connect to the server
and perform a live tool invocation.

## Audit Logging

Every tool invocation must record:

- timestamp
- tool name
- sanitized arguments
- success/failure status

## Required Demonstrations

1. Discover the MCP server.
2. Discover the three tools.
3. Verify their schemas.
4. Discover/read the resource.
5. Invoke a tool successfully.
6. Demonstrate a meaningful error case.
7. Show the invocation log.