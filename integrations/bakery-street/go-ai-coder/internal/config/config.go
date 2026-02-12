package config

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// Config holds all configuration for the application
type Config struct {
	// AI Configuration
	Model       string  `json:"model"`
	MaxTokens   int     `json:"max_tokens"`
	Temperature float64 `json:"temperature"`
	OllamaURL   string  `json:"ollama_url"`

	// GitHub Configuration
	GitHubToken string `json:"-"` // Never log or expose this

	// Application Configuration
	LearningDir  string `json:"learning_dir"`
	CacheEnabled bool   `json:"cache_enabled"`
	AutoSave     bool   `json:"auto_save"`
	Verbose      bool   `json:"verbose"`

	// Security Configuration
	SessionID string `json:"session_id"`
	DataDir   string `json:"data_dir"`
	LogLevel  string `json:"log_level"`
}

// LoadConfig loads configuration from environment and command line
func LoadConfig() (*Config, error) {
	config := &Config{
		Model:        getEnv("AI_MODEL", "llama3.2:3b"),
		MaxTokens:    getEnvInt("AI_MAX_TOKENS", 2000),
		Temperature:  getEnvFloat("AI_TEMPERATURE", 0.7),
		OllamaURL:    getEnv("OLLAMA_URL", "http://localhost:11434/v1"),
		GitHubToken:  getEnv("GITHUB_TOKEN", ""),
		LearningDir:  getEnv("LEARNING_DIR", "ai_learning"),
		CacheEnabled: getEnvBool("CACHE_ENABLED", true),
		AutoSave:     getEnvBool("AUTO_SAVE", true),
		Verbose:      getEnvBool("VERBOSE", false),
		DataDir:      getDataDir(),
		LogLevel:     getEnv("LOG_LEVEL", "info"),
	}

	// Generate secure session ID
	sessionID, err := generateSessionID()
	if err != nil {
		return nil, fmt.Errorf("failed to generate session ID: %w", err)
	}
	config.SessionID = sessionID

	// Ensure data directory exists
	if err := os.MkdirAll(config.DataDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create data directory: %w", err)
	}

	// Ensure learning directory exists
	if err := os.MkdirAll(config.LearningDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create learning directory: %w", err)
	}

	return config, nil
}

// getDataDir returns the appropriate data directory
func getDataDir() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return ".go-ai-coder"
	}
	return filepath.Join(homeDir, ".go-ai-coder")
}

// generateSessionID creates a secure random session ID
func generateSessionID() (string, error) {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

// Helper functions for environment variables
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvFloat(key string, defaultValue float64) float64 {
	if value := os.Getenv(key); value != "" {
		if floatValue, err := strconv.ParseFloat(value, 64); err == nil {
			return floatValue
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

// MaskToken safely masks sensitive tokens for display
func (c *Config) MaskToken() string {
	if c.GitHubToken == "" {
		return "Not set"
	}
	if len(c.GitHubToken) < 8 {
		return "***"
	}
	return c.GitHubToken[:4] + "***" + c.GitHubToken[len(c.GitHubToken)-4:]
}

// Validate checks if the configuration is valid
func (c *Config) Validate() error {
	if c.Model == "" {
		return fmt.Errorf("model cannot be empty")
	}
	if c.MaxTokens <= 0 {
		return fmt.Errorf("max_tokens must be positive")
	}
	if c.Temperature < 0 || c.Temperature > 1 {
		return fmt.Errorf("temperature must be between 0 and 1")
	}
	if c.OllamaURL == "" {
		return fmt.Errorf("ollama_url cannot be empty")
	}
	return nil
}
