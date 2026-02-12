# AGENTS.md – BeeAI Hive 999 Agent Guide

## 1. Project Overview
BeeAI Hive 999 is a full‑screen terminal UI for a hybrid multi‑agent system (local Ollama + cloud LangChain). It consists of a Queen Bee orchestrator, 9 Worker Bees (blockchain specialists), 9 Drone Agents (stakeholder analysts), 9 Forager Agents (trend researchers), and a Mantis Mail agent. A new Terminal 221b detective layer adds Solana investigation agents.

## 2. Build / Lint / Test Commands

### 2.1 Core Scripts
- `./run.sh` – launch the TUI (default) or CLI (`./run.sh cli`).
- `./run.sh check` – run system checks (model availability, config sanity).
- `./run.sh embed` – regenerate ChromaDB embeddings.

### 2.2 Python Environment
```bash
# Install dependencies (if a requirements.txt exists)
pip install -r requirements.txt

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.3 Linting
```bash
# Ruff (primary linter - fast and strict)
ruff check .
# Auto-fix linting errors
ruff check . --fix

# Black (code formatter)
black .
```

### 2.4 Type Checking
```bash
mypy .
```

### 2.5 Testing
- **Run all tests** (pytest is the default test runner):
```bash
pytest
```
- **Run a single test file**:
```bash
pytest tests/test_hive_core.py
```
- **Run a single test case**:
```bash
pytest tests/test_hive_core.py::TestConfiguration::test_default_config
```
- **Run tests with coverage report**:
```bash
pytest --cov=. tests/
pytest --cov-report=html --cov=. tests/  # HTML report
```
- **Run tests with asyncio support**:
```bash
pytest tests/test_hive_core.py -v -xvs
```

### 2.6 CI Helpers
- `./scripts/setup_all_secrets.py` – load secrets into environment.
- `./scripts/zoho_domain_verify.sh` – verify Zoho mail domain.

## 3. Code Style Guidelines

### 3.1 General Python Conventions
- **PEP 8** compliance, max line length **100** characters.
- **Type hints** on all public functions and methods (use typing module).
- **Google‑style docstrings** for public callables.
- **Imports** ordered: standard library → third‑party → local imports, each group separated by a blank line.
- Use **`isort`** for import sorting.

### 3.2 Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions / Variables: `snake_case`
- Constants: `UPPER_CASE`
- Private members: `_leading_underscore`
- Async functions: `async def foo_async(...):`

### 3.3 Formatting
- 4‑space indentation, no tabs.
- Trailing commas in multi‑line collections.
- Blank line after top‑level imports and between functions.
- End files with a newline.
- Use `black` for automatic formatting.

### 3.4 Error Handling
- Raise **custom exceptions** derived from `BeeAIError` where appropriate.
- Use **`try/except`** only around code that can reasonably fail; log the error with `logger.exception` and re‑raise if needed.
- Do **not** expose secrets in exception messages.

### 3.5 Logging
- Use the project‑wide `logger` (`logging.getLogger(__name__)`).
- Log at `INFO` for normal flow, `DEBUG` for verbose, `WARNING`/`ERROR` for problems.
- Never log raw API keys or passwords.

### 3.6 Tool Definition Pattern
```python
from beeai_framework.tools import StringToolOutput, tool

@tool
def my_tool(param: str) -> StringToolOutput:
    """Brief description.

    Args:
        param: parameter description

    Returns:
        StringToolOutput with result
    """
    return StringToolOutput(result="...")
```

### 3.7 Agent Factory Pattern
```python
async def create_worker_bee(blockchain_name: str) -> RequirementAgent:
    """Factory for a Worker Bee specialized in `blockchain_name`."""
    llm = ChatModel.from_name("ollama:llama3.2:3b")
    instructions = f"""You are a Worker Bee specialized in {blockchain_name}.
    ...
    """
    return RequirementAgent(
        llm=llm,
        tools=[query_blockchain_nodes],
        memory=UnconstrainedMemory(),
        instructions=instructions,
    )
```

### 3.8 Project‑Root Path Handling
```python
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

## 4. Cursor / Copilot Rules
- No `.cursor` or `.cursorrules` directories are present.
- No `.github/copilot-instructions.md` file exists.
- If added later, follow the same style as above.

## 5. Testing Checklist (Manual)
- ✅ `./run.sh` launches TUI, Alt+Q switches to Queen Bee.
- ✅ `:art <topic>` displays ANSI art.
- ✅ `:backend cloud` switches backend, `:status` shows config.
- ✅ `python agents/queen_bee/orchestrator.py showcase` runs without error.
- ✅ All tests pass (`pytest`).

## 6. Development Workflow
1. **Create/modify** code.
2. **Run** `ruff check . && black . && mypy . && pytest` locally.
3. **Commit** only after lint and tests succeed.
4. **Update** this AGENTS.md if new conventions are introduced.

---
*This document is consumed by autonomous coding agents to enforce consistency across the BeeAI Hive 999 repository.*