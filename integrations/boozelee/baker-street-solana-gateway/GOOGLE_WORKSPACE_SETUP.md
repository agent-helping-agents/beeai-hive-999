# Google Workspace Extension: Account Configuration Guide

To authorize the Google Workspace extension for your accounts, follow these steps:

1. **Open your terminal.**
2. **Run the configuration command:**
   ```bash
   gemini extensions config google-workspace
   ```
3. **Follow the OAuth flow:** 
   - A browser window will open automatically.
   - Log in with `kiliaanv2@gmail.com`.
   - Grant the requested permissions.
4. **Repeat for the second account:**
   - Run the same command again: `gemini extensions config google-workspace`
   - Log in with `iamthatiamresearch@gmail.com`.

**Note:** If you get a message saying "no settings to configure," ensure you have the `experimental.extensionConfig` setting enabled (which we did earlier) and try running a drive/gmail tool directly (e.g., `gemini -p "list drive" -e google-workspace`) to trigger the authorization prompt.
