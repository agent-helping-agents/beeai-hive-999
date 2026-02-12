package main

import (
	"bufio"
	"context"
	"fmt"
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

func main() {
	// Get API key from environment
	apiKey := os.Getenv("AIMLAPI_API_KEY")
	if apiKey == "" {
		log.Fatal("Please set AIMLAPI_API_KEY environment variable")
	}

	// Create OpenAI client with AIMLAPI configuration
	client := openai.NewClient(apiKey)
	client.BaseURL = baseURL

	// Check for verbose flag
	verbose := len(os.Args) > 1 && os.Args[1] == "--verbose"

	fmt.Println("🤖 Coding Agent Workshop - Basic Chat")
	fmt.Println("=====================================")
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

		// Send message to Claude
		response, err := sendMessage(client, userInput, verbose)
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

func sendMessage(client *openai.Client, message string, verbose bool) (string, error) {
	if verbose {
		fmt.Printf("🔍 Sending message to Claude: %s\n", message)
	}

	// Create chat completion request
	req := openai.ChatCompletionRequest{
		Model: model,
		Messages: []openai.ChatCompletionMessage{
			{
				Role:    openai.ChatCompletionMessageRoleUser,
				Content: message,
			},
		},
		MaxTokens: 1000,
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

	response := resp.Choices[0].Message.Content

	if verbose {
		fmt.Printf("🔍 Received response from Claude: %s\n", response)
	}

	return response, nil
}
