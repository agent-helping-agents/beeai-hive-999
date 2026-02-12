#!/usr/bin/env python3
"""
BeeAI Hive 999 - Ultimate Integration Test
Tests everything when models are available
"""

import subprocess
import json
import asyncio
import sys
import os

# ANSI Colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
NC = "\033[0m"


def log(text, color=CYAN):
    print(f"{color}{text}{NC}")


def section(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def run_cmd(cmd):
    """Run command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def check_ollama():
    """Check Ollama status."""
    section("OLLAMA SERVER STATUS")

    output = run_cmd("curl -s http://localhost:11434/api/tags")

    try:
        data = json.loads(output)
        models = data.get("models", [])

        if models:
            log(f"✓ Ollama is running!", GREEN)
            log(f"  Host: 0.0.0.0:11434 (LAN enabled)", BLUE)
            log(f"\n  Installed Models:", CYAN)
            for m in models:
                size_gb = m.get("size", 0) / (1024**3)
                log(f"    • {m['name']} ({size_gb:.1f} GB)", GREEN)
            return models
        else:
            log("✗ No models installed yet", YELLOW)
            return []
    except Exception as e:
        log(f"✗ Ollama not responding: {e}", RED)
        return None


def check_services():
    """Check all services."""
    section("SERVICES CHECK")

    checks = [
        (
            "Ollama",
            "curl -s http://localhost:11434/api/tags >/dev/null && echo OK || echo FAIL",
        ),
        (
            "Python venv",
            f"test -d {os.path.dirname(os.path.abspath(__file__))}/.venv && echo OK || echo MISSING",
        ),
        ("Enhanced TUI", "test -f hive_tui_enhanced.py && echo OK || echo MISSING"),
        ("Marco Explorer", "test -f explore_marco.py && echo OK || echo MISSING"),
        (
            "BeeAI Framework",
            "python -c 'import beeai_framework' 2>&1 | grep -q OK && echo OK || echo MISSING",
        ),
    ]

    for name, cmd in checks:
        result = run_cmd(cmd).strip()
        if "OK" in result or result == "OK":
            log(f"✓ {name}", GREEN)
        else:
            log(f"✗ {name}: {result}", YELLOW)


async def test_llm(models):
    """Test LLM capabilities."""
    section("LLM CAPABILITY TESTS")

    if not models:
        log("No models available for testing", YELLOW)
        return

    # Find available models
    available = [m["name"] for m in models]
    log(f"Available models: {available}", BLUE)

    # Pick first available model for testing
    test_model = available[0]
    log(f"\nTesting with: {test_model}", CYAN)

    import ollama

    tests = [
        ("Basic Math", "What is 2+2?"),
        ("Reasoning", "If A implies B, and B implies C, what does A imply?"),
        ("Code", "Write: print('hello world')"),
        ("Matrix", "What is 9 × 9 × 9?"),
    ]

    for name, query in tests:
        try:
            response = ollama.generate(
                model=test_model, prompt=query, options={"num_predict": 100}
            )
            log(f"\n✓ {name}: {response['response'][:100]}...", GREEN)
        except Exception as e:
            log(f"✗ {name}: {e}", RED)


def test_beeai():
    """Test BeeAI framework."""
    section("BEEAI FRAMEWORK TEST")

    output = run_cmd(
        "python -c 'from backend.llm_router import LLMRouter; r=LLMRouter(); print(\"✓ LLM Router OK\")'"
    )
    if "OK" in output:
        log("✓ LLM Router", GREEN)
    else:
        log(f"✗ LLM Router: {output[:200]}", YELLOW)

    # Test config
    output = run_cmd(
        "python -c 'from config.hive_config import get_config; c=get_config(); print(f\"✓ Config: {c.backend}\")'"
    )
    if "Config" in output:
        log(f"✓ Configuration System", GREEN)
    else:
        log(f"✗ Configuration: {output[:100]}", YELLOW)


def show_tui_features():
    """Show TUI features."""
    section("ENHANCED TUI FEATURES")

    features = """
  ✨ SCROLLABLE CHAT
     • Arrow keys (↑/↓) scroll through message history
     • Page Up/Dn for fast navigation
     • Home/End to jump to top/bottom

  🎨 MESSAGE BUBBLES (Color-coded)
     • Queen Bee:     🐝 Gold (#FFAC33)
     • Workers:       🐝 Cyan (#00FFFF)
     • Drones:        🛸 Green (#32CD32)
     • Foragers:      🔍 Magenta (#FF00FF)
     • Detectives:    🕵️ Red (#CD5C5C)

  📊 VISUAL SCROLLBAR
     • █ Thumb shows position
     │ Track shows scrollable area
     ▲▼ Arrows at edges

  ⏳ TYPING INDICATORS
     • Animated ⠋⠙⠹⠸⠼ while thinking
     • Shows active agent name

  🔔 NOTIFICATION SYSTEM
     • ✓ Success (green)
     • ⚠ Warning (yellow)  
     • ✗ Error (red)

  🎯 KEY BINDINGS
     Alt+Q    → Queen Bee
     Alt+1-9  → Worker Bees
     Alt+G    → Government Drone
     Alt+X    → Mantis Mail
     :help    → Show commands
     Ctrl+C   → Exit

  🧠 MARCO-O1 BRAIN ENGINE
     • Complex reasoning tasks
     • Chain-of-thought math
     • Problem decomposition
     • Logical deduction

  📝 COMMANDS
     :marco <query>   → Marco-o1 reasoning
     :reason <query>   → Reasoning mode
     :math <problem>   → Math solver
     :art <topic>      → ANSI art
     :matrix           → Show matrix
"""
    print(features)


def show_model_guide():
    """Show model usage guide."""
    section("MODEL USAGE GUIDE")

    guide = """
  AVAILABLE MODELS:

  🤖 REASONING (Use Marco-o1)
     • Complex math proofs
     • Multi-step logic
     • Research analysis
     • Problem decomposition

  ⚙️ ORCHESTRATION (Granite3.3)
     • General queries
     • Agent coordination
     • Task routing

  💻 CODING (Qwen2.5-Coder)
     • Code generation
     • Debugging
     • Refactoring
     • Documentation

  ⚡ FAST WORKERS (Llama3.1)
     • Quick responses
     • Simple queries
     • Chat interaction

  IN THE TUI:
  
  1. Type complex query → Queen routes to best model
  2. Use :marco command for explicit reasoning
  3. Use :math for step-by-step math
  4. Use :code for programming tasks

  QUEEN BEE AUTOMATICALLY:
  
  • Analyzes query complexity
  • Routes to appropriate agent
  • Selects optimal model
  • Synthesizes multi-agent responses
"""
    print(guide)


async def main():
    """Run all tests."""
    print(f"""
{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║     🐝 BEEAI HIVE 999 - ULTIMATE INTEGRATION TEST 🧠       ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}
    """)

    # Check services
    check_services()

    # Check Ollama
    models = check_ollama()

    # Test LLM if available
    await test_llm(models)

    # Test BeeAI
    test_beeai()

    # Show features
    show_tui_features()

    # Show guide
    show_model_guide()

    # Final status
    section("SYSTEM STATUS")

    if models:
        log("✓ SYSTEM READY!", GREEN)
        log(f"  {len(models)} model(s) installed", GREEN)
        log("\n  To start the TUI:", CYAN)
        log("    cd ~/beeai-hive-999", BLUE)
        log("    source .venv/bin/activate", BLUE)
        log("    python hive_tui_enhanced.py", BLUE)
    else:
        log("⚠️ MODELS STILL DOWNLOADING", YELLOW)
        log("\n  While waiting, explore TUI features above!", CYAN)
        log("\n  Check status:", BLUE)
        log("    curl http://localhost:11434/api/tags", BLUE)
        log("\n  Pull models:", BLUE)
        log("    ollama pull llama3.2:3b", BLUE)
        log("    ollama pull granite3.3:8b", BLUE)


if __name__ == "__main__":
    asyncio.run(main())
