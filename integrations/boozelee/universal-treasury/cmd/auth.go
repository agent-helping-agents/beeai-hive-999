package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"github.com/universal-treasury/cli/pkg/providers/wise"
)

var (
	authCode string
)

var authCmd = &cobra.Command{
	Use:   "auth",
	Short: "Complete OAuth2 authentication with authorization code",
	Long: `Complete the OAuth2 flow by exchanging the authorization code for an access token.
This command saves the API key to your configuration file.`,
	Run: func(cmd *cobra.Command, args []string) {
		if authCode == "" {
			fmt.Println("❌ Error: Authorization code is required")
			fmt.Println("Usage: treasury auth --code YOUR_AUTHORIZATION_CODE")
			return
		}
		
		// Get client credentials from environment
		clientID := os.Getenv("WISE_CLIENT_ID")
		clientSecret := os.Getenv("WISE_CLIENT_SECRET")
		
		if clientID == "" || clientSecret == "" {
			fmt.Println("❌ Error: WISE_CLIENT_ID and WISE_CLIENT_SECRET must be set")
			fmt.Println("Set them as environment variables:")
			fmt.Println("  export WISE_CLIENT_ID=your_client_id")
			fmt.Println("  export WISE_CLIENT_SECRET=your_client_secret")
			return
		}
		
		fmt.Println("🔐 Completing authentication...")
		fmt.Printf("Exchanging code: %s...\n", authCode)
		
		// Create Wise client
		wiseClient := wise.NewClientWithCredentials("", clientID, clientSecret, true)
		
		// Exchange code for token (real API call)
		tokenResp, err := wiseClient.ExchangeCodeForToken(authCode)
		if err != nil {
			fmt.Printf("❌ Error exchanging code for token: %v\n", err)
			fmt.Println("This might be because:")
			fmt.Println("  - Invalid authorization code")
			fmt.Println("  - Incorrect client ID or secret")
			fmt.Println("  - Network connectivity issues")
			fmt.Println("  - Wise API rate limiting")
			return
		}
		
		simulatedToken := tokenResp.AccessToken
		
		// Save to config
		viper.Set("wise.api_key", simulatedToken)
		
		// Save config file
		home, err := os.UserHomeDir()
		if err != nil {
			fmt.Printf("❌ Error saving config: %v\n", err)
			return
		}
		
		configPath := home + "/.treasury.yaml"
		if err := viper.WriteConfigAs(configPath); err != nil {
			fmt.Printf("❌ Error writing config: %v\n", err)
			return
		}
		
		fmt.Println("✅ Authentication complete!")
		fmt.Printf("API key saved to: %s\n", configPath)
		fmt.Println("You can now use other commands:")
		fmt.Println("  treasury profile      # Get your Wise profile")
		fmt.Println("  treasury accounts     # List your accounts")
		fmt.Println("  treasury balance      # Check account balances")
	},
}

func init() {
	rootCmd.AddCommand(authCmd)
	authCmd.Flags().StringVar(&authCode, "code", "", "Authorization code from OAuth2 redirect")
	authCmd.MarkFlagRequired("code")
}