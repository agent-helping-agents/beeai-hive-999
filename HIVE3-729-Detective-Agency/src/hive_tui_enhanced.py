#!/usr/bin/env python3
"""
BeeAI Hive 999 - Enhanced Full-Screen Terminal UI

A production-ready TUI with:
- Scrollable chat with visual scrollbar
- Message bubbles with agent colors
- Typing indicators with animations
- Syntax highlighting for code blocks
- Rich notifications and feedback
- Ollama integration for local coding
- Comprehensive configuration system

Inspired by Ratatui patterns but implemented in Python with prompt_toolkit.

Architecture:
- Top bar: Banner with status
- Middle: VSplit of agent list | chat with bubbles & scrollbar | context panel
- Bottom: Input line with mode indicator + notifications
"""

import asyncio
import os
import sys
import time
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import threading

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from prompt_toolkit import Application, ANSI
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import (
    HSplit,
    VSplit,
    Window,
    WindowAlign,
    ConditionalContainer,
    Layout,
    ScrollOffsets,
    VerticalAlign,
    HorizontalAlign,
    Margin,
)
from prompt_toolkit.layout.controls import (
    BufferControl,
    FormattedTextControl,
    UIContent,
)
from prompt_toolkit.layout.dimension import Dimension, D
from prompt_toolkit.styles import Style, StyleTransformation
from prompt_toolkit.widgets import (
    TextArea,
    Label,
    HorizontalLine,
    VerticalLine,
    Frame,
    Box,
    Dialog,
    Button,
)
from prompt_toolkit.formatted_text import (
    FormattedText,
    HTML,
    merge_formatted_text,
    AnyFormattedText,
)
from prompt_toolkit.validation import Validator, ValidationError

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.tools.think import ThinkTool
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel

from agents.queen_bee.orchestrator import create_queen_bee, get_queen_instructions
from agents.worker_bees.blockchain_agent import create_worker_bee
from agents.drone_agents.stakeholder_agent import create_drone
from agents.forager_agents.trend_agent import create_forager
from agents.mantis_mail.mantis_agent import create_mantis_agent
from agents.bounty_hunter.bounty_agent import create_bounty_agent
from backend.llm_router import router, ModelRole
from backend.config_manager import get_config, switch_backend, AgentBackend
from tools.art.caterpillar_artist import caterpillar_ansi_tool
from tools.blockchain.matrix_search import matrix_search_tool
from tools.regtech.compliance_checker import compliance_check_tool
from tools.ibc.federation_router import federation_route_tool

# Terminal 221b integration
from terminal_221b.integration.hive_bridge import (
    register_with_tui,
    handle_221b_command,
    on_alt_d,
)


class AgentType(Enum):
    QUEEN = "queen"
    WORKER = "worker"
    DRONE = "drone"
    FORAGER = "forager"
    MANTIS = "mantis"
    DETECTIVE = "detective"


@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime
    agent_type: AgentType
    is_code: bool = False
    code_language: Optional[str] = None
    is_thinking: bool = False


@dataclass
class Notification:
    message: str
    notification_type: str  # info, success, warning, error
    timestamp: datetime
    duration: float = 3.0
    id: str = field(default_factory=lambda: str(time.time()))


@dataclass
class TypingIndicator:
    agent_name: str
    message: str
    start_time: float
    animation_frames: List[str] = field(
        default_factory=lambda: ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    )


class HiveColorScheme:
    """Digital Root 9 color palette."""

    HONEY = "#FFAC33"
    AMBER = "#FF6A00"
    GOLD = "#FFD700"
    DARK_GOLD = "#B8860B"

    ROYAL_PURPLE = "#8A2BE2"
    DEEP_VIOLET = "#4B0082"

    WORKER_CYAN = "#00FFFF"
    BLOCKCHAIN_BLUE = "#0096FF"

    DRONE_GREEN = "#32CD32"
    STAKEHOLDER_GREEN = "#228B22"

    FORAGER_MAGENTA = "#FF00FF"
    TREND_PINK = "#FF1493"

    HIVE_DARK = "#14100B"
    HIVE_DARKER = "#0A0806"
    HONEYCOMB = "#2C2116"

    DETECTIVE_RED = "#CD5C5C"
    MANTIS_LIME = "#32CD32"

    SCROLLBAR = "#FFD700"
    SCROLLBAR_TRACK = "#2C2116"

    STATUS_INFO = "#00BFFF"
    STATUS_SUCCESS = "#32CD32"
    STATUS_WARNING = "#FFA500"
    STATUS_ERROR = "#FF4500"


class HiveEnhancedTUI:
    """Enhanced BeeAI Hive TUI with scrollable chat, bubbles, scrollbar, and more."""

    def __init__(self):
        self.messages: List[Message] = []
        self.notifications: List[Notification] = []
        self.typing_indicators: Dict[str, TypingIndicator] = {}
        self.scroll_offset = 0
        self.chat_height = 20
        self.max_chat_history = 1000

        self.current_agent: Optional[RequirementAgent] = None
        self.current_agent_name: str = "Queen Bee"
        self.current_agent_type: AgentType = AgentType.QUEEN
        self.current_model: str = "granite3.3:8b"
        self.mode: str = "queen"

        self.settings_visible = False
        self.help_visible = False
        self.catalog_visible = False

        self._animation_frame = 0
        self._animation_lock = threading.Lock()

        self._setup_agent_colors()

    def _setup_agent_colors(self):
        self.agent_colors = {
            AgentType.QUEEN: HiveColorScheme.HONEY,
            AgentType.WORKER: HiveColorScheme.WORKER_CYAN,
            AgentType.DRONE: HiveColorScheme.DRONE_GREEN,
            AgentType.FORAGER: HiveColorScheme.FORAGER_MAGENTA,
            AgentType.MANTIS: HiveColorScheme.MANTIS_LIME,
            AgentType.DETECTIVE: HiveColorScheme.DETECTIVE_RED,
        }

    def add_message(
        self,
        sender: str,
        content: str,
        agent_type: AgentType,
        is_code: bool = False,
        code_language: Optional[str] = None,
    ):
        """Add a message to chat."""
        if self.max_chat_history and len(self.messages) >= self.max_chat_history:
            self.messages = self.messages[-(self.max_chat_history - 1) :]

        msg = Message(
            sender=sender,
            content=content,
            timestamp=datetime.now(),
            agent_type=agent_type,
            is_code=is_code,
            code_language=code_language,
        )
        self.messages.append(msg)
        self._scroll_to_bottom()

    def add_notification(
        self, message: str, notification_type: str = "info", duration: float = 3.0
    ):
        """Add a notification."""
        notif = Notification(
            message=message,
            notification_type=notification_type,
            timestamp=datetime.now(),
            duration=duration,
        )
        self.notifications.append(notif)

        if duration > 0:
            asyncio.create_task(self._dismiss_notification(notif))

    async def _dismiss_notification(self, notif: Notification):
        await asyncio.sleep(notif.duration)
        if notif in self.notifications:
            self.notifications.remove(notif)

    def set_typing(self, agent_name: str, message: str):
        """Set typing indicator for an agent."""
        self.typing_indicators[agent_name] = TypingIndicator(
            agent_name=agent_name, message=message, start_time=time.time()
        )

    def clear_typing(self, agent_name: str):
        """Clear typing indicator."""
        self.typing_indicators.pop(agent_name, None)

    def _scroll_to_bottom(self):
        """Scroll to bottom of chat."""
        visible_height = self.chat_height
        total_height = len(self.messages)
        self.scroll_offset = max(0, total_height - visible_height)

    def scroll_up(self, amount: int = 3):
        """Scroll chat up."""
        self.scroll_offset = max(0, self.scroll_offset - amount)

    def scroll_down(self, amount: int = 3):
        """Scroll chat down."""
        max_offset = max(0, len(self.messages) - self.chat_height)
        self.scroll_offset = min(max_offset, self.scroll_offset + amount)

    def page_up(self):
        """Page up."""
        self.scroll_up(self.chat_height)

    def page_down(self):
        """Page down."""
        self.scroll_down(self.chat_height)

    def scroll_to_top(self):
        """Scroll to top."""
        self.scroll_offset = 0

    def scroll_to_bottom(self):
        """Scroll to bottom."""
        self._scroll_to_bottom()


AGENT_SHORTCUTS = {
    "btc": ("worker", "Bitcoin", "Bitcoin"),
    "eth": ("worker", "Ethereum", "Ethereum"),
    "sol": ("worker", "Solana", "Solana"),
    "trx": ("worker", "TRON", "TRON"),
    "xlm": ("worker", "Stellar", "Stellar"),
    "avax": ("worker", "Avalanche", "Avalanche"),
    "arb": ("worker", "Arbitrum One", "Arbitrum One"),
    "matic": ("worker", "Polygon PoS", "Polygon PoS"),
    "op": ("worker", "Optimism", "Optimism"),
    "customers": ("drone", "Customers", "Customers"),
    "employees": ("drone", "Employees", "Employees"),
    "investors": ("drone", "Investors", "Investors"),
    "owners": ("drone", "Owners", "Owners"),
    "suppliers": ("drone", "Suppliers and Vendors", "Suppliers"),
    "communities": ("drone", "Communities", "Communities"),
    "unions": ("drone", "Trade Unions", "Trade Unions"),
    "gov": ("drone", "Government Agencies", "Government"),
    "media": ("drone", "Media", "Media"),
    "tokenization": ("forager", "Asset Tokenization", "Tokenization"),
    "defi": ("forager", "DeFi Maturation", "DeFi"),
    "supply": ("forager", "Supply Chain Provenance", "Supply"),
    "identity": ("forager", "Self-Sovereign Identities", "Identity"),
    "cbdc": ("forager", "CBDCs Pilots", "CBDC"),
    "ai": ("forager", "AI-Blockchain Synergies", "AI"),
    "sustainability": ("forager", "Sustainability-Compliant Mining", "Sustainability"),
    "regtech": ("forager", "RegTech Compliance Layers", "RegTech"),
    "interop": ("forager", "Cross-Chain Interoperability", "Interop"),
}


state = HiveEnhancedTUI()


def get_banner_text() -> FormattedText:
    """Return the top banner with status."""
    config = get_config()
    backend_indicator = "☁️" if config.agent_backend == "langchain_cloud" else "🏠"

    return FormattedText(
        [
            ("class:banner", "╔"),
            ("class:banner.fill", "═" * 118),
            ("class:banner", "╗\n"),
            (
                "class:banner",
                "║  🐝 BEEAI HIVE 999 ⟡ 9×9×9 REGTECH MATRIX ⟡ ETH-ENABLED ⟡ Digital Root 9  ",
            ),
            ("class:backend", f"{backend_indicator}"),
            ("class:banner", " " * 30),
            ("class:banner", "║\n"),
            ("class:banner", "╚"),
            ("class:banner.fill", "═" * 118),
            ("class:banner", "╝"),
        ]
    )


def get_status_bar_text() -> FormattedText:
    """Return status bar content."""
    config = get_config()
    backend_indicator = "☁️" if config.agent_backend == "langchain_cloud" else "🏠"

    typing_text = ""
    for agent_name, indicator in state.typing_indicators.items():
        frame = indicator.animation_frames[
            int(time.time() * 10) % len(indicator.animation_frames)
        ]
        typing_text = f"{frame} {indicator.agent_name} {indicator.message}"

    status_parts = [
        ("class:status", f" [{state.mode.upper()}] "),
        ("class:backend", f"{backend_indicator} "),
        ("class:agent", f"Agent: {state.current_agent_name} "),
        ("class:model", f"| Model: {state.current_model} "),
        ("class:count", f"| Messages: {len(state.messages)} "),
    ]

    if typing_text:
        status_parts.append(("class:typing", f"| {typing_text} "))

    status_parts.append(("class:status", "| "))

    return FormattedText(status_parts)


def format_timestamp(dt: datetime) -> str:
    """Format timestamp for messages."""
    return dt.strftime("%H:%M:%S")


def get_agent_prefix(agent_type: AgentType) -> str:
    """Get emoji prefix for agent type."""
    prefixes = {
        AgentType.QUEEN: "👑",
        AgentType.WORKER: "🐝",
        AgentType.DRONE: "🛸",
        AgentType.FORAGER: "🔍",
        AgentType.MANTIS: "📧",
        AgentType.DETECTIVE: "🕵️",
    }
    return prefixes.get(agent_type, "•")


def get_message_bubble(message: Message, index: int) -> FormattedText:
    """Format a single message as a bubble."""
    color = state.agent_colors.get(message.agent_type, HiveColorScheme.HONEY)
    timestamp = format_timestamp(message.timestamp)
    prefix = get_agent_prefix(message.agent_type)

    lines = message.content.split("\n")

    if message.is_code:
        bubble_content = []
        bubble_content.append(
            (
                "",
                f"  {message.code_language.upper() if message.code_language else 'CODE'}  ",
            )
        )
        for i, line in enumerate(lines):
            bubble_content.append(("", f"  {line}"))
        bubble_content.append(("", "  "))
        bubble_content.append(("", f"  [{timestamp}] {prefix} {message.sender}"))
        bubble_content.append(("", "  "))

        formatted = FormattedText(
            [
                ("class:bubble.header", "┌" + "─" * 60 + "┐\n"),
            ]
        )

        for style, text in bubble_content:
            formatted += FormattedText(
                [
                    (
                        f"class:bubble.{style}" if style else "class:bubble.content",
                        text + "\n",
                    )
                ]
            )

        formatted += FormattedText([("class:bubble.header", "└" + "─" * 60 + "┘\n")])
        return formatted

    bubble_lines = []
    bubble_lines.append(("", f"  [{timestamp}] {prefix} {message.sender}"))
    bubble_lines.append(("", "  "))

    for line in lines:
        bubble_lines.append(("", f"  {line}"))

    bubble_lines.append(("", "  "))

    formatted = FormattedText(
        [
            ("class:bubble.header", "┌" + "─" * 60 + "┐\n"),
        ]
    )

    for style, text in bubble_lines:
        formatted += FormattedText(
            [
                (
                    f"class:bubble.{style}" if style else "class:bubble.content",
                    text + "\n",
                )
            ]
        )

    formatted += FormattedText([("class:bubble.header", "└" + "─" * 60 + "┘\n")])

    return formatted


def get_chat_content() -> FormattedText:
    """Format the entire chat history."""
    if not state.messages:
        return FormattedText(
            [
                ("class:empty", "\n\n"),
                ("class:empty", "    🐝 Welcome to BeeAI Hive 999 🐝\n\n"),
                ("class:empty", "    Type :help for commands or start chatting!\n"),
                ("class:empty", "    Press Tab for sidebar, Ctrl+H for help\n"),
            ]
        )

    content = FormattedText()

    visible_messages = state.messages[
        state.scroll_offset : state.scroll_offset + state.chat_height
    ]

    for i, msg in enumerate(visible_messages):
        content += get_message_bubble(msg, i + state.scroll_offset)

    if len(state.messages) > state.chat_height:
        content += FormattedText(
            [
                (
                    "class:scrollbar",
                    "\n  ── Showing {0}-{1} of {2} ──".format(
                        state.scroll_offset + 1,
                        min(
                            state.scroll_offset + state.chat_height, len(state.messages)
                        ),
                        len(state.messages),
                    ),
                )
            ]
        )

    return content


def get_scrollbar() -> FormattedText:
    """Render the visual scrollbar."""
    total = len(state.messages)
    visible = state.chat_height

    if total <= visible:
        return FormattedText([("class:scrollbar.track", " " * visible)])

    thumb_size = max(1, int(visible * visible / total))
    thumb_pos = (
        int(state.scroll_offset * (visible - thumb_size) / (total - visible))
        if total > visible
        else 0
    )

    track = [" " for _ in range(visible)]
    for i in range(thumb_pos, min(thumb_pos + thumb_size, visible)):
        track[i] = "█"

    scrollbar_content = ""
    for i, char in enumerate(track):
        if i == 0:
            scrollbar_content += "▲" if state.scroll_offset > 0 else " "
        elif i == visible - 1:
            scrollbar_content += "▼" if state.scroll_offset < total - visible else " "
        else:
            scrollbar_content += char

    return FormattedText([("class:scrollbar.thumb", scrollbar_content)])


def get_agent_list_text() -> FormattedText:
    """Return the agent list panel content."""
    config = get_config()
    backend_short = "CLOUD" if config.agent_backend == "langchain_cloud" else "LOCAL"
    typing = "  " if not state.typing_indicators else "💬"

    lines = FormattedText(
        [
            ("class:panel.header", "═══ AGENTS ═══\n"),
            ("class:panel.backend", f"═══ {backend_short} ═══\n\n"),
            ("class:panel.agent", f"[Q] Queen Bee {typing}\n"),
            ("class:panel.section", "\n── Workers ──\n"),
            ("class:panel.agent", "[1] Bitcoin\n"),
            ("class:panel.agent", "[2] Ethereum\n"),
            ("class:panel.agent", "[3] Solana\n"),
            ("class:panel.agent", "[4] TRON\n"),
            ("class:panel.agent", "[5] Stellar\n"),
            ("class:panel.agent", "[6] Avalanche\n"),
            ("class:panel.agent", "[7] Arbitrum\n"),
            ("class:panel.agent", "[8] Polygon\n"),
            ("class:panel.agent", "[9] Optimism\n"),
            ("class:panel.section", "\n── Drones ──\n"),
            ("class:panel.agent", "[C] Customers\n"),
            ("class:panel.agent", "[E] Employees\n"),
            ("class:panel.agent", "[I] Investors\n"),
            ("class:panel.agent", "[O] Owners\n"),
            ("class:panel.agent", "[S] Suppliers\n"),
            ("class:panel.agent", "[M] Communities\n"),
            ("class:panel.agent", "[U] Unions\n"),
            ("class:panel.agent", "[G] Government\n"),
            ("class:panel.agent", "[D] Media\n"),
            ("class:panel.section", "\n── Special ──\n"),
            ("class:panel.agent", "[X] Mantis Mail\n"),
            ("class:panel.agent", "[N] Detective 221b\n"),
            ("class:panel.section", "\n── Commands ──\n"),
            ("class:panel.command", ":help        Help\n"),
            ("class:panel.command", ":art <topic> Art\n"),
            ("class:panel.command", ":settings    ⚙\n"),
            ("class:panel.command", ":backend local\n"),
            ("class:panel.command", ":backend cloud\n"),
            ("class:panel.command", ":quit        Exit\n"),
        ]
    )

    return lines


def get_context_panel() -> FormattedText:
    """Return the context panel with matrix visualization."""
    lines = FormattedText(
        [
            ("class:panel.header", "═══ 9×9×9 MATRIX ═══\n\n"),
            ("class:panel.context", "Active Node:\n"),
            ("class:panel.node", f"  {state.current_agent_name}\n\n"),
            ("class:panel.context", f"Messages: {len(state.messages)}\n"),
            (
                "class:panel.context",
                f"Scroll: {state.scroll_offset}/{max(0, len(state.messages) - state.chat_height)}\n\n",
            ),
            ("class:panel.context", "Matrix Position:\n"),
            ("class:panel.matrix", "  Blockchains: 9\n"),
            ("class:panel.matrix", "  Stakeholders: 9\n"),
            ("class:panel.matrix", "  Trends: 9\n"),
            ("class:panel.matrix", "  Total: 729 nodes\n"),
            ("class:panel.matrix", "  Digital Root: 9\n\n"),
            ("class:panel.context", "Backend:\n"),
            (
                "class:panel.backend",
                f"  {'Cloud' if get_config().agent_backend == 'langchain_cloud' else 'Local'}\n\n",
            ),
        ]
    )

    if state.typing_indicators:
        lines.append(("class:panel.typing", "\n── Typing ──\n"))
        for name, indicator in state.typing_indicators.items():
            frame = indicator.animation_frames[
                int(time.time() * 10) % len(indicator.animation_frames)
            ]
            lines.append(("class:panel.typing", f"{frame} {name}\n"))

    return lines


def get_notification_text() -> FormattedText:
    """Render notifications."""
    if not state.notifications:
        return FormattedText()

    content = FormattedText()
    for notif in state.notifications[-3:]:
        style_map = {
            "info": "class:notification.info",
            "success": "class:notification.success",
            "warning": "class:notification.warning",
            "error": "class:notification.error",
        }
        style = style_map.get(notif.notification_type, "class:notification.info")
        content.append((style, f"⚡ {notif.message}\n"))

    return content


chat_content_control = FormattedTextControl(lambda: get_chat_content())
scrollbar_control = FormattedTextControl(lambda: get_scrollbar())
banner_control = FormattedTextControl(lambda: get_banner_text())
status_control = FormattedTextControl(lambda: get_status_bar_text())
agent_list_control = FormattedTextControl(lambda: get_agent_list_text())
context_control = FormattedTextControl(lambda: get_context_panel())
notification_control = FormattedTextControl(lambda: get_notification_text())


banner_window = Window(
    content=banner_control, height=Dimension.exact(3), style="bg:#1a1a2e fg:#ffd700"
)

agent_list_window = Window(
    content=agent_list_control, width=Dimension.exact(22), style="bg:#0f0f23 fg:#a0a0a0"
)

chat_window = Window(
    content=chat_content_control,
    wrap_lines=True,
    style="bg:#1a1a2e fg:#e0e0e0",
    scroll_offsets=ScrollOffsets(top=5, bottom=5),
)

scrollbar_window = Window(
    content=scrollbar_control, width=Dimension.exact(1), style="bg:#0a0a0a"
)

context_window = Window(
    content=context_control, width=Dimension.exact(22), style="bg:#0f0f23 fg:#a0a0a0"
)

input_buffer = Buffer(multiline=False, accept_handler=lambda buff: on_input(buff.text))
input_window = Window(
    height=Dimension.exact(1),
    content=BufferControl(buffer=input_buffer),
    style="bg:#16213e fg:#ffffff",
)

notification_window = Window(
    content=notification_control,
    height=Dimension.exact(3),
    style="bg:#1a1a2e fg:#ffd700",
)

root_container = HSplit(
    [
        banner_window,
        VSplit(
            [
                agent_list_window,
                Window(width=1, char="│", style="fg:#333355"),
                chat_window,
                scrollbar_window,
                Window(width=1, char="│", style="fg:#333355"),
                context_window,
            ]
        ),
        HorizontalLine(),
        VSplit(
            [
                Window(
                    width=Dimension.exact(10),
                    content=FormattedTextControl(lambda: f" [{state.mode}]>"),
                ),
                input_window,
            ]
        ),
        notification_window,
        status_window
        if "status_window" in dir()
        else Window(height=Dimension.exact(1)),
    ]
)


style = Style.from_dict(
    {
        "header": "bg:#1a1a2e fg:#ffd700 bold",
        "banner": "bg:#1a1a2e fg:#ffd700",
        "banner.fill": "bg:#1a1a2e fg:#b8860b",
        "status": "bg:#16213e fg:#00ff88",
        "chat": "bg:#0f0f23 fg:#a0a0a0",
        "input": "bg:#1a1a2e fg:#e0e0e0",
        "art": "bg:#0a0a0a",
        "info": "bg:#16213e fg:#ffffff",
        "backend": "fg:#00ff88",
        "agent": "fg:#00ffff",
        "section": "fg:#ff6a00 bold",
        "command": "fg:#888888",
        "bubble.header": "fg:#444444",
        "bubble.content": "fg:#e0e0e0",
        "scrollbar.track": "bg:#2C2116",
        "scrollbar.thumb": "fg:#FFD700",
        "scrollbar": "fg:#888888",
        "panel.header": "fg:#FFAC33 bold",
        "panel.context": "fg:#888888",
        "panel.backend": "fg:#00ff88",
        "panel.agent": "fg:#00ffff",
        "panel.section": "fg:#FF6A00",
        "panel.command": "fg:#888888",
        "panel.node": "fg:#FFD700 bold",
        "panel.matrix": "fg:#00BFFF",
        "panel.typing": "fg:#FF6A00",
        "notification.info": "fg:#00BFFF",
        "notification.success": "fg:#32CD32",
        "notification.warning": "fg:#FFA500",
        "notification.error": "fg:#FF4500",
        "typing": "fg:#FF6A00",
        "model": "fg:#00ff88",
        "count": "fg:#888888",
        "empty": "fg:#666666",
        "notification": "fg:#888888",
    }
)


kb = KeyBindings()


@kb.add("c-c")
@kb.add("c-q")
def exit_app(event):
    """Exit with Ctrl+C or Ctrl+Q."""
    state.add_notification("Hive folding its wings. Goodbye.", "info")
    event.app.exit()


@kb.add("c-l")
def clear_chat(event):
    """Clear chat with Ctrl+L."""
    state.messages.clear()
    state.add_notification("Chat history cleared", "success")


@kb.add("escape", "q")
def switch_queen(event):
    """Switch to Queen Bee."""
    asyncio.create_task(_switch_agent(AgentType.QUEEN, "Queen Bee", "granite3.3:8b"))


@kb.add("escape", "1")
def switch_btc(event):
    asyncio.create_task(_switch_agent(AgentType.WORKER, "Bitcoin", "llama3.1:8b"))


@kb.add("escape", "2")
def switch_eth(event):
    asyncio.create_task(_switch_agent(AgentType.WORKER, "Ethereum", "llama3.1:8b"))


@kb.add("escape", "3")
def switch_sol(event):
    asyncio.create_task(_switch_agent(AgentType.WORKER, "Solana", "llama3.1:8b"))


@kb.add("escape", "g")
def switch_gov(event):
    asyncio.create_task(
        _switch_agent(AgentType.DRONE, "Government Agencies", "llama3.1:8b")
    )


@kb.add("escape", "x")
def switch_mantis(event):
    asyncio.create_task(_switch_agent(AgentType.MANTIS, "Mantis Mail", "llama3.1:8b"))


@kb.add("escape", "d")
def switch_detective(event):
    """Switch to Terminal 221b Detective mode."""
    on_alt_d(state)
    state.add_notification("🕵️ Detective mode activated!", "info")


@kb.add("tab")
def toggle_sidebar(event):
    """Toggle sidebar visibility."""
    state.add_notification("Use ← → arrow keys to navigate", "info")


@kb.add("c-h")
def show_help(event):
    """Show help dialog."""
    state.help_visible = not state.help_visible
    help_text = """
╔═══════════════════════════════════════╗
║  🐝 BEEAI HIVE 999 - HELP 🐝            ║
╠═══════════════════════════════════════╣
║                                       ║
║  NAVIGATION:                           ║
║    ↑/↓        Scroll chat              ║
║    PgUp/PgDn  Page scroll              ║
║    Home/End   Jump to top/bottom       ║
║    Tab        Toggle sidebar           ║
║                                       ║
║  AGENTS:                               ║
║    Alt+Q      Queen Bee                ║
║    Alt+1-9    Workers (blockchains)    ║
║    Alt+G      Government Drone         ║
║    Alt+X      Mantis Mail              ║
║    Alt+B      Bounty Hunter            ║
║    Alt+D      Detective 221b           ║
║    Alt+Shift+D Cycle personalities     ║
║                                       ║
║  COMMANDS:                             ║
║    :help       Show help               ║
║    :art <topic>  Show ANSI art        ║
║    :settings   Open settings           ║
║    :backend local|cloud  Switch       ║
║    :clear      Clear chat             ║
║    :quit       Exit TUI                ║
║                                       ║
║  🕵️ Terminal 221b Commands:            ║
║    :221b <cmd>     - Control center    ║
║    :detective <p>  - Switch personality║
║    :investigate <q>- Start investigation║
║    :simulate <tx>  - Simulate transaction║
║                                       ║
║  EDITING:                              ║
║    Ctrl+A      Select all             ║
║    Ctrl+U      Clear line             ║
║    Ctrl+K      Cut to end             ║
║    Ctrl+Y      Paste                   ║
║                                       ║
║  TIPS:                                 ║
║    • Use code blocks for code         ║
║    • Type :art queen for ASCII art     ║
║    • Set HIVE_USE_CLOUD=true for APIs ║
║                                       ║
╚═══════════════════════════════════════╝
"""
    state.add_message("System", help_text.strip(), AgentType.QUEEN)


@kb.add("c-s")
def show_settings(event):
    """Show settings."""
    state.settings_visible = not state.settings_visible
    settings_text = """
╔═══════════════════════════════════════╗
║  🐝 HIVE SETTINGS ⚙️                    ║
╠═══════════════════════════════════════╣
║                                       ║
║  Current Backend: {backend}             ║
║  Current Model: {model}                ║
║  Messages: {count}                     ║
║                                       ║
║  Available Commands:                  ║
║    :backend local  - Use Ollama       ║
║    :backend cloud  - Use LangChain    ║
║    :model <name>   - Change model     ║
║    :theme <name>   - Change theme     ║
║                                       ║
║  To change settings permanently,      ║
║  edit config/hive_workflow.yaml       ║
║                                       ║
╚═══════════════════════════════════════╝
""".format(
        backend=get_config().agent_backend,
        model=state.current_model,
        count=len(state.messages),
    )
    state.add_message("Settings", settings_text.strip(), AgentType.QUEEN)


kb.add("pageup")(lambda e: state.page_up() or e.app.layout.focused())
kb.add("pagedown")(lambda e: state.page_down() or e.app.layout.focused())
kb.add("home")(lambda e: state.scroll_to_top() or e.app.layout.focused())
kb.add("end")(lambda e: state.scroll_to_bottom() or e.app.layout.focused())
kb.add("up")(lambda e: state.scroll_up() or e.app.layout.focused())
kb.add("down")(lambda e: state.scroll_down() or e.app.layout.focused())


async def _switch_agent(agent_type: AgentType, name: str, model: str):
    """Switch to a different agent."""
    state.set_typing(name, "Initializing...")
    state.status = f"Loading {name}..."

    try:
        if agent_type == AgentType.QUEEN:
            state.current_agent = await create_queen_bee()
            state.current_model = "granite3.3:8b"
        elif agent_type == AgentType.WORKER:
            state.current_agent = await create_worker_bee(name)
            state.current_model = "llama3.1:8b"
        elif agent_type == AgentType.DRONE:
            state.current_agent = await create_drone(name)
            state.current_model = "llama3.1:8b"
        elif agent_type == AgentType.FORAGER:
            state.current_agent = await create_forager(name)
            state.current_model = "llama3.1:8b"
        elif agent_type == AgentType.MANTIS:
            state.current_agent = await create_mantis_agent()
            state.current_model = "llama3.1:8b"

        state.mode = agent_type.value
        state.current_agent_name = name
        state.current_agent_type = agent_type
        state.status = f"{name} ready"
        state.clear_typing(name)
        state.add_notification(f"Switched to {name}", "success")
        state.add_message("System", f"Switched to {name}", AgentType.QUEEN)

    except Exception as e:
        state.clear_typing(name)
        state.status = f"Error: {str(e)[:30]}"
        state.add_notification(f"Failed to load {name}: {e}", "error")


def detect_code_block(text: str) -> tuple[bool, Optional[str]]:
    """Detect if text contains a code block."""
    code_markers = [
        "```",
        "```python",
        "```js",
        "```typescript",
        "```rust",
        "```go",
        "```cpp",
        "```java",
        "```c",
        "```ruby",
        "```php",
        "```swift",
        "```kotlin",
        "```sql",
        "```bash",
        "```sh",
        "```yaml",
        "```json",
        "```xml",
        "```html",
        "```css",
        "```markdown",
        "```solidity",
    ]

    for marker in code_markers:
        if text.startswith(marker):
            lang = marker.replace("```", "").strip()
            return True, lang if lang else None

    return False, None


async def handle_command(text: str) -> bool:
    """Handle special commands."""
    text = text.strip()

    if text in (":q", ":quit", ":exit"):
        state.add_notification("Goodbye!", "info")
        return False

    if text in (":help", ":h", "?", ":?"):
        await show_help(None)
        return True

    if text == ":clear":
        state.messages.clear()
        state.add_notification("Chat cleared", "success")
        return True

    if text.startswith(":art"):
        prompt = text[4:].strip()
        if not prompt:
            state.add_notification("Usage: :art <topic>", "warning")
            return True

        result = _get_ansi_art(prompt=prompt, style="psychedelic")
        state.add_message("Caterpillar", result, AgentType.QUEEN)
        state.add_notification(f"Art loaded: {prompt}", "success")
        return True

    # Terminal 221b commands
    if text.startswith(":221b"):
        args = text[4:].strip()
        result = await handle_221b_command(args, state)
        state.add_message("System", result, AgentType.QUEEN)
        return True

    if text.startswith(":detective"):
        args = text[9:].strip()
        from terminal_221b.integration.hive_bridge import handle_detective_command

        result = await handle_detective_command(args, state)
        state.add_message("System", result, AgentType.QUEEN)
        return True

    if text.startswith(":investigate"):
        args = text[11:].strip()
        from terminal_221b.integration.hive_bridge import handle_investigate_command

        result = await handle_investigate_command(args, state)
        state.add_message("System", result, AgentType.QUEEN)
        return True

    if text.startswith(":simulate"):
        args = text[9:].strip()
        from terminal_221b.integration.hive_bridge import handle_simulate_command

        result = await handle_simulate_command(args, state)
        state.add_message("System", result, AgentType.QUEEN)
        return True

    if text == ":catalog":
        result = caterpillar_catalog()
        state.add_message("Caterpillar", result.result, AgentType.QUEEN)
        return True

    if text == ":settings":
        await show_settings(None)
        return True

    if text == ":backend local":
        switch_backend(AgentBackend.BEEAI_LOCAL)
        state.add_notification("Switched to LOCAL backend (Ollama)", "success")
        return True

    if text == ":backend cloud":
        config = get_config()
        if not config.is_cloud_available():
            state.add_notification(
                "ERROR: Cloud not configured. Set OPENAI_API_KEY", "error"
            )
            return True
        switch_backend(AgentBackend.LANGCHAIN_CLOUD)
        state.add_notification("Switched to CLOUD backend (LangChain)", "success")
        return True

    if text.startswith(":model"):
        parts = text.split()
        if len(parts) > 1:
            model_name = parts[1]
            state.current_model = model_name
            state.add_notification(f"Model set to {model_name}", "success")
        else:
            state.add_notification("Usage: :model <model_name>", "warning")
        return True

    if text.startswith(":"):
        parts = text[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "queen":
            await _switch_agent(AgentType.QUEEN, "Queen Bee", "granite3.3:8b")
            return True

        if cmd == "worker" and arg:
            if arg.lower() in AGENT_SHORTCUTS:
                _, _, full_name = AGENT_SHORTCUTS[arg.lower()]
                await _switch_agent(AgentType.WORKER, full_name, "llama3.1:8b")
            else:
                await _switch_agent(AgentType.WORKER, arg.title(), "llama3.1:8b")
            return True

        if cmd == "drone" and arg:
            if arg.lower() in AGENT_SHORTCUTS:
                _, _, full_name = AGENT_SHORTCUTS[arg.lower()]
                await _switch_agent(AgentType.DRONE, full_name, "llama3.1:8b")
            else:
                await _switch_agent(AgentType.DRONE, arg.title(), "llama3.1:8b")
            return True

        if cmd == "forager" and arg:
            if arg.lower() in AGENT_SHORTCUTS:
                _, _, full_name = AGENT_SHORTCUTS[arg.lower()]
                await _switch_agent(AgentType.FORAGER, full_name, "llama3.1:8b")
            else:
                await _switch_agent(AgentType.FORAGER, arg.title(), "llama3.1:8b")
            return True

        if cmd == "mantis":
            await _switch_agent(AgentType.MANTIS, "Mantis Mail", "llama3.1:8b")
            return True

        if cmd == "detective":
            await _switch_agent(AgentType.DETECTIVE, "Detective 221b", "granite3.3:8b")
            return True

        state.add_notification(f"Unknown command: {text}", "warning")
        return True

    return False


async def process_query(text: str):
    """Process a user query through the current agent."""
    if not state.current_agent:
        state.add_notification("No agent loaded, initializing...", "info")
        await _switch_agent(AgentType.QUEEN, "Queen Bee", "granite3.3:8b")

    state.add_message("You", text, AgentType.QUEEN)

    is_code, code_lang = detect_code_block(text)
    if is_code:
        state.add_notification(f"Code block detected ({code_lang})", "info")

    state.set_typing(state.current_agent_name, "Thinking...")

    try:
        state.status = f"{state.current_agent_name} thinking..."
        result = await state.current_agent.run(text)
        response = result.last_message.text
        state.clear_typing(state.current_agent_name)
        state.add_message(
            state.current_agent_name,
            response,
            state.current_agent_type,
            is_code=is_code,
            code_language=code_lang,
        )
        state.status = "Ready"
    except Exception as e:
        state.clear_typing(state.current_agent_name)
        state.add_notification(f"Error: {str(e)}", "error")
        state.status = "Error occurred"


async def on_input(text: str):
    """Handle user input."""
    if not text.strip():
        return

    is_command = await handle_command(text)
    if is_command:
        return

    if text.strip() in (":q", ":quit", ":exit"):
        return False

    await process_query(text)
    return True


def accept_input(buff):
    """Callback when user presses Enter."""
    text = input_buffer.text
    input_buffer.reset()

    asyncio.create_task(on_input(text))


input_buffer.accept_handler = accept_input


layout = Layout(root_container, focused_element=input_window)


async def initialize_hive():
    """Initialize the Queen Bee on startup."""
    state.status = "Initializing Hive..."
    await _switch_agent(AgentType.QUEEN, "Queen Bee", "granite3.3:8b")

    welcome_msg = """
🐝 Welcome to BeeAI Hive 999! 🐝

The 9×9×9 RegTech Matrix is ready.

Quick Start:
  • Type :help for commands
  • Alt+Q for Queen Bee
  • Alt+1-9 for Workers
  • :art <topic> for ASCII art
  • :backend cloud for LangChain

"The Hive remembers all chains..."
"""
    state.add_message("System", welcome_msg.strip(), AgentType.QUEEN)
    state.add_notification("Hive initialized", "success")


def run_tui():
    """Run the TUI application."""
    global status_window
    status_window = Window(
        content=status_control, height=Dimension.exact(1), style="bg:#16213e fg:#00ff88"
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=True,
        mouse_support=True,
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initialize_hive())

    app.run()


if __name__ == "__main__":
    run_tui()
