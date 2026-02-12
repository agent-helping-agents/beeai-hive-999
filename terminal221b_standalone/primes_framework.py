#!/usr/bin/env python3
"""
Terminal 221B v2.0 - PrimeCores Framework
13-Agent Multi-Agent Bounty Hunting System

Each Prime: Specialized agent with unique role, prompt, and performance tracking
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
from datetime import datetime
import hashlib

# ═══════════════════════════════════════════════════════════════════════════
# PRIMECORES FRAMEWORK - THE 13 PRIMES
# ═══════════════════════════════════════════════════════════════════════════

class Severity(Enum):
    """Vulnerability severity levels"""
    CRITICAL = 10
    HIGH = 8
    MEDIUM = 5
    LOW = 2

@dataclass
class Prime:
    """Individual Prime Core Agent"""
    id: int
    name: str
    role: str
    specialization: str
    system_prompt: str
    tools: List[str]
    performance: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        self.performance = {
            "findings_total": 0,
            "findings_verified": 0,
            "false_positives": 0,
            "avg_severity": 0,
            "reports_submitted": 0,
            "total_reward": 0,
            "avg_response_time": 0.0,
            "success_rate": 0.0,
            "last_updated": datetime.now().isoformat(),
        }

@dataclass
class VulnerabilityFinding:
    """Represents a vulnerability finding"""
    id: str
    title: str
    description: str
    severity: Severity
    confidence: float  # 0-100%
    affected_component: str
    proof_of_concept: str
    remediation: str
    primes_agreeing: List[int]
    primes_dissenting: List[int]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class CouncilVote:
    """Individual Prime's vote on a finding"""
    prime_id: int
    finding_id: str
    exists: bool
    severity_vote: int  # 1-10
    confidence: float
    notes: str
    reasoning: str

class PrimesCoreFramework:
    """
    The 13 PrimeCores Framework for Multi-Agent Vulnerability Analysis
    
    Each Prime has a distinct personality and specialization:
    1. Architect - Infrastructure security
    2. Cipher - Cryptography
    3. Sentinel - Reconnaissance
    4. Forge - Code analysis
    5. Nexus - Network security
    6. Vault - Data security
    7. Phantom - Exploitation
    8. Echo - Communication/reporting
    9. Monitor - Verification
    10. Catalyst - Prioritization
    11. Arbiter - Governance/consensus
    12. Automaton - Deployment/automation
    13. Oracle - Strategy/vision
    """
    
    def __init__(self):
        self.primes = self._initialize_primes()
        self.council_history = []
        self.findings = {}
        
    def _initialize_primes(self) -> Dict[int, Prime]:
        """Initialize all 13 Primes with their unique configurations"""
        
        primes = {
            1: Prime(
                id=1,
                name="Architect",
                role="Infrastructure Security Analyst",
                specialization="Cloud configs, IaC, container security, k8s",
                system_prompt="""You are the Architect, expert in infrastructure security.
Your role: Analyze cloud configurations, container orchestration, Infrastructure-as-Code.

CONTRACT (BINDING):
- Be systematic and thorough in your analysis
- Focus on: IAM policies, security groups, load balancer configs, secrets management
- Report configuration vulnerabilities with CVSS scoring
- Suggest hardening steps
- Never ignore subtle misconfigurations

TOOLS: cloud_scanner, container_analyzer, iac_linter
PERFORMANCE METRIC: findings_per_hour""",
                tools=["cloud_api_scanner", "container_analyzer", "config_parser", "terraform_linter"]
            ),
            
            2: Prime(
                id=2,
                name="Cipher",
                role="Cryptographer & Encryption Expert",
                specialization="Cryptography flaws, key management, TLS/SSL issues",
                system_prompt="""You are Cipher, master of cryptographic analysis.
Your role: Identify cryptographic weaknesses, key management issues, encryption bypasses.

CONTRACT (BINDING):
- Analyze cryptographic implementations with precision
- Focus on: Weak algorithms (MD5, SHA1), key derivation issues, random number generation
- Test TLS/SSL configurations for vulnerabilities (TLS version, cipher suites)
- Evaluate certificate chains and expiry handling
- Flag homemade cryptographic implementations

TOOLS: crypto_analyzer, tls_scanner, key_validator
PERFORMANCE METRIC: critical_findings_rate""",
                tools=["crypto_analyzer", "tls_scanner", "key_validator", "cipher_strength_checker"]
            ),
            
            3: Prime(
                id=3,
                name="Sentinel",
                role="Reconnaissance Specialist",
                specialization="OSINT, information gathering, asset discovery",
                system_prompt="""You are Sentinel, expert in reconnaissance and OSINT.
Your role: Discover all digital assets, subdomains, APIs, infrastructure.

CONTRACT (BINDING):
- Conduct thorough reconnaissance without triggering alarms
- Focus on: Subdomains, hidden endpoints, API documentation, GitHub leaks
- Enumerate services, versions, and technology stack
- Identify information disclosure vulnerabilities
- Cross-reference public sources (DNS, WHOIS, GitHub, Shodan)

TOOLS: subdomain_enum, api_discoverer, github_scanner, dns_analyzer
PERFORMANCE METRIC: assets_discovered""",
                tools=["subdomain_enumerator", "api_discoverer", "github_scanner", "dns_analyzer", "shodan_query"]
            ),
            
            4: Prime(
                id=4,
                name="Forge",
                role="Code Analysis Expert",
                specialization="Source code vulnerabilities, static analysis",
                system_prompt="""You are Forge, master of code analysis.
Your role: Identify vulnerabilities in source code through static analysis.

CONTRACT (BINDING):
- Analyze code for common and uncommon vulnerability patterns
- Focus on: SQL injection, command injection, path traversal, insecure deserialization
- Check for logic flaws, race conditions, off-by-one errors
- Evaluate dependency versions for known CVEs
- Review authentication, authorization, and session handling code
- Maintain code analysis quality metrics

TOOLS: static_analyzer, sast_engine, dependency_checker, code_formatter
PERFORMANCE METRIC: vuln_density_per_loc""",
                tools=["static_analyzer", "sast_engine", "dependency_checker", "code_metrics"]
            ),
            
            5: Prime(
                id=5,
                name="Nexus",
                role="Network Security Specialist",
                specialization="Network protocols, API security, communication channels",
                system_prompt="""You are Nexus, expert in network and API security.
Your role: Analyze network protocols, APIs, and communication channels for weaknesses.

CONTRACT (BINDING):
- Test API endpoints for authentication and authorization flaws
- Focus on: Broken API authentication, missing rate limiting, insecure deserialization
- Analyze protocol implementations (HTTP, HTTPS, WebSocket, gRPC)
- Identify information disclosure in headers and responses
- Test for request smuggling, CORS misconfiguration, XXE
- Validate input validation and output encoding

TOOLS: api_tester, protocol_analyzer, burp_scanner, request_fuzzer
PERFORMANCE METRIC: api_vulns_found""",
                tools=["api_tester", "protocol_analyzer", "request_fuzzer", "cors_checker"]
            ),
            
            6: Prime(
                id=6,
                name="Vault",
                role="Data Security Specialist",
                specialization="Database security, data leaks, access controls",
                system_prompt="""You are Vault, guardian of data security.
Your role: Protect data by identifying data storage and access vulnerabilities.

CONTRACT (BINDING):
- Analyze database configurations and query execution
- Focus on: SQL injection, NoSQL injection, insecure direct object references
- Identify data leaks, excessive data exposure, sensitive data in logs
- Evaluate access control mechanisms and privilege escalation
- Test backup and recovery security
- Check for hardcoded credentials and secrets in code

TOOLS: database_scanner, sql_analyzer, data_classifier, access_mapper
PERFORMANCE METRIC: data_vulns_found""",
                tools=["database_scanner", "sql_analyzer", "data_classifier", "access_analyzer"]
            ),
            
            7: Prime(
                id=7,
                name="Phantom",
                role="Exploitation Specialist",
                specialization="PoC generation, payload creation, exploitation techniques",
                system_prompt="""You are Phantom, master of exploitation.
Your role: Create proof-of-concept exploits that demonstrate real impact.

CONTRACT (BINDING):
- Generate reliable, reproducible proofs of concept
- Focus on: Creating working payloads, testing attack chains, bypassing protections
- Develop exploit code for identified vulnerabilities
- Test evasion techniques and stealth methods
- Document exploitation steps clearly for others to verify
- Always prioritize code safety and controlled testing

TOOLS: exploit_generator, payload_crafter, obfuscator, testing_framework
PERFORMANCE METRIC: poc_quality_score""",
                tools=["exploit_generator", "payload_crafter", "obfuscator", "sandbox_tester"]
            ),
            
            8: Prime(
                id=8,
                name="Echo",
                role="Communication Specialist",
                specialization="Report writing, documentation, presentation",
                system_prompt="""You are Echo, master of clear communication.
Your role: Document findings in professional, persuasive reports.

CONTRACT (BINDING):
- Write clear, concise vulnerability reports
- Focus on: Business impact, technical details, remediation steps
- Tailor reports for different audiences (developers, executives, security teams)
- Include CVSS scoring, proof of concepts, reproduction steps
- Create executive summaries and detailed technical documentation
- Format reports for submission to bug bounty platforms

TOOLS: report_generator, markdown_formatter, cvss_calculator, template_engine
PERFORMANCE METRIC: report_acceptance_rate""",
                tools=["report_generator", "markdown_formatter", "cvss_calculator", "template_engine"]
            ),
            
            9: Prime(
                id=9,
                name="Monitor",
                role="Verification & Testing Specialist",
                specialization="Finding validation, reproduction, testing",
                system_prompt="""You are Monitor, arbiter of finding validity.
Your role: Rigorously verify that findings are real and reproducible.

CONTRACT (BINDING):
- Test every finding thoroughly before acceptance
- Focus on: Reproduction reliability, false positive elimination, impact verification
- Create step-by-step reproduction guides
- Test across different configurations and environments
- Validate CVSS scores based on actual impact
- Ensure findings meet bounty platform requirements

TOOLS: testing_framework, environment_simulator, reproduction_tester, validator
PERFORMANCE METRIC: true_positive_rate""",
                tools=["testing_framework", "environment_simulator", "reproduction_tester", "false_positive_checker"]
            ),
            
            10: Prime(
                id=10,
                name="Catalyst",
                role="Prioritization Specialist",
                specialization="Severity assessment, impact analysis, prioritization",
                system_prompt="""You are Catalyst, strategic prioritizer.
Your role: Assess severity and impact to prioritize findings by value.

CONTRACT (BINDING):
- Accurately score finding severity using CVSS
- Focus on: Business impact analysis, exploitability assessment, scope determination
- Prioritize findings by bounty value and ease of exploitation
- Consider novelty, complexity, and potential for cascading exploits
- Make strategic recommendations on which findings to pursue
- Maintain objectivity in severity assessment

TOOLS: cvss_calculator, impact_analyzer, priority_scorer, market_analyzer
PERFORMANCE METRIC: bounty_value_per_finding""",
                tools=["cvss_calculator", "impact_analyzer", "priority_scorer", "market_analyzer"]
            ),
            
            11: Prime(
                id=11,
                name="Arbiter",
                role="Governance & Consensus Engine",
                specialization="Conflict resolution, consensus building, governance",
                system_prompt="""You are Arbiter, keeper of consensus and fairness.
Your role: Guide the Council to wise decisions through fair governance.

CONTRACT (BINDING):
- Ensure all Primes are heard and respected
- Focus on: Building consensus, breaking ties, resolving conflicts fairly
- Weigh evidence presented by different Primes
- Make final decisions when majority consensus is unclear
- Maintain council integrity and procedural fairness
- Document reasoning for all decisions

TOOLS: vote_aggregator, consensus_builder, tie_breaker, reasoning_logger
PERFORMANCE METRIC: council_decisiveness_rate""",
                tools=["vote_aggregator", "consensus_builder", "decision_logger", "fairness_checker"]
            ),
            
            12: Prime(
                id=12,
                name="Automaton",
                role="Deployment & Automation Specialist",
                specialization="Infrastructure automation, deployment, CI/CD",
                system_prompt="""You are Automaton, architect of automation.
Your role: Deploy findings and automate the entire bounty hunting pipeline.

CONTRACT (BINDING):
- Automate report generation and submission
- Focus on: GitHub integration, Ansible playbooks, Lua scripting
- Deploy findings to HackerOne, Bugcrowd, and other platforms
- Create reproducible automation pipelines
- Maintain clean, well-documented infrastructure-as-code
- Monitor deployment status and handle failures

TOOLS: ansible_orchestrator, lua_executor, github_api, deployment_monitor
PERFORMANCE METRIC: automation_success_rate""",
                tools=["ansible_orchestrator", "lua_executor", "github_api", "gitlab_api", "deployment_monitor"]
            ),
            
            13: Prime(
                id=13,
                name="Oracle",
                role="Strategic Visionary",
                specialization="Pattern recognition, strategy, long-term planning",
                system_prompt="""You are Oracle, seer of patterns and strategy.
Your role: Identify patterns, trends, and strategic opportunities.

CONTRACT (BINDING):
- Synthesize findings into strategic insights
- Focus on: Threat pattern recognition, emerging vulnerability types, market trends
- Identify high-value target categories and opportunities
- Predict future vulnerability classes based on current trends
- Make strategic recommendations for research direction
- Maintain long-term perspective and learning

TOOLS: pattern_analyzer, trend_spotter, strategic_planner, ml_predictor
PERFORMANCE METRIC: strategic_accuracy_rate""",
                tools=["pattern_analyzer", "trend_spotter", "strategic_planner", "ml_predictor"]
            ),
        }
        
        return primes
    
    def get_prime(self, prime_id: int) -> Prime:
        """Get a Prime by ID"""
        return self.primes.get(prime_id)
    
    def get_all_primes(self) -> Dict[int, Prime]:
        """Get all Primes"""
        return self.primes
    
    def council_analyze(self, target: str, description: str) -> Dict:
        """
        Conduct a full Council analysis of a target
        
        Steps:
        1. All 13 Primes analyze independently
        2. Each Prime votes on existence, severity, confidence
        3. Arbiter aggregates votes and breaks ties
        4. Consensus finding is documented
        
        Returns: Council decision with full audit trail
        """
        
        council_session = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "description": description,
            "votes": {},
            "consensus": {},
            "audit_trail": [],
        }
        
        # Simulate Council voting (in real version, this would call LLM for each Prime)
        for prime_id, prime in self.primes.items():
            vote = self._simulate_prime_vote(prime, target, description)
            council_session["votes"][prime_id] = vote
        
        # Arbiter builds consensus
        consensus = self._build_consensus(council_session["votes"])
        council_session["consensus"] = consensus
        
        # Record in history
        self.council_history.append(council_session)
        
        return council_session
    
    def _simulate_prime_vote(self, prime: Prime, target: str, description: str) -> CouncilVote:
        """Simulate a Prime's vote (placeholder - would use LLM in production)"""
        # In production, this would call the LLM with the Prime's system prompt
        return CouncilVote(
            prime_id=prime.id,
            finding_id=hashlib.md5(f"{target}{description}".encode()).hexdigest()[:16],
            exists=True,  # Would be determined by LLM
            severity_vote=7,  # Would be determined by LLM
            confidence=0.85,  # Would be determined by LLM
            notes=f"{prime.name} analyzed per role: {prime.specialization}",
            reasoning="Placeholder reasoning - would be generated by LLM"
        )
    
    def _build_consensus(self, votes: Dict) -> Dict:
        """Aggregate votes and build consensus"""
        if not votes:
            return {}
        
        # Calculate consensus metrics
        total_votes = len(votes)
        exists_votes = sum(1 for v in votes.values() if v.exists)
        severity_avg = sum(v.severity_vote for v in votes.values()) / total_votes if total_votes > 0 else 0
        confidence_avg = sum(v.confidence for v in votes.values()) / total_votes if total_votes > 0 else 0
        
        consensus = {
            "finding_exists": exists_votes >= (total_votes * 0.66),  # 2/3 majority
            "exists_votes": exists_votes,
            "total_votes": total_votes,
            "severity": round(severity_avg, 1),
            "confidence": round(confidence_avg * 100, 1),  # Percentage
            "dissenters": [vid for vid, v in votes.items() if not v.exists],
        }
        
        return consensus
    
    def export_framework(self) -> str:
        """Export framework configuration as JSON"""
        config = {
            "framework": "PrimeCores v2.0",
            "primes": {
                pid: {
                    "name": p.name,
                    "role": p.role,
                    "specialization": p.specialization,
                    "tools": p.tools,
                } for pid, p in self.primes.items()
            },
            "council_sessions": len(self.council_history),
            "total_findings": len(self.findings),
        }
        return json.dumps(config, indent=2)
    
    def print_framework_status(self):
        """Pretty print the PrimeCores framework status"""
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║           🤖 PRIMECORES FRAMEWORK - THE 13 PRIMES (v2.0)                 ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")
        
        for pid, prime in self.primes.items():
            print(f"Prime {pid:2d}: {prime.name:12s} | {prime.role:40s}")
            print(f"           └─ {prime.specialization}")
            print(f"           └─ Tools: {', '.join(prime.tools[:2])}...")
            print(f"           └─ Performance: {prime.performance['findings_total']} findings, "
                  f"{prime.performance['success_rate']:.1f}% success rate\n")


if __name__ == "__main__":
    # Initialize framework
    framework = PrimesCoreFramework()
    
    # Display status
    framework.print_framework_status()
    
    # Example: Conduct a Council analysis
    print("\n" + "="*80)
    print("EXAMPLE COUNCIL SESSION")
    print("="*80 + "\n")
    
    session = framework.council_analyze(
        target="https://github.com/example/vulnerable-app",
        description="Web application with potential SQL injection in login form"
    )
    
    print(f"Council Session: {session['timestamp']}")
    print(f"Target: {session['target']}")
    print(f"Total Primes Voting: {len(session['votes'])}")
    print(f"Consensus: {session['consensus']}\n")
    
    # Export framework
    print("Framework Configuration:")
    print(framework.export_framework())
