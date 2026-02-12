package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	cfgFile string
	Provider string
)

var rootCmd = &cobra.Command{
	Use:   "treasury",
	Short: "Universal Financial Operations CLI",
	Long: `The Universal Treasury CLI bridges the gap between banking APIs and developer experience.
Current Provider Focus: Wise (Beta)
Competitor Analysis: Beats standard tools by offering local webhook tunneling.`,
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.treasury.yaml)")
	rootCmd.PersistentFlags().StringVarP(&Provider, "provider", "p", "wise", "Financial provider (wise, stripe, revolut)")
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, err := os.UserHomeDir()
		if err != nil {
			cobra.CheckErr(err)
		}
		viper.AddConfigPath(home)
		viper.SetConfigType("yaml")
		viper.SetConfigName(".treasury")
	}
	viper.AutomaticEnv()
	viper.ReadInConfig()
}