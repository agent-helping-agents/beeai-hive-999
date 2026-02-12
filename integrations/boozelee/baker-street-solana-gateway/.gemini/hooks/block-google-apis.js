#!/usr/bin/env node

const fs = require('fs');

/**
 * BeforeTool Hook: Blocks tools that rely on centralized Google APIs
 * to maintain the decentralized nature of the Solana project.
 */

try {
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const toolName = input.tool_name;

  const forbiddenTools = [
    'google_web_search',
    'gmail.search',
    'gmail.get',
    'gmail.send',
    'gmail.createDraft',
    'drive.list',
    'drive.get',
    'drive.create'
  ];

  if (forbiddenTools.includes(toolName)) {
    console.log(JSON.stringify({
      decision: 'deny',
      reason: `Tool '${toolName}' is blocked to maintain project decentralization. Use decentralized alternatives or local tools instead.`,
      systemMessage: `🚨 Decentralization Guard: Blocked centralized tool '${toolName}'.`
    }));
  } else {
    console.log(JSON.stringify({ decision: 'allow' }));
  }
} catch (err) {
  // If parsing fails, allow by default but log to stderr
  process.stderr.write(`Hook Error: ${err.message}
`);
  console.log(JSON.stringify({ decision: 'allow' }));
}
