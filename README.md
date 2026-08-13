# Email Agent (from scratch)

An ambient email assistant built with LangGraph, Cerebras, and human-in-the-loop.  
This project re-implements the architecture of [langchain-ai/agents-from-scratch](https://github.com/langchain-ai/agents-from-scratch) as a proper Python package, focusing on triage, routing, tool use, human review, and long-term memory.

# Prerequisites

Python ≥ 3.10

Cerebras API key (or access to another OpenAI‑compatible provider)

Optional: LangSmith for tracing and evaluation

# Installation

```bash
git clone https://github.com/BhimPrasadAdhikari/email-agent
cd email-agent
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

# configuration

```bash
cp .env.example .env
```

# Contributing

This project is a personal portfolio piece. If you'd like to contribute, feel free to open an issue or pull request.

# LICENSE

MIT

