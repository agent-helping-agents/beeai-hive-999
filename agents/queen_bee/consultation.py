"""
Queen Bee Consultation System

Provides architectural guidance and wisdom from the Queen Bee.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ArchitectureDomain(Enum):
    """Domains for architectural consultation."""

    AGENTS = "agents"
    BACKEND = "backend"
    TUI = "tui"
    TOOLS = "tools"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class Consultation:
    """A consultation response from the Queen Bee."""

    question: str
    domain: ArchitectureDomain
    answer: str
    recommendations: List[str]
    warnings: List[str]
    timestamp: datetime


AGENTS_ANSWER = """The BeeAI architecture follows a hierarchical multi-agent system:

1. Queen Bee - Central orchestrator
   - Routes queries to appropriate agents
   - Synthesizes responses from Workers, Drones, Foragers
   - Uses ThinkTool for complex reasoning
   - Delegates to specialized agents based on query type

2. Worker Bees (9) - Blockchain specialists
   - One per blockchain: BTC, ETH, SOL, TRX, XLM, AVAX, ARB, MATIC, OP
   - Deep technical knowledge of each chain
   - Fast response model (llama3.1:8b)

3. Drone Agents (9) - Stakeholder analysts
   - Analyze from stakeholder perspective
   - Use llama3.1:8b for fast analysis

4. Forager Agents (9) - Trend researchers
   - Research emerging trends
   - Use llama3.1:8b

5. Mantis Mail - Email communication
   - Zoho Mail integration

6. Terminal 221b (4) - Detective specialists
   - Sherlock Holmes-inspired investigation
   - Safe transaction simulation"""


BACKEND_ANSWER = """The Hive supports DUAL backend architecture:

LOCAL (Ollama) - Privacy-first, no API costs, works offline:
- granite3.3:8b - Queen Bee primary
- marco-o1:latest - Reasoning tasks
- deepseek-r1:8b - Deep reasoning
- llama3.1:8b - Fast Workers/Drones/Foragers
- qwen2.5-coder:32b - Code generation
- nomic-embed-text - Embeddings

CLOUD (LangChain/LangSmith) - Speed, scale, monitoring:
- GPT-4 - Queen primary
- Claude-3-Opus - Reasoning
- GPT-3.5-turbo - Fast workers

ROUTING DECISIONS:
- Privacy required -> LOCAL
- Latency critical -> CLOUD
- Cost sensitive -> LOCAL for simple, CLOUD for complex"""


TUI_ANSWER = """For a production TUI, follow these patterns (inspired by Ratatui):

LAYOUT STRUCTURE:
+------------------------------------------+
|  BEEAI HIVE 999                         |
+--------+---------+----------+------------+
| Agents |  Chat   | Context  | Scroll    |
| Sidebar| Bubbles | Panel    | Bar       |
+--------+---------+----------+------------+
|  [Input]                             |
+------------------------------------------+
|  Status Bar                          |
+------------------------------------------+

CORE COMPONENTS:
1. ScrollableChat - Message history with offset tracking
2. VisualScrollbar - Position indicator with thumb
3. MessageBubbles - Color-coded by agent type
4. TypingIndicator - Animated feedback during processing
5. ContextPanel - Show matrix position

KEY FEATURES:
- Arrow keys for scroll
- Tab to toggle panels
- Ctrl+L to clear
- Color scheme: Honey/Dark with Digital Root 9 palette"""


TOOLS_ANSWER = """Tools extend the Queen Bee's capabilities:

REQUIRED TOOLS:
1. ThinkTool - Always use first for complex queries
2. matrix_search - RAG semantic search across 729 nodes
3. compliance_check - RegTech/KYC/AML/ESG evaluation
4. federation_route - Cross-chain IBC-style routing
5. caterpillar_ansi - ANSI art rendering

TOOL PATTERN:
from beeai_framework.tools import StringToolOutput, tool

@tool
def my_tool(param: str) -> StringToolOutput:
    '''Description.
    
    Args:
        param: Description
        
    Returns:
        StringToolOutput with result
    '''
    return StringToolOutput(result="...")

TOOL BEST PRACTICES:
- Use @tool decorator
- Document all parameters
- Return StringToolOutput
- Handle errors gracefully
- Implement rate limiting for API tools"""


TESTING_ANSWER = """Comprehensive testing ensures reliability:

TEST PYRAMID:

1. Unit Tests (70%) - Test individual components
   - Configuration loading
   - Model routing logic
   - Agent creation
   - Tool functions
   - Matrix operations

2. Integration Tests (20%) - Test component interaction
   - Agent + LLM flow
   - Tool chains
   - Backend switching
   - TUI rendering

3. E2E Tests (10%) - Test complete workflows
   - Full query flow
   - Agent switching
   - Configuration changes

TESTING TOOLS:
- pytest - Test runner
- pytest-asyncio - Async tests
- pytest-cov - Coverage reporting
- unittest.mock - Mocking

COVERAGE TARGETS:
- Unit: 90%+
- Integration: 80%+
- Overall: 80%+"""


SECURITY_ANSWER = """Security is paramount for production:

KEY SECURITY PRACTICES:

1. Secrets Management
   - Load API keys from environment only
   - Never commit .env files
   - Mask secrets in logs/displays
   - Use HashiCorp Vault for production

2. Input Validation
   - Validate all user inputs
   - Sanitize file paths
   - Handle special characters
   - Implement rate limiting

3. Network Security
   - Use HTTPS for all API calls
   - Validate SSL certificates
   - Implement timeouts
   - Handle connection errors

4. Agent Safety
   - Sandbox agent tool execution
   - Limit resource consumption
   - Implement timeouts per agent
   - Monitor for prompt injection

5. Data Protection
   - Encrypt sensitive data
   - Implement data retention policies
   - Secure vector store access
   - Backup strategies

COMPLIANCE:
- MiCA for EU crypto regulations
- KYC/AML for financial operations
- GDPR for EU user data"""


PERFORMANCE_ANSWER = """Optimize for speed and resource efficiency:

MODEL SELECTION:
- Simple queries -> llama3.1:8b (fast)
- Complex analysis -> deepseek-r1:8b (reasoning)
- Code generation -> qwen2.5-coder:32b (specialized)
- Queen -> granite3.3:8b (orchestration)

CACHING STRATEGIES:
1. Response Caching
   - Cache RAG query results
   - Implement TTL for freshness
   - Use LRU eviction

2. Embedding Caching
   - Cache computed embeddings
   - Use ChromaDB for persistence
   - Batch embedding requests

3. Model Warm-up
   - Pre-load frequently used models
   - Keep models in memory during session
   - Use model pooling

PARALLELIZATION:
- Process independent queries concurrently
- Use asyncio for I/O bound tasks
- Implement worker pools for parallel agents

MEMORY MANAGEMENT:
- Limit chat history (default: 1000 messages)
- Use streaming for long responses
- Implement cleanup routines"""


class QueenBeeConsultant:
    """
    The Queen Bee provides architectural wisdom and guidance.
    """

    def __init__(self):
        self._wisdom_db = self._build_wisdom_database()

    def _build_wisdom_database(
        self,
    ) -> Dict[ArchitectureDomain, Dict[str, Consultation]]:
        """Build the wisdom database."""
        return {
            ArchitectureDomain.AGENTS: {
                "agent_design": Consultation(
                    question="How should agents be designed?",
                    domain=ArchitectureDomain.AGENTS,
                    answer=AGENTS_ANSWER,
                    recommendations=[
                        "Keep agents focused on single responsibility",
                        "Use ThinkTool for complex reasoning tasks",
                        "Implement proper memory management with UnconstrainedMemory",
                        "Consider agent timeout limits for production",
                    ],
                    warnings=[
                        "Don't create agents with overlapping responsibilities",
                        "Avoid blocking operations in agent loops",
                        "Monitor token usage for cost control",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.BACKEND: {
                "hybrid_backend": Consultation(
                    question="How does the hybrid backend work?",
                    domain=ArchitectureDomain.BACKEND,
                    answer=BACKEND_ANSWER,
                    recommendations=[
                        "Default to LOCAL for development",
                        "Use CLOUD for production with rate limits",
                        "Implement fallback: CLOUD -> LOCAL on failure",
                        "Monitor LangSmith traces for optimization",
                    ],
                    warnings=[
                        "Never hardcode API keys",
                        "Set timeout limits to prevent hangs",
                        "Handle cloud provider rate limits gracefully",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.TUI: {
                "tui_design": Consultation(
                    question="How should the TUI be designed?",
                    domain=ArchitectureDomain.TUI,
                    answer=TUI_ANSWER,
                    recommendations=[
                        "Use prompt_toolkit for Python TUI",
                        "Implement scroll offset tracking",
                        "Add visual scrollbar with proper thumb sizing",
                        "Use FormattedTextControl for rich content",
                    ],
                    warnings=[
                        "Don't block UI during agent operations",
                        "Limit chat history to prevent memory bloat",
                        "Handle terminal resize events",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.TOOLS: {
                "tool_design": Consultation(
                    question="How should tools be designed?",
                    domain=ArchitectureDomain.TOOLS,
                    answer=TOOLS_ANSWER,
                    recommendations=[
                        "Start with ThinkTool for reasoning",
                        "Use matrix_search for domain queries",
                        "Implement proper error handling",
                        "Add timeout to external API calls",
                    ],
                    warnings=[
                        "Don't make blocking calls in tools",
                        "Validate all inputs before processing",
                        "Never log secrets or API keys",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.TESTING: {
                "testing_strategy": Consultation(
                    question="What testing strategy should be used?",
                    domain=ArchitectureDomain.TESTING,
                    answer=TESTING_ANSWER,
                    recommendations=[
                        "Use pytest fixtures for setup/teardown",
                        "Mock external services (Ollama, LangChain)",
                        "Run tests in CI/CD pipeline",
                        "Maintain test documentation",
                    ],
                    warnings=[
                        "Don't skip tests for 'simple' code",
                        "Avoid tests that depend on timing",
                        "Never commit without running tests",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.SECURITY: {
                "security_practices": Consultation(
                    question="What security practices are essential?",
                    domain=ArchitectureDomain.SECURITY,
                    answer=SECURITY_ANSWER,
                    recommendations=[
                        "Use environment variables for all secrets",
                        "Implement request timeouts throughout",
                        "Add rate limiting for API endpoints",
                        "Log security events for audit",
                    ],
                    warnings=[
                        "Never log API keys or secrets",
                        "Don't execute arbitrary code from agents",
                        "Validate all external inputs",
                        "Keep dependencies updated",
                    ],
                    timestamp=datetime.now(),
                )
            },
            ArchitectureDomain.PERFORMANCE: {
                "performance_optimization": Consultation(
                    question="How to optimize performance?",
                    domain=ArchitectureDomain.PERFORMANCE,
                    answer=PERFORMANCE_ANSWER,
                    recommendations=[
                        "Profile before optimizing",
                        "Use async/await for I/O operations",
                        "Implement streaming for long responses",
                        "Monitor memory usage in production",
                    ],
                    warnings=[
                        "Don't cache without TTL",
                        "Avoid blocking operations in async code",
                        "Don't load all models simultaneously",
                    ],
                    timestamp=datetime.now(),
                )
            },
        }

    def consult(
        self, question: str, domain: Optional[ArchitectureDomain] = None
    ) -> Consultation:
        """
        Consult the Queen Bee about architecture.

        Args:
            question: Your question
            domain: Optional domain to filter

        Returns:
            Consultation response
        """
        question_lower = question.lower()

        if domain and domain in self._wisdom_db:
            for key, consultation in self._wisdom_db[domain].items():
                if (
                    key in question_lower
                    or consultation.question.lower() in question_lower
                ):
                    return consultation

        if domain is None:
            for wisdom_domain in self._wisdom_db.values():
                for consultation in wisdom_domain.values():
                    if consultation.question.lower() in question_lower:
                        return consultation

        return Consultation(
            question=question,
            domain=ArchitectureDomain.AGENTS,
            answer="I don't have specific guidance for that question. Try asking about:\n"
            "- Agent design\n"
            "- Hybrid backend\n"
            "- TUI design\n"
            "- Tool design\n"
            "- Testing strategy\n"
            "- Security practices\n"
            "- Performance optimization",
            recommendations=[],
            warnings=["Please rephrase your question"],
            timestamp=datetime.now(),
        )

    def list_domains(self) -> List[str]:
        """List available consultation domains."""
        return [d.value for d in ArchitectureDomain]

    def get_domain_wisdom(self, domain: ArchitectureDomain) -> List[Consultation]:
        """Get all wisdom for a domain."""
        return list(self._wisdom_db.get(domain, {}).values())


def consult_queen(question: str, domain: Optional[str] = None) -> Consultation:
    """
    Convenience function to consult the Queen Bee.

    Usage:
        >>> wisdom = consult_queen("How should agents be designed?")
        >>> print(wisdom.answer)
    """
    consultant = QueenBeeConsultant()
    domain_enum = None

    if domain:
        try:
            domain_enum = ArchitectureDomain(domain.lower())
        except ValueError:
            pass

    return consultant.consult(question, domain_enum)


if __name__ == "__main__":
    consultant = QueenBeeConsultant()

    print("Queen Bee Consultation System")
    print("=" * 50)
    print("\nAvailable domains:")
    for domain in consultant.list_domains():
        print(f"  - {domain}")

    print("\n" + "=" * 50)
    print("\nExample consultations:\n")

    for domain in ArchitectureDomain:
        wisdom = consultant.get_domain_wisdom(domain)
        if wisdom:
            c = wisdom[0]
            print(f"Q: {c.question}")
            print(f"Domain: {c.domain.value}")
            print("-" * 30)
