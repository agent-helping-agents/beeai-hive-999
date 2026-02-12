import logging
from textual.widgets import Static, DataTable
from textual.containers import Container, Vertical
from textual.app import ComposeResult
from datetime import datetime
from typing import Dict, Any

class AgentStatusWidget(Static):
    """A widget to display agent statuses."""
    def __init__(self, name: str, orchestrator_ref: Any, **kwargs):
        super().__init__(name, **kwargs)
        self.orchestrator = orchestrator_ref
        self.agent_status_display = Static("Loading data...") # Initialize as Static widget here
        self.logger = logging.getLogger(f"UI.{name}")

    def compose(self) -> ComposeResult:
        yield Static("### Agent Status")
        yield self.agent_status_display # Yield the Static widget

    def on_mount(self):
        self.logger.debug(f"{self.name} mounted.")
        self.update_timer = self.set_interval(1, self.refresh_data)

    def refresh_data(self):
        self.logger.debug(f"{self.name} refreshing data.")
        status_lines = []
        if self.orchestrator and hasattr(self.orchestrator, 'status_registry'):
            self.logger.debug(f"Orchestrator status_registry: {self.orchestrator.status_registry}")
            for agent_name, status_info in self.orchestrator.status_registry.items():
                last_run_time = datetime.fromtimestamp(status_info["last_run"]).strftime("%H:%M:%S") if status_info["last_run"] else "N/A"
                status_lines.append(f"- **{agent_name}**: {status_info['status']} | Opportunities: {status_info['opportunities']} | Last Run: {last_run_time}")
        else:
            status_lines.append("Orchestrator not connected or registry empty.")
        
        self.agent_status_display.update("\n".join(status_lines)) # Update the specific Static widget

class PortfolioWidget(Static):
    """A widget to display current holdings."""
    def __init__(self, name: str, orchestrator_ref: Any, **kwargs):
        super().__init__(name, **kwargs)
        self.orchestrator = orchestrator_ref
        self.logger = logging.getLogger(f"UI.{name}")

    def compose(self) -> ComposeResult:
        yield Static("### Portfolio Overview")
        yield DataTable()

    def on_mount(self):
        self.logger.debug(f"{self.name} mounted.")
        self.update_timer = self.set_interval(1, self.refresh_data)
        self.table = self.query_one(DataTable)
        self.table.add_columns("Asset", "Amount", "Value (USD)")

    def refresh_data(self):
        self.logger.debug(f"{self.name} refreshing data.")
        self.table.clear()
        if self.orchestrator and hasattr(self.orchestrator, 'portfolio'):
            total_value = self.orchestrator.portfolio.get_total_value()
            holdings = self.orchestrator.portfolio.holdings
            prices = self.orchestrator.portfolio.prices

            self.table.add_row("Total Value", "", f"${total_value:,.2f}")
            for token, amount in holdings.items():
                value = amount * prices.get(token, 0.0)
                self.table.add_row(token, f"{amount:,.2f}", f"${value:,.2f}")
        else:
            self.table.add_row("Orchestrator not connected or portfolio empty.", "", "")