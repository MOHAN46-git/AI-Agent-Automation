# Autonomous AI Agent with Tool Calling & State Loop

An autonomous, multi-step AI systems engineering agent built with Python and the official Google GenAI SDK (google-genai), powered by gemini-3.5-flash.

The agent implements the ReAct (Reason + Act) pattern to decompose high-level user tasks, plan actions, invoke deterministic local tools, observe execution outputs, and produce a verified synthesis.

---

## Architecture & Flow

1. User Goal Ingestion: The agent receives a high-level task.
2. Sense & Plan: Breaks the task into sequential tool calls.
3. Action / Execution: Invokes deterministic local Python functions:
   - calculate_expression (safe mathematical evaluation)
   - read_system_metric (telemetry and system state retrieval)
   - write_local_log (filesystem report persistence)
4. Observation Feedback Loop: Ingests tool outputs back into context.
5. Grounded Synthesis: Generates a final verified status summary.

---

## Features

- Multi-Step Tool Sequencing: Coordinates telemetry retrieval, arithmetic evaluation, and file persistence.
- Deterministic Reliability: Offloads math and state checks to code to prevent hallucination.
- Strict Type Signatures: Relies on Python type hints and docstrings for automatic OpenAPI schema generation.

---

## Project Structure

AI-Agent-Automation/
├── agent.py               # Core ReAct agent loop
├── tools.py               # Deterministic tool registry
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── .gitignore             # Secrets and workspace exclusions
└── agent_workspace/       # Local directory for generated logs

---

## Quickstart

1. Clone repository:
   git clone https://github.com/MOHAN46-git/AI-Agent-Automation.git
   cd AI-Agent-Automation

2. Set up virtual environment and install dependencies:
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt

3. Set up environment:
   cp .env.example .env
   # Add your GEMINI_API_KEY in .env

4. Run the autonomous agent:
   python agent.py
