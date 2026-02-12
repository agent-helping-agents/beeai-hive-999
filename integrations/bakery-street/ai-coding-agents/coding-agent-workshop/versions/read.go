package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
)

const (
	// AIMLAPI base URL and model
	baseURL = "https://api.aimlapi.com/v1"
	model   = "anthropic/claude-3-5-sonnet-20240620"
)

// Tool definitions for Claude
type Tool struct {
	Type     string                 `json:"type"`
	Function ToolFunction           `json:"function"`
}

type ToolFunction struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	Parameters  map[string]interface{} `json:"parameters"`
}

// Tool call response structure
type ToolCall struct {
	ID       string                 `json:"id"`
	Type     string                 `json:"type"`
	Function ToolCallFunction       `json:"function"`
}

type ToolCallFunction struct {
	Name      string `json:"name"`
	Arguments string `json:"arguments"`
}

type ToolCallArguments struct {
	FilePath string `json:"file_path"`
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

	fmt.Println("🤖 Coding Agent Workshop - File Reader")
	fmt.Println("======================================")
	fmt.Println("Claude can now read files! Try: 'Read fizzbuzz.js'")
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

		// Send message to Claude with file reading capability
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

	// Define the read_file tool
	readFileTool := Tool{
		Type: "function",
		Function: ToolFunction{
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
			if toolCall.Function.Name == "read_file" {
				// Parse arguments
				var args ToolCallArguments
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

	file, err := os.Open(filePath)
	if err != nil {
		return "", fmt.Errorf("failed to open file %s: %w", filePath, err)
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return "", fmt.Errorf("failed to read file %s: %w", filePath, err)
	}

	return string(content), nil
}
