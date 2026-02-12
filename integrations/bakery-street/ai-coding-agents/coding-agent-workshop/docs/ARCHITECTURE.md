# Coding Agent Architecture

## Overview

This document explains the architecture and design patterns used in the coding agent workshop.

## Event Loop Pattern

Each agent follows a consistent event loop pattern:

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

### 1. User Input Processing
- Continuous loop waiting for user input
- Basic input validation and exit command handling
- Input sanitization and trimming

### 2. Claude Communication
- OpenAI-compatible API calls to AIMLAPI
- Tool definition and registration
- Response parsing and tool call detection

### 3. Tool Execution
- Dynamic tool call handling
- Argument parsing and validation
- Tool-specific logic execution
- Result formatting and error handling

### 4. Response Generation
- Tool results integration
- Final response generation
- User-friendly output formatting

## Tool System Design

### Tool Registration
Tools are defined using OpenAI's function calling format:

```go
{
    Type: "function",
    Function: openai.Function{
        Name:        "tool_name",
        Description: "Tool description",
        Parameters: map[string]interface{}{
            "type": "object",
            "properties": map[string]interface{}{
                "param_name": map[string]interface{}{
                    "type":        "string",
                    "description": "Parameter description",
                },
            },
            "required": []string{"param_name"},
        },
    },
}
```

### Tool Execution Flow
1. **Request Parsing**: Extract tool name and arguments from Claude's response
2. **Argument Validation**: Parse JSON arguments and validate required fields
3. **Tool Execution**: Run tool-specific logic with error handling
4. **Result Formatting**: Format results for Claude's consumption
5. **Response Integration**: Send results back to Claude for final response

## Security Considerations

### Command Execution Safety
- Dangerous command filtering (rm, sudo, etc.)
- Timeout enforcement for long-running commands
- Context cancellation for command termination
- Output size limits to prevent memory issues

### File System Safety
- Path validation and sanitization
- Relative path handling with safe defaults
- Permission checks before file operations
- Backup considerations for destructive operations

### API Security
- Environment variable for API key storage
- Request timeout handling
- Error message sanitization
- Rate limiting considerations

## Error Handling Strategy

### Graceful Degradation
- Tool failures don't crash the entire agent
- Fallback mechanisms (e.g., grep when ripgrep unavailable)
- User-friendly error messages
- Verbose logging for debugging

### Error Categories
1. **API Errors**: Network issues, authentication failures
2. **Tool Errors**: File not found, permission denied
3. **Command Errors**: Invalid commands, timeouts
4. **Parsing Errors**: Malformed JSON, missing arguments

## Performance Considerations

### Memory Management
- Streaming responses for large files
- Output size limits
- Garbage collection optimization
- Resource cleanup (file handles, processes)

### Concurrency
- Single-threaded design for simplicity
- Sequential tool execution
- Context-based cancellation
- Timeout management

## Extensibility Patterns

### Adding New Tools
1. Define tool schema in OpenAI function format
2. Add tool to the tools array in requests
3. Implement tool execution logic in switch statement
4. Add argument parsing and validation
5. Implement error handling and result formatting

### Tool Categories
- **File Operations**: read, write, list, search
- **Command Execution**: shell commands, git operations
- **Code Analysis**: pattern matching, syntax highlighting
- **Development Tools**: build, test, deploy operations

## Testing Strategy

### Unit Testing
- Individual tool functions
- Error handling scenarios
- Argument validation
- Output formatting

### Integration Testing
- End-to-end tool execution
- API communication
- Error propagation
- User interaction flows

### Manual Testing
- Interactive testing with sample files
- Edge case validation
- Performance testing
- Security testing

## Future Enhancements

### Advanced Features
- Multi-file operations
- Git integration
- Code analysis and refactoring
- Plugin system for custom tools
- Web interface
- Multi-language support

### Performance Improvements
- Parallel tool execution
- Caching mechanisms
- Streaming responses
- Background processing
- Resource pooling
