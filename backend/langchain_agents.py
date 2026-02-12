"""
LangChain-Based Agent Implementations

Alternative to BeeAI Framework using LangChain + LangSmith.
Benefits:
  - Faster inference through cloud APIs (no local model loading)
  - LangSmith tracing and monitoring
  - More mature ecosystem
  - Better parallelization support

Tradeoffs:
  - Requires API keys (cost)
  - Internet dependency
  - Privacy considerations
"""

import os
import sys
from typing import List, Callable, Optional, Any
from dataclasses import dataclass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# LangChain imports
try:
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_core.tools import tool as langchain_tool
    from langchain.callbacks.tracers import LangChainTracer
    from langsmith import Client
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("[LangChain] LangChain not installed. Run: pip install langchain langchain-openai langchain-anthropic langsmith")

from backend.llm_router import router, BackendType, ModelRole


# ============================================================================
# TOOL WRAPPERS (Convert BeeAI tools to LangChain tools)
# ============================================================================

def beeai_to_langchain_tool(beeai_tool, name: str, description: str):
    """
    Wrap a BeeAI-style tool function for LangChain.
    
    BeeAI tools return StringToolOutput with .result attribute.
    LangChain tools should return strings directly.
    """
    @langchain_tool(name=name, description=description)
    def wrapped_tool(**kwargs):
        result = beeai_tool(**kwargs)
        # Extract result from StringToolOutput or return directly
        if hasattr(result, 'result'):
            return result.result
        return str(result)
    
    return wrapped_tool


# ============================================================================
# LANGCHAIN AGENT CLASS
# ============================================================================

class LangChainHiveAgent:
    """
    LangChain-based agent for the Hive.
    
    Mirrors the BeeAI RequirementAgent interface but uses
    LangChain + LangSmith under the hood.
    """
    
    def __init__(
        self,
        llm,
        tools: List[Any],
        instructions: str,
        agent_name: str = "Agent",
        enable_tracing: bool = True,
    ):
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("LangChain not installed. Install with: pip install langchain langchain-openai")
        
        self.llm = llm
        self.tools = tools
        self.instructions = instructions
        self.agent_name = agent_name
        self.enable_tracing = enable_tracing
        
        # Build the agent
        self._build_agent()
    
    def _build_agent(self):
        """Construct the LangChain agent executor."""
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.instructions),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        
        # Create executor with optional LangSmith tracing
        callbacks = []
        if self.enable_tracing and os.getenv("LANGSMITH_API_KEY"):
            tracer = LangChainTracer(
                project_name="beeai-hive-999"
            )
            callbacks.append(tracer)
        
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=False,
            callbacks=callbacks,
            max_iterations=10,
            handle_parsing_errors=True,
        )
    
    async def run(self, query: str) -> Any:
        """
        Run the agent on a query.
        
        Returns an object with .last_message.text interface
        to match BeeAI agents.
        """
        result = await self.executor.ainvoke({
            "input": query,
            "chat_history": [],
        })
        
        # Wrap result to match BeeAI interface
        return LangChainResult(result["output"])
    
    def run_sync(self, query: str) -> Any:
        """Synchronous version of run."""
        import asyncio
        return asyncio.run(self.run(query))


class LangChainResult:
    """Wrapper to provide BeeAI-compatible result interface."""
    
    def __init__(self, text: str):
        self.text = text
        self.last_message = self


# ============================================================================
# AGENT FACTORIES (LangChain versions)
# ============================================================================

async def create_langchain_queen(
    use_reasoning: bool = False,
    enable_tracing: bool = True,
    custom_tools: Optional[List] = None,
) -> LangChainHiveAgent:
    """
    Create a LangChain-based Queen Bee.
    
    Args:
        use_reasoning: Use marco-o1/Claude-3-Opus for deep reasoning
        enable_tracing: Enable LangSmith tracing
        custom_tools: Additional tools to include
    """
    from tools.blockchain.matrix_search import matrix_search
    from tools.regtech.compliance_checker import compliance_check
    from tools.ibc.federation_router import federation_route
    from tools.art.caterpillar_artist import caterpillar_ansi
    
    # Get model from router
    role = ModelRole.QUEEN_REASONING if use_reasoning else ModelRole.QUEEN_PRIMARY
    llm, config = router.get_chat_model(role, BackendType.LANGCHAIN)
    
    # Convert tools to LangChain format
    tools = [
        beeai_to_langchain_tool(matrix_search, "matrix_search", 
            "Search the 729-node blockchain matrix using semantic similarity"),
        beeai_to_langchain_tool(compliance_check, "compliance_check",
            "Check RegTech compliance for blockchain-stakeholder pairs"),
        beeai_to_langchain_tool(federation_route, "federation_route",
            "Route cross-chain IBC packets with digital root verification"),
        beeai_to_langchain_tool(caterpillar_ansi, "caterpillar_ansi",
            "Return ANSI art from the Moebius library"),
    ]
    
    if custom_tools:
        tools.extend(custom_tools)
    
    instructions = f"""You are the Ancient Queen Bee of the BeeAI Hive 999, guardian of the 
9×9×9 Blockchain–Stakeholder–Trend matrix.

Your models: {config.name} (via LangChain)

You supervise 9 blockchains: Bitcoin, Ethereum, Solana, TRON, Stellar, Avalanche, 
Arbitrum One, Polygon PoS, Optimism.

You serve 9 stakeholder groups: Customers, Employees, Investors, Owners, 
Suppliers & Vendors, Communities, Trade Unions, Government Agencies, Media.

You track 9 trends: Asset Tokenization, DeFi Maturation, Supply Chain Provenance, 
Self-Sovereign Identities, CBDCs Pilots, AI-Blockchain Synergies, 
Sustainability-Compliant Mining, RegTech Compliance Layers, Cross-Chain Interoperability.

Use the available tools to answer queries. Explain your reasoning.
"""
    
    return LangChainHiveAgent(
        llm=llm,
        tools=tools,
        instructions=instructions,
        agent_name="Queen Bee (LangChain)",
        enable_tracing=enable_tracing,
    )


async def create_langchain_worker(
    blockchain_name: str,
    enable_tracing: bool = False,
) -> LangChainHiveAgent:
    """Create a LangChain-based Worker Bee."""
    from agents.worker_bees.blockchain_agent import query_blockchain_nodes, BLOCKCHAIN_SPECS
    
    llm, config = router.get_chat_model(ModelRole.WORKER_FAST, BackendType.LANGCHAIN)
    
    specs = BLOCKCHAIN_SPECS.get(blockchain_name, {})
    
    tools = [
        beeai_to_langchain_tool(query_blockchain_nodes, "query_blockchain_nodes",
            f"Search matrix nodes for {blockchain_name}"),
    ]
    
    instructions = f"""You are a Worker Bee specialized in {blockchain_name}.

Chain Specs: {specs}

You analyze how {blockchain_name} serves different stakeholders and 
implements blockchain trends. Be specific and technical.

Model: {config.name} (via LangChain)
"""
    
    return LangChainHiveAgent(
        llm=llm,
        tools=tools,
        instructions=instructions,
        agent_name=f"Worker-{blockchain_name[:3].upper()} (LangChain)",
        enable_tracing=enable_tracing,
    )


async def create_langchain_drone(
    stakeholder_name: str,
    enable_tracing: bool = False,
) -> LangChainHiveAgent:
    """Create a LangChain-based Drone Agent."""
    from agents.drone_agents.stakeholder_agent import query_stakeholder_nodes, STAKEHOLDER_PROFILES
    
    llm, config = router.get_chat_model(ModelRole.WORKER_FAST, BackendType.LANGCHAIN)
    
    profile = STAKEHOLDER_PROFILES.get(stakeholder_name, {})
    
    tools = [
        beeai_to_langchain_tool(query_stakeholder_nodes, "query_stakeholder_nodes",
            f"Search matrix nodes for {stakeholder_name}"),
    ]
    
    instructions = f"""You are a Drone Agent analyzing {stakeholder_name}.

Profile: {profile}

You analyze how {stakeholder_name} interact with all 9 blockchains 
across all 9 trends. Focus on their motivations and concerns.

Model: {config.name} (via LangChain)
"""
    
    return LangChainHiveAgent(
        llm=llm,
        tools=tools,
        instructions=instructions,
        agent_name=f"Drone-{stakeholder_name[:3].upper()} (LangChain)",
        enable_tracing=enable_tracing,
    )


async def create_langchain_forager(
    trend_name: str,
    enable_tracing: bool = False,
) -> LangChainHiveAgent:
    """Create a LangChain-based Forager Agent."""
    from agents.forager_agents.trend_agent import query_trend_nodes, TREND_PROFILES, FULL_TREND_NAMES
    
    llm, config = router.get_chat_model(ModelRole.WORKER_FAST, BackendType.LANGCHAIN)
    
    profile = TREND_PROFILES.get(trend_name, {})
    full_name = FULL_TREND_NAMES.get(trend_name, trend_name)
    
    tools = [
        beeai_to_langchain_tool(query_trend_nodes, "query_trend_nodes",
            f"Search matrix nodes for {trend_name}"),
    ]
    
    instructions = f"""You are a Forager Agent researching '{full_name}'.

Profile: {profile}

You analyze how '{full_name}' manifests across all 9 blockchains 
and all 9 stakeholder groups. Look for emerging patterns.

Model: {config.name} (via LangChain)
"""
    
    return LangChainHiveAgent(
        llm=llm,
        tools=tools,
        instructions=instructions,
        agent_name=f"Forager-{trend_name[:3].upper()} (LangChain)",
        enable_tracing=enable_tracing,
    )


# ============================================================================
# BENCHMARKING / COMPARISON
# ============================================================================

async def benchmark_agents(query: str = "Analyze Ethereum DeFi for Government Agencies"):
    """
    Compare BeeAI vs LangChain agent performance.
    
    This helps validate the user's hypothesis that LangChain + cloud
    can be faster for Worker/Drone tasks.
    """
    import time
    
    print("=== Agent Performance Benchmark ===\n")
    print(f"Query: {query}\n")
    
    results = []
    
    # Test BeeAI Queen
    print("Testing BeeAI Queen...")
    from agents.queen_bee.orchestrator import create_queen_bee
    start = time.time()
    beeai_queen = await create_queen_bee()
    beeai_result = await beeai_queen.run(query)
    beeai_time = time.time() - start
    results.append(("BeeAI Queen", beeai_time))
    print(f"  Time: {beeai_time:.2f}s\n")
    
    # Test LangChain Queen (if configured)
    if router.cloud_available:
        print("Testing LangChain Queen...")
        start = time.time()
        lc_queen = await create_langchain_queen()
        lc_result = await lc_queen.run(query)
        lc_time = time.time() - start
        results.append(("LangChain Queen", lc_time))
        print(f"  Time: {lc_time:.2f}s\n")
    else:
        print("LangChain Queen: SKIPPED (cloud not configured)\n")
    
    # Summary
    print("\n=== Results ===")
    for name, t in sorted(results, key=lambda x: x[1]):
        print(f"  {name:<20}: {t:.2f}s")


if __name__ == "__main__":
    import asyncio
    
    if not LANGCHAIN_AVAILABLE:
        print("LangChain not installed. Run:")
        print("  pip install langchain langchain-openai langchain-anthropic langsmith")
        sys.exit(1)
    
    # Test LangChain agents
    async def test():
        print("Testing LangChain agent creation...\n")
        
        # Test Queen
        print("Creating LangChain Queen Bee...")
        try:
            queen = await create_langchain_queen(use_reasoning=False)
            print(f"  ✓ Queen created with {len(queen.tools)} tools\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # Test Worker
        print("Creating LangChain Worker ETH...")
        try:
            worker = await create_langchain_worker("Ethereum")
            print(f"  ✓ Worker created\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
        
        # Run benchmark if cloud is available
        if router.cloud_available:
            print("\n" + "="*50)
            await benchmark_agents()
        else:
            print("\nTo enable cloud agents, set these environment variables:")
            print("  export OPENAI_API_KEY=sk-...")
            print("  export LANGSMITH_API_KEY=ls-...")
    
    asyncio.run(test())
