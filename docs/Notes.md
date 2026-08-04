# Notes

This folder contains learning notes, references, and implementation details collected during the AI Development project.

## Development Progress - 02/08/2026

### Tool Layer Implementation

Implemented the initial tool layer for the Self-Correcting SQL Agent.

### Schema Inspection Tool

Created `tools/schema_tool.py`.

The tool connects to the SQLite database and dynamically retrieves:

- Available database tables
- Column names
- Column data types

The tool was successfully tested with the sample employee database.

Detected schema:

- Table: employees
- id - INTEGER
- name - TEXT
- department - TEXT
- salary - REAL

### SQL Execution Tool

Created `tools/sql_tool.py`.

The tool accepts an SQL query, executes it against the SQLite database and returns a structured result containing:

- Execution status
- Column names
- Query results
- Error information

### Successful Query Test

Test query:

SELECT * FROM employees;

The query successfully returned all five employee records.

### Error Handling Test

An intentionally invalid query was tested:

SELECT * FROM definitely_not_a_real_table;

The SQL execution tool successfully captured the database error:

no such table: definitely_not_a_real_table

The application handled the error without crashing.

### Current Status

The project currently provides two callable tools:

1. Database Schema Inspection Tool
2. SQL Execution Tool

These tools will later be integrated into the Perceive-Plan-Act-Observe agent loop.

### Next Development Milestone

The next milestone is to begin implementing the agent loop and integrate an actual LLM for SQL generation and correction.

## Development Progress - 03/08/2026

### Perceive and Plan Pipeline

Implemented the initial Perceive and Plan stages of the Self-Correcting SQL Agent.

### Perceive Stage

Created `agent/perceive.py`.

The Perceive stage collects:

- The user's natural-language database question
- The actual database schema retrieved through the Schema Inspection Tool

This ensures that the agent has access to the real database structure before planning an operation.

### Plan Stage

Created `agent/planner.py`.

The current planner is a deterministic rule-based prototype that converts the perceived information into structured execution steps.

The planner currently recognizes basic requests involving:

- Employee records
- Department filtering
- Salary-related requests
- Listing employee records

### Testing

The following questions were tested successfully:

1. `Show all employees from the IT department.`
2. `Show employee salary details.`
3. `List all employees.`

The Perceive stage correctly displayed the `employees` table containing:

- id - INTEGER
- name - TEXT
- department - TEXT
- salary - REAL

### Rule-Based Planner Limitation

The following natural-language question was also tested:

`Who earns the highest amount?`

The current planner could not infer that "highest amount" refers to the `salary` column.

This is an expected limitation of the deterministic prototype and demonstrates the need for LLM-based natural-language reasoning.

### Python Package Execution

The agent modules are executed from the project root using:

`py -m agent.perceive`

and:

`py -m agent.planner`

This preserves the correct Python package import context.

### Current Agent Pipeline

User Question

↓

Perceive

↓

User Question + Database Schema

↓

Plan

↓

Structured Execution Plan

### Next Development Milestone

The next milestone is to continue the agent loop by connecting planning with executable actions and observation of tool results. LLM integration will later replace or enhance the deterministic planning logic for natural-language reasoning.

## Development Progress - 04/08/2026

### ACT Stage Implementation

Implemented the ACT stage of the Self-Correcting SQL Agent.

Created:

`agent/act.py`

The ACT stage receives a SQL query and invokes the existing SQL Execution Tool.

The ACT stage is responsible for tool execution only. SQL generation will later be handled by the LLM-based reasoning/planning component.

### Current Execution Flow

User Question

↓

PERCEIVE

↓

PLAN

↓

ACT

↓

SQL Execution Tool

↓

SQLite Database

### ACT Stage Responsibilities

The ACT stage:

- Receives a SQL query
- Invokes the `execute_sql()` tool
- Stores the executed SQL query
- Stores the tool execution result
- Preserves successful query results
- Preserves SQL error information
- Handles zero-row query results without crashing

### Manual Testing

The ACT stage was manually tested with:

1. A valid department query
2. A valid salary-ordering query
3. An invalid table query
4. A valid query returning zero rows

The system correctly distinguished between:

- Successful queries containing records
- Successful queries returning zero records
- Failed SQL queries

### Automated Testing

Created:

`tests/test_act.py`

Automated tests verified:

- Successful SQL execution
- Salary query execution
- SQL tool failure handling
- Zero-row result handling

Final automated test result:

**4/4 tests passed**

### Current Limitation

The current ACT stage does not generate SQL from natural-language questions.

The existing PLAN stage is also still a deterministic prototype.

A real LLM must later be integrated into the planning/reasoning stage to satisfy the Agent Loop assignment requirement.

### Next Development Milestone

The next stage is OBSERVE.

OBSERVE will analyze the result returned by ACT and determine whether:

- The query succeeded with useful records
- The query returned zero rows
- The SQL execution failed

This observation will later support retry and self-correction behavior.