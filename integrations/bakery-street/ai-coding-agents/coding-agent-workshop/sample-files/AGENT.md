# Coding Agent Workshop Environment

## Project Overview
This is a step-by-step workshop for building your own coding agent using Go and the AIMLAPI service.

## Environment Details
- **Language**: Go 1.24+
- **API**: AIMLAPI (OpenAI-compatible)
- **Model**: Claude 3.5 Sonnet
- **Tools**: File operations, shell commands, code search

## Workshop Structure
```
coding-agent-workshop/
├── versions/           # Progressive agent implementations
├── sample-files/       # Test files for the agents
├── docs/              # Additional documentation
└── README.md          # Main workshop guide
```

## Agent Versions
1. **chat.go** - Basic Claude conversation
2. **read.go** - File reading capability
3. **list_files.go** - Directory listing
4. **bash_tool.go** - Shell command execution
5. **edit_tool.go** - File editing
6. **code_search_tool.go** - Code pattern search

## Getting Started
1. Set your AIMLAPI API key: `export AIMLAPI_API_KEY="your-key"`
2. Run any version: `go run versions/chat.go`
3. Try the sample files for testing

## Sample Files
- `fizzbuzz.js` - JavaScript implementation for testing file operations
- `riddle.txt` - Text file for exploring file reading
- `AGENT.md` - This environment information file

Happy coding!
