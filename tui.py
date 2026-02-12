#!/usr/bin/env python3
"""
Hive 999 TUI — Full-screen terminal interface using prompt_toolkit.

Layout:
  ┌─────────────────────────────────────────────────────┐
  │  🐝 HIVE 999 — BeeAI Multi-Agent System    [status]│
  ├────────────┬──────────────────────┬─────────────────┤
  │ AGENTS     │   CHAT LOG           │   ANSI ART      │
  │ [keybinds] │   (scrollable)       │                  │
  ├────────────┴──────────────────────┴─────────────────┤
  │ [queen] > _                                         │
  └─────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea

# ── State ───────────────────────────────────────────────────────────

class HiveState:
    """Global TUI state."""

    def __init__(self) -> None:
        self.current_agent: str = "queen"
        self.chat_lines: list[str] = [
            "🐝 Welcome to Hive 999!",
            "   Type a message or use :commands",
            "   :queen  :worker eth  :drone gov  :forager regtech  :mantis",
            "   :art queen bee  |  :art hive  |  :art eth shrine",
            "",
        ]
        self.art_content: str = "   (no art loaded)\n\n   Use :art <name>"
        self.status: str = "IDLE"
        self.agents_loaded: dict[str, Any] = {}

    def add_chat(self, text: str) -> None:
        self.chat_lines.append(text)

    @property
    def chat_text(self) -> str:
        return "\n".join(self.chat_lines)

    @property
    def prompt_prefix(self) -> str:
        return f"[{self.current_agent}] > "


state = HiveState()

# ── Agent loading (lazy) ────────────────────────────────────────────

def _load_queen():
    if "queen" not in state.agents_loaded:
        state.add_chat("⏳ Loading Queen Bee (granite3.3:8b)...")
        from agents.queen_bee import create_queen_bee
        state.agents_loaded["queen"] = create_queen_bee()
        state.add_chat("👑 Queen Bee ready.")
    return state.agents_loaded["queen"]


def _load_mantis():
    if "mantis" not in state.agents_loaded:
        from agents.mantis_mail import create_mantis_agent
        state.agents_loaded["mantis"] = create_mantis_agent()
        state.add_chat("🦗 Mantis Mail ready (stub).")
    return state.agents_loaded["mantis"]


# ── Command processing ──────────────────────────────────────────────

async def process_input(text: str) -> None:
    """Handle user input — commands or agent queries."""
    text = text.strip()
    if not text:
        return

    # Commands
    if text.startswith(":"):
        await handle_command(text[1:])
        return

    # Send to current agent
    state.add_chat(f"\n🧑 {text}")
    state.status = "THINKING"

    try:
        if state.current_agent == "queen":
            agent = _load_queen()
            state.add_chat("👑 Queen is thinking...")
            result = await agent.run(text)
            state.add_chat(f"👑 {result.result.text}")

        elif state.current_agent == "mantis":
            mantis = _load_mantis()
            response = await mantis.run(text)
            state.add_chat(f"🦗 {response}")

        elif state.current_agent.startswith("worker:"):
            chain = state.current_agent.split(":", 1)[1]
            key = f"worker:{chain}"
            if key not in state.agents_loaded:
                state.add_chat(f"⏳ Loading Worker Bee for {chain}...")
                from agents.worker_bees.blockchain_agent import create_worker_bee
                state.agents_loaded[key] = create_worker_bee(chain)
            agent = state.agents_loaded[key]
            result = await agent.run(text)
            state.add_chat(f"🐝 [{chain}] {result.result.text}")

        elif state.current_agent.startswith("drone:"):
            sk = state.current_agent.split(":", 1)[1]
            key = f"drone:{sk}"
            if key not in state.agents_loaded:
                from agents.drone_agents.stakeholder_agent import create_drone
                state.agents_loaded[key] = create_drone(sk)
            agent = state.agents_loaded[key]
            result = await agent.run(text)
            state.add_chat(f"🔷 [{sk}] {result.result.text}")

        elif state.current_agent.startswith("forager:"):
            trend = state.current_agent.split(":", 1)[1]
            key = f"forager:{trend}"
            if key not in state.agents_loaded:
                from agents.forager_agents.trend_agent import create_forager
                state.agents_loaded[key] = create_forager(trend)
            agent = state.agents_loaded[key]
            result = await agent.run(text)
            state.add_chat(f"🌿 [{trend}] {result.result.text}")

        else:
            state.add_chat(f"❓ Unknown agent: {state.current_agent}")

    except Exception as e:
        state.add_chat(f"❌ Error: {e}")
    finally:
        state.status = "IDLE"


async def handle_command(cmd: str) -> None:
    """Process colon-commands."""
    parts = cmd.strip().split(maxsplit=1)
    verb = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if verb == "queen":
        state.current_agent = "queen"
        state.add_chat("👑 Switched to Queen Bee")

    elif verb == "worker":
        from agents.worker_bees.blockchain_agent import resolve_chain
        chain = resolve_chain(arg)
        if chain:
            state.current_agent = f"worker:{chain}"
            state.add_chat(f"🐝 Switched to Worker Bee: {chain}")
        else:
            state.add_chat(f"❓ Unknown chain alias: {arg}")

    elif verb == "drone":
        from agents.drone_agents.stakeholder_agent import resolve_stakeholder
        sk = resolve_stakeholder(arg)
        if sk:
            state.current_agent = f"drone:{sk}"
            state.add_chat(f"🔷 Switched to Drone: {sk}")
        else:
            state.add_chat(f"❓ Unknown stakeholder alias: {arg}")

    elif verb == "forager":
        from agents.forager_agents.trend_agent import resolve_trend
        trend = resolve_trend(arg)
        if trend:
            state.current_agent = f"forager:{trend}"
            state.add_chat(f"🌿 Switched to Forager: {trend}")
        else:
            state.add_chat(f"❓ Unknown trend alias: {arg}")

    elif verb == "mantis":
        state.current_agent = "mantis"
        state.add_chat("🦗 Switched to Mantis Mail")

    elif verb == "art":
        from tools.art.caterpillar_artist import caterpillar_ansi_tool
        result = caterpillar_ansi_tool.fn(art_name=arg or "queen bee")
        state.art_content = result
        state.add_chat(f"🎨 Loaded art: {arg or 'queen bee'}")

    elif verb in ("quit", "exit", "q"):
        raise SystemExit(0)

    elif verb == "help":
        state.add_chat(
            "Commands: :queen  :worker <chain>  :drone <stakeholder>  "
            ":forager <trend>  :mantis  :art <name>  :quit"
        )
    else:
        state.add_chat(f"❓ Unknown command: :{verb}")


# ── Layout ──────────────────────────────────────────────────────────

SIDEBAR_TEXT = """\
  🐝 AGENTS
  ─────────
  Alt+Q  Queen Bee
  Alt+1  Bitcoin
  Alt+2  Ethereum
  Alt+3  Solana
  Alt+4  TRON
  Alt+5  Stellar
  Alt+6  Avalanche
  Alt+7  Arbitrum
  Alt+8  Polygon
  Alt+9  Optimism

  COMMANDS
  ─────────
  :queen
  :worker <chain>
  :drone <group>
  :forager <trend>
  :mantis
  :art <name>
  :quit
"""

chat_buffer = Buffer(name="chat", read_only=True)
art_buffer = Buffer(name="art", read_only=True)
input_area = TextArea(
    height=1,
    prompt="[queen] > ",
    multiline=False,
)


def _refresh_buffers() -> None:
    chat_buffer.set_document(Document(state.chat_text), bypass_readonly=True)
    art_buffer.set_document(Document(state.art_content), bypass_readonly=True)
    input_area.prompt = state.prompt_prefix


def get_title_bar() -> str:
    return f" 🐝 HIVE 999 — BeeAI Multi-Agent System              [{state.status}] "


body = HSplit([
    # Title bar
    Window(
        content=FormattedTextControl(get_title_bar),
        height=1,
        style="bg:#333333 fg:#ffcc00 bold",
    ),
    # Main area
    VSplit([
        # Left sidebar
        Frame(
            Window(
                content=FormattedTextControl(SIDEBAR_TEXT),
                width=22,
            ),
            title="Agents",
        ),
        # Center chat
        Frame(
            Window(
                content=BufferControl(buffer=chat_buffer),
                wrap_lines=True,
            ),
            title="Chat",
        ),
        # Right art panel
        Frame(
            Window(
                content=BufferControl(buffer=art_buffer),
                width=40,
                wrap_lines=False,
            ),
            title="ANSI Art",
        ),
    ]),
    # Input
    Frame(input_area, title="Input"),
])

layout = Layout(body, focused_element=input_area)

# ── Key Bindings ────────────────────────────────────────────────────

kb = KeyBindings()

WORKER_CHAINS = [
    "Bitcoin", "Ethereum", "Solana", "TRON", "Stellar",
    "Avalanche", "Arbitrum One", "Polygon PoS", "Optimism",
]


@kb.add("escape", "q")
def _switch_queen(event) -> None:
    state.current_agent = "queen"
    state.add_chat("👑 Switched to Queen Bee")
    _refresh_buffers()


for _i, _chain in enumerate(WORKER_CHAINS, 1):
    def _make_handler(chain: str):
        @kb.add("escape", str(_i))
        def _handler(event, c=chain) -> None:
            state.current_agent = f"worker:{c}"
            state.add_chat(f"🐝 Switched to Worker: {c}")
            _refresh_buffers()
    _make_handler(_chain)


@kb.add("c-c")
def _exit(event) -> None:
    event.app.exit()


# ── Input handler ───────────────────────────────────────────────────

async def _on_accept(buff: Buffer) -> bool:
    text = buff.text
    _refresh_buffers()
    await process_input(text)
    _refresh_buffers()
    return False  # Clear the input


input_area.buffer.accept_handler = lambda buff: asyncio.ensure_future(_on_accept(buff))  # type: ignore


# ── Application ─────────────────────────────────────────────────────

app = Application(
    layout=layout,
    key_bindings=kb,
    full_screen=True,
    mouse_support=True,
)


def main() -> None:
    """Launch the Hive 999 TUI."""
    _refresh_buffers()
    app.run()


if __name__ == "__main__":
    main()
