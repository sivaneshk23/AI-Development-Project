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