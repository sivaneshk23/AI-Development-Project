# Cycle 1 - Agent Loop Requirements

## Selected Use Case

UC3 - Self-Correcting SQL Agent

## Mandatory Requirements

The implementation must satisfy the following requirements.

### 1. Explicit Agent Loop

Every iteration must contain four clearly identifiable stages:

1. Perceive
2. Plan
3. Act
4. Observe

Each stage must be logged separately.

### 2. Real LLM

The Plan stage must use a real Large Language Model.

The project will not use hardcoded if/else statements as a replacement for LLM reasoning.

### 3. Minimum Two Tools

The agent must have at least two callable tools/functions available during the Act stage.

Planned tools:

- Database schema inspection tool
- SQL execution tool

### 4. Termination Rules

The agent must stop when either:

- A valid non-empty SQL result is obtained, or
- The maximum number of iterations is reached.

### 5. Iteration Logging

Every iteration must be logged to a file.

The log must capture:

- Iteration number
- Perceive stage
- Plan stage
- Action taken
- Observation received
- Success status

### 6. Failure Recovery

The agent must recover from at least one tool failure without crashing.

Example:

An invalid SQL query produces a database error.

The error is returned to the agent as an observation.

The LLM then attempts to generate a corrected SQL query.

## Final Cycle Deliverables

- Working runnable project
- GitHub repository with incremental commits
- README.md
- Architecture diagram
- Setup and run instructions
- Sample input and output
- 3-5 minute live demo video
- Viva preparation