"""\
# ═══════════════════════════════════════════════════════════════════════════════
\
# HIVE³ - The 729 Detective Agency
\
# Copyright (c) 2026 HIVE³ Organization
\
# Licensed under the HIVE³ Commercial License v1.0
\
# See LICENSE.md for full terms
\
#
\
# This file is part of the HIVE³ multi-agent system:
\
# - 9 Blockchains × 9 Stakeholders × 9 Trends = 729 nodes
\
# - 28 Specialized AI Agents (Queen + Workers + Drones + Foragers + Mantis)
\
# - Solana Blockchain Integration
\
# - Terminal 221b Detective Framework
\
#
\
# Digital Root: 9
\
# ═══════════════════════════════════════════════════════════════════════════════
\
\"\""
\


#!/usr/bin/env python3
"""
🐝 Enhanced Hive TUI - Ratatui-Inspired Implementation

Features:
- Scrollable chat with visual scrollbar
- ANSI art integration
- 3-panel layout (sidebar | chat | context)
- Color-coded agent message bubbles
- Honey/amber color scheme

Inspired by Ratatui patterns, implemented with prompt_toolkit
"""

import asyncio
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict, Tuple

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import (
    ConditionalContainer,
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
    Layout as PTLayout,
)
from prompt_toolkit.layout.controls import (
    BufferControl,
    FormattedTextControl,
)
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import (
    Frame,
    TextArea,
    Label,
    HorizontalLine,
    VerticalLine,
)
from prompt_toolkit.formatted_text import ANSI, HTML, FormattedText, to_formatted_text
from prompt_toolkit.output import ColorDepth


# ═══════════════════════════════════════════════════════════════════════════
# Color Palette - "Digital Root 9"
# ═══════════════════════════════════════════════════════════════════════════

class HiveColors:
    """ANSI color palette inspired by honey and the hive"""
    
    # Honey/Amber (Primary)
    HONEY = "#FFAC33"
    AMBER = "#FF6A00"
    GOLD = "#FFD700"
    DARK_GOLD = "#B8860B"
    
    # Royal (Queen)
    ROYAL_PURPLE = "#8A2BE2"
    DEEP_VIOLET = "#4B0082"
    
    # Workers (Cyan/Blue)
    WORKER_CYAN = "#00FFFF"
    BLOCKCHAIN_BLUE = "#0096FF"
    
    # Drones (Green)
    DRONE_GREEN = "#32CD32"
    STAKEHOLDER_GREEN = "#228B22"
    
    # Foragers (Magenta)
    FORAGER_MAGENTA = "#FF00FF"
    TREND_PINK = "#FF1493"
    
    # Detectives (Red/Brown)
    DETECTIVE_RED = "#DC143C"
    SHERLOCK_BROWN = "#8B4513"
    
    # Background
    HIVE_DARK = "#14100B"
    HIVE_DARKER = "#0A0806"
    HONEYCOMB = "#2C2116"
    
    # Neutral
    WHITE = "#FFFFFF"
    GRAY = "#808080"
    DARK_GRAY = "#404040"


# ═══════════════════════════════════════════════════════════════════════════
# Agent Types & Message Model
# ═══════════════════════════════════════════════════════════════════════════

class AgentType(Enum):
    QUEEN = ("👑 Queen Bee", HiveColors.AMBER, "hive_logo.ans")
    WORKER = ("🐝 Worker", HiveColors.WORKER_CYAN, "worker_bee.ans")
    DRONE = ("🛸 Drone", HiveColors.DRONE_GREEN, "drone_agent.ans")
    FORAGER = ("🔍 Forager", HiveColors.FORAGER_MAGENTA, "forager_agent.ans")
    DETECTIVE = ("🕵️ Detective", HiveColors.DETECTIVE_RED, "detective_221b.ans")
    MANTIS = ("📧 Mantis", HiveColors.DRONE_GREEN, "mantis_mail.ans")
    USER = ("You", HiveColors.WHITE, None)
    SYSTEM = ("System", HiveColors.GRAY, None)
    
    def __init__(self, label: str, color: str, art_file: Optional[str]):
        self.label = label
        self.color = color
        self.art_file = art_file


@dataclass
class ChatMessage:
    """A single chat message"""
    content: str
    agent_type: AgentType
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def format_lines(self, width: int = 80) -> List[Tuple[str, str]]:
        """Format message as list of (style, text) tuples"""
        lines = []
        
        # Header with timestamp
        time_str = self.timestamp.strftime("%H:%M:%S")
        lines.append((f"fg:{HiveColors.DARK_GRAY}", f"[{time_str}] "))
        lines.append((f"fg:{self.agent_type.color} bold", f"{self.agent_type.label}:"))
        lines.append(("", "\n"))
        
        # Content lines with indentation
        content_lines = self._wrap_text(self.content, width - 4)
        for line in content_lines:
            lines.append((f"fg:{self.agent_type.color}", f"  {line}"))
            lines.append(("", "\n"))
        
        # Empty line after message
        lines.append(("", "\n"))
        return lines
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [""]


# ═══════════════════════════════════════════════════════════════════════════
# Scrollable Chat Widget (Ratatui-inspired)
# ═══════════════════════════════════════════════════════════════════════════

class ScrollableChat:
    """
    Scrollable chat history widget inspired by Ratatui's Scrollbar pattern
    """
    
    def __init__(self, height: int = 20):
        self.messages: List[ChatMessage] = []
        self.scroll_offset: int = 0
        self.viewport_height: int = height
        self.follow_bottom: bool = True
        self.content_lines: List[Tuple[str, str]] = []
        
    def add_message(self, message: ChatMessage) -> None:
        """Add a message and update content"""
        self.messages.append(message)
        self._rebuild_content()
        
        if self.follow_bottom:
            self.scroll_to_bottom()
    
    def _rebuild_content(self) -> None:
        """Rebuild the formatted content from messages"""
        self.content_lines = []
        for msg in self.messages:
            self.content_lines.extend(msg.format_lines())
    
    def scroll_up(self, lines: int = 3) -> None:
        """Scroll up by N lines"""
        self.follow_bottom = False
        self.scroll_offset = max(0, self.scroll_offset - lines)
    
    def scroll_down(self, lines: int = 3) -> None:
        """Scroll down by N lines"""
        max_offset = max(0, len(self.content_lines) - self.viewport_height)
        self.scroll_offset = min(max_offset, self.scroll_offset + lines)
        
        # Re-enable auto-scroll if at bottom
        if self.scroll_offset >= max_offset:
            self.follow_bottom = True
    
    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of chat"""
        self.scroll_offset = max(0, len(self.content_lines) - self.viewport_height)
        self.follow_bottom = True
    
    def page_up(self) -> None:
        """Page up"""
        self.scroll_up(self.viewport_height - 2)
    
    def page_down(self) -> None:
        """Page down"""
        self.scroll_down(self.viewport_height - 2)
    
    def get_visible_content(self) -> FormattedText:
        """Get the currently visible portion of chat"""
        start = self.scroll_offset
        end = min(len(self.content_lines), start + self.viewport_height)
        
        visible = self.content_lines[start:end]
        
        # Pad with empty lines if needed
        while len(visible) < self.viewport_height:
            visible.append(("", "\n"))
        
        return visible
    
    def get_scrollbar_info(self) -> Tuple[int, int, int]:
        """Get scrollbar info: (position, content_length, viewport_length)"""
        content_length = max(1, len(self.content_lines))
        return (self.scroll_offset, content_length, self.viewport_height)
    
    def render_scrollbar(self, height: int) -> str:
        """Render a visual scrollbar"""
        if len(self.content_lines) <= self.viewport_height:
            return "│\n" * height
        
        _, content_len, viewport_len = self.get_scrollbar_info()
        ratio = viewport_len / content_len
        thumb_size = max(1, int(height * ratio))
        
        thumb_pos = int((self.scroll_offset / content_len) * height)
        thumb_pos = min(thumb_pos, height - thumb_size)
        
        lines = []
        for i in range(height):
            if thumb_pos <= i < thumb_pos + thumb_size:
                lines.append("█\n")
            elif i == 0:
                lines.append("▲\n")
            elif i == height - 1:
                lines.append("▼\n")
            else:
                lines.append("│\n")
        
        return "".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# ANSI Art Loader
# ═══════════════════════════════════════════════════════════════════════════

class ArtLibrary:
    """Library for loading and caching ANSI art files"""
    
    def __init__(self, art_dir: str = "art"):
        self.art_dir = art_dir
        self._cache: Dict[str, str] = {}
    
    def load(self, filename: str) -> str:
        """Load an ANSI art file"""
        if filename in self._cache:
            return self._cache[filename]
        
        filepath = os.path.join(self.art_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self._cache[filename] = content
            return content
        return f"[Art not found: {filename}]"
    
    def get_formatted(self, filename: str) -> FormattedText:
        """Get art as formatted text"""
        content = self.load(filename)
        return to_formatted_text(ANSI(content))


# ═══════════════════════════════════════════════════════════════════════════
# Main TUI Application
# ═══════════════════════════════════════════════════════════════════════════

class HiveTUI:
    """Main Hive TUI Application"""
    
    def __init__(self):
        self.art_library = ArtLibrary()
        self.chat = ScrollableChat(height=25)
        self.selected_agent: AgentType = AgentType.QUEEN
        self.show_matrix_panel: bool = True
        self.show_sidebar: bool = True
        
        # Sample messages
        self._load_sample_data()
        
        # Create UI components
        self._create_layout()
        self._create_keybindings()
    
    def _load_sample_data(self) -> None:
        """Load some sample chat messages"""
        sample_messages = [
            (AgentType.QUEEN, "Welcome to Hive 999. All systems operational. The 9×9×9 matrix is active with 729 intersection nodes."),
            (AgentType.WORKER, "Bitcoin network analysis complete. Hash rate at 450 EH/s. Difficulty adjustment in 3 blocks."),
            (AgentType.DRONE, "Stakeholder alert: New SEC guidance on crypto custody affects Investors node."),
            (AgentType.FORAGER, "Trend detected: Asset Tokenization sector showing 340% YoY growth."),
            (AgentType.DETECTIVE, "Solana transaction analysis: Detected unusual pattern in SPL token transfers. Investigating..."),
            (AgentType.SYSTEM, "Worker Bee 3 (Avalanche) connected. Model: llama3.2:3b"),
            (AgentType.QUEEN, "Routing query to optimal worker. Privacy level: Local. Backend: Ollama."),
            (AgentType.WORKER, "Ethereum gas analysis: Current base fee 15 gwei. Optimal transaction window identified."),
            (AgentType.USER, "What's the current status of the CBDC pilots trend?"),
            (AgentType.FORAGER, "CBDC Pilots: 134 countries exploring, 65 in advanced phases. China (e-CNY) leads with $250B+ transaction volume."),
        ]
        
        for agent, content in sample_messages:
            msg = ChatMessage(content=content, agent_type=agent)
            self.chat.add_message(msg)
    
    def _create_layout(self) -> None:
        """Create the TUI layout (3-panel design)"""
        
        # Header with logo
        header_art = self.art_library.get_formatted("hive_logo.ans")
        self.header = Window(
            content=FormattedTextControl(header_art),
            height=Dimension.exact(10),
            style=f"bg:{HiveColors.HIVE_DARKER}",
        )
        
        # Sidebar - Agent selector
        self.sidebar = self._create_sidebar()
        
        # Main chat area with scrollbar
        self.chat_window = self._create_chat_window()
        
        # Context panel (matrix info)
        self.context_panel = self._create_context_panel()
        
        # Input area
        self.input_buffer = Buffer(multiline=False)
        self.input_area = TextArea(
            height=Dimension.exact(3),
            prompt="> ",
            style=f"fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARKER}",
            focus_on_click=True,
        )
        self.input_area.buffer = self.input_buffer
        
        # Status bar
        self.status_bar = Label(
            text=f" 🐝 Hive 999 │ Backend: Local │ Agents: 28 │ Nodes: 729 │ Press ? for help ",
            style=f"fg:{HiveColors.HIVE_DARK} bg:{HiveColors.HONEY}",
        )
        
        # Main content area (sidebar | chat | context)
        content_row = VSplit([
            ConditionalContainer(
                content=self.sidebar,
                filter=lambda: self.show_sidebar,
            ),
            VerticalLine(),
            self.chat_window,
            ConditionalContainer(
                content=VSplit([
                    VerticalLine(),
                    self.context_panel,
                ]),
                filter=lambda: self.show_matrix_panel,
            ),
        ])
        
        # Root layout
        root_container = HSplit([
            self.header,
            HorizontalLine(),
            content_row,
            HorizontalLine(),
            self.input_area,
            self.status_bar,
        ])
        
        self.layout = PTLayout(root_container)
    
    def _create_sidebar(self) -> Frame:
        """Create the agent sidebar"""
        agents = [
            AgentType.QUEEN,
            AgentType.WORKER,
            AgentType.DRONE,
            AgentType.FORAGER,
            AgentType.DETECTIVE,
            AgentType.MANTIS,
        ]
        
        lines = []
        for agent in agents:
            cursor = ">>> " if agent == self.selected_agent else "    "
            lines.append((f"fg:{agent.color} bold", f"{cursor}{agent.label}\n"))
        
        sidebar_content = FormattedTextControl(lines)
        
        return Frame(
            Window(content=sidebar_content, width=Dimension.exact(20)),
            title=" Agents ",
            style=f"fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARK}",
        )
    
    def _create_chat_window(self) -> Frame:
        """Create the scrollable chat window"""
        
        def get_chat_content() -> FormattedText:
            return self.chat.get_visible_content()
        
        def get_scrollbar() -> str:
            return self.chat.render_scrollbar(self.chat.viewport_height)
        
        chat_control = FormattedTextControl(get_chat_content)
        scrollbar_control = FormattedTextControl(
            lambda: [(f"fg:{HiveColors.AMBER}", get_scrollbar())]
        )
        
        chat_with_scrollbar = VSplit([
            Window(content=chat_control),
            Window(
                content=scrollbar_control,
                width=Dimension.exact(1),
                style=f"fg:{HiveColors.AMBER}",
            ),
        ])
        
        return Frame(
            chat_with_scrollbar,
            title=" 💬 Hive Chat ",
            style=f"fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARK}",
        )
    
    def _create_context_panel(self) -> Frame:
        """Create the context panel with matrix info"""
        matrix_art = self.art_library.get_formatted("matrix_729.ans")
        
        return Frame(
            Window(
                content=FormattedTextControl(matrix_art),
                width=Dimension.exact(50),
            ),
            title=" 9×9×9 Matrix ",
            style=f"fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARK}",
        )
    
    def _create_keybindings(self) -> None:
        """Create keyboard shortcuts"""
        self.kb = KeyBindings()
        
        @self.kb.add('q', filter=lambda: True)
        def _(event):
            """Quit"""
            event.app.exit()
        
        @self.kb.add('up')
        def _(event):
            """Scroll up"""
            self.chat.scroll_up()
            self._refresh()
        
        @self.kb.add('down')
        def _(event):
            """Scroll down"""
            self.chat.scroll_down()
            self._refresh()
        
        @self.kb.add('pageup')
        def _(event):
            """Page up"""
            self.chat.page_up()
            self._refresh()
        
        @self.kb.add('pagedown')
        def _(event):
            """Page down"""
            self.chat.page_down()
            self._refresh()
        
        @self.kb.add('home')
        def _(event):
            """Scroll to top"""
            self.chat.scroll_offset = 0
            self.chat.follow_bottom = False
            self._refresh()
        
        @self.kb.add('end')
        def _(event):
            """Scroll to bottom"""
            self.chat.scroll_to_bottom()
            self._refresh()
        
        @self.kb.add('tab')
        def _(event):
            """Toggle sidebar"""
            self.show_sidebar = not self.show_sidebar
            self._refresh()
        
        @self.kb.add('c-t')
        def _(event):
            """Toggle matrix panel"""
            self.show_matrix_panel = not self.show_matrix_panel
            self._refresh()
        
        @self.kb.add('c-n')
        def _(event):
            """Cycle to next agent"""
            agents = list(AgentType)[:6]  # First 6 agents
            current_idx = agents.index(self.selected_agent)
            self.selected_agent = agents[(current_idx + 1) % len(agents)]
            self.sidebar = self._create_sidebar()
            self._refresh()
        
        @self.kb.add('enter')
        def _(event):
            """Send message"""
            text = self.input_buffer.text.strip()
            if text:
                msg = ChatMessage(
                    content=text,
                    agent_type=AgentType.USER,
                )
                self.chat.add_message(msg)
                self.input_buffer.reset()
                self._refresh()
    
    def _refresh(self) -> None:
        """Refresh the UI"""
        # Recreate components that need updating
        self.chat_window = self._create_chat_window()
        self.sidebar = self._create_sidebar()
        
        # Update layout
        content_row = VSplit([
            ConditionalContainer(
                content=self.sidebar,
                filter=lambda: self.show_sidebar,
            ),
            VerticalLine(),
            self.chat_window,
            ConditionalContainer(
                content=VSplit([
                    VerticalLine(),
                    self.context_panel,
                ]),
                filter=lambda: self.show_matrix_panel,
            ),
        ])
        
        root_container = HSplit([
            self.header,
            HorizontalLine(),
            content_row,
            HorizontalLine(),
            self.input_area,
            self.status_bar,
        ])
        
        self.layout = PTLayout(root_container)
        
        # Invalidate to trigger redraw
        if hasattr(self, 'app') and self.app:
            self.app.layout = self.layout
            self.app.invalidate()
    
    def run(self) -> None:
        """Run the TUI application"""
        style = Style.from_dict({
            '': f'fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARK}',
            'frame.border': f'fg:{HiveColors.AMBER}',
            'frame.label': f'fg:{HiveColors.GOLD} bold',
            'text-area': f'fg:{HiveColors.HONEY} bg:{HiveColors.HIVE_DARKER}',
            'text-area.prompt': f'fg:{HiveColors.AMBER} bold',
        })
        
        self.app = Application(
            layout=self.layout,
            key_bindings=self.kb,
            style=style,
            full_screen=True,
            mouse_support=True,
            color_depth=ColorDepth.TRUE_COLOR,
        )
        
        self.app.run()


# ═══════════════════════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    print("Starting Hive 999 Enhanced TUI...")
    print("Loading ANSI art library...")
    
    tui = HiveTUI()
    
    print("Launching interface...")
    print("Keys: ↑/↓=Scroll, PgUp/PgDn=Page, Home/End=Top/Bottom,")
    print("      Tab=Toggle Sidebar, Ctrl+T=Toggle Matrix, Ctrl+N=Next Agent, Q=Quit")
    input("Press Enter to continue...")
    
    tui.run()


if __name__ == "__main__":
    main()
