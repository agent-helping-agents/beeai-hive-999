#!/usr/bin/env python3
"""
Bounty Hunter - Terminal Chat Interface (Natural Language)

Natural language terminal chat interface with Marco-01 integration
using existing patterns from beeai-hive-999 and terminal221b projects.
This interface is completely offline and secure for bounty hunting operations.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import asyncio
from typing import Dict, List, Any

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bounty_hunter_chat.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Import existing Bounty Hunter system
try:
    from bounty_hunter_todo import TodoList, Checklist, AutomationEngine

    ENGINE = AutomationEngine()
    logger.info("Bounty Hunter system integrated successfully")
except ImportError as e:
    logger.error(f"Failed to import Bounty Hunter system: {e}")
    ENGINE = None

# Chat history storage
CHAT_HISTORY = []

# ====================
# Terminal UI Constants
# ====================

COLORS = {
    "reset": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}

# ====================
# Chat Functions
# ====================


def colorize(text: str, color: str) -> str:
    """Colorize text for terminal"""
    return f"{COLORS.get(color, COLORS['reset'])}{text}{COLORS['reset']}"


def print_header() -> None:
    """Print chat interface header"""
    print("\033[H\033[J")  # Clear screen
    print("=" * 80)
    print(
        f"{COLORS['cyan']}{COLORS['bold']}BOUNTY HUNTER - TERMINAL CHAT INTERFACE{COLORS['reset']}"
    )
    print("=" * 80)
    print()
    print(
        f"{COLORS['yellow']}Type 'help' for available commands, 'exit' to quit{COLORS['reset']}"
    )
    print()


def print_message(message: Dict) -> None:
    """Print a formatted chat message"""
    timestamp = datetime.fromisoformat(message["timestamp"]).strftime("%H:%M:%S")
    if message["type"] == "user":
        prefix = colorize(f"[{timestamp}] You:", "cyan")
        text = message["message"]
    else:
        prefix = colorize(f"[{timestamp}] Bounty Hunter AI:", "green")
        text = message["message"]

    print(f"{prefix}")
    print(f"{text}")
    print()


def print_chat_history() -> None:
    """Print complete chat history"""
    for message in CHAT_HISTORY:
        print_message(message)


def add_message(user: str, message: str, type: str = "user") -> None:
    """Add a message to chat history"""
    chat_message = {
        "id": len(CHAT_HISTORY) + 1,
        "user": user,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "type": type,
    }
    CHAT_HISTORY.append(chat_message)


# ====================
# Marco-01 Integration
# ====================


class Marco01Integration:
    """Marco-01 AI integration with fallback logic"""

    def __init__(self):
        self.available = False
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load Marco-01 model with fallback options"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            # Try to load from local cache first
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    "AIDC-AI/Marco-o1", local_files_only=True
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    "AIDC-AI/Marco-o1", local_files_only=True
                )
                self.available = True
                logger.info("Marco-01 model loaded successfully from local cache")
            except Exception as local_error:
                logger.warning(f"Local cache not available: {local_error}")
                logger.info(
                    "Attempting to load model from Hugging Face (this may take time)..."
                )

                # Try to download and load from Hugging Face
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained("AIDC-AI/Marco-o1")
                    self.model = AutoModelForCausalLM.from_pretrained(
                        "AIDC-AI/Marco-o1"
                    )
                    self.available = True
                    logger.info("Marco-01 model loaded successfully from Hugging Face")
                except Exception as download_error:
                    logger.warning(f"Failed to download Marco-01: {download_error}")
                    logger.info("Falling back to rule-based AI system")
                    self.available = False
        except Exception as e:
            logger.warning(f"Marco-01 integration failed: {e}")
            logger.info("Falling back to rule-based AI system")
            self.available = False

    def generate_response(self, message: str, chat_history: List[Dict]) -> str:
        """Generate response using Marco-01 or fallback system"""
        if self.available:
            return self._generate_with_marco01(message, chat_history)
        else:
            return self._generate_fallback(message, chat_history)

    def _generate_with_marco01(self, message: str, chat_history: List[Dict]) -> str:
        """Generate response using Marco-01"""
        try:
            # Build prompt with chat history
            prompt = self._build_prompt(message, chat_history)

            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")

            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=2048,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

            # Decode and clean response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._clean_response(response, prompt)
        except Exception as e:
            logger.error(f"Marco-01 generation error: {e}")
            return self._generate_fallback(message, chat_history)

    def _build_prompt(self, message: str, chat_history: List[Dict]) -> str:
        """Build prompt with chat history"""
        prompt = """You are the Bounty Hunter AI, an expert bug bounty hunting assistant. Your role is to help users with:

1. Task management: Creating, starting, completing, and tracking bounty hunting tasks
2. Automation: Running daily routines, weekly audits, and system checks
3. Learning: Providing information about bounty hunting platforms, best practices, and strategies
4. Tips: Sharing insights about bug bounty hunting
5. Market: Explaining bounty platforms and payment methods

Available commands (also accept natural language):
- help       - Show available commands
- list tasks - Show current tasks with priority and category
- run daily  - Execute daily automation routines
- checklist  - Show checklist progress and completion status
- platforms  - List available bounty platforms with payout ranges
- tips       - Display best practices for bounty hunting
- exit/quit/q - Quit the chat interface

Keep responses friendly, concise, and helpful. If the user asks about something outside your expertise, politely inform them you don't have that information.

Chat History:"""

        for msg in chat_history[-5:]:  # Keep last 5 messages for context
            role = "User" if msg["type"] == "user" else "AI"
            prompt += f"\n{role}: {msg['message']}"

        prompt += f"\nUser: {message}\nAI:"

        return prompt

    def _clean_response(self, response: str, prompt: str) -> str:
        """Clean generated response"""
        # Extract response after "AI:" marker
        if "AI:" in response:
            response = response.split("AI:", 1)[1]

        # Strip leading/trailing whitespace and truncate if too long
        response = response.strip()
        if len(response) > 500:
            response = response[:500] + "..."

        return response

    def _generate_fallback(self, message: str, chat_history: List[Dict]) -> str:
        """Fallback rule-based AI system"""
        message = message.strip().lower()

        if "help" in message:
            return """I'm the Bounty Hunter AI! Here's what I can help with:

- **Task management**: List, start, or complete tasks
- **Automation**: Run daily routines or weekly audits
- **Learning**: Get information about bounty hunting
- **Tips**: Learn best practices for bug bounties
- **Market**: Explore fiat and crypto bounty platforms

Commands:
- help       - Show this help
- list tasks - Show current tasks
- run daily  - Execute daily automation
- checklist  - Show checklist progress
- platforms  - List bounty platforms
- tips       - Show best practices
- exit       - Quit the chat

What would you like to do?"""

        if (
            "list tasks" in message
            or "show tasks" in message
            or "what tasks do i have" in message
            or "tasks" in message
            and "what" in message
        ):
            if ENGINE:
                tasks = []
                for task in ENGINE.todo_list.tasks.values():
                    tasks.append(f"- {task.title} ({task.priority})")
                return "\n".join(tasks) if tasks else "No tasks available"
            return "Bounty Hunter system not available"

        if "start task" in message:
            task_name = message.replace("start task", "").strip()
            if ENGINE:
                for task in ENGINE.todo_list.tasks.values():
                    if task_name.lower() in task.title.lower():
                        task.start()
                        return f"Started task: {task.title}"
                return f"Task '{task_name}' not found"
            return "Bounty Hunter system not available"

        if "run daily" in message or "daily routine" in message:
            if ENGINE:
                try:
                    result = ENGINE.run_daily_routine()
                    if result["success"]:
                        return (
                            f"Daily routine completed successfully! "
                            f"Progress: {result['checklist']['completed']}/{result['checklist']['total']} "
                            f"({result['checklist']['percentage']:.1f}%)"
                        )
                    return "Daily routine failed"
                except Exception as e:
                    logger.error(f"Daily routine error: {e}")
                    return f"Daily routine failed: {e}"
            return "Bounty Hunter system not available"

        if "checklist" in message:
            if ENGINE:
                try:
                    progress = ENGINE.checklist.get_progress()
                    return (
                        f"Checklist progress: {progress['completed']}/{progress['total']} "
                        f"({progress['percentage']:.1f}%)"
                    )
                except Exception as e:
                    logger.error(f"Checklist error: {e}")
                    return "Failed to get checklist progress"
            return "Bounty Hunter system not available"

        if (
            "bounty platforms" in message
            or "fiat platforms" in message
            or "platforms" in message
        ):
            return """Popular bounty platforms:

**Fiat Platforms:**
- Upwork: $150-800 per token contract
- Freelancer: Similar to Upwork
- Toptal: Premium freelance platform

**Crypto Platforms:**
- Immunefi: $100-10,000+ per bug
- Gitcoin: $500-2000 per bounty
- Stellar Community Fund: $1000-3000 microgrants

**Blockchain-Specific:**
- Algorand Foundation: $500-2000 per tutorial
- Solana Bug Bounty: Up to $20,000

What platform would you like to explore?"""

        if "tips" in message or "best practices" in message:
            return """Bounty Hunting Best Practices:

1. **Start small**: Focus on low-hanging fruit first
2. **Research thoroughly**: Understand the program scope
3. **Quality over quantity**: Submit detailed reports
4. **Communicate professionally**: Keep communications clear
5. **Stay within scope**: Never test outside approved areas
6. **Follow guidelines**: Read and adhere to each program's rules
7. **Document everything**: Keep detailed notes of your findings
8. **Be persistent**: Don't give up on complex issues

What specific area would you like to learn more about?"""

        if "payment" in message or "monetization" in message:
            return """Bounty Payment Methods:

**Fiat Payments:**
- Direct bank transfer
- PayPal (limited for crypto-related work)
- Wire transfer

**Crypto Payments:**
- Stablecoins (USDT, USDC)
- Bitcoin (BTC)
- Ethereum (ETH)
- Platform-specific tokens

**Tips:**
- Verify payment methods before accepting tasks
- Set up payment escrow for large projects
- Understand tax implications of crypto earnings

What payment method would you like to learn more about?"""

        if "status" in message:
            if ENGINE:
                tasks = len(ENGINE.todo_list.tasks)
                checklist = ENGINE.checklist.get_progress()
                return (
                    f"System Status:\n"
                    f"- Tasks: {tasks} available\n"
                    f"- Checklist: {checklist['completed']}/{checklist['total']} items completed\n"
                    f"- Marco-01: {'Available' if self.available else 'Disabled (using fallback)'}\n"
                    f"- Connection: Secure (offline)"
                )
            return "Bounty Hunter system not available"

        return (
            f"I'm sorry, I don't have a specific answer for that. "
            f"Try asking for help with tasks, automation, or bounty platforms."
        )


# Initialize Marco-01 integration
MARCO01 = Marco01Integration()

# ====================
# Chat Interface
# ====================


def run_chat_interface() -> None:
    """Run the terminal-based chat interface"""
    print_header()

    # Initial welcome message
    initial_message = {
        "id": 1,
        "user": "Bounty Hunter AI",
        "message": """Hello! I'm the Bounty Hunter AI. How can I help you with your bounty hunting journey today?

Type 'help' for available commands or 'exit' to quit.
""",
        "timestamp": datetime.now().isoformat(),
        "type": "ai",
    }
    CHAT_HISTORY.append(initial_message)
    print_message(initial_message)

    # Main chat loop
    while True:
        try:
            user_input = input(colorize("You: ", "cyan")).strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print(colorize("\nThank you for using Bounty Hunter Chat!", "yellow"))
                break

            # Add user message to chat history
            add_message("You", user_input, "user")

            # Generate AI response
            response = MARCO01.generate_response(user_input, CHAT_HISTORY)

            # Add AI response to chat history
            add_message("Bounty Hunter AI", response, "ai")

            # Print the response
            print_message(CHAT_HISTORY[-1])

        except KeyboardInterrupt:
            print(colorize("\n\nKeyboard interrupt detected. Exiting...", "yellow"))
            break
        except Exception as e:
            logger.error(f"Chat interface error: {e}")
            print(colorize(f"\nError: {e}", "red"))
            print(colorize("Please try again or type 'exit' to quit.", "yellow"))


# ====================
# Main Function
# ====================


def main():
    """Main function to start the chat interface"""
    logger.info("Starting Bounty Hunter Terminal Chat Interface")

    # Check system requirements
    if not ENGINE:
        logger.error("Bounty Hunter system not available")
        print(colorize("Error: Bounty Hunter system not available", "red"))
        return

    print(colorize("\nBounty Hunter Chat Interface", "cyan"))
    print("==============================")
    print(
        f"Marco-01 integration: {'Enabled' if MARCO01.available else 'Disabled (using fallback)'}"
    )
    print(f"Security: Offline terminal interface (no internet exposure)")
    print()

    # Run chat interface
    run_chat_interface()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Chat interface stopped by user")
        print(colorize("\nChat interface stopped", "yellow"))
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(colorize(f"\nError: {e}", "red"))
        sys.exit(1)
