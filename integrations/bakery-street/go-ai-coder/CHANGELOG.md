# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- License verification system with tiered access (Free/Pro/Enterprise)
- Automated release builds for Linux, macOS, and Windows
- Daily run limits for free tier users (5 runs/day)
- Token limits per tier (Free: 1K, Pro: 10K, Enterprise: Unlimited)
- License status display command
- TODO_MVP.md gap analysis document

### Changed
- Updated CI/CD pipeline with release automation
- Release workflow builds from `github_ai_agent.go`

### Security
- Environment-based license key storage (LICENSE_KEY)
- No hardcoded secrets in codebase

---

## [0.1.0] - 2025-09-15

### Added
- Initial release
- Ollama integration for local LLM processing
- GitHub repository analysis
- Web scraping capabilities
- CLI interface with interactive mode
- File reading and editing tools
- Code search functionality
- Bash command execution

### Features
- `read <file>` - Read and analyze file content
- `list <directory>` - List directory contents
- `github repos` - List your repositories
- `github search <query>` - Search GitHub repositories
- `ai learn` - Comprehensive Go ecosystem research
- `ai research <topic>` - Research specific topics
- `go resources` - Show curated Go learning resources

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.1.0 | 2025-09-15 | Initial prototype |
| 1.0.0 | TBD | Production release with licensing |

---

## Upgrade Guide

### From 0.x to 1.x

1. Set `LICENSE_KEY` environment variable (optional, defaults to free tier)
2. Download new binary from GitHub Releases
3. Replace existing binary

```bash
# Linux/macOS
export LICENSE_KEY=PRO_your_key_here  # Optional - for Pro tier
curl -sSL https://github.com/Bakery-street-project/go-ai-coder/releases/latest/download/go-ai-coder-linux-amd64 -o go-ai-coder
chmod +x go-ai-coder
./go-ai-coder --help
```

### Windows

```powershell
$env:LICENSE_KEY = "PRO_your_key_here"  # Optional
Invoke-WebRequest -Uri "https://github.com/Bakery-street-project/go-ai-coder/releases/latest/download/go-ai-coder-windows-amd64.exe" -OutFile "go-ai-coder.exe"
.\go-ai-coder.exe --help
```

---

## License Tiers

| Tier | Runs/Day | Tokens/Run | Price |
|------|----------|------------|-------|
| Free | 5 | 1,000 | $0 |
| Pro | 100 | 10,000 | $9/mo |
| Enterprise | Unlimited | Unlimited | Contact |

Purchase: https://bakerstreetproject221B.store/pricing
