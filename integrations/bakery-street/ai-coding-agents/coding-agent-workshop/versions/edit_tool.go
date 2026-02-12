package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io/fs"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

const (
	// AIMLAPI base URL and model
	baseURL = "https://api.aimlapi.com/v1"
	model   = "anthropic/claude-3-5-sonnet-20240620"
)

// Tool call response structure
type ToolCallArguments struct {
	DirectoryPath string `json:"directory_path"`
	Recursive     bool   `json:"recursive,omitempty"`
	Command       string `json:"command"`
	Timeout       int    `json:"timeout,omitempty"`
	FilePath      string `json:"file_path"`
	Content       string `json:"content"`
	Operation     string `json:"operation"`
}

func main() {
	// Get API key from environment
	apiKey := os.Getenv("AIMLAPI_API_KEY")
	if apiKey == "" {
		log.Fatal("Please set AIMLAPI_API_KEY environment variable")
	}

	// Create OpenAI client with AIMLAPI configuration
	client := openai.NewClient(
		option.WithAPIKey(apiKey),
		option.WithBaseURL(baseURL),
	)

	// Check for verbose flag
	verbose := len(os.Args) > 1 && os.Args[1] == "--verbose"

	fmt.Println("🤖 Coding Agent Workshop - File Editor")
	fmt.Println("======================================")
	fmt.Println("Claude can now read files, list directories, run commands, AND edit files!")
	fmt.Println("Try: 'Create a Python hello world script' or 'Add a comment to the top of fizzbuzz.js'")
	fmt.Println("Type 'quit' or 'exit' to stop the conversation")
	fmt.Println()

	// Create a scanner for user input
	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("You: ")
		if !scanner.Scan() {
			break
		}

		userInput := strings.TrimSpace(scanner.Text())
		if userInput == "" {
			continue
		}

		// Check for exit commands
		if userInput == "quit" || userInput == "exit" {
			fmt.Println("Goodbye! 👋")
			break
		}

		// Send message to Claude with all capabilities including file editing
		response, err := sendMessageWithTools(client, userInput, verbose)
		if err != nil {
			fmt.Printf("❌ Error: %v\n", err)
			continue
		}

		fmt.Printf("Claude: %s\n\n", response)
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Error reading input: %v", err)
	}
}

func sendMessageWithTools(client *openai.Client, message string, verbose bool) (string, error) {
	if verbose {
		fmt.Printf("🔍 Sending message to Claude: %s\n", message)
	}

	// Create chat completion request with tools
	req := openai.ChatCompletionRequest{
		Model: model,
		Messages: []openai.ChatCompletionMessage{
			{
				Role:    openai.ChatCompletionMessageRoleUser,
				Content: message,
			},
		},
		Tools: []openai.Tool{
			{
				Type: "function",
				Function: openai.Function{
					Name:        "read_file",
					Description: "Read the contents of a file from the filesystem",
					Parameters: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"file_path": map[string]interface{}{
								"type":        "string",
								"description": "The path to the file to read",
							},
						},
						"required": []string{"file_path"},
					},
				},
			},
			{
				Type: "function",
				Function: openai.Function{
					Name:        "list_files",
					Description: "List files and directories in a given directory path",
					Parameters: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"directory_path": map[string]interface{}{
								"type":        "string",
								"description": "The path to the directory to list",
							},
							"recursive": map[string]interface{}{
								"type":        "boolean",
								"description": "Whether to list files recursively (default: false)",
							},
						},
						"required": []string{"directory_path"},
					},
				},
			},
			{
				Type: "function",
				Function: openai.Function{
					Name:        "run_command",
					Description: "Execute a shell command safely. Use for file operations, git commands, and other safe operations. Avoid dangerous commands like rm, sudo, etc.",
					Parameters: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"command": map[string]interface{}{
								"type":        "string",
								"description": "The shell command to execute",
							},
							"timeout": map[string]interface{}{
								"type":        "integer",
								"description": "Timeout in seconds (default: 30)",
							},
						},
						"required": []string{"command"},
					},
				},
			},
			{
				Type: "function",
				Function: openai.Function{
					Name:        "edit_file",
					Description: "Create, modify, or delete files. Use 'create' to create new files, 'write' to overwrite existing files, 'append' to add content to the end, or 'delete' to remove files.",
					Parameters: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"file_path": map[string]interface{}{
								"type":        "string",
								"description": "The path to the file to edit",
							},
							"operation": map[string]interface{}{
								"type":        "string",
								"enum":        []string{"create", "write", "append", "delete"},
								"description": "The operation to perform: create (new file), write (overwrite), append (add to end), delete (remove file)",
							},
							"content": map[string]interface{}{
								"type":        "string",
								"description": "The content to write to the file (not needed for delete operation)",
							},
						},
						"required": []string{"file_path", "operation"},
					},
				},
			},
		},
		MaxTokens:   2000,
		Temperature: 0.7,
	}

	// Send request to AIMLAPI
	resp, err := client.Chat.Completions.Create(context.Background(), req)
	if err != nil {
		return "", fmt.Errorf("failed to get completion: %w", err)
	}

	if len(resp.Choices) == 0 {
		return "", fmt.Errorf("no response from Claude")
	}

	choice := resp.Choices[0]
	
	// Check if Claude wants to use a tool
	if len(choice.Message.ToolCalls) > 0 {
		if verbose {
			fmt.Printf("🔧 Claude wants to use tools: %d tool calls\n", len(choice.Message.ToolCalls))
		}

		// Process tool calls
		var toolResults []openai.ChatCompletionMessage
		for _, toolCall := range choice.Message.ToolCalls {
			switch toolCall.Function.Name {
			case "read_file":
				// Parse arguments
				var args struct {
					FilePath string `json:"file_path"`
				}
				if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &args); err != nil {
					return "", fmt.Errorf("failed to parse tool arguments: %w", err)
				}

				if verbose {
					fmt.Printf("📖 Reading file: %s\n", args.FilePath)
				}

				// Read the file
				content, err := readFile(args.FilePath)
				if err != nil {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    fmt.Sprintf("Error reading file: %v", err),
						ToolCallID: toolCall.ID,
					})
				} else {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    content,
						ToolCallID: toolCall.ID,
					})
				}

			case "list_files":
				// Parse arguments
				var args ToolCallArguments
				if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &args); err != nil {
					return "", fmt.Errorf("failed to parse tool arguments: %w", err)
				}

				if verbose {
					fmt.Printf("📁 Listing files in: %s (recursive: %v)\n", args.DirectoryPath, args.Recursive)
				}

				// List files
				content, err := listFiles(args.DirectoryPath, args.Recursive)
				if err != nil {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    fmt.Sprintf("Error listing files: %v", err),
						ToolCallID: toolCall.ID,
					})
				} else {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    content,
						ToolCallID: toolCall.ID,
					})
				}

			case "run_command":
				// Parse arguments
				var args ToolCallArguments
				if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &args); err != nil {
					return "", fmt.Errorf("failed to parse tool arguments: %w", err)
				}

				if args.Timeout == 0 {
					args.Timeout = 30 // Default timeout
				}

				if verbose {
					fmt.Printf("⚡ Running command: %s (timeout: %ds)\n", args.Command, args.Timeout)
				}

				// Run the command
				output, err := runCommand(args.Command, args.Timeout)
				if err != nil {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    fmt.Sprintf("Command failed: %v", err),
						ToolCallID: toolCall.ID,
					})
				} else {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    output,
						ToolCallID: toolCall.ID,
					})
				}

			case "edit_file":
				// Parse arguments
				var args ToolCallArguments
				if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &args); err != nil {
					return "", fmt.Errorf("failed to parse tool arguments: %w", err)
				}

				if verbose {
					fmt.Printf("✏️ Editing file: %s (operation: %s)\n", args.FilePath, args.Operation)
				}

				// Edit the file
				result, err := editFile(args.FilePath, args.Operation, args.Content)
				if err != nil {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    fmt.Sprintf("Error editing file: %v", err),
						ToolCallID: toolCall.ID,
					})
				} else {
					toolResults = append(toolResults, openai.ChatCompletionMessage{
						Role:       openai.ChatCompletionMessageRoleTool,
						Content:    result,
						ToolCallID: toolCall.ID,
					})
				}
			}
		}

		// Send tool results back to Claude
		messages := []openai.ChatCompletionMessage{
			{
				Role:    openai.ChatCompletionMessageRoleUser,
				Content: message,
			},
			{
				Role:       openai.ChatCompletionMessageRoleAssistant,
				Content:    choice.Message.Content,
				ToolCalls:  choice.Message.ToolCalls,
			},
		}
		messages = append(messages, toolResults...)

		// Get final response
		finalReq := openai.ChatCompletionRequest{
			Model:       model,
			Messages:    messages,
			MaxTokens:   2000,
			Temperature: 0.7,
		}

		finalResp, err := client.Chat.Completions.Create(context.Background(), finalReq)
		if err != nil {
			return "", fmt.Errorf("failed to get final completion: %w", err)
		}

		if len(finalResp.Choices) == 0 {
			return "", fmt.Errorf("no final response from Claude")
		}

		return finalResp.Choices[0].Message.Content, nil
	}

	// No tool calls, return direct response
	return choice.Message.Content, nil
}

func readFile(filePath string) (string, error) {
	// Handle relative paths by looking in sample-files directory
	if !strings.HasPrefix(filePath, "/") && !strings.Contains(filePath, "/") {
		filePath = "sample-files/" + filePath
	}

	content, err := os.ReadFile(filePath)
	if err != nil {
		return "", fmt.Errorf("failed to read file %s: %w", filePath, err)
	}

	return string(content), nil
}

func listFiles(directoryPath string, recursive bool) (string, error) {
	// Handle relative paths
	if !strings.HasPrefix(directoryPath, "/") {
		directoryPath = "./" + directoryPath
	}

	var result strings.Builder
	result.WriteString(fmt.Sprintf("Contents of directory: %s\n", directoryPath))
	result.WriteString(strings.Repeat("=", 50) + "\n")

	if recursive {
		err := filepath.WalkDir(directoryPath, func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return err
			}
			
			relPath, _ := filepath.Rel(directoryPath, path)
			if relPath == "." {
				return nil // Skip the root directory itself
			}
			
			if d.IsDir() {
				result.WriteString(fmt.Sprintf("📁 %s/\n", relPath))
			} else {
				info, _ := d.Info()
				result.WriteString(fmt.Sprintf("📄 %s (%d bytes)\n", relPath, info.Size()))
			}
			return nil
		})
		
		if err != nil {
			return "", fmt.Errorf("failed to walk directory %s: %w", directoryPath, err)
		}
	} else {
		entries, err := os.ReadDir(directoryPath)
		if err != nil {
			return "", fmt.Errorf("failed to read directory %s: %w", directoryPath, err)
		}

		for _, entry := range entries {
			if entry.IsDir() {
				result.WriteString(fmt.Sprintf("📁 %s/\n", entry.Name()))
			} else {
				info, _ := entry.Info()
				result.WriteString(fmt.Sprintf("📄 %s (%d bytes)\n", entry.Name(), info.Size()))
			}
		}
	}

	return result.String(), nil
}

func runCommand(command string, timeoutSeconds int) (string, error) {
	// Basic safety checks
	dangerousCommands := []string{"rm", "sudo", "su", "passwd", "chmod", "chown", "kill", "killall", "pkill", "shutdown", "reboot", "halt", "poweroff"}
	commandLower := strings.ToLower(command)
	
	for _, dangerous := range dangerousCommands {
		if strings.Contains(commandLower, dangerous) {
			return "", fmt.Errorf("command contains potentially dangerous operation: %s", dangerous)
		}
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeoutSeconds)*time.Second)
	defer cancel()

	// Parse command into parts
	parts := strings.Fields(command)
	if len(parts) == 0 {
		return "", fmt.Errorf("empty command")
	}

	// Create command
	cmd := exec.CommandContext(ctx, parts[0], parts[1:]...)
	
	// Capture both stdout and stderr
	output, err := cmd.CombinedOutput()
	
	if ctx.Err() == context.DeadlineExceeded {
		return "", fmt.Errorf("command timed out after %d seconds", timeoutSeconds)
	}
	
	if err != nil {
		return string(output), fmt.Errorf("command failed: %w", err)
	}

	return string(output), nil
}

func editFile(filePath, operation, content string) (string, error) {
	// Handle relative paths by looking in sample-files directory for new files
	if !strings.HasPrefix(filePath, "/") && !strings.Contains(filePath, "/") {
		filePath = "sample-files/" + filePath
	}

	switch operation {
	case "create":
		// Check if file already exists
		if _, err := os.Stat(filePath); err == nil {
			return "", fmt.Errorf("file %s already exists, use 'write' to overwrite", filePath)
		}
		
		// Create the file
		err := os.WriteFile(filePath, []byte(content), 0644)
		if err != nil {
			return "", fmt.Errorf("failed to create file %s: %w", filePath, err)
		}
		return fmt.Sprintf("Successfully created file: %s (%d bytes)", filePath, len(content)), nil

	case "write":
		// Overwrite the file
		err := os.WriteFile(filePath, []byte(content), 0644)
		if err != nil {
			return "", fmt.Errorf("failed to write file %s: %w", filePath, err)
		}
		return fmt.Sprintf("Successfully wrote to file: %s (%d bytes)", filePath, len(content)), nil

	case "append":
		// Append to the file
		file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			return "", fmt.Errorf("failed to open file %s for appending: %w", filePath, err)
		}
		defer file.Close()

		_, err = file.WriteString(content)
		if err != nil {
			return "", fmt.Errorf("failed to append to file %s: %w", filePath, err)
		}
		return fmt.Sprintf("Successfully appended to file: %s (%d bytes added)", filePath, len(content)), nil

	case "delete":
		// Delete the file
		err := os.Remove(filePath)
		if err != nil {
			return "", fmt.Errorf("failed to delete file %s: %w", filePath, err)
		}
		return fmt.Sprintf("Successfully deleted file: %s", filePath), nil

	default:
		return "", fmt.Errorf("unknown operation: %s (supported: create, write, append, delete)", operation)
	}
}
