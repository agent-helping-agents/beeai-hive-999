# Coding Agent Examples

This document provides practical examples of how to use each version of the coding agent.

## Basic Chat (chat.go)

The simplest version - just conversation with Claude.

### Example Interactions

```
You: Hello! Can you help me understand what this workshop is about?

Claude: Hello! I'd be happy to help you understand this workshop. This is a step-by-step guide to building your own coding agent - essentially an AI assistant that can help with programming tasks, similar to tools like Cursor, Windsurf, or Cline.

The workshop progresses through 6 different versions, each adding new capabilities:
1. Basic Chat (what we're doing now) - simple conversation
2. File Reader - ability to read code files
3. File Explorer - list files in directories
4. Command Runner - execute shell commands
5. File Editor - create and modify files
6. Code Search - search for patterns in code

Each version builds on the previous one, teaching you how to integrate tools with an AI model to create increasingly powerful coding assistants. Would you like to know more about any specific aspect?

You: What programming language is this built in?

Claude: This coding agent workshop is built in Go! Go is an excellent choice for this type of application because:

1. **Concurrency**: Go's goroutines make it easy to handle multiple operations
2. **Performance**: Fast compilation and execution
3. **Simplicity**: Clean, readable code that's easy to understand
4. **Cross-platform**: Works on Windows, macOS, and Linux
5. **Standard library**: Rich built-in libraries for file operations, HTTP requests, etc.

The workshop uses the OpenAI Go SDK to communicate with the AIMLAPI service, which provides access to Claude models. This makes it easy to integrate AI capabilities into your Go applications.

You: quit

Goodbye! 👋
```

## File Reader (read.go)

Adds the ability to read files.

### Example Interactions

```
You: Read fizzbuzz.js

Claude: I'll read the fizzbuzz.js file for you.

// FizzBuzz implementation in JavaScript
// Prints numbers 1-100, but for multiples of 3 prints "Fizz",
// for multiples of 5 prints "Buzz", and for multiples of both prints "FizzBuzz"

function fizzBuzz() {
    for (let i = 1; i <= 100; i++) {
        if (i % 15 === 0) {
            console.log("FizzBuzz");
        } else if (i % 3 === 0) {
            console.log("Fizz");
        } else if (i % 5 === 0) {
            console.log("Buzz");
        } else {
            console.log(i);
        }
    }
}

// Run the function
fizzBuzz();

This is a classic FizzBuzz implementation in JavaScript. It iterates through numbers 1-100 and prints:
- "FizzBuzz" for numbers divisible by both 3 and 5 (15)
- "Fizz" for numbers divisible by 3
- "Buzz" for numbers divisible by 5
- The number itself for all other cases

You: What's in the riddle.txt file?

Claude: I'll read the riddle.txt file for you.

I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?

Answer: An echo.

---

Here's another one:

The more you take, the more you leave behind. What am I?

Answer: Footsteps.

---

And one more:

I'm tall when I'm young, and short when I'm old. What am I?

Answer: A candle.

This file contains three riddles with their answers! They're fun brain teasers that demonstrate the file reading capability.
```

## File Explorer (list_files.go)

Adds directory listing capabilities.

### Example Interactions

```
You: List all files in this folder

Claude: I'll list the files in the current directory for you.

Contents of directory: ./
==================================================
📁 docs/
📁 sample-files/
📁 versions/
📄 go.mod
📄 README.md
📄 setup.sh

This shows the main structure of the coding agent workshop. You can see:
- `docs/` - Documentation files
- `sample-files/` - Test files for the agents
- `versions/` - The different agent implementations
- `go.mod` - Go module file
- `README.md` - Main workshop guide
- `setup.sh` - Setup script

You: What's in the sample-files directory?

Claude: I'll list the contents of the sample-files directory.

Contents of directory: ./sample-files
==================================================
📄 AGENT.md
📄 fizzbuzz.js
📄 riddle.txt

The sample-files directory contains three test files:
- `AGENT.md` - Project environment information
- `fizzbuzz.js` - JavaScript FizzBuzz implementation
- `riddle.txt` - Collection of riddles

These files are used throughout the workshop to test the different agent capabilities.
```

## Command Runner (bash_tool.go)

Adds shell command execution.

### Example Interactions

```
You: Run git status

Claude: I'll run the git status command for you.

On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   README.md
        modified:   go.mod

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        coding-agent-workshop/

no changes added to commit (use "git commit" or "git add .")

You: List all .go files using bash

Claude: I'll use the find command to list all Go files.

./versions/chat.go
./versions/read.go
./versions/list_files.go
./versions/bash_tool.go
./versions/edit_tool.go
./versions/code_search_tool.go

These are all the Go source files in the workshop, located in the versions directory. Each file represents a different stage of the coding agent development.
```

## File Editor (edit_tool.go)

Adds file creation and editing capabilities.

### Example Interactions

```
You: Create a Python hello world script

Claude: I'll create a Python hello world script for you.

Successfully created file: sample-files/hello.py (25 bytes)

The file has been created! Here's what was written:

```python
#!/usr/bin/env python3

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

This is a simple Python hello world script with proper structure and shebang line.

You: Add a comment to the top of fizzbuzz.js

Claude: I'll add a comment to the top of the fizzbuzz.js file.

Successfully appended to file: sample-files/fizzbuzz.js (15 bytes added)

I've added a comment to the beginning of the fizzbuzz.js file. The comment explains that this is a classic programming interview question implementation.

You: Create a simple HTML file

Claude: I'll create a simple HTML file for you.

Successfully created file: sample-files/index.html (156 bytes)

The HTML file has been created! Here's what was written:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coding Agent Workshop</title>
</head>
<body>
    <h1>Welcome to the Coding Agent Workshop!</h1>
    <p>This is a simple HTML file created by the coding agent.</p>
    <p>Try editing it or creating more complex HTML structures!</p>
</body>
</html>
```
```

## Code Search (code_search_tool.go)

Adds pattern search capabilities using ripgrep.

### Example Interactions

```
You: Find all function definitions in Go files

Claude: I'll search for function definitions in Go files.

versions/chat.go:15:func main() {
versions/chat.go:45:func sendMessage(client *openai.Client, message string, verbose bool) (string, error) {
versions/read.go:15:func main() {
versions/read.go:50:func sendMessageWithTools(client *openai.Client, message string, verbose bool) (string, error) {
versions/read.go:200:func readFile(filePath string) (string, error) {
versions/list_files.go:15:func main() {
versions/list_files.go:50:func sendMessageWithTools(client *openai.Client, message string, verbose bool) (string, error) {
versions/list_files.go:200:func readFile(filePath string) (string, error) {
versions/list_files.go:220:func listFiles(directoryPath string, recursive bool) (string, error) {
versions/bash_tool.go:15:func main() {
versions/bash_tool.go:50:func sendMessageWithTools(client *openai.Client, message string, verbose bool) (string, error) {
versions/bash_tool.go:200:func readFile(filePath string) (string, error) {
versions/bash_tool.go:220:func listFiles(directoryPath string, recursive bool) (string, error) {
versions/bash_tool.go:280:func runCommand(command string, timeoutSeconds int) (string, error) {
versions/edit_tool.go:15:func main() {
versions/edit_tool.go:50:func sendMessageWithTools(client *openai.Client, message string, verbose bool) (string, error) {
versions/edit_tool.go:200:func readFile(filePathPath string) (string, error) {
versions/edit_tool.go:220:func listFiles(directoryPath string, recursive bool) (string, error) {
versions/edit_tool.go:280:func runCommand(command string, timeoutSeconds int) (string, error) {
versions/edit_tool.go:320:func editFile(filePath, operation, content string) (string, error) {
versions/code_search_tool.go:15:func main() {
versions/code_search_tool.go:50:func sendMessageWithTools(client *openio.Client, message string, verbose bool) (string, error) {
versions/code_search_tool.go:200:func readFile(filePath string) (string, error) {
versions/code_search_tool.go:220:func listFiles(directoryPath string, recursive bool) (string, error) {
versions/code_search_tool.go:280:func runCommand(command string, timeoutSeconds int) (string, error) {
versions/code_search_tool.go:320:func editFile(filePath, operation, content string) (string, error) {
versions/code_search_tool.go:380:func searchCode(pattern, filePattern string, caseSensitive bool) (string, error) {
versions/code_search_tool.go:420:func searchWithGrep(pattern, filePattern string, caseSensitive bool) (string, error) {

Found 25 function definitions across all Go files! This shows the progression of the workshop, with each version adding new functions for different capabilities.

You: Search for TODO comments

Claude: I'll search for TODO comments in the codebase.

No matches found for the given pattern.

It looks like there are no TODO comments in the current codebase. This is good - it means the code is complete and well-structured!

You: Find all import statements in Go files

Claude: I'll search for import statements in Go files.

versions/chat.go:1:package main
versions/chat.go:3:import (
versions/chat.go:4:	"bufio"
versions/chat.go:5:	"context"
versions/chat.go:6:	"fmt"
versions/chat.go:7:	"log"
versions/chat.go:8:	"os"
versions/chat.go:9:	"strings"
versions/chat.go:10:
versions/chat.go:11:	"github.com/openai/openai-go"
versions/chat.go:12:	"github.com/openai/openai-go/option"
versions/chat.go:13:)
versions/read.go:1:package main
versions/read.go:3:import (
versions/read.go:4:	"bufio"
versions/read.go:5:	"context"
versions/read.go:6:	"encoding/json"
versions/read.go:7:	"fmt"
versions/read.go:8:	"io"
versions/read.go:9:	"log"
versions/read.go:10:	"os"
versions/read.go:11:	"strings"
versions/read.go:12:
versions/read.go:13:	"github.com/openai/openai-go"
versions/read.go:14:	"github.com/openai/openai-go/option"
versions/read.go:15:)
[... more import statements ...]

This shows all the import statements across the Go files. You can see the progression of imports as more functionality is added - starting with basic imports in chat.go and adding more specialized ones like "encoding/json" and "io" in later versions.
```

## Advanced Usage Examples

### Combining Multiple Tools

```
You: Create a new Go file with a simple function, then search for it

Claude: I'll create a new Go file with a simple function and then search for it.

First, let me create the file:

Successfully created file: sample-files/utils.go (89 bytes)

Now let me search for the function I just created:

sample-files/utils.go:1:package main
sample-files/utils.go:3:import "fmt"
sample-files/utils.go:5:func Add(a, b int) int {
sample-files/utils.go:6:    return a + b
sample-files/utils.go:7:}
sample-files/utils.go:9:func main() {
sample-files/utils.go:10:    result := Add(5, 3)
sample-files/utils.go:11:    fmt.Println("Result:", result)
sample-files/utils.go:12:}

Perfect! I created a simple Go file with an Add function and then successfully found it using the code search tool. This demonstrates how the different tools can work together.
```

### Error Handling Examples

```
You: Read a file that doesn't exist

Claude: I'll try to read a file that doesn't exist.

Error reading file: failed to read file nonexistent.txt: open nonexistent.txt: no such file or directory

As expected, the tool gracefully handles the error and provides a clear message about what went wrong. This is important for user experience and debugging.

You: Run a command that will fail

Claude: I'll run a command that will fail.

Command failed: command failed: exit status 1

The command failed as expected, and the tool provided a clear error message. This demonstrates the robust error handling built into the system.
```

## Tips for Effective Usage

1. **Be Specific**: The more specific your requests, the better the results
2. **Use Context**: Reference files and directories by name when possible
3. **Combine Tools**: Use multiple tools together for complex tasks
4. **Test Edge Cases**: Try commands that might fail to see error handling
5. **Use Verbose Mode**: Add `--verbose` flag for detailed logging
6. **Explore Gradually**: Start with simple commands and build up complexity

## Troubleshooting Common Issues

### API Key Issues
```
You: Hello
❌ Error: Please set AIMLAPI_API_KEY environment variable
```
**Solution**: Set your API key with `export AIMLAPI_API_KEY="your-key"`

### File Not Found
```
You: Read myfile.txt
Error reading file: failed to read file myfile.txt: open myfile.txt: no such file or directory
```
**Solution**: Check the file path or create the file first

### Command Blocked
```
You: Run rm -rf /
Command failed: command contains potentially dangerous operation: rm
```
**Solution**: The system blocks dangerous commands for safety

### No Search Results
```
You: Find nonexistent pattern
No matches found for the given pattern.
```
**Solution**: Try different search terms or check if the pattern exists
