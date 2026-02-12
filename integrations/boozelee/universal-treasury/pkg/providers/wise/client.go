package wise

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

const (
	SandboxBaseURL   = "https://api.sandbox.transferwise.tech"
	ProductionBaseURL = "https://api.transferwise.com"
	AuthPath         = "/oauth/authorize"
	TokenPath        = "/oauth/token"
)

type TokenResponse struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int    `json:"expires_in"`
	RefreshToken string `json:"refresh_token"`
	Scope        string `json:"scope"`
}

type Client struct {
	APIKey       string
	BaseURL      string
	HTTPClient   *http.Client
	IsSandbox    bool
	ClientID     string
	ClientSecret string
}

type Profile struct {
	ID        int    `json:"id"`
	Type      string `json:"type"`
}

type Account struct {
	ID        string `json:"id"`
	Currency  string `json:"currency"`
	Balance   float64 `json:"balance"`
}

func NewClient(apiKey string) *Client {
	return &Client{
		APIKey:    apiKey,
		BaseURL:   SandboxBaseURL,
		IsSandbox: true,
		HTTPClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func NewClientWithCredentials(apiKey, clientID, clientSecret string, isSandbox bool) *Client {
	baseURL := SandboxBaseURL
	if !isSandbox {
		baseURL = ProductionBaseURL
	}
	
	return &Client{
		APIKey:       apiKey,
		BaseURL:      baseURL,
		IsSandbox:    isSandbox,
		ClientID:     clientID,
		ClientSecret: clientSecret,
		HTTPClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func (c *Client) GetAuthURL() string {
	return c.BaseURL + AuthPath + "?client_id=" + c.ClientID + "&redirect_uri=" + url.QueryEscape("http://localhost:8080/callback") + "&response_type=code"
}

func (c *Client) ExchangeCodeForToken(authCode string) (*TokenResponse, error) {
	tokenURL := c.BaseURL + TokenPath
	
	data := url.Values{}
	data.Set("grant_type", "authorization_code")
	data.Set("code", authCode)
	data.Set("redirect_uri", "http://localhost:8080/callback")
	
	req, err := http.NewRequest("POST", tokenURL, strings.NewReader(data.Encode()))
	if err != nil {
		return nil, err
	}
	
	req.SetBasicAuth(c.ClientID, c.ClientSecret)
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	
	if resp.StatusCode >= 400 {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("token exchange failed: %s - %s", resp.Status, string(body))
	}
	
	var tokenResp TokenResponse
	if err := json.NewDecoder(resp.Body).Decode(&tokenResp); err != nil {
		return nil, err
	}
	
	return &tokenResp, nil
}

func (c *Client) doRequest(method, endpoint string, body interface{}) ([]byte, error) {
	url := c.BaseURL + endpoint
	
	var req *http.Request
	var err error
	
	if body != nil {
		jsonBody, _ := json.Marshal(body)
		req, err = http.NewRequest(method, url, bytes.NewBuffer(jsonBody))
	} else {
		req, err = http.NewRequest(method, url, nil)
	}
	
	if err != nil {
		return nil, err
	}
	
	req.Header.Set("Authorization", "Bearer "+c.APIKey)
	req.Header.Set("Content-Type", "application/json")
	
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	
	if resp.StatusCode >= 400 {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API error: %s - %s", resp.Status, string(body))
	}
	
	return io.ReadAll(resp.Body)
}

func (c *Client) GetProfile() (*Profile, error) {
	// For demo purposes, return a mock profile
	// In production, this would call the real API:
	// body, err := c.doRequest("GET", "/v3/profiles", nil)
	
	// Mock response for testing
	mockProfile := &Profile{
		ID:   12345678,
		Type: "personal",
	}
	
	return mockProfile, nil
}

func (c *Client) GetAccounts() ([]Account, error) {
	// For demo purposes, return mock accounts
	// In production, this would call the real API:
	// body, err := c.doRequest("GET", "/v4/accounts", nil)
	
	// Mock response for testing
	mockAccounts := []Account{
		{
			ID:       "12345678",
			Currency: "EUR",
			Balance:  1500.75,
		},
		{
			ID:       "87654321",
			Currency: "USD",
			Balance:  2500.50,
		},
	}
	
	return mockAccounts, nil
}



func GetAPIKeyFromEnv() string {
	return os.Getenv("WISE_API_KEY")
}