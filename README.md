# AI Development Project

> **B.Tech Artificial Intelligence and Data Science — Regulation 2021**
> **J.J. College of Engineering and Technology (JJCET)**
> **Training & Placement Cell — AI Development Preparation**

## 1. Project Overview

This repository contains the student's implementation for the **AI Development Preparation — Agentic AI Skill-Building Assignment**, organized as independent 15-day development cycles.

The project follows the official cycle structure:

| Cycle | Topic | Status | Selected Use Case |
|---|---|---|---|
| Cycle 1 | Agent Loop | Completed | UC3 — Self-Correcting SQL Agent |
| Cycle 2 | MCP Server | In Progress | UC4 — E-Commerce Order MCP Server |
| Cycle 3 | Multi-agent Orchestration | Planned | UC5 — Feature-Delivery Crew |
| Cycle 4 | A2A Protocol paired with MCP | Planned | UC4 — IT Helpdesk Federation |
| Cycle 5 | Agent Harness | Optional | To be decided |
| Cycle 6 | Human in the Loop | Optional | To be decided |

Topics 1–4 are compulsory. Topics 5–6 are optional bonus cycles.

This repository is maintained as a sequence of independently runnable cycle projects while preserving a clean, incremental Git history.

---

## 2. Assignment Alignment

The project follows the official **AI Development Preparation** assignment and its cycle-based requirements.

For every compulsory cycle, the implementation is developed as a working, runnable project rather than a mockup or non-functional prototype.

Each cycle is intended to include:

- a clearly defined problem/use case
- the mandatory technical requirements for its topic
- a runnable implementation
- automated/manual verification appropriate to the topic
- cycle-specific documentation
- a README with problem statement, architecture, setup/run instructions, and sample input/output
- a one-page architecture diagram
- a 3–5 minute working demonstration
- preparation for the individual viva-voce
- clean, incremental Git commits

The project also follows the requirement that secrets and API keys are not committed to GitHub. Local environment configuration is kept outside version control.

---

## 3. Cycle Schedule

| Cycle | Topic | Days | Official Deadline | Status |
|---|---|---:|---|---|
| 1 | Agent Loop | Day 1–15 | 12 Aug 2026 | Completed |
| 2 | MCP Server | Day 16–30 | 27 Aug 2026 | In Progress |
| 3 | Multi-agent Orchestration | Day 31–45 | 11 Sep 2026 | Planned |
| 4 | A2A Protocol paired with MCP | Day 46–60 | 26 Sep 2026 | Planned |
| 5 | Agent Harness | Day 61–75 | 11 Oct 2026 | Optional |
| 6 | Human in the Loop | Day 76–90 | 26 Oct 2026 | Optional |

The official assignment specifies a 15-day cycle for each topic and states that Topics 1–4 are compulsory. fileciteturn14file2

---

## 4. Repository Structure

```text
AI-Development-Project/
│
├── agent-loop/
│   ├── agent/
│   ├── database/
│   ├── docs/
│   ├── logs/
│   ├── tests/
│   ├── tools/
│   └── README.md
│
├── mcp-server/
│   └── Cycle 2 implementation
│
├── multi-agent/
│   └── Cycle 3 implementation
│
├── a2a-mcp/
│   └── Cycle 4 implementation
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
└── requirements.txt
```

Local-only files such as `.env`, `.venv`, pytest caches, and generated runtime logs are excluded from version control as appropriate.

---

# 5. Cycle 1 — Agent Loop

## 5.1 Selected Use Case

**UC3 — Self-Correcting SQL Agent**

The agent generates SQL, executes it, observes the result, and retries with a revised SQL plan when execution fails or returns no rows.

## 5.2 Problem Statement

Users should be able to query a sample employee database using natural language instead of manually writing SQL.

The agent receives a natural-language question, understands the available database schema, generates SQL using a real local LLM, executes the SQL through callable tools, observes the result, and automatically retries when the first attempt fails.

The system must terminate when the result satisfies the success condition or when the hard maximum iteration limit is reached.

## 5.3 Architecture

```text
User Question
      │
      ▼
┌───────────────┐
│   PERCEIVE    │
│ Question +    │
│ DB Schema     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     PLAN      │
│ Ollama        │
│ qwen3.5:9b    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│      ACT      │
│ Schema Tool   │
│ SQL Tool      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    OBSERVE    │
│ Status +      │
│ returned rows │
└───────┬───────┘
        │
        ▼
┌──────────────────────┐
│ Success + non-empty  │
│ result?              │
└───────┬──────────────┘
    YES │       │ NO
        │       │
        ▼       ▼
      STOP    RE-PLAN
                │
                └──────► PLAN

Maximum iterations: 3
Iteration trace: logs/agent_trace.jsonl
```

The editable architecture source and exported diagram are stored under:

```text
agent-loop/docs/
```

## 5.4 Technology

- Python 3.14.6
- Ollama
- `qwen3.5:9b`
- Ollama Python client 0.6.2
- python-dotenv 1.2.2
- SQLite
- pytest

The exact framework/client versions used for Cycle 1 are documented in the cycle README.

## 5.5 Implemented Agent Stages

### Perceive

Receives the natural-language question and obtains the SQLite database schema.

### Plan

Uses the real local Ollama `qwen3.5:9b` model to produce a structured SQL plan.

### Act

Uses two callable tools:

1. `inspect_database_schema`
2. `execute_sql`

### Observe

Evaluates the execution result and determines whether the loop has succeeded or must retry.

### Termination

The loop has:

- a hard maximum iteration limit of 3
- an explicit success-condition check

## 5.6 Failure Recovery

The implementation was verified with a deliberate SQL failure:

```sql
SELECT * FROM employeez;
```

The database does not contain `employeez`.

The agent observes the SQL error and retries. The next planning iteration corrects the table name to:

```sql
SELECT * FROM employees;
```

The corrected query succeeds.

## 5.7 Testing

Cycle 1 has a verified automated test suite with:

```text
13 passed
```

Tests cover the agent tools, planner, observation, logging, loop behavior, and self-correction.

## 5.8 Cycle 1 Documentation

The detailed cycle-specific documentation is available in:

```text
agent-loop/README.md
agent-loop/docs/
```

---

# 6. Cycle 2 — MCP Server

## 6.1 Selected Use Case

**UC4 — E-Commerce Order MCP Server**

The server will expose:

- `track_order`
- `check_stock`
- `initiate_return`

using a mock product/orders database.

The official assignment specifies UC4 as an E-Commerce Order MCP Server backed by a mock product/orders database using JSON or SQLite. fileciteturn14file4

## 6.2 Mandatory Technical Requirements

Cycle 2 must implement:

- the official MCP SDK
- Python `mcp` or TypeScript `@modelcontextprotocol/sdk`
- at least 3 MCP tools
- fully specified JSON schemas for tool inputs and outputs
- at least 1 resource endpoint
- stdio transport for local testing
- verification using MCP Inspector
- a real MCP client connection
- a live end-to-end tool call
- timestamped invocation logging with sanitized arguments

These are mandatory Cycle 2 requirements. fileciteturn14file4

## 6.3 Planned Architecture

```text
                MCP Client
                    │
                  stdio
                    │
                    ▼
          ┌────────────────────┐
          │   MCP Server       │
          │                    │
          │  track_order       │
          │  check_stock       │
          │  initiate_return   │
          │                    │
          │  Resource Endpoint │
          └─────────┬──────────┘
                    │
                    ▼
              SQLite Database
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       products   orders    returns

                    │
                    ▼
          Invocation Audit Log
```

The final architecture will be updated to reflect the actual implementation.

---

# 7. Cycle 3 — Multi-agent Orchestration

## Selected Use Case

**UC5 — Feature-Delivery Crew**

Planned roles:

- Requirement-Analyzer
- Coder
- Tester
- Reviewer

The assignment requires at least 3 distinct agents, one orchestration framework, an explicit orchestrator/supervisor, shared state or memory, runtime branching, and failure handling. fileciteturn14file5

The exact framework will be selected and recorded in the Cycle 3 README before implementation.

---

# 8. Cycle 4 — A2A Protocol Paired with MCP

## Selected Use Case

**UC4 — IT Helpdesk Federation**

Planned architecture:

```text
Support Agent
     │
     │ A2A
     ▼
Infra Specialist Agent
     │
     │ MCP
     ▼
DevOps MCP Server
```

The assignment requires at least two independent agents, valid Agent Cards, the official A2A SDK, JSON-RPC task exchange, a real cross-agent handoff, full trace capture, and separate local processes/ports. At least one agent must use an MCP server internally. fileciteturn14file17

Cycle 2's MCP server may be reused as permitted by the assignment.

---

# 9. Optional Cycles

## Cycle 5 — Agent Harness

Optional.

Potential future use cases include wrapping the Cycle 1 or Cycle 3 agent with persistence, structured observability, sandboxing, or a kill-switch. The assignment specifically allows an existing Cycle 1/3 agent to be wrapped rather than rewriting its reasoning core. fileciteturn14file19

## Cycle 6 — Human in the Loop

Optional.

Potential future use cases include a mandatory human approval/edit gate for a high-risk action. The assignment requires explicit human input, editable proposed actions, decision logging, and a confidence/risk threshold if this cycle is selected. fileciteturn14file18

---

# 10. Security and Configuration

Secrets must never be committed to GitHub.

Local configuration is maintained using:

```text
.env
```

The repository provides:

```text
.env.example
```

The `.env` file is excluded through `.gitignore`.

Generated runtime logs are also excluded from version control where appropriate.

---

# 11. Development and Git Practices

The repository uses incremental Conventional Commit-style history.

Examples:

```text
feat(cycle-1): implement agent loop
test(cycle-1): add loop recovery tests
docs(cycle-1): document agent architecture
refactor(cycle-1): organize Cycle 1 into agent-loop
feat(cycle-2): implement MCP tools
test(cycle-2): verify MCP tool behavior
docs(cycle-2): document MCP server setup
```

Changes should be small, working, testable increments rather than one large final commit.

---

# 12. Verification Standard

Before considering a cycle technically complete:

```text
Implementation
    ↓
Automated tests
    ↓
Manual runtime verification
    ↓
Failure/edge-case verification
    ↓
Documentation
    ↓
Architecture diagram
    ↓
Demo recording
    ↓
Git review
    ↓
Commit
    ↓
Push
```

No cycle should be declared complete merely because the code was written.

---

# 13. Submission Package

For each cycle, the final package must include:

- GitHub repository link
- clean incremental Git history
- cycle README
- problem statement
- architecture diagram
- setup/run instructions
- sample input/output
- working 3–5 minute live demo
- one-page architecture diagram
- individual viva preparation

These requirements come directly from the AI Development Preparation assignment. fileciteturn15file10

---

# 14. Current Project Status — 14 August 2026

## Cycle 1

**Technical implementation:** Complete

**Repository organization:** Complete

**GitHub main branch:** Synchronized

**Testing:** Verified

**Submission artifacts:** Must be individually verified before final closure

## Cycle 2

**Topic:** MCP Server

**Use Case:** UC4 — E-Commerce Order MCP Server

**Current phase:** Beginning after Cycle 1 closure

**Official deadline:** 27 August 2026

---

# 15. Official Reference Documents

This project follows:

1. `R2021_Sem5_AI_Development_Preparation_Assignment.pdf`
2. `R2021_Sem5_Placement_Planner_V1.2_28Jul2026.docx`

The Placement Planner identifies the AI Development Project as the 15-day-cycle AI development component and directs students to follow the AI Development Preparation Assignment for its execution. fileciteturn16file0

---

# 16. Project Principle

The objective is not simply to finish six folders.

Every cycle should demonstrate:

**Understand → Design → Implement → Test → Verify → Document → Demonstrate → Defend**

The final repository should remain understandable, reproducible, professionally structured, and defensible in an individual viva.

---

## Project Status

**AI Development Project — Active**

**Current Cycle:** Cycle 2 — MCP Server

**Selected Cycle 2 Use Case:** UC4 — E-Commerce Order MCP Server

**Last documented project date:** 14 August 2026
