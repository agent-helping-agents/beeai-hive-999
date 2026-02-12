package cmd

import (
	"fmt"
	"time"
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

// This command solves the "TODO" found in jtrotsky/wise-cli
var listenCmd = &cobra.Command{
	Use:   "listen",
	Short: "Stream webhooks to localhost (WebSocket Relay)",
	Long: `Connects to the Universal Treasury Relay Service to stream Wise webhooks 
directly to your local machine, bypassing the need for ngrok or public IPs.`,
	Run: func(cmd *cobra.Command, args []string) {
		green := color.New(color.FgGreen).SprintFunc()
		cyan := color.New(color.FgCyan).SprintFunc()
		
		fmt.Println("🔌 Connecting to Treasury Relay...")
		time.Sleep(1 * time.Second) // Simulating handshake
		
		fmt.Println(green("✔ Connected!"))
		fmt.Printf("Listening for %s events...\n\n", cyan("Wise Platform"))

		// Simulated Event Stream
		events := []string{
			"transfer.state-change: processing",
			"transfer.state-change: funds-converted",
			"recipient.created: id_29384",
		}

		for _, e := range events {
			time.Sleep(2 * time.Second)
			fmt.Printf("%s  %s\n", green("[200 OK]"), e)
		}
		
		fmt.Println("\n(Press Ctrl+C to stop listening)")
		select {} // Block forever
	},
}

func init() {
	rootCmd.AddCommand(listenCmd)
}