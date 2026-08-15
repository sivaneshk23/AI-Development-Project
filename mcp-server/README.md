# Cycle 2 — E-Commerce Order MCP Server

## 1. Project Overview

This project implements **Cycle 2 — MCP Server** of the AI Development Preparation assignment.

### Selected Use Case

**UC4 — E-Commerce Order MCP Server**

The server exposes e-commerce order, inventory, and return-management capabilities through the Model Context Protocol (MCP).

The implementation uses a local SQLite database containing mock product, order, and return data.

---

## 2. Problem Statement

E-commerce applications commonly need standardized access to order status, inventory information, and return operations.

This project provides those capabilities through an MCP server so that an MCP-compatible client can discover the available tools and invoke them using structured inputs and outputs.

The system supports:

- retrieving order status and tracking information
- checking product information and available stock
- initiating a return request for an eligible order
- reading a read-only summary of the e-commerce dataset

---

## 3. Mandatory Cycle 2 Requirements

| Requirement | Implementation |
|---|---|
| Official MCP SDK | Python `mcp` package |
| MCP tools | `track_order`, `check_stock`, `initiate_return` |
| Minimum tools | 3 |
| Tool input schemas | Explicit Python type annotations |
| Tool output schemas | Pydantic structured models |
| MCP resource | `ecommerce://summary` |
| Local transport | stdio |
| MCP Inspector | Verified |
| Real MCP client | Custom Python MCP client |
| Live end-to-end call | Verified |
| Invocation logging | Timestamped JSONL logging |
| Database | SQLite |

---

## 4. Architecture

```text
                    ┌──────────────────────┐
                    │   MCP Client         │
                    │ Custom Python Client │
                    └──────────┬───────────┘
                               │
                               │ stdio
                               ▼
                    ┌──────────────────────┐
                    │   MCP Server         │
                    │  ecommerce-order     │
                    │      server          │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       track_order       check_stock     initiate_return
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    SQLite Database   │
                    │ products / orders /  │
                    │ returns              │
                    └──────────────────────┘

                    ┌──────────────────────┐
                    │ ecommerce://summary  │
                    │ Read-only Resource   │
                    └──────────────────────┘

                    ┌──────────────────────┐
                    │ Invocation Logger   │
                    │ Timestamp + tool +  │
                    │ sanitized arguments │
                    └──────────────────────┘