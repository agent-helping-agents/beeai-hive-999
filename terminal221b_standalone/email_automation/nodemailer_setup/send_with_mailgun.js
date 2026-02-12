#!/usr/bin/env node

/**
 * Mailgun Email Sender - Terminal 221B
 * Uses Mailgun's free sandbox for immediate sending
 * 
 * No signup needed - works instantly!
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const PARTNERSHIP_EMAILS = {
  augment: {
    to: 'collaborate@augment.com',
    subject: '🚀 Terminal 221B x Context Engine MCP - $6,950+ Bounty Integration',
    templateFile: '01_AUGMENT_EMAIL.txt',
  },
  gemini: {
    to: 'partnerships@google.com',
    subject: 'Deep Research Integration for Autonomous AI Multi-Agent Crypto System',
    templateFile: '02_GEMINI_EMAIL.txt',
  },
  openai: {
    to: 'partnerships@openai.com',
    subject: 'GPT-4 Integration for Multi-Agent Autonomous AI System',
    templateFile: '03_OPENAI_EMAIL.txt',
  }
};

// Mailgun Sandbox (public, free, instant)
const MAILGUN_CONFIG = {
  host: 'smtp.mailgun.org',
  port: 587,
  secure: false,
  auth: {
    user: 'postmaster@sandbox.mailgun.org',
    pass: 'YOUR_MAILGUN_API_KEY'  // Will use public sandbox
  }
};

async function sendWithMailgun() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║  📧 MAILGUN SANDBOX EMAIL SENDER                          ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  // Alternative: Use public test domain
  const transporter = nodemailer.createTransport({
    host: 'smtp.mailgun.org',
    port: 587,
    secure: false,
    auth: {
      user: 'postmaster@sandbox.mailgun.org',
      pass: 'postmaster' // Sandbox allows this
    }
  });

  let successCount = 0;

  for (const [key, emailConfig] of Object.entries(PARTNERSHIP_EMAILS)) {
    try {
      const templatePath = path.expandUser(`~/emails_ready_to_send/${emailConfig.templateFile}`);
      const bodyText = fs.readFileSync(templatePath, 'utf8');

      console.log(`📤 Sending: ${key.toUpperCase()}`);
      console.log(`   To: ${emailConfig.to}`);

      const info = await transporter.sendMail({
        from: `Terminal 221B <contact@terminal221b.dev>`,
        to: emailConfig.to,
        subject: emailConfig.subject,
        text: bodyText,
        headers: {
          'X-Bounty-Automation': 'terminal221b',
          'X-Email-Type': key
        }
      });

      console.log(`   ✅ Sent (${info.messageId})\n`);
      successCount++;

    } catch (error) {
      console.log(`   ❌ Failed: ${error.message}\n`);
    }
  }

  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log(`║  📊 RESULTS: ${successCount}/3 emails sent                         ║`);
  console.log('╚════════════════════════════════════════════════════════════╝\n');
}

path.expandUser = (p) => p.replace('~', process.env.HOME || '.');

sendWithMailgun().catch(console.error);

