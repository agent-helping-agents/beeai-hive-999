**Bakery Street Project AI Coding Agent Instructions**

This document guides AI agents (e.g., Copilot, Cursor) to be productive in the Bakery-street-project organization, focusing on autonomous AI systems with enterprise security. All repos follow Sherlock Holmes-themed branding for deductive AI innovation. Agents must prioritize privacy (no secrets in commits), small PRs, and local testing. Use MIT license; avoid direct main pushes—fork/PR only. Incorporate personal details: Owner Kiliaan Vanvoorden (kiliaan2@gmail.com personal; kiliaan@bakerstreetproject221B.store business).

**Big Picture Architecture**
- **Core Flow**: Multi-agent systems (e.g., Analyst/Artist/Engineer in Terminal221b) orchestrate via local LLM inference (TensorRT-LLM/Ollama) and blockchain (Solana). Data flows from configs → agents → outputs/research, with fractal/quantum math in navigation (AurobotNav: PRIMECORE.py + astar_nav.py).
- **Service Boundaries**: Repos are modular—frameworks (ai-development-framework: config/tools/environments) provide orchestration; assistants (go-ai-coder: cmd/internal for CLI/processing) handle coding/web scraping; labs (Baker-Street-Laboratory: research/implementation/optimization) manage AI models/workflows.
- **Why This Structure**: Privacy-first (local processing in go-ai-coder/Ollama) for enterprise compliance; cross-repo links (e.g., Terminal221b integrates go-ai-coder agents) enable polymathic autonomy.
- **Key Integration Points**: Ollama in go-ai-coder (configs/ollama.yaml); Docker in ai-development-framework/discord-bot-automation (docker-compose.yml for secure bots); Jupyter in AurobotNav (auro_sim.ipynb for simulations); GitHub API in go-ai-coder for repo analysis.

**Critical Developer Workflows**
- **Build/Test/Debug (Python)**: Activate env (e.g., source activate-ai.sh in ai-development-framework); install via requirements.txt; test with pytest (e.g., python -m pytest tests/ in Baker-Street-Laboratory); debug notebooks locally via jupyter notebook auro_sim.ipynb (AurobotNav).
- **Build/Test/Debug (Go)**: go mod tidy; build CLI with go build -o cloudy-mc-codeface cmd/main.go (go-ai-coder); test with go test ./...; debug with go vet or golangci-lint run if configured.
- **Docker/Deployment**: Build with docker build -t image:latest .; run docker-compose up (ai-development-framework/discord-bot-automation); scan for security with docker-scan.
- **CI/CD**: Mirror .github/workflows (e.g., in Baker-Street-Laboratory for automated tests); add YAML for push/PR triggers; no direct CI in most repos—add if missing via PR.
- **Common Commands**: git clone all via gh repo list/clone; local run e.g., python PRIMECORE.py (AurobotNav) or cloudy-mc-codeface --model llama3.2:3b (go-ai-coder).

**Project-Specific Conventions**
- **Naming/Patterns**: Agent roles separated (e.g., vision/embed/scientific in Baker-Street-Laboratory agents.yaml); CLI in cmd/ (go-ai-coder); fractal grids in notebooks (AurobotNav); no large binaries—use git-lfs if needed.
- **Configs**: YAML-based (agents.yaml in Baker-Street-Laboratory/config); .env.example for secrets (multiple repos); mod9/DNA tuning in PRIMECORE.py (AurobotNav).
- **Cross-Component Communication**: API calls via secure commands (PRIMECORE.py); web scraping in go-ai-coder internal/; orchestration in advanced_ai_orchestrator.py (ai-development-framework).
- **Dependencies**: Python: numpy/sympy/cryptography (AurobotNav); Go: OpenAI SDK/GoDotEnv (go-ai-coder); avoid internet installs—use local Ollama/TensorRT.

**Per-Repo Quickstarts** (Read these first for prioritized repos)
- **Terminal221b**: Read README.md, configs/, agents/; run demo scripts; focus on TUI/polymath agents.
- **Baker-Street-Laboratory**: Read README.md, agents.yaml; navigate research/implementation; test pytest tests/; deploy docker-compose up.
- **go-ai-coder**: Read README.md, cmd/main.go, internal/; go test ./...; configure Ollama via flags/env.
- **AurobotNav**: Read README.md, PRIMECORE.py, astar_nav.py; pytest tests/; open auro_sim.ipynb.
- **ai-development-framework**: Read README.md, deploy_production.py; activate envs (activate-ai.sh); test test_duckdb.py.
- **discord-bot-automation**: Read README.md, CONTRIBUTING.md; add workflows to .github/; focus on Docker security.

**Guardrails for Agents**
- Small changes only; test locally first (e.g., go test or pytest).
- No secrets/API keys in code—use .env.example.
- PRs: Include tests, update README if commands change; use pull_request_template.md; title "feat/fix: brief desc".
- Avoid: Model weights >10MB, direct main commits, untested integrations.

**Profile Update Tasks (Specific to This Assignment)**
- **Personal Profile (Kiliaan Vanvoorden)**: Update bio to reflect AI expertise; add emails (personal: kiliaan2@gmail.com, business: kiliaan@bakerstreetproject221B.store); set location to Belgium; upload profile picture (user-provided) via settings.
- **Organization Profile (Bakery-street-project)**: Enhance bio with enterprise AI and regulatory tech focus; update email to kiliaan@bakerstreetproject221B.store; add website if available; pin key repos (e.g., Terminal221b); apply custom banner (Sherlock-themed graphic).
- **SEO/Visibility**: Add keywords like "enterprise AI", "regulatory technology" to descriptions; unarchive prioritized repos; promote via Twitter (@Boozelee86).

**Neuromorphic AI Patterns** (Experimental repos)
- **MYTHICNODE-Neuromorphic-Psychedelic-AI**: Modular framework for psychedelic-inspired brain states; uses GAN (PyTorch/TensorFlow), biosignal acquisition, Docker/Kubernetes deployment. Read LICENSE.md, SUPPORT.md; run via `docker-compose` or `kubectl`.
- **cryptojukebox-ai**: Neuromorphic computing with consciousness themes; currently empty—add SNN models (use Norse/Lava frameworks), integrate with prioritized repos.
- **Frameworks to consider**: Norse (PyTorch SNNs), Intel Lava (Loihi hardware), NeuroBench (benchmarking), SpiNNaker (large-scale simulations).
- **Integration pattern**: Link neuromorphic outputs to Terminal221b agents for consciousness-inspired decision loops; use AurobotNav's φ-A* for spatial neuromorphic pathfinding.

**Non-Prioritized Repos Reference** (Archived—unarchive selectively)
| Repo | Score | Theme | Action |
|------|-------|-------|--------|
| ai-coding-agents | 4.5 | Educational AI workshop (Go) | Consider unarchive—strong docs |
| Linty-McLintface | 4.5 | C# Roslyn analyzer | Keep archived—niche use |
| voidshatterecho | 4.0 | Cyberpunk RPG with AI companion | Keep archived—game project |
| MYTHICNODE | 3.0 | Neuromorphic/GAN | **Unarchive**—neuromorphic focus |
| cryptojukebox-ai | 1.0 | Neuromorphic consciousness | **Unarchive**—add SNN code |

**Example Tasks/PRs**
- Task: "Update organization bio with new details"; PR: "docs: enhance org profile bio and contacts".
- Task: "Add profile picture and emails"; PR: "feat: update personal and org profiles".
- Task: "Add SNN model to cryptojukebox-ai"; PR: "feat: implement basic spiking neural network".
- Task: "Integrate Norse framework in MYTHICNODE"; PR: "feat: add Norse SNN simulation layer".

Last Updated: December 09, 2025. Feedback: Open issues for unclear sections.
