# Tool Development Guide

This guide explains how to add new tools to the coding agent and understand the existing tool implementations.

## Tool Development Process

### 1. Define Tool Schema

First, define your tool using the OpenAI function calling format:

```go
{
    Type: "function",
    Function: openai.Function{
        Name:        "your_tool_name",
        Description: "Clear description of what the tool does",
        Parameters: map[string]interface{}{
            "type": "object",
            "properties": map[string]interface{}{
                "param1": map[string]interface{}{
                    "type":        "string",
                    "description": "Description of parameter 1",
                },
                "param2": map[string]interface{}{
                    "type":        "integer",
                    "description": "Description of parameter 2",
                },
            },
            "required": []string{"param1"},
        },
    },
}
```

### 2. Add Tool to Request

Include your tool in the `Tools` array when making requests to Claude:

```go
req := openai.ChatCompletionRequest{
    Model: model,
    Messages: messages,
    Tools: []openai.Tool{
        // ... existing tools
        yourNewTool,
    },
    // ... other options
}
```

### 3. Handle Tool Execution

Add a case in the tool execution switch statement:

```go
case "your_tool_name":
    // Parse arguments
    var args YourToolArgs
    if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &args); err != nil {
        return "", fmt.Errorf("failed to parse tool arguments: %w", err)
    }
    
    // Execute tool logic
    result, err := yourToolFunction(args.Param1, args.Param2)
    if err != nil {
        toolResults = append(toolResults, openai.ChatCompletionMessage{
            Role:       openai.ChatCompletionMessageRoleTool,
            Content:    fmt.Sprintf("Error: %v", err),
            ToolCallID: toolCall.ID,
        })
    } else {
        toolResults = append(toolResults, openai.ChatCompletionMessage{
            Role:       openai.ChatCompletionMessageRoleTool,
            Content:    result,
            ToolCallID: toolCall.ID,
        })
    }
```

### 4. Implement Tool Logic

Create the actual tool implementation:

```go
func yourToolFunction(param1 string, param2 int) (string, error) {
    // Your tool logic here
    // Return formatted string result or error
}
```

## Existing Tools Reference

### 1. read_file

**Purpose**: Read contents of a file from the filesystem

**Parameters**:
- `file_path` (string, required): Path to the file to read

**Example Usage**:
```
"Read the contents of fizzbuzz.js"
```

**Implementation Notes**:
- Handles relative paths by looking in `sample-files/` directory
- Returns file contents as string
- Provides clear error messages for missing files

### 2. list_files

**Purpose**: List files and directories in a given directory

**Parameters**:
- `directory_path` (string, required): Path to directory to list
- `recursive` (boolean, optional): Whether to list recursively

**Example Usage**:
```
"List all files in the current directory"
"What files are in the sample-files folder?"
```

**Implementation Notes**:
- Uses `os.ReadDir` for non-recursive listing
- Uses `filepath.WalkDir` for recursive listing
- Formats output with emojis and file sizes

### 3. run_command

**Purpose**: Execute shell commands safely

**Parameters**:
- `command` (string, required): Shell command to execute
- `timeout` (integer, optional): Timeout in seconds (default: 30)

**Example Usage**:
```
"Run git status"
"List all .go files using find command"
```

**Implementation Notes**:
- Blocks dangerous commands (rm, sudo, etc.)
- Uses context with timeout for command execution
- Captures both stdout and stderr
- Returns command output or error message

### 4. edit_file

**Purpose**: Create, modify, or delete files

**Parameters**:
- `file_path` (string, required): Path to file to edit
- `operation` (string, required): Operation type (create, write, append, delete)
- `content` (string, optional): Content to write (not needed for delete)

**Example Usage**:
```
"Create a new Python script called hello.py"
"Add a comment to the top of fizzbuzz.js"
"Delete the test.txt file"
```

**Implementation Notes**:
- Supports four operations: create, write, append, delete
- Creates new files in `sample-files/` directory by default
- Validates file existence for create operation
- Returns success message with file size information

### 5. search_code

**Purpose**: Search for patterns in code using ripgrep

**Parameters**:
- `pattern` (string, required): Search pattern (supports regex)
- `file_pattern` (string, optional): File pattern to search in (e.g., *.go)
- `case_sensitive` (boolean, optional): Case sensitivity (default: false)

**Example Usage**:
```
"Find all function definitions in Go files"
"Search for TODO comments in JavaScript files"
"Find all imports in Python files"
```

**Implementation Notes**:
- Uses ripgrep if available, falls back to grep
- Supports regex patterns and file type filtering
- Returns formatted search results with line numbers
- Handles case sensitivity options

## Best Practices

### Tool Design
1. **Clear Descriptions**: Write clear, concise tool descriptions
2. **Parameter Validation**: Always validate required parameters
3. **Error Handling**: Provide meaningful error messages
4. **Output Formatting**: Format results for human readability
5. **Safety First**: Implement safety checks for destructive operations

### Error Handling
1. **Graceful Failures**: Tools should fail gracefully without crashing
2. **User-Friendly Messages**: Convert technical errors to user-friendly messages
3. **Logging**: Use verbose logging for debugging
4. **Fallbacks**: Provide fallback mechanisms when possible

### Security
1. **Input Validation**: Validate all inputs before processing
2. **Path Safety**: Sanitize file paths and prevent directory traversal
3. **Command Safety**: Block dangerous commands and operations
4. **Resource Limits**: Implement timeouts and size limits

### Performance
1. **Efficient Operations**: Use appropriate data structures and algorithms
2. **Resource Management**: Clean up resources (files, processes)
3. **Caching**: Consider caching for expensive operations
4. **Streaming**: Use streaming for large data processing

## Testing Your Tools

### Manual Testing
1. Test with various input combinations
2. Test error conditions and edge cases
3. Verify output formatting
4. Test with different file types and sizes

### Example Test Cases
```bash
# Test file reading
"Read fizzbuzz.js"
"Read a non-existent file"

# Test file listing
"List files in current directory"
"List files recursively in sample-files"

# Test command execution
"Run ls -la"
"Run a command that will fail"

# Test file editing
"Create a new test file"
"Append content to an existing file"
"Delete a test file"

# Test code search
"Find all function definitions"
"Search for TODO comments"
"Find imports in specific file types"
```

## Common Pitfalls

1. **Missing Error Handling**: Always handle potential errors
2. **Insecure Operations**: Avoid dangerous commands or file operations
3. **Poor Output Formatting**: Make results readable and informative
4. **Missing Validation**: Validate all inputs and parameters
5. **Resource Leaks**: Clean up files, processes, and other resources
6. **Infinite Loops**: Implement timeouts and cancellation
7. **Path Traversal**: Sanitize file paths to prevent security issues
