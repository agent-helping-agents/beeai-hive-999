#!/usr/bin/env python3
"""
BeeAI Hive 999 - Smart Model Tester
Tests Ollama and runs Marco-o1 exploration when models are available
"""

import asyncio
import subprocess
import json
import sys

GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
NC = "\033[0m"


def print_header(text):
    print(f"\n{CYAN}{'=' * 60}{NC}")
    print(f"{CYAN}  {text}{NC}")
    print(f"{CYAN}{'=' * 60}{NC}\n")


def print_success(text):
    print(f"{GREEN}[✓] {text}{NC}")


def print_error(text):
    print(f"{RED}[✗] {text}{NC}")


def print_info(text):
    print(f"{BLUE}[i] {text}{NC}")


def check_ollama():
    """Check Ollama server."""
    print_header("Ollama Server Check")

    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print_error("Ollama not responding")
            return None, []

        data = json.loads(result.stdout)
        models = data.get("models", [])

        print_success(f"Ollama is running!")
        print(f"  Host: 0.0.0.0:11434 (LAN enabled)")

        if models:
            print(f"\n  Installed Models ({len(models)}):")
            for m in models:
                size_gb = m.get("size", 0) / (1024**3)
                print(f"    • {m['name']} ({size_gb:.1f} GB)")
            return models, []
        else:
            print_warning("No models installed yet")
            return models, []

    except Exception as e:
        print_error(f"Error: {e}")
        return None, []


def print_warning(text):
    print(f"{YELLOW}[!] {text}{NC}")


def wait_for_model(max_wait=300):
    """Wait for any model to be installed."""
    print_header("Waiting for Models")

    import time

    start = time.time()

    while time.time() - start < max_wait:
        models, _ = check_ollama()
        if models:
            return models
        print_info(f"Waiting... ({int(time.time() - start)}s)")
        time.sleep(5)

    print_error("Timeout waiting for models")
    return []


async def test_available_models(models):
    """Test whatever models are available."""
    print_header("Testing Available Models")

    import ollama

    test_queries = {
        "general": "What is 2+2?",
        "reasoning": "If A implies B, and B implies C, what does A imply?",
        "coding": "Write: print('hello')",
    }

    for model_info in models:
        model_name = model_info["name"]
        print_info(f"\nTesting {model_name}...")

        for test_type, query in test_queries.items():
            try:
                response = ollama.generate(
                    model=model_name, prompt=query, options={"num_predict": 100}
                )
                print_success(f"  {test_type}: {response['response'][:80]}...")
            except Exception as e:
                print_error(f"  {test_type}: {e}")


async def explore_with_marco(models):
    """Explore Marco-o1 capabilities if available."""
    print_header("Marco-o1 Brain Engine Exploration")

    import ollama

    # Check if marco-o1 is available
    marco = None
    for m in models:
        if "marco" in m["name"].lower():
            marco = m["name"]
            break

    if not marco:
        print_warning("marco-o1 not yet installed")
        print_info("Available models:")
        for m in models:
            print(f"  - {m['name']}")
        return

    print_success(f"Found {marco}!")

    # Marco-o1 specific tests
    tests = [
        {
            "name": "Chain of Thought Math",
            "query": """Solve step by step: If x² + 6x + 9 = 25, find all possible values of x. Show your reasoning at each step.""",
            "temp": 0.1,
        },
        {
            "name": "Logical Deduction",
            "query": """All Worker Bees are agents. Some Bees live in hives. What can we logically conclude? Use formal logic.""",
            "temp": 0.3,
        },
        {
            "name": "Problem Decomposition",
            "query": """Decompose the problem of 'optimizing blockchain transaction fees' into sub-problems. List each with rationale.""",
            "temp": 0.4,
        },
        {
            "name": "Digital Root Calculation",
            "query": """The digital root of a number is obtained by summing its digits repeatedly until a single digit remains.
            
Calculate the digital root of 729 (the number of nodes in our matrix).
Show your work step by step.""",
            "temp": 0.2,
        },
    ]

    for test in tests:
        print(f"\n{BLUE}--- {test['name']} ---{NC}")
        try:
            response = ollama.generate(
                model=marco,
                prompt=test["query"],
                options={"temperature": test["temp"], "num_predict": 500},
            )
            print(response["response"])
        except Exception as e:
            print_error(f"Error: {e}")


async def test_beeai_integration():
    """Test BeeAI framework integration."""
    print_header("BeeAI Framework Integration")

    try:
        from backend.llm_router import LLMRouter, ModelRole

        router = LLMRouter()

        # Test routing
        test_cases = [
            ("Simple", "low", False, "low"),
            ("Reasoning", "high", True, "medium"),
            ("Coding", "medium", False, "high"),
        ]

        print_success("LLM Router working!")
        print("\nTask Routing Examples:")

        for name, complexity, privacy, latency in test_cases:
            role, config = router.route_task(
                task_complexity=complexity,
                privacy_required=privacy,
                latency_sensitivity=latency,
            )
            print(f"  {name}: {role.value} → {config.name}")

    except Exception as e:
        print_error(f"BeeAI integration: {e}")


async def explore_tui_capabilities():
    """Explore what the TUI can do."""
    print_header("Enhanced TUI Capabilities")

    print("""
The Enhanced TUI includes:

  ✨ SCROLLABLE CHAT
     • Arrow keys (↑/↓) to scroll
     • Page Up/Down for fast navigation
     • Home/End to jump to edges

  🎨 MESSAGE BUBBLES
     • Queen Bee: 🐝 Gold/Amber (#FFAC33)
     • Workers:   🐝 Cyan (#00FFFF)
     • Drones:    🛸 Green (#32CD32)
     • Foragers:  🔍 Magenta (#FF00FF)

  📊 VISUAL SCROLLBAR
     • █ Thumb shows position
     │ Track shows scrollable area
     ▲▼ Arrows at edges

  ⏳ TYPING INDICATORS
     • Animated dots while thinking
     • Shows which agent is active

  🔔 NOTIFICATIONS
     • Success: Green ✓
     • Warning: Yellow !
     • Error: Red ✗

  🧠 MARCO-O1 INTEGRATION
     • Use :marco command for reasoning
     • :reason <query> for chain-of-thought
     • :math <problem> for step-by-step math

  🎯 KEY BINDINGS
     Alt+Q    → Queen Bee
     Alt+1-9  → Worker Bees
     Alt+G    → Government Drone
     Alt+X    → Mantis Mail
     :help    → Show commands
     Ctrl+C   → Exit
""")


async def main():
    """Main test runner."""
    print(f"""
{GREEN}
╔═══════════════════════════════════════════════════════════════════╗
║       🐝 BEEAI HIVE 999 - Smart Model Tester 🧠           ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}
    """)

    # Check Ollama
    models = wait_for_model(max_wait=10)

    if not models:
        print_info("No models yet. Downloading in background...")
        print_info("While waiting, exploring TUI capabilities...")
        await explore_tui_capabilities()
        await test_beeai_integration()
        return

    # Test available models
    await test_available_models(models)

    # Explore Marco-o1 if available
    await explore_with_marco(models)

    # Test BeeAI integration
    await test_beeai_integration()

    # Explore TUI
    await explore_tui_capabilities()

    print_header("Ready!")
    print("""
To run the Enhanced TUI:
    
    cd ~/beeai-hive-999
    source .venv/bin/activate
    python hive_tui_enhanced.py

To explore more with Marco-o1 (when installed):
    
    python explore_marco.py
""")


if __name__ == "__main__":
    asyncio.run(main())
