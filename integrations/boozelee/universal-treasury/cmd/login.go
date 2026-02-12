package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
	"github.com/universal-treasury/cli/pkg/providers/wise"
)

var (
	clientID    string
	redirectURI string
)

var loginCmd = &cobra.Command{
	Use:   "login",
	Short: "Authenticate via OAuth2 with Wise",
	Long: `Authenticate with Wise API using OAuth2 flow.
Requires WISE_CLIENT_ID and WISE_REDIRECT_URI environment variables.
After authentication, the API key will be saved to ~/.treasury.yaml`,
	Run: func(cmd *cobra.Command, args []string) {
		// Get client ID and redirect URI from flags or environment
		if clientID == "" {
			clientID = os.Getenv("WISE_CLIENT_ID")
		}
		if redirectURI == "" {
			redirectURI = os.Getenv("WISE_REDIRECT_URI")
		}
		
		if clientID == "" || redirectURI == "" {
			fmt.Println("❌ Error: WISE_CLIENT_ID and WISE_REDIRECT_URI must be set")
			fmt.Println("Export them as environment variables or use flags:")
			fmt.Println("  export WISE_CLIENT_ID=your_client_id")
			fmt.Println("  export WISE_REDIRECT_URI=your_redirect_uri")
			fmt.Println("Or use flags:")
			fmt.Println("  treasury login --client-id YOUR_ID --redirect-uri YOUR_URI")
			return
		}
		
		// Create Wise client
		wiseClient := wise.NewClientWithCredentials("", clientID, "", true)
		authURL := wiseClient.GetAuthURL()
		
		fmt.Println("🔐 Wise Authentication")
		fmt.Println("==================================================")
		fmt.Printf("1. Open this URL in your browser:\n   %s\n\n", authURL)
		fmt.Println("2. Authorize the application")
		fmt.Println("3. You will be redirected to your redirect URI with a code")
		fmt.Println("4. Copy the code and use it with the 'auth' command:")
		fmt.Printf("   treasury auth --code YOUR_CODE\n")
		fmt.Println("==================================================")
	},
}

func init() {
	rootCmd.AddCommand(loginCmd)
	loginCmd.Flags().StringVar(&clientID, "client-id", "", "Wise client ID")
	loginCmd.Flags().StringVar(&redirectURI, "redirect-uri", "", "Wise redirect URI")
}