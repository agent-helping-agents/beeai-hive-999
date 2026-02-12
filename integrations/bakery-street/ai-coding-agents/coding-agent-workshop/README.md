# Build Your Own Coding Agent - Step-by-Step Workshop

A comprehensive workshop that teaches you how to build your own coding agent similar to Roo code, Cline, Amp, Cursor, or Windsurf.

## 🎯 What You'll Learn

By the end of this workshop, you'll understand how to:
- Connect to the AIMLAPI API using a Claude model
- Build a simple AI chatbot
- Add tools for reading files, editing code, and running commands
- Handle tool requests and errors gracefully
- Enhance agent capabilities step by step

## 🏗️ What We're Building

The workshop builds 6 progressive versions of a coding assistant, each adding new capabilities:

1. **Basic Chat** — Talk to Claude via AIMLAPI
2. **File Reader** — Read code files
3. **File Explorer** — List files in folders
4. **Command Runner** — Run shell commands
5. **File Editor** — Modify files
6. **Code Search** — Search codebase with patterns (using ripgrep)

## 🏛️ Architecture Overview

Each agent follows a simple event loop:
1. Wait for user input
2. Send input to Claude via AIMLAPI
3. Claude responds directly or requests a tool (e.g., read a file)
4. The agent runs the tool and sends results back to Claude
5. Claude provides the final answer

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   User      │───▶│   Agent      │───▶│   Claude    │
│   Input     │    │   (Go)       │    │  (AIMLAPI)  │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                    │
                           │                    │
                           ▼                    ▼
                   ┌──────────────┐    ┌─────────────┐
                   │   Tool       │    │   Tool      │
                   │   Registry   │    │   Request   │
                   └──────────────┘    └─────────────┘
```

## 🚀 Getting Started

### Prerequisites
- Go 1.24.2 or later
- AIMLAPI account (free tier available)

### Set Up Your Environment

**Option 1: Recommended (using devenv)**
```bash
devenv shell  # Loads everything you need
```

**Option 2: Manual setup**
```bash
# Make sure Go is installed
go mod tidy
```

### Add Your API Key
Set the AIMLAPI API key:
```bash
export AIMLAPI_API_KEY="your-api-key-here"
```

## 📚 Workshop Steps

### 1. Basic Chat (`versions/chat.go`)
A simple chatbot that talks to Claude via AIMLAPI.

**Run:**
```bash
go run versions/chat.go
```

**Try:** "Hello!" or add `--verbose` for detailed logs.

### 2. File Reader (`versions/read.go`)
Claude can now read files.

**Run:**
```bash
go run versions/read.go
```

**Try:** "Read fizzbuzz.js"

### 3. File Explorer (`versions/list_files.go`)
Claude can list files in directories.

**Run:**
```bash
go run versions/list_files.go
```

**Try:** "List all files in this folder" or "What's in fizzbuzz.js?"

### 4. Command Runner (`versions/bash_tool.go`)
Claude can run safe terminal commands.

**Run:**
```bash
go run versions/bash_tool.go
```

**Try:** "Run git status" or "List all .go files using bash"

### 5. File Editor (`versions/edit_tool.go`)
Claude can modify code, create files, and make changes.

**Run:**
```bash
go run versions/edit_tool.go
```

**Try:** "Create a Python hello world script" or "Add a comment to the top of fizzbuzz.js"

### 6. Code Search (`versions/code_search_tool.go`)
Uses ripgrep for pattern search.

**Run:**
```bash
go run versions/code_search_tool.go
```

**Try:** "Find all function definitions in Go files" or "Search for TODO comments"

## 📁 Sample Files

The workshop includes sample files to test with:
- `sample-files/fizzbuzz.js` - JavaScript FizzBuzz implementation
- `sample-files/riddle.txt` - A fun text file to explore
- `sample-files/AGENT.md` - Project environment information

## 🔧 Troubleshooting

- **API key issues**: Check setup and ensure your AIMLAPI account is verified
- **Go errors**: Run `go mod tidy`, ensure Go 1.24.2 or later
- **Tool errors**: Use `--verbose` for logs, check file paths and permissions
- **Environment issues**: Use `devenv shell` to avoid config problems
- **Model availability**: Check AIMLAPI docs for exact model names and free tier limits

## 🛠️ How Tools Work (Under the Hood)

The tools are integrated using the tool calling features in the AIMLAPI (via OpenAI-compatible API), where the model can request tools in responses, and the agent loops to execute them. The code handles this using the OpenAI Go SDK with AIMLAPI's base URL.

## 📖 Additional Resources

- [AIMLAPI Documentation](https://aimlapi.com/docs)
- [OpenAI Go SDK](https://github.com/openai/openai-go)
- [Claude Models](https://docs.anthropic.com/claude/docs/models-overview)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This workshop is open source and available under the MIT License.
