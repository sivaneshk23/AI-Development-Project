# AI Development Project

## Cycle 1 — Agent Loop

### Selected Use Case

**UC3 — Self-Correcting SQL Agent**

This project implements a single-agent loop that converts a natural-language
database request into a read-only SQL query, executes the query against a
local SQLite database, observes the result, and retries with a corrected
query when execution fails or returns zero rows.

The agent follows:

Perceive → Plan → Act → Observe

until a valid non-empty result is obtained or the maximum iteration limit
is reached.

---

## Problem Statement

Users may know what information they need from a database without knowing
the SQL syntax required to retrieve it.

The Self-Correcting SQL Agent accepts a natural-language request and uses
a local Large Language Model through Ollama to generate a SQL query.

If the generated SQL fails or produces no rows, the result is passed back
into the next planning iteration so the model can correct the query.

---

## Architecture

```text
User
  |
  v
Agent Loop
  |
  +--> PERCEIVE
  |       |
  |       +--> User Request
  |       +--> Database Schema
  |
  +--> PLAN
  |       |
  |       +--> Ollama
  |              |
  |              +--> SQL Query
  |              +--> Plan Summary
  |
  +--> ACT
  |       |
  |       +--> Schema Inspection Tool
  |       |
  |       +--> SQL Execution Tool
  |                    |
  |                    v
  |               SQLite Database
  |
  +--> OBSERVE
          |
          +--> Success + Non-empty Result
          |          |
          |          v
          |         STOP
          |
          +--> Error / Zero Rows
                     |
                     v
                 Next Plan