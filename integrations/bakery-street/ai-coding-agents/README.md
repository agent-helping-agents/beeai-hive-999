# 🤖 AI Coding Agents - Complete Ecosystem

A comprehensive collection of AI coding agents for both educational and production use, featuring progressive learning and enterprise-grade capabilities.

## 🎯 What's Included

### 📚 **coding-agent-workshop** - Educational Framework
Complete workshop for learning how to build AI coding assistants like Cursor, Windsurf, or Cline.

**Features:**
- **6 Progressive Versions** - From basic chat to full coding assistant
- **Tool System** - File operations, command execution, code search
- **Security Features** - Safe command execution and validation
- **Comprehensive Documentation** - Architecture guides and examples

**Versions:**
1. `chat.go` - Basic Claude conversation via AIMLAPI
2. `read.go` - File reading capability
3. `list_files.go` - Directory listing functionality
4. `bash_tool.go` - Shell command execution
5. `edit_tool.go` - File editing and creation
6. `code_search_tool.go` - Pattern search using ripgrep

### 🚀 **go-ai-coder** - Production-Ready Agent
Enterprise-grade AI coding agent with advanced features and GitHub integration.

**Features:**
- **GitHub Integration** - Repository analysis, issue tracking, PR management
- **AI Learning System** - Web scraping, research, auto-learning
- **Ollama Integration** - Local AI model support
- **Conversation History** - Context-aware responses
- **Auto-save** - Conversation persistence
- **Advanced Configuration** - Flexible settings and tooling

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Coding Agent Ecosystem                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📚 Educational Workshop          🚀 Production Agent       │
│  ┌─────────────────────────┐     ┌─────────────────────────┐ │
│  │ • Progressive Learning  │     │ • GitHub Integration    │ │
│  │ • Tool Development      │     │ • AI Learning System    │ │
│  │ • Security Features     │     │ • Ollama Integration    │ │
│  │ • Documentation         │     │ • Enterprise Features   │ │
│  └─────────────────────────┘     └─────────────────────────┘ │
│                                                             │
│  🔧 Shared Technologies                                     │
│  • Go Programming Language                                  │
│  • OpenAI Go SDK                                            │
│  • AIMLAPI Integration                                      │
│  • Tool Calling Patterns                                    │
│  • Security Best Practices                                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Go 1.24+ 
- AIMLAPI account (for workshop)
- Ollama (for production agent)
- GitHub token (optional, for enhanced features)

### Educational Workshop
```bash
cd coding-agent-workshop
export AIMLAPI_API_KEY="your-api-key-here"
go run versions/chat.go
```

### Production Agent
```bash
cd go-ai-coder
export GITHUB_TOKEN="your-github-token"  # Optional
go run cmd/main.go
```

## 📖 Documentation

### Workshop Documentation
- [Workshop README](coding-agent-workshop/README.md) - Complete learning guide
- [Architecture Guide](coding-agent-workshop/docs/ARCHITECTURE.md) - System design
- [Tool Development Guide](coding-agent-workshop/docs/TOOL_GUIDE.md) - Extending functionality
- [Examples](coding-agent-workshop/docs/EXAMPLES.md) - Practical usage

### Production Agent Features
- **GitHub Commands**: `github repos`, `github search`, `github issues`, `github prs`
- **AI Learning**: `ai learn`, `ai research <topic>`, `ai scrape <url>`
- **File Operations**: `read <file>`, `list <directory>`
- **Go Resources**: `go resources` for curated learning materials

## 🛠️ Technology Stack

### Core Technologies
- **Go 1.24+** - Main programming language
- **OpenAI Go SDK** - API client library
- **AIMLAPI** - Claude model access
- **Ollama** - Local AI model support
- **ripgrep/grep** - Code search functionality

### Integration APIs
- **GitHub API** - Repository management and analysis
- **Web Scraping** - Content extraction and learning
- **OAuth2** - Secure authentication flows

## 🔒 Security Features

### Workshop Security
- **Dangerous Command Blocking** - Prevents harmful operations
- **Path Sanitization** - Input validation and security
- **Timeout Enforcement** - Prevents hanging operations
- **Error Handling** - Graceful degradation

### Production Security
- **Token Management** - Secure credential handling
- **Rate Limiting** - API abuse prevention
- **Input Validation** - Safe data processing
- **Error Recovery** - Robust failure handling

## 📊 Learning Outcomes

After using this ecosystem, you'll understand:

### Core Concepts
- AI model integration with custom tools
- Tool calling patterns and implementation
- Error handling and user experience design
- Security considerations for AI agents

### Technical Skills
- Go programming for AI applications
- OpenAI API integration
- File system operations and safety
- Command execution and security
- Pattern matching and code search

### Best Practices
- Progressive feature development
- Tool design and documentation
- Security and safety measures
- User experience optimization
- Code organization and structure

## 🎯 Use Cases

### Educational
- **Learning AI Integration** - Understand how coding agents work
- **Tool Development** - Build custom tools and capabilities
- **Security Awareness** - Learn safe AI agent practices
- **Progressive Learning** - Step-by-step complexity building

### Production
- **Code Analysis** - Analyze repositories and codebases
- **GitHub Management** - Manage issues, PRs, and repositories
- **AI Learning** - Automatically research and learn new topics
- **Development Assistance** - Get AI help with coding tasks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add feature"`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/Bakery-street-projct/ai-coding-agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Bakery-street-projct/ai-coding-agents/discussions)
- **Documentation**: Check the docs/ folders in each project

### Common Issues
1. **API key issues**: Check setup and ensure your AIMLAPI account is verified
2. **Go errors**: Run `go mod tidy`, ensure Go 1.24+ is installed
3. **Tool errors**: Use `--verbose` for logs, check file paths and permissions
4. **GitHub integration**: Set GITHUB_TOKEN for enhanced features

## 🏆 Success Metrics

This ecosystem successfully delivers:
- ✅ **Complete working examples** - All versions compile and run
- ✅ **Progressive complexity** - Clear learning progression
- ✅ **Comprehensive documentation** - Multiple learning resources
- ✅ **Safety and security** - Production-ready practices
- ✅ **Extensibility** - Easy to modify and extend
- ✅ **User experience** - Intuitive and helpful interface

---

**Made with ❤️ by Bakery Street Project**

*Complete AI Coding Agent Ecosystem for Education and Production*
