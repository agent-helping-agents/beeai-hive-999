"""
Hive Bridge - Integration between Terminal 221b and BeeAI Hive 999

Enables the TUI to dispatch to Detective agents alongside the existing
Queen/Worker/Drone/Forager hierarchy. Adds:
- :detective command for 221b mode
- :investigate command for case management
- :simulate command for safe transaction testing
- Alt+D keybinding for quick detective access

"Elementary, my dear Watson. The Hive has expanded."
"""

import asyncio
from typing import Optional, Dict, Any, TYPE_CHECKING
from enum import Enum

# Avoid circular imports
if TYPE_CHECKING:
    from tui import HiveTUIState

from terminal_221b.agents.advisor_deps import AdvisorDeps, get_simulation_config
from terminal_221b.agents.detective_agent import DetectiveAgent, create_detective
from terminal_221b.simulation.sim_server import SimServer


class DetectiveMode(Enum):
    """Available detective specializations."""
    HOLMES = "holmes"
    WATSON = "watson"
    MYCROFT = "mycroft"
    IRENE = "irene"


# Global state for detective integration
_detective_state: Dict[str, Any] = {
    "active": False,
    "current_agent": None,
    "mode": DetectiveMode.HOLMES,
    "sim_server": None,
}


async def register_with_tui(tui_state: "HiveTUIState") -> Dict[str, Any]:
    """
    Register Terminal 221b capabilities with the Hive TUI.
    
    Call this from tui.py initialization to add detective functionality.
    
    Returns:
        Registration info for keybindings and commands
    """
    return {
        "keybindings": {
            "alt-d": "switch_detective",
            "alt-shift-d": "switch_detective_next",
        },
        "commands": {
            ":detective": {
                "handler": handle_detective_command,
                "help": "Switch to detective mode: :detective [holmes|watson|mycroft|irene]"
            },
            ":investigate": {
                "handler": handle_investigate_command,
                "help": "Start investigation: :investigate <address or query>"
            },
            ":simulate": {
                "handler": handle_simulate_command,
                "help": "Simulate transaction: :simulate <description>"
            },
            ":221b": {
                "handler": handle_221b_command,
                "help": "Terminal 221b control center"
            },
        },
        "art_entries": {
            "detective": "detective_office.ans",
            "holmes": "holmes_portrait.ans",
            "magnifying_glass": "magnifying_glass.ans",
            "sherlock": "sherlock_silhouette.ans",
        }
    }


async def handle_221b_command(args: str, tui_state: "HiveTUIState") -> str:
    """
    Main 221b command handler - the control center.
    
    Usage:
        :221b status          - Show detective status
        :221b mode holmes     - Switch to Holmes personality
        :221b sim start       - Start simulation server
        :221b sim stop        - Stop simulation server
        :221b env simulation  - Switch to simulation environment
        :221b env devnet      - Switch to devnet
    """
    parts = args.strip().split()
    if not parts:
        return _get_221b_help()
    
    subcommand = parts[0].lower()
    
    if subcommand == "status":
        return await _get_status()
    
    elif subcommand == "mode":
        if len(parts) < 2:
            return "Usage: :221b mode [holmes|watson|mycroft|irene]"
        return await _switch_mode(parts[1])
    
    elif subcommand == "sim":
        if len(parts) < 2:
            return "Usage: :221b sim [start|stop|status]"
        return await _handle_sim_command(parts[1])
    
    elif subcommand == "env":
        if len(parts) < 2:
            return "Usage: :221b env [simulation|devnet|testnet|mainnet]"
        return await _switch_environment(parts[1])
    
    elif subcommand == "help":
        return _get_221b_help()
    
    return f"Unknown 221b command: {subcommand}. Try :221b help"


def _get_221b_help() -> str:
    """Get help text for 221b commands."""
    return """
╔══════════════════════════════════════════════════════════╗
║              🕵️  TERMINAL 221b - CONTROL CENTER           ║
╠══════════════════════════════════════════════════════════╣
║  :221b status              - Show detective status       ║
║  :221b mode <personality>  - Switch detective mode       ║
║  :221b sim [start|stop]    - Control simulation server   ║
║  :221b env <environment>   - Switch network environment  ║
║  :investigate <query>      - Start investigation         ║
║  :simulate <transaction>   - Simulate transaction        ║
╠══════════════════════════════════════════════════════════╣
║  Personalities: holmes | watson | mycroft | irene        ║
║  Environments: simulation | devnet | testnet | mainnet   ║
╚══════════════════════════════════════════════════════════╝
"""


async def handle_detective_command(args: str, tui_state: "HiveTUIState") -> str:
    """Handle :detective command to switch personalities."""
    mode = args.strip().lower() or "holmes"
    return await _switch_mode(mode)


async def handle_investigate_command(args: str, tui_state: "HiveTUIState") -> str:
    """Handle :investigate command."""
    if not args.strip():
        return "Usage: :investigate <Solana address or query>"
    
    # Ensure we have an active detective
    if not _detective_state["current_agent"]:
        await _initialize_detective()
    
    agent = _detective_state["current_agent"]
    
    # Check if it's an address
    query = args.strip()
    if len(query) == 44 and query[0].isalnum():  # Likely a Solana address
        investigation = await agent.analyze_address(query)
        return (
            f"🔍 Investigation opened: **{investigation.case_id}**\n"
            f"Target: `{query}`\n"
            f"Status: {investigation.status}\n"
            f"Confidence: {investigation.confidence_score:.0%}"
        )
    else:
        # General investigation
        response = await agent.investigate(query)
        return response


async def handle_simulate_command(args: str, tui_state: "HiveTUIState") -> str:
    """Handle :simulate command for transaction simulation."""
    if not args.strip():
        return "Usage: :simulate <transaction description>"
    
    # Ensure simulation server is running
    if not _detective_state["sim_server"]:
        await _start_simulation()
    
    # Parse and simulate
    # In production, this would construct and simulate the actual transaction
    return (
        f"🔬 Simulation initiated for: `{args.strip()}`\n"
        f"Status: ✅ Simulation server active\n"
        f"Result: [Would show detailed simulation results]\n"
        f"\n*No real funds were moved. This was a simulation.*"
    )


async def _initialize_detective():
    """Initialize the detective agent."""
    mode = _detective_state["mode"]
    
    # Use simulation config by default for safety
    deps = get_simulation_config()
    
    agent = await create_detective(
        deps=deps,
        personality=mode.value,
        enable_simulation=True,
    )
    
    _detective_state["current_agent"] = agent
    _detective_state["sim_server"] = agent.sim_server
    _detective_state["active"] = True


async def _switch_mode(mode: str) -> str:
    """Switch detective personality."""
    try:
        new_mode = DetectiveMode(mode.lower())
    except ValueError:
        return f"Unknown personality: {mode}. Choose from: holmes, watson, mycroft, irene"
    
    _detective_state["mode"] = new_mode
    
    # Reinitialize agent with new personality
    if _detective_state["current_agent"]:
        old_agent = _detective_state["current_agent"]
        if old_agent.sim_server:
            await old_agent.sim_server.stop()
    
    await _initialize_detective()
    
    personalities = {
        DetectiveMode.HOLMES: (
            "🔍 **Sherlock Holmes** now on the case.\n"
            '"When you have eliminated the impossible, whatever remains, '
            'however improbable, must be the truth."'
        ),
        DetectiveMode.WATSON: (
            "🩺 **Dr. Watson** at your service.\n"
            '"Let me explain this in terms we can both understand. '
            'The blockchain tells quite a story..."'
        ),
        DetectiveMode.MYCROFT: (
            "🌐 **Mycroft Holmes** observing from above.\n"
            '"The network effects here are... significant. '
            'Let me trace the connections."'
        ),
        DetectiveMode.IRENE: (
            "💋 **Irene Adler** - always one step ahead.\n"
            '"The obvious answer is rarely the complete one. '
            'Let me show you what others miss."'
        ),
    }
    
    return personalities[new_mode]


async def _handle_sim_command(action: str) -> str:
    """Handle simulation server commands."""
    if action == "start":
        if _detective_state["sim_server"]:
            return "Simulation server already running."
        await _start_simulation()
        return "🚀 Simulation server started on port 8899"
    
    elif action == "stop":
        if not _detective_state["sim_server"]:
            return "No simulation server running."
        await _stop_simulation()
        return "🛑 Simulation server stopped"
    
    elif action == "status":
        if _detective_state["sim_server"]:
            return "✅ Simulation server: ACTIVE (port 8899)"
        return "⚪ Simulation server: INACTIVE"
    
    return f"Unknown sim command: {action}"


async def _switch_environment(env: str) -> str:
    """Switch network environment."""
    env_map = {
        "simulation": "simulation",
        "devnet": "devnet",
        "testnet": "testnet",
        "mainnet": "mainnet",
    }
    
    if env not in env_map:
        return f"Unknown environment: {env}"
    
    # Reinitialize with new environment
    from terminal_221b.agents.advisor_deps import (
        NetworkEnvironment,
        get_simulation_config,
        get_devnet_config,
    )
    
    # Stop current agent
    if _detective_state["current_agent"]:
        old_agent = _detective_state["current_agent"]
        if old_agent.sim_server:
            await old_agent.sim_server.stop()
    
    # Create new config
    if env == "simulation":
        deps = get_simulation_config()
    elif env == "devnet":
        deps = get_devnet_config()
    else:
        # Would need proper config for testnet/mainnet
        deps = AdvisorDeps(environment=NetworkEnvironment(env))
    
    _detective_state["current_agent"] = await create_detective(
        deps=deps,
        personality=_detective_state["mode"].value,
    )
    
    warnings = {
        "simulation": "🔬 Simulation mode - no real transactions",
        "devnet": "🧪 Devnet mode - test SOL only",
        "testnet": "🧪 Testnet mode - for validator testing",
        "mainnet": "⚠️  MAINNET MODE - Real funds at stake!",
    }
    
    return f"Environment switched to: **{env}**\n{warnings[env]}"


async def _start_simulation():
    """Start the simulation server."""
    sim = SimServer(port=8899)
    await sim.start()
    _detective_state["sim_server"] = sim


async def _stop_simulation():
    """Stop the simulation server."""
    if _detective_state["sim_server"]:
        await _detective_state["sim_server"].stop()
        _detective_state["sim_server"] = None


async def _get_status() -> str:
    """Get current 221b status."""
    agent = _detective_state.get("current_agent")
    sim = _detective_state.get("sim_server")
    mode = _detective_state.get("mode", DetectiveMode.HOLMES)
    
    lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║              🕵️  TERMINAL 221b STATUS                    ║",
        "╠══════════════════════════════════════════════════════════╣",
        f"║  Detective: {mode.value.upper():<15} {'🟢 ACTIVE' if agent else '⚪ INACTIVE':<20} ║",
        f"║  Simulation: {'🟢 RUNNING' if sim else '⚪ STOPPED':<33} ║",
    ]
    
    if agent:
        stats = agent.get_stats()
        lines.extend([
            "╠══════════════════════════════════════════════════════════╣",
            f"║  Transactions Simulated: {stats['transactions_simulated']:<26} ║",
            f"║  Transactions Executed: {stats['transactions_executed']:<27} ║",
            f"║  Active Cases: {stats['active_cases']:<36} ║",
            f"║  Conversation Turns: {stats['conversation_turns']:<30} ║",
        ])
    
    lines.extend([
        "╚══════════════════════════════════════════════════════════╝",
    ])
    
    return "\n".join(lines)


# Keybinding handlers
def on_alt_d(tui_state: "HiveTUIState"):
    """Handle Alt+D - activate detective mode."""
    asyncio.create_task(_activate_detective_mode(tui_state))


def on_alt_shift_d(tui_state: "HiveTUIState"):
    """Handle Alt+Shift+D - cycle detective personalities."""
    modes = list(DetectiveMode)
    current_idx = modes.index(_detective_state.get("mode", DetectiveMode.HOLMES))
    next_mode = modes[(current_idx + 1) % len(modes)]
    asyncio.create_task(_switch_mode(next_mode.value))


async def _activate_detective_mode(tui_state: "HiveTUIState"):
    """Activate detective mode in the TUI."""
    if not _detective_state["active"]:
        await _initialize_detective()
    
    # Update TUI state
    tui_state.current_agent_name = f"Detective {_detective_state['mode'].value.title()}"
    tui_state.current_model = "Terminal 221b"
    tui_state.mode = "detective"
    
    # Update art panel
    tui_state.art_content = _get_detective_art(_detective_state["mode"])


def _get_detective_art(mode: DetectiveMode) -> str:
    """Get ASCII art for detective mode."""
    arts = {
        DetectiveMode.HOLMES: """
╔══════════════════════════════════════════╗
║         🕵️  SHERLOCK HOLMES              ║
║                                          ║
║         "The game is afoot!"             ║
║                                          ║
║         Consulting Detective             ║
║         221B Baker Street                ║
╚══════════════════════════════════════════╝
""",
        DetectiveMode.WATSON: """
╔══════════════════════════════════════════╗
║         🩺  DR. JOHN WATSON              ║
║                                          ║
║      "Steady on, old friend."            ║
║                                          ║
║         Chronicler & Companion           ║
║         Queen's Army Medical             ║
╚══════════════════════════════════════════╝
""",
        DetectiveMode.MYCROFT: """
╔══════════════════════════════════════════╗
║         🌐  MYCROFT HOLMES               ║
║                                          ║
║   "I am the British Government."         ║
║                                          ║
║         The Diogenes Club                ║
║         Strategic Oversight              ║
╚══════════════════════════════════════════╝
""",
        DetectiveMode.IRENE: """
╔══════════════════════════════════════════╗
║         💋  IRENE ADLER                  ║
║                                          ║
║      "I am the woman."                   ║
║                                          ║
║         The Woman                        ║
║         Always Three Moves Ahead         ║
╚══════════════════════════════════════════╝
""",
    }
    return arts.get(mode, arts[DetectiveMode.HOLMES])
