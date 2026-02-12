from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container, Horizontal, Vertical
from typing import TYPE_CHECKING
from .agent_portfolio_widgets import AgentStatusWidget, PortfolioWidget
import asyncio
import logging

if TYPE_CHECKING:
    from monetization.core.orchestrator import MonetizationOrchestrator

class MonetizationDashboard(App):
    """Terminal 221B v2.0 - Monetization Dashboard."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-rows: 10% 90%;
    }
    #main-container {
        column-span: 2;
        layout: horizontal;
    }
    .panel {
        border: solid green;
        margin: 1;
        padding: 1;
    }
    """

    TITLE = "Terminal 221B Monetization Engine"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, orchestrator: "MonetizationOrchestrator", **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = orchestrator
        self.app_logger = logging.getLogger("MonetizationDashboard") # Renamed to app_logger

    def compose(self) -> ComposeResult:
        self.app_logger.info("Composing UI...")
        yield Header()
        yield Container(
            Vertical(AgentStatusWidget("Agents", self.orchestrator), classes="panel"),
            Vertical(PortfolioWidget("Portfolio", self.orchestrator), classes="panel"),
            id="main-container"
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.app_logger.info("Dashboard mounted. Starting orchestrator in background.")
        # Start the orchestrator's main loop as a background task
        self.orchestrator_task = asyncio.create_task(self.orchestrator.start())
        # Force an initial iteration to populate data immediately
        await self.orchestrator.run_iteration()

    async def on_unmount(self) -> None:
        self.app_logger.info("Dashboard unmounted. Stopping orchestrator.")
        self.orchestrator.stop()
        self.orchestrator_task.cancel()
        try:
            await self.orchestrator_task
        except asyncio.CancelledError:
            self.app_logger.info("Orchestrator task cancelled during unmount.")
