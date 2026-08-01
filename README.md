# AI Development Project

## Cycle 1 - Agent Loop

### Self-Correcting SQL Agent

This repository contains my Semester 5 AI Development assignments based on the Agentic AI Skill-Building Preparation.

The current compulsory cycle focuses on implementing a single-agent loop using the Perceive → Plan → Act → Observe pattern.

## Selected Use Case

UC3 - Self-Correcting SQL Agent

The agent accepts a natural-language database request and uses a real LLM to generate an SQL query.

The generated query is executed against a sample database.

If the query fails or returns no useful result, the agent observes the failure, sends the observation back to the LLM and attempts to generate a corrected query.

The process continues until a valid non-empty result is obtained or the maximum iteration count is reached.

## Agent Loop

```text
Perceive
   ↓
Plan
   ↓
Act
   ↓
Observe
   ↓
Success?
 ↙       ↘
No       Yes
↓         ↓
Repeat   Stop
```

## Mandatory Requirements

- Explicit Perceive → Plan → Act → Observe stages
- Real LLM in the Plan stage
- Minimum two callable tools
- Maximum iteration termination
- Explicit success-condition termination
- Iteration logging
- Tool-failure recovery

## Planned Tools

1. Database Schema Inspection Tool
2. SQL Execution Tool

## Technology

- Python
- SQLite
- Ollama
- Git
- GitHub

Exact framework, SDK and model versions will be documented once the implementation environment is finalized.

## Current Status

Cycle 1 - Planning and Initial Design

## Deadline

12 August 2026

## Final Deliverables

- Working runnable Agent Loop
- Clean incremental GitHub history
- README with setup and run instructions
- Architecture diagram
- Sample input and output
- 3-5 minute live demo video
- Live viva demonstration