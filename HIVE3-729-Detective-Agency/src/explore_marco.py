#!/usr/bin/env python3
"""
BeeAI Hive 999 - Marco-o1 Brain Engine Explorer

This script explores the capabilities of the marco-o1 reasoning model
and tests its integration with the Hive.
"""

import asyncio
import json
import sys
import time
from datetime import datetime

# ANSI Colors
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


def print_info(text):
    print(f"{BLUE}[i] {text}{NC}")


def print_warning(text):
    print(f"{YELLOW}[!] {text}{NC}")


def print_error(text):
    print(f"{RED}[✗] {text}{NC}")


def check_ollama():
    """Check Ollama server status."""
    print_header("Ollama Server Status")

    try:
        import ollama

        response = ollama.list()
        models = response.get("models", [])

        print_success("Ollama connected!")

        if models:
            print(f"\nInstalled Models ({len(models)}):")
            for m in models:
                size_gb = m.get("size", 0) / (1024**3)
                print(f"  - {m['name']} ({size_gb:.1f} GB)")
        else:
            print_warning("No models installed yet")

        return True
    except Exception as e:
        print_error(f"Ollama not available: {e}")
        return False


async def test_marco_o1():
    """Test marco-o1 reasoning capabilities."""
    print_header("Marco-o1 Brain Engine Test")

    import ollama

    print_info("Testing with complex reasoning query...")

    query = """
    Think through this step by step:

    A blockchain transaction goes from address A to B.
    B then sends half to C, and keeps half.
    C sends a fraction of their portion to D.
    
    Calculate the final distribution if the original amount was 100 units.
    Show your reasoning at each step.
    """

    try:
        response = ollama.generate(
            model="marco-o1:latest",
            prompt=query,
            options={
                "temperature": 0.7,
                "num_predict": 1000,
            },
        )

        print_success("Response received!")
        print(f"\n{GREEN}--- Marco-o1 Response ---{NC}")
        print(response["response"])
        print(f"{GREEN}--- End Response ---{NC}\n")

        return True
    except Exception as e:
        print_error(f"Marco-o1 test failed: {e}")
        return False


async def test_granite():
    """Test granite3.3:8b for comparison."""
    print_header("Granite 3.3:8b Test (Comparison)")

    import ollama

    query = "Explain blockchain consensus mechanisms in 2 sentences."

    try:
        response = ollama.generate(
            model="granite3.3:8b",
            prompt=query,
            options={"temperature": 0.7, "num_predict": 200},
        )

        print_success("Granite response:")
        print(f"  {response['response'][:200]}...")
        return True
    except Exception as e:
        print_error(f"Granite test failed: {e}")
        return False


async def test_coder():
    """Test coding capabilities."""
    print_header("Code Generation Test (Qwen2.5-Coder)")

    import ollama

    query = """Write a Python function to calculate Fibonacci numbers.
    Include both iterative and recursive implementations.
    Add type hints and docstrings."""

    try:
        response = ollama.generate(
            model="qwen2.5-coder:32b",
            prompt=query,
            options={"temperature": 0.2, "num_predict": 500},
        )

        print_success("Code generated!")
        print(f"\n{MAGENTA}--- Generated Code ---{NC}")
        print(response["response"])
        print(f"{MAGENTA}--- End Code ---{NC}\n")
        return True
    except Exception as e:
        print_error(f"Coder test failed: {e}")
        return False


async def test_matrix_query():
    """Test matrix reasoning."""
    print_header("Matrix Query Test")

    import ollama

    query = """
    In a 9x9x9 matrix:
    - First dimension: Blockchains (9)
    - Second dimension: Stakeholders (9)
    - Third dimension: Trends (9)
    
    If each cell represents an intersection, how many total intersections exist?
    What's the digital root of this number?
    Explain your reasoning.
    """

    try:
        response = ollama.generate(
            model="marco-o1:latest",
            prompt=query,
            options={"temperature": 0.3, "num_predict": 500},
        )

        print_success("Matrix reasoning:")
        print(response["response"])
        return True
    except Exception as e:
        print_error(f"Matrix test failed: {e}")
        return False


async def test_beeai_integration():
    """Test integration with BeeAI framework."""
    print_header("BeeAI Framework Integration")

    try:
        from backend.llm_router import LLMRouter, ModelRole

        router = LLMRouter()

        print_info("Testing LLM Router...")

        # Test task routing
        role, config = router.route_task(
            task_complexity="reasoning", privacy_required=True
        )

        print_success(f"Router recommends: {role.value} -> {config.name}")
        return True

    except Exception as e:
        print_error(f"BeeAI integration test failed: {e}")
        return False


async def explore_marco_capabilities():
    """Explore marco-o1 specific capabilities."""
    print_header("Marco-o1 Capability Exploration")

    import ollama

    tests = [
        {
            "name": "Mathematical Reasoning",
            "query": "Solve: If x squared plus 2x plus 1 equals 9, find x. Show all steps.",
            "temp": 0.1,
        },
        {
            "name": "Chain of Thought",
            "query": "A password is 'Bee' + (year Queen Bee was created: 2024) + 'Hive'. What is the password?",
            "temp": 0.3,
        },
        {
            "name": "Logical Deduction",
            "query": "All bees are insects. Some insects can fly. What can we conclude about bees? Use formal logic.",
            "temp": 0.4,
        },
        {
            "name": "Problem Decomposition",
            "query": "Break down the problem of 'optimizing a blockchain gas fee strategy' into sub-problems.",
            "temp": 0.5,
        },
    ]

    for test in tests:
        print(f"\n{BLUE}--- {test['name']} ---{NC}")
        try:
            response = ollama.generate(
                model="marco-o1:latest",
                prompt=test["query"],
                options={"temperature": test["temp"], "num_predict": 300},
            )
            print(response["response"][:500])
        except Exception as e:
            print_error(f"Failed: {e}")

    return True


def show_model_comparison():
    """Show model comparison table."""
    print_header("Model Comparison")

    models = {
        "marco-o1:latest": {
            "type": "Reasoning Engine",
            "strengths": ["Chain of thought", "Complex math", "Logic puzzles"],
            "best_for": "Deep analysis, research",
        },
        "granite3.3:8b": {
            "type": "Orchestrator",
            "strengths": ["Reliability", "Speed", "General tasks"],
            "best_for": "General conversation, coordination",
        },
        "qwen2.5-coder:32b": {
            "type": "Code Expert",
            "strengths": ["Code generation", "Debugging", "Refactoring"],
            "best_for": "Programming tasks",
        },
        "llama3.1:8b": {
            "type": "Fast Worker",
            "strengths": ["Speed", "Low latency", "Simple tasks"],
            "best_for": "Quick responses",
        },
    }

    for name, info in models.items():
        print(f"\n{CYAN}{name}{NC}")
        print(f"  Type: {info['type']}")
        print(f"  Strengths: {', '.join(info['strengths'])}")
        print(f"  Best for: {info['best_for']}")


async def main():
    """Run all tests."""
    print(f"""
{GREEN}
╔═══════════════════════════════════════════════════════════════════╗
║     🐝 Marco-o1 Brain Engine Explorer 🧠                  ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}
    """)

    results = []

    # Check Ollama
    if not check_ollama():
        print_error("Ollama not available. Start with: ollama serve")
        return

    # Show model comparison
    show_model_comparison()

    # Test marco-o1
    results.append(("Marco-o1 Reasoning", await test_marco_o1()))

    # Test granite
    results.append(("Granite 3.3", await test_granite()))

    # Test coder
    results.append(("Qwen2.5-Coder", await test_coder()))

    # Test matrix
    results.append(("Matrix Query", await test_matrix_query()))

    # Test BeeAI integration
    results.append(("BeeAI Integration", await test_beeai_integration()))

    # Explore capabilities
    await explore_marco_capabilities()

    # Summary
    print_header("Summary")
    for name, success in results:
        if success:
            print_success(name)
        else:
            print_error(name)

    print(f"\n{GREEN}Marco-o1 exploration complete!{NC}\n")


if __name__ == "__main__":
    asyncio.run(main())
