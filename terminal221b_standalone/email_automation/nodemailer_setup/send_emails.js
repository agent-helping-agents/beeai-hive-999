#!/usr/bin/env node

/**
 * Email Assistant - Send bounty partnership emails
 * Uses: Nodemailer (most popular Node.js email library - 16k+ stars)
 * 
 * Setup Instructions:
 * 1. Create .env file with EMAIL_USER and EMAIL_PASSWORD
 * 2. For Gmail: Use app-specific password (16 chars)
 * 3. Run: node send_emails.js
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Email templates
const EMAILS = {
  augment: {
    to: 'collaborate@augment.com',
    subject: 'Terminal 221B x Context Engine MCP - Production Integration',
    template: '01_AUGMENT_EMAIL.txt'
  },
  gemini: {
    to: 'partnerships@google.com',
    subject: 'Deep Research Integration for Autonomous AI Multi-Agent Crypto System',
    template: '02_GEMINI_EMAIL.txt'
  },
  openai: {
    to: 'partnerships@openai.com',
    subject: 'GPT-4 Integration for Multi-Agent Autonomous AI System',
    template: '03_OPENAI_EMAIL.txt'
  }
};

async function sendEmails() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║  📧 Email Assistant - Sending Partnership Emails           ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  // Setup Nodemailer transporter
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASSWORD  // App-specific password
    }
  });

  const results = {};
  let successCount = 0;

  // Send each email
  for (const [key, emailConfig] of Object.entries(EMAILS)) {
    try {
      // Read template
      const templatePath = path.expanduser(`~/emails_ready_to_send/${emailConfig.template}`);
      const body = fs.readFileSync(templatePath, 'utf8');

      // Send email
      const info = await transporter.sendMail({
        from: process.env.EMAIL_USER,
        to: emailConfig.to,
        subject: emailConfig.subject,
        text: body,
        headers: {
          'X-Bounty-Automation': 'terminal221b',
          'X-Email-Type': key
        }
      });

      console.log(`✅ ${key.toUpperCase()}: Sent to ${emailConfig.to}`);
      console.log(`   Message ID: ${info.messageId}\n`);
      
      results[key] = { success: true, to: emailConfig.to };
      successCount++;

    } catch (error) {
      console.log(`❌ ${key.toUpperCase()}: Failed - ${error.message}\n`);
      results[key] = { success: false, error: error.message };
    }
  }

  // Summary
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log(`║  📊 RESULTS: ${successCount}/3 emails sent                         ║`);
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  // Log results
  fs.appendFileSync(
    path.expandUser('~/terminal221b/logs/email_assistant.log'),
    `\n${new Date().toISOString()} - Send Campaign\n${JSON.stringify(results, null, 2)}\n`
  );

  process.exit(successCount === 3 ? 0 : 1);
}

// Helper for path.expanduser
path.expandUser = (p) => p.replace('~', process.env.HOME);

// Run
if (!process.env.EMAIL_USER || !process.env.EMAIL_PASSWORD) {
  console.error('❌ Error: EMAIL_USER and EMAIL_PASSWORD not set in .env');
  console.error('Setup your .env file:\n  EMAIL_USER=your-email@gmail.com\n  EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx');
  process.exit(1);
}

sendEmails().catch(console.error);
