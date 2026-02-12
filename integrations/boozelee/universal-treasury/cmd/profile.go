package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"github.com/universal-treasury/cli/pkg/providers/wise"
)

var profileCmd = &cobra.Command{
	Use:   "profile",
	Short: "Get your Wise profile information",
	Long: `Retrieve your Wise profile information including account details and personal information.
Requires a valid API key in your configuration.`,
	Run: func(cmd *cobra.Command, args []string) {
		// Get API key from config
		apiKey := viper.GetString("wise.api_key")
		if apiKey == "" {
			apiKey = wise.GetAPIKeyFromEnv()
		}
		
		if apiKey == "" {
			fmt.Println("❌ Error: No Wise API key found")
			fmt.Println("Please authenticate first:")
			fmt.Println("  treasury login")
			fmt.Println("  treasury auth --code YOUR_CODE")
			return
		}
		
		fmt.Println("📋 Fetching your Wise profile...")
		
		// Create Wise client
		client := wise.NewClient(apiKey)
		
		// Get profile (simulated for now)
		profile, err := client.GetProfile()
		if err != nil {
			fmt.Printf("❌ Error fetching profile: %v\n", err)
			return
		}
		
		// Get accounts
		accounts, err := client.GetAccounts()
		if err != nil {
			fmt.Printf("❌ Error fetching accounts: %v\n", err)
			return
		}
		
		fmt.Println("✅ Profile Information:")
		fmt.Printf("  Profile ID: %d\n", profile.ID)
		fmt.Printf("  Profile Type: %s\n", profile.Type)
		
		fmt.Println("\n💰 Your Accounts:")
		for i, account := range accounts {
			fmt.Printf("  %d. Account ID: %s\n", i+1, account.ID)
			fmt.Printf("     Currency: %s\n", account.Currency)
			fmt.Printf("     Balance: %.2f %s\n", account.Balance, account.Currency)
			fmt.Println()
		}
		
		fmt.Println("📊 Summary:")
		fmt.Printf("  Total Accounts: %d\n", len(accounts))
		
		// Calculate total balance across all accounts
		var totalBalance float64
		for _, account := range accounts {
			totalBalance += account.Balance
		}
		fmt.Printf("  Estimated Total Balance: %.2f (across all currencies)\n", totalBalance)
	},
}

func init() {
	rootCmd.AddCommand(profileCmd)
}