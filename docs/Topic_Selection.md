# Topic Selection

## Cycle 1

### Topic

Agent Loop

### Status

Compulsory

### Deadline

12 August 2026

### Selected Use Case

UC3 - Self-Correcting SQL Agent

## Problem

Users may know what information they want from a database but may not know how to write SQL queries.

An AI agent can convert a natural-language request into SQL and execute it against a sample database.

If the generated SQL contains an error or produces no useful result, the agent should observe the result, revise the SQL query and try again.

## Agent Loop

The project follows:

Perceive
→ Plan
→ Act
→ Observe
→ Repeat if required
→ Success or Termination

## Expected Behaviour

1. Accept a natural-language database request.
2. Understand the request.
3. Use a real LLM to generate SQL.
4. Execute the generated SQL.
5. Observe the result or error.
6. If unsuccessful, provide the observation back to the LLM.
7. Generate a corrected SQL query.
8. Repeat until successful or the maximum iteration count is reached.

## Current Status

Cycle 1 Agent Loop foundation has been implemented and tested.

Completed:
- Perceive stage
- Plan stage prototype
- Act stage
- Observe stage
- Self-correction mechanism
- Agent loop controller
- Retry and termination handling
- SQL error recovery
- Zero-result handling
- Integration testing

Current Cycle 1 pending requirements:
- Replace deterministic planning logic with a real LLM-based Plan stage.
- Integrate both required tools during the Act stage.
- Add iteration-level file logging.
- Complete full Cycle 1 validation and demonstration requirements.

Cycle 1 is not yet marked complete.