# Cycle 1 - Architecture Plan

## Self-Correcting SQL Agent

The system follows a single-agent iterative loop.

## High-Level Flow

User
↓
Natural Language Request
↓
Agent

### Perceive

Read the user's request and the previous observation.

↓

### Plan

Send the request, database schema and previous observation to a real LLM.

The LLM generates or corrects an SQL query.

↓

### Act

The agent selects and calls an available tool.

Available tools:

1. Inspect Database Schema
2. Execute SQL Query

↓

### Observe

Capture:

- SQL result
- SQL error
- Empty result

↓

### Decision

If a valid non-empty result is obtained:

SUCCESS → Stop

Otherwise:

Return observation to Plan → Try again

If maximum iterations are reached:

TERMINATE

## Architecture

User
  |
  v
Agent Loop
  |
  +----> Perceive
  |        |
  |        v
  +----> Plan
  |        |
  |        v
  |      Real LLM
  |        |
  |        v
  +----> Act
  |        |
  |        +----> Schema Inspection Tool
  |        |
  |        +----> SQL Execution Tool
  |                   |
  |                   v
  |              Sample Database
  |
  +----> Observe
           |
           +---- Success ----> Stop
           |
           +---- Failure ----> Repeat

## Logging

Every loop iteration will be recorded in a log file for debugging, evaluation and demonstration.

## Safety

The initial implementation will operate only on a local sample database.

The SQL execution tool will be restricted according to the project requirements during implementation.