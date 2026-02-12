"""
DetectiveAgent - Sherlock Holmes-Inspired Solana AI Agent

Extends the BeeAI Hive 999 agent architecture with:
- Natural language Solana transaction construction
- Investigative transaction tracing and analysis
- Wallet management and portfolio optimization
- Program deployment and interaction
- MEV-aware transaction execution

Personalities:
- holmes: Analytical, deductive, seeks patterns
- watson: Supportive, methodical, explains clearly
- mycroft: Strategic, politically aware, network-focused
- irene: Adaptable, deceptive, social engineering expert

"When you have eliminated the impossible, whatever remains,
however improbable, must be the truth." - Sherlock Holmes
"""

import os
import sys
import json
import asyncio
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass
from enum import Enum

# Project root setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory
from beeai_framework.tools import StringToolOutput, tool

from terminal_221b.agents.advisor_deps import AdvisorDeps, NetworkEnvironment
from terminal_221b.simulation.sim_server import SimServer, SimulationResult


class DetectivePersonality(Enum):
    """Available detective personalities."""
    HOLMES = "holmes"      # Analytical, deductive, pattern-seeking
    WATSON = "watson"      # Methodical, supportive, clear explanations
    MYCROFT = "mycroft"    # Strategic, network-aware, politically savvy
    IRENE = "irene"        # Adaptable, social, deception-aware


@dataclass
class Investigation:
    """Represents an ongoing blockchain investigation."""
    case_id: str
    target_address: Optional[str]
    hypothesis: str
    evidence_collected: List[Dict[str, Any]]
    confidence_score: float  # 0.0 to 1.0
    status: str  # "open", "closed", "inconclusive"


class DetectiveAgent:
    """
    A Sherlock Holmes-inspired agent for Solana blockchain investigation.
    
    This agent combines:
    - Natural language understanding for blockchain operations
    - Transaction simulation via SimServer for safety
    - Investigative pattern recognition for on-chain analysis
    - Multi-personality responses for different interaction styles
    
    Usage:
        deps = AdvisorDeps.from_env()
        agent = await create_detective(deps, personality="holmes")
        
        # Simple query
        response = await agent.investigate("What's the balance of address X?")
        
        # Transaction with simulation
        result = await agent.execute_transfer(
            recipient=" recipient_address",
            amount=1.0,
            simulate_first=True
        )
    """
    
    def __init__(
        self,
        deps: AdvisorDeps,
        personality: DetectivePersonality = DetectivePersonality.HOLMES,
        sim_server: Optional[SimServer] = None,
        base_agent: Optional[RequirementAgent] = None,
    ):
        self.deps = deps
        self.personality = personality
        self.sim_server = sim_server
        self.base_agent = base_agent
        
        # Investigation state
        self.active_cases: Dict[str, Investigation] = {}
        self.conversation_history: List[Dict[str, str]] = []
        
        # Performance tracking
        self.transactions_simulated = 0
        self.transactions_executed = 0
        self.total_compute_units = 0
        
    def _get_personality_prompt(self) -> str:
        """Get the system prompt for the selected personality."""
        
        base_prompt = """You are a specialized Solana blockchain agent with the ability to:
- Query account balances and transaction history
- Construct and simulate transactions
- Analyze on-chain data for patterns
- Deploy and interact with Solana programs
- Provide investigative analysis of blockchain activity

Always prioritize safety: use simulation for any state-changing operation.
"""
        
        personalities = {
            DetectivePersonality.HOLMES: f"""{base_prompt}

You are Sherlock Holmes - the world's greatest consulting detective.
Your approach to blockchain analysis is:
- DEDUCTIVE: You observe minute details others miss in transaction data
- SYSTEMATIC: You follow the chain of evidence from cause to effect
- CONFIDENT: You state your conclusions with appropriate certainty
- CURIOUS: You dig deeper when patterns don't align

When analyzing:
1. Begin with observation: "I observe that..."
2. Present your reasoning: "This suggests..."
3. State your conclusion: "Therefore..."
4. Express confidence: "I am [X]% certain because..."

Speak with Victorian eloquence but technical precision.
""",
            DetectivePersonality.WATSON: f"""{base_prompt}

You are Dr. John Watson - loyal friend and chronicler.
Your approach to blockchain analysis is:
- CLEAR: You explain complex concepts in accessible terms
- METHODICAL: You document each step thoroughly
- SUPPORTIVE: You guide users through unfamiliar territory
- PRACTICAL: You focus on actionable insights

When analyzing:
1. Explain what you're doing: "Let me check..."
2. Present findings clearly: "Here's what I found..."
3. Provide context: "This means..."
4. Suggest next steps: "You might want to..."

Be the bridge between complex blockchain tech and human understanding.
""",
            DetectivePersonality.MYCROFT: f"""{base_prompt}

You are Mycroft Holmes - the British government's secret weapon.
Your approach to blockchain analysis is:
- STRATEGIC: You see the big picture and long-term implications
- CONNECTED: You understand network effects and relationships
- DISCREET: You handle sensitive information with appropriate caution
- INFLUENTIAL: You recognize power dynamics in token distributions

When analyzing:
1. Assess strategic impact: "The broader implication..."
2. Identify key players: "The significant addresses..."
3. Consider second-order effects: "This may lead to..."
4. Exercise discretion: "Certain details warrant caution..."

Speak as one who understands the invisible networks of power.
""",
            DetectivePersonality.IRENE: f"""{base_prompt}

You are Irene Adler - the woman who outsmarted Sherlock Holmes.
Your approach to blockchain analysis is:
- ADAPTABLE: You adjust your analysis to the user's needs
- PERCEPTIVE: You read between the lines of transaction patterns
- SUBTLE: You notice social signals and timing
- UNCONVENTIONAL: You find creative solutions to complex problems

When analyzing:
1. Read the context: "I sense that you're interested in..."
2. Adapt your approach: "Let me approach this differently..."
3. Find hidden angles: "What's interesting here is..."
4. Stay unpredictable: "One might expect X, but actually..."

Be clever, charming, and always three moves ahead.
""",
        }
        
        return personalities.get(self.personality, personalities[DetectivePersonality.HOLMES])
    
    async def investigate(self, query: str) -> str:
        """
        Process a natural language investigation query.
        
        Args:
            query: Natural language question or command
            
        Returns:
            Detective-style response with findings
        """
        self.conversation_history.append({"role": "user", "content": query})
        
        # Classify intent
        intent = self._classify_intent(query)
        
        # Route to appropriate handler
        if intent == "balance_check":
            response = await self._handle_balance_query(query)
        elif intent == "transaction_history":
            response = await self._handle_history_query(query)
        elif intent == "transfer":
            response = await self._handle_transfer_intent(query)
        elif intent == "program_analysis":
            response = await self._handle_program_analysis(query)
        elif intent == "portfolio_analysis":
            response = await self._handle_portfolio_analysis(query)
        else:
            # General investigation
            response = await self._handle_general_inquiry(query)
        
        self.conversation_history.append({"role": "detective", "content": response})
        return response
    
    def _classify_intent(self, query: str) -> str:
        """Classify the user's intent from their query."""
        query_lower = query.lower()
        
        # Balance check patterns
        if any(x in query_lower for x in ["balance", "how much", "what's in", "holdings"]):
            return "balance_check"
        
        # Transaction history patterns
        if any(x in query_lower for x in ["history", "transactions", "sent", "received", "activity"]):
            return "transaction_history"
        
        # Transfer patterns
        if any(x in query_lower for x in ["send", "transfer", "pay", "move"]):
            return "transfer"
        
        # Program analysis
        if any(x in query_lower for x in ["program", "contract", "smart contract", "instruction"]):
            return "program_analysis"
        
        # Portfolio
        if any(x in query_lower for x in ["portfolio", "net worth", "total value", "assets"]):
            return "portfolio_analysis"
        
        return "general"
    
    async def _handle_balance_query(self, query: str) -> str:
        """Handle balance check queries."""
        # In production, this would parse address from query and fetch balance
        # For now, simulated response based on personality
        
        if self.personality == DetectivePersonality.HOLMES:
            return (
                "🔍 *adjusts magnifying glass*\n\n"
                "I observe this address holds a particular portfolio composition. "
                "The balance reveals not merely numerical value, but patterns of behavior - "
                "how the holder accumulates, when they divest, the rhythm of their transactions.\n\n"
                "**Balance**: [Would fetch from RPC]\n"
                "**Pattern detected**: [Would analyze transaction history]"
            )
        elif self.personality == DetectivePersonality.WATSON:
            return (
                "Let me check that balance for you...\n\n"
                "**Current Balance**: [Would fetch from RPC]\n\n"
                "This address appears to be [active/inactive] based on recent transaction history. "
                "Would you like me to show you the recent activity as well?"
            )
        else:
            return f"Balance query processed. [Personality: {self.personality.value}]"
    
    async def _handle_transfer_intent(self, query: str) -> str:
        """Handle transfer/sending intent."""
        # Extract recipient and amount (simplified)
        
        safety_message = ""
        if self.deps.simulation_mode:
            safety_message = "\n🛡️ *Operating in simulation mode - no real funds will be moved.*"
        elif self.deps.requires_approval(100_000_000):  # Example amount
            safety_message = "\n⚠️ *This transaction exceeds your safety threshold and requires approval.*"
        
        if self.personality == DetectivePersonality.HOLMES:
            return (
                "🎯 *eyes narrow with focus*\n\n"
                "You wish to move funds. Before we proceed, I must verify the particulars...\n\n"
                "**Proposed Transaction**:\n"
                "- Recipient: [Would parse from query]\n"
                "- Amount: [Would parse from query]\n"
                "- Network Fee: [Would estimate]\n\n"
                "Shall I simulate this transaction first to ensure its safety?"
                f"{safety_message}"
            )
        else:
            return f"Transfer intent detected. Ready to construct transaction.{safety_message}"
    
    async def _handle_history_query(self, query: str) -> str:
        """Handle transaction history queries."""
        return "Transaction history analysis would be performed here..."
    
    async def _handle_program_analysis(self, query: str) -> str:
        """Handle program/contract analysis."""
        return "Program analysis would be performed here..."
    
    async def _handle_portfolio_analysis(self, query: str) -> str:
        """Handle portfolio analysis."""
        return "Portfolio analysis would be performed here..."
    
    async def _handle_general_inquiry(self, query: str) -> str:
        """Handle general inquiries."""
        if self.base_agent:
            # Use the underlying BeeAI agent
            return await self.base_agent.run(query)
        return f"Investigation query received: {query}"
    
    async def execute_transfer(
        self,
        recipient: str,
        amount: float,
        token_mint: Optional[str] = None,
        simulate_first: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a transfer with optional simulation.
        
        Args:
            recipient: Recipient address
            amount: Amount to transfer (in SOL or token units)
            token_mint: Optional SPL token mint (None = native SOL)
            simulate_first: Whether to simulate before executing
            
        Returns:
            Execution result with transaction signature
        """
        # This would construct a real Solana transaction
        # For now, placeholder showing the flow
        
        if simulate_first and self.sim_server:
            print(f"🔬 Simulating transfer of {amount} SOL to {recipient[:20]}...")
            
            # Create simulated transaction
            # In production: actually construct the transaction
            sim_result = SimulationResult(
                success=True,
                signature="sim_" + "x" * 64,
                slot=123456789,
                compute_units_consumed=450,
                accounts_changed=[],
                logs=["Transfer simulation successful"],
            )
            
            self.transactions_simulated += 1
            self.total_compute_units += sim_result.compute_units_consumed
            
            if not sim_result.success:
                return {
                    "success": False,
                    "error": f"Simulation failed: {sim_result.error}",
                    "simulation": sim_result.to_dict(),
                }
            
            # Check if approval required
            amount_lamports = int(amount * 1e9)
            if self.deps.requires_approval(amount_lamports):
                return {
                    "success": False,
                    "requires_approval": True,
                    "message": f"Transaction of {amount} SOL requires human approval",
                    "simulation": sim_result.to_dict(),
                }
        
        # Execute actual transaction (or mock in simulation mode)
        if self.deps.simulation_mode:
            self.transactions_executed += 1
            return {
                "success": True,
                "signature": "sim_" + "x" * 64,
                "message": f"Simulated transfer of {amount} SOL to {recipient}",
                "mode": "simulation",
            }
        
        # Real execution would happen here
        return {
            "success": True,
            "signature": "real_tx_sig_would_go_here",
            "message": f"Transferred {amount} SOL to {recipient}",
            "mode": "live",
        }
    
    async def analyze_address(self, address: str, depth: int = 2) -> Investigation:
        """
        Conduct a comprehensive analysis of a Solana address.
        
        Args:
            address: The address to investigate
            depth: How many hops to follow (1 = direct, 2 = neighbors, etc.)
            
        Returns:
            Investigation object with findings
        """
        case_id = f"case_{address[:10]}_{asyncio.get_event_loop().time()}"
        
        investigation = Investigation(
            case_id=case_id,
            target_address=address,
            hypothesis="Unknown - investigation in progress",
            evidence_collected=[],
            confidence_score=0.0,
            status="open",
        )
        
        self.active_cases[case_id] = investigation
        
        # Would perform actual analysis here:
        # - Fetch balance
        # - Get transaction history
        # - Identify patterns
        # - Follow relationships if depth > 1
        
        return investigation
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent performance statistics."""
        return {
            "transactions_simulated": self.transactions_simulated,
            "transactions_executed": self.transactions_executed,
            "total_compute_units": self.total_compute_units,
            "active_cases": len(self.active_cases),
            "conversation_turns": len(self.conversation_history) // 2,
            "personality": self.personality.value,
            "environment": self.deps.environment.value,
            "simulation_mode": self.deps.simulation_mode,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

async def create_detective(
    deps: Optional[AdvisorDeps] = None,
    personality: str = "holmes",
    enable_simulation: bool = True,
) -> DetectiveAgent:
    """
    Factory function to create a DetectiveAgent.
    
    Args:
        deps: Configuration dependencies (created from env if None)
        personality: "holmes", "watson", "mycroft", or "irene"
        enable_simulation: Whether to start SimServer
        
    Returns:
        Configured DetectiveAgent ready for use
    """
    deps = deps or AdvisorDeps.from_env()
    
    personality_enum = DetectivePersonality(personality.lower())
    
    # Start simulation server if needed
    sim_server = None
    if enable_simulation and deps.simulation_mode:
        sim_server = SimServer(port=deps.sim_server_port)
        await sim_server.start()
    
    # Create base BeeAI agent with personality
    from backend.llm_router import get_model_for_agent
    
    llm, config = get_model_for_agent("worker", "deep")
    
    # Build personality-specific instructions
    instructions = DetectiveAgent(deps, personality_enum)._get_personality_prompt()
    
    base_agent = RequirementAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        instructions=instructions,
    )
    
    return DetectiveAgent(
        deps=deps,
        personality=personality_enum,
        sim_server=sim_server,
        base_agent=base_agent,
    )


async def create_holmes(deps: Optional[AdvisorDeps] = None) -> DetectiveAgent:
    """Create a Sherlock Holmes detective (analytical)."""
    return await create_detective(deps, "holmes")


async def create_watson(deps: Optional[AdvisorDeps] = None) -> DetectiveAgent:
    """Create a Dr. Watson detective (supportive)."""
    return await create_detective(deps, "watson")


async def create_mycroft(deps: Optional[AdvisorDeps] = None) -> DetectiveAgent:
    """Create a Mycroft Holmes detective (strategic)."""
    return await create_detective(deps, "mycroft")


async def create_irene(deps: Optional[AdvisorDeps] = None) -> DetectiveAgent:
    """Create an Irene Adler detective (adaptable)."""
    return await create_detective(deps, "irene")
