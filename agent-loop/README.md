# Cycle 1 — Self-Correcting SQL Agent

## 1. Project Overview

This project implements Cycle 1 (Agent Loop) of the AI Development Preparation assignment.

The selected use case is **UC3 — Self-Correcting SQL Agent**.

The system accepts a natural-language database request, uses a real local LLM to generate a SQL plan, executes the SQL through callable tools, observes the result, and automatically retries with a corrected plan when the tool execution fails or produces no rows.

The implementation follows the required agent-loop stages:

**Perceive → Plan → Act → Observe**

The loop has both:
- a maximum iteration limit, and
- an explicit success-condition check.

A tool failure is handled inside the loop without crashing the program.

---

## 2. Problem Statement

Users should be able to ask questions about a sample employee database using natural language instead of writing SQL manually.

The agent must:

1. Understand the user's database question.
2. Inspect the available database schema.
3. Use a real LLM to generate an appropriate SQL query.
4. Execute the SQL through callable tools.
5. Inspect the execution result.
6. Detect SQL errors or empty results.
7. Revise the SQL plan when necessary.
8. Re-execute the corrected query.
9. Stop only when the success condition is satisfied or the maximum iteration limit is reached.
10. Record each iteration in a file-based trace log.

---

## 3. Selected Use Case

### UC3 — Self-Correcting SQL Agent

The assignment defines this use case as a loop that:

**generate SQL → execute → if it errors or returns zero rows, revise the query → re-execute, until a valid non-empty result is returned.**

This implementation uses a local SQLite employee database and a local Ollama LLM.

---

## 4. Architecture

The system follows this architecture:

```text
                    ┌─────────────────────────┐
                    │      User Question      │
                    │  Natural-language input │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │        PERCEIVE          │
                    │ Extract question +      │
                    │ inspect database schema │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │          PLAN           │
                    │ Real Ollama LLM         │
                    │ qwen3.5:9b              │
                    │ Generates SQL + summary │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │           ACT           │
                    │ Callable database tools │
                    │ 1. inspect schema       │
                    │ 2. execute SQL          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │         OBSERVE         │
                    │ Check execution status  │
                    │ and returned rows       │
                    └────────────┬────────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
              Success condition        Error / zero rows
                     │                       │
                     ▼                       ▼
                  ┌──────┐          ┌─────────────────┐
                  │ STOP │          │ Retry planning  │
                  └──────┘          │ with observation│
                                    └───────┬─────────┘
                                            │
                                            └──────► PLAN
```

The editable one-page architecture diagram is provided separately as:

`docs/Architecture_Cycle1.drawio`

The exported visual version is:

`docs/Architecture_Cycle1.png`

---

## 5. Project Structure

```text
agent-loop/
│
├── agent/
│   ├── __init__.py
│   ├── act.py
│   ├── llm.py
│   ├── logger.py
│   ├── loop.py
│   ├── observe.py
│   ├── perceive.py
│   ├── planner.py
│   └── self_correct.py
│
├── database/
│   ├── setup_database.py
│   └── sample.db
│
├── docs/
│   ├── Architecture.md
│   ├── Architecture_Cycle1.drawio
│   ├── Architecture_Cycle1.png
│   ├── Notes.md
│   ├── Project_Plan.md
│   ├── Requirements.md
│   └── Topic_Selection.md
│
├── logs/
│   └── agent_trace.jsonl
│
├── tests/
│   ├── test_act.py
│   ├── test_logger.py
│   ├── test_loop.py
│   ├── test_observe.py
│   ├── test_planner.py
│   └── test_self_correct.py
│
├── tools/
│   ├── __init__.py
│   ├── schema_tool.py
│   └── sql_tool.py
│
└── README.md
```

Runtime-generated logs are kept local and are excluded from version control.

---

## 6. Agent Loop Stages

### 6.1 Perceive

The Perceive stage receives the user's natural-language question and obtains the available database schema.

Example:

```text
User Question:
Who earns the highest salary?

Database Schema:
employees
- id INTEGER
- name TEXT
- department TEXT
- salary REAL
```

### 6.2 Plan

The Plan stage calls the real local Ollama LLM.

The model receives the user question and database schema and returns structured JSON containing:

- `sql_query`
- `plan_summary`

No hardcoded if/else logic is used to pretend that the system is reasoning.

### 6.3 Act

The Act stage invokes callable database tools.

The implemented tools are:

1. `inspect_database_schema`
2. `execute_sql`

### 6.4 Observe

The Observe stage evaluates the tool result.

A successful execution with a non-empty result satisfies the success condition.

An SQL error or zero-row result causes the loop to retry.

### 6.5 Termination

The agent uses:

- a maximum iteration count of 3, and
- an explicit success condition.

The agent stops when:

```text
status == success
AND
the result contains rows
```

If the maximum number of iterations is reached without success, the loop terminates instead of continuing indefinitely.

---

## 7. Self-Correction and Failure Recovery

The system demonstrates recovery from an SQL tool failure.

Example deliberate failure:

```sql
SELECT * FROM employeez;
```

The table does not exist.

The first iteration produces:

```text
Status: error
Message: no such table: employeez
Should retry: True
```

The observation is supplied to the next planning iteration.

The LLM then corrects the table name:

```sql
SELECT * FROM employees;
```

The second iteration succeeds and returns the employee records.

This demonstrates that a tool failure is handled inside the loop rather than crashing the program.

---

## 8. Database

The project uses a local SQLite database.

### Table

`employees`

### Columns

| Column | Type |
|---|---|
| id | INTEGER |
| name | TEXT |
| department | TEXT |
| salary | REAL |

The database is created using:

```text
database/setup_database.py
```

---

## 9. Technology Stack

### Programming Language

Python **3.14.6**

### LLM

Ollama local model:

```text
qwen3.5:9b
```

### Ollama Python Client

```text
ollama 0.6.2
```

### Environment Configuration

```text
python-dotenv 1.2.2
```

### Database

SQLite

### Testing

pytest

The exact installed versions above were verified in the development environment.

---

## 10. Prerequisites

Install or have available:

- Python 3.14.6
- Ollama
- the `qwen3.5:9b` local model
- Git

The Python dependencies are installed inside the project virtual environment.

---

## 11. Setup

### 11.1 Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Development-Project
```

### 11.2 Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

If the virtual environment does not exist yet, create one:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 11.3 Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 11.4 Configure environment variables

Create a local `.env` file at the repository root.

Example:

```env
LLM_MODEL=qwen3.5:9b
OLLAMA_HOST=http://localhost:11434
MAX_ITERATIONS=3
```

Do not commit `.env` or any secrets to GitHub.

### 11.5 Verify the Ollama model

```powershell
ollama list
```

The required local model should be available:

```text
qwen3.5:9b
```

Make sure the Ollama service is running.

---

## 12. Database Setup

Move into the Cycle 1 directory:

```powershell
cd agent-loop
```

If the sample database needs to be recreated:

```powershell
py database\setup_database.py
```

---

## 13. Running the Agent

From:

```text
AI-Development-Project\agent-loop
```

run:

```powershell
py -m agent.loop
```

Enter a natural-language database question.

Example:

```text
Who earns the highest salary?
```

---

## 14. Sample Input and Output

### Input

```text
Who earns the highest salary?
```

### Generated SQL

```sql
SELECT id, name, department, salary
FROM employees
ORDER BY salary DESC
LIMIT 1;
```

### Result

```text
id: 3
name: Kumar
department: IT
salary: 60000.0
```

### Final status

```text
status: success
iterations: 1
```

---

## 15. Failure-Recovery Demonstration

A deliberate invalid SQL query can be used to demonstrate recovery:

```sql
SELECT * FROM employeez;
```

Expected first observation:

```text
Status: error
Message: no such table: employeez
Should retry: True
```

The next iteration should correct the query to:

```sql
SELECT * FROM employees;
```

and return the five employee records.

Expected final status:

```text
status: success
iterations: 2
```

---

## 16. Testing

Run all automated tests from the `agent-loop` directory:

```powershell
py -m pytest -q
```

The verified Cycle 1 test suite contains:

```text
13 passed
```

The tests cover the agent tools, planner behavior, observation behavior, logging, loop behavior, and self-correction behavior.

---

## 17. Iteration Logging

Every agent iteration is recorded in:

```text
logs/agent_trace.jsonl
```

Each record captures the iteration information required for reviewing the loop, including:

- timestamp
- iteration number
- perception information
- plan
- SQL query
- action/tool result
- observation
- success state

The runtime log is intentionally excluded from Git version control.

---

## 18. Verification Checklist

### Required Agent Loop Features

- [x] Perceive stage
- [x] Plan stage
- [x] Act stage
- [x] Observe stage
- [x] Real LLM call
- [x] Local Ollama model
- [x] At least two callable tools
- [x] Maximum iteration limit
- [x] Explicit success condition
- [x] File-based iteration logging
- [x] Tool failure recovery
- [x] Working runnable implementation

### Submission Artifacts

- [x] GitHub repository
- [x] Incremental Git history
- [x] README.md
- [x] One-page architecture diagram
- [x] Editable `.drawio` architecture source
- [x] PNG architecture export
- [ ] 3–5 minute live demo video
- [ ] Live viva-voce

---

## 19. Demo Flow

The recommended live demonstration is:

1. Show the project structure.
2. Show the installed local Ollama model.
3. Run the automated tests.
4. Run a successful natural-language SQL request.
5. Show the generated SQL and database result.
6. Run the deliberate SQL failure.
7. Show the failed first iteration.
8. Show the LLM correcting the SQL.
9. Show the successful second iteration.
10. Show the iteration trace log.
11. Briefly explain the Perceive → Plan → Act → Observe architecture.

The demonstration must be a live screen recording of the working system rather than a slide-only presentation.

---

## 20. Assignment Alignment

This implementation follows the Cycle 1 Agent Loop requirements:

- single-agent Perceive → Plan → Act → Observe loop
- real LLM in the Plan stage
- minimum two callable Act-stage tools
- maximum iteration count plus explicit success-condition check
- file-based iteration logging
- recovery from a tool failure without crashing

Selected use case:

**UC3 — Self-Correcting SQL Agent**

---

## 21. Cycle Status

**Cycle 1 — Agent Loop: Technical Implementation Complete**

The technical implementation and verification are complete.

The final submission package consists of the GitHub repository, README, one-page architecture diagram, editable diagram source, exported PNG, working demo video, and live viva-voce.
