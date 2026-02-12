#!/usr/bin/env node

/**
 * Partnership Email Sender - Terminal 221B
 * Sends bounty collaboration emails to: Augment, Gemini, OpenAI
 * 
 * Uses: Nodemailer (16k+ GitHub stars, production-ready)
 * Supports: Gmail, Zoho Mail, and other SMTP providers
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });

// Email templates configuration
const PARTNERSHIP_EMAILS = {
  augment: {
    to: 'collaborate@augment.com',
    cc: 'partnerships@augment.com',
    subject: '🚀 Terminal 221B x Context Engine MCP - $6,950+ Bounty Integration',
    templateFile: '01_AUGMENT_EMAIL.txt',
    description: 'Augment - Semantic Code Search Integration'
  },
  gemini: {
    to: 'partnerships@google.com',
    subject: 'Deep Research Integration for Autonomous AI Multi-Agent Crypto System',
    templateFile: '02_GEMINI_EMAIL.txt',
    description: 'Google Gemini - Deep Research & Analysis'
  },
  openai: {
    to: 'partnerships@openai.com',
    subject: 'GPT-4 Integration for Multi-Agent Autonomous AI System',
    templateFile: '03_OPENAI_EMAIL.txt',
    description: 'OpenAI - GPT-4 & Advanced Reasoning'
  }
};

class EmailSender {
  constructor() {
    this.transporter = null;
    this.results = {};
    this.logFile = path.expandUser('~/terminal221b/logs/email_sender.log');
  }

  setupTransporter(provider = process.env.ACTIVE_EMAIL_PROVIDER || 'GMAIL1') {
    console.log(`📧 Setting up transporter for: ${provider}`);

    let config;

    if (provider === 'GMAIL1') {
      config = {
        service: 'gmail',
        auth: {
          user: process.env.EMAIL_USER_GMAIL1,
          pass: process.env.EMAIL_PASSWORD_GMAIL1
        }
      };
    } else if (provider === 'GMAIL2') {
      config = {
        service: 'gmail',
        auth: {
          user: process.env.EMAIL_USER_GMAIL2,
          pass: process.env.EMAIL_PASSWORD_GMAIL2
        }
      };
    } else if (provider === 'ZOHO') {
      config = {
        host: process.env.EMAIL_SMTP_ZOHO || 'smtp.zoho.com',
        port: parseInt(process.env.EMAIL_SMTP_PORT_ZOHO || 465),
        secure: true,
        auth: {
          user: process.env.EMAIL_USER_ZOHO,
          pass: process.env.EMAIL_PASSWORD_ZOHO
        }
      };
    } else {
      throw new Error(`Unknown email provider: ${provider}`);
    }

    this.transporter = nodemailer.createTransport(config);
    this.fromEmail = config.auth.user;
    this.provider = provider;
  }

  async verifyConnection() {
    try {
      await this.transporter.verify();
      console.log(`✅ ${this.provider}: Email service ready`);
      return true;
    } catch (error) {
      console.error(`❌ ${this.provider}: Connection failed - ${error.message}`);
      return false;
    }
  }

  async sendEmail(emailKey, emailConfig) {
    try {
      // Read email template
      const templatePath = path.expandUser(`~/emails_ready_to_send/${emailConfig.templateFile}`);
      
      if (!fs.existsSync(templatePath)) {
        throw new Error(`Template not found: ${templatePath}`);
      }

      const bodyText = fs.readFileSync(templatePath, 'utf8');

      // Send email
      const info = await this.transporter.sendMail({
        from: `Terminal 221B <${this.fromEmail}>`,
        to: emailConfig.to,
        cc: emailConfig.cc || undefined,
        subject: emailConfig.subject,
        text: bodyText,
        headers: {
          'X-Bounty-Automation': 'terminal221b',
          'X-Email-Type': emailKey,
          'X-Provider': this.provider,
          'X-Timestamp': new Date().toISOString()
        }
      });

      console.log(`✅ ${emailKey.toUpperCase()}: Sent to ${emailConfig.to}`);
      console.log(`   Message ID: ${info.messageId}`);
      console.log(`   Response: ${info.response}\n`);

      this.results[emailKey] = {
        success: true,
        to: emailConfig.to,
        messageId: info.messageId,
        timestamp: new Date().toISOString()
      };

      return true;

    } catch (error) {
      console.error(`❌ ${emailKey.toUpperCase()}: ${error.message}\n`);
      
      this.results[emailKey] = {
        success: false,
        to: emailConfig.to,
        error: error.message,
        timestamp: new Date().toISOString()
      };

      return false;
    }
  }

  async sendAll() {
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║  📧 PARTNERSHIP EMAIL CAMPAIGN - TERMINAL 221B             ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');

    let successCount = 0;

    for (const [key, config] of Object.entries(PARTNERSHIP_EMAILS)) {
      console.log(`📤 Sending: ${config.description}`);
      console.log(`   To: ${config.to}`);
      
      const sent = await this.sendEmail(key, config);
      if (sent) successCount++;
      
      // Small delay between emails
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Summary
    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log(`║  📊 RESULTS: ${successCount}/3 emails sent successfully        ║`);
    console.log('╚════════════════════════════════════════════════════════════╝\n');

    // Log results
    this.logResults();

    return successCount === 3;
  }

  logResults() {
    // Ensure logs directory exists
    const logDir = path.expandUser('~/terminal221b/logs');
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }

    const logEntry = {
      timestamp: new Date().toISOString(),
      provider: this.provider,
      fromEmail: this.fromEmail,
      results: this.results
    };

    fs.appendFileSync(
      this.logFile,
      JSON.stringify(logEntry, null, 2) + '\n' + '─'.repeat(60) + '\n'
    );

    console.log(`📋 Log saved: ${this.logFile}`);
  }
}

// Path helper
Object.defineProperty(path, 'expandUser', {
  value: (p) => p.replace('~', process.env.HOME || '.')
});

// Main execution
async function main() {
  // Validate credentials
  const provider = process.env.ACTIVE_EMAIL_PROVIDER || 'GMAIL1';
  
  let hasCredentials = false;

  if (provider === 'GMAIL1') {
    hasCredentials = process.env.EMAIL_USER_GMAIL1 && process.env.EMAIL_PASSWORD_GMAIL1;
  } else if (provider === 'GMAIL2') {
    hasCredentials = process.env.EMAIL_USER_GMAIL2 && process.env.EMAIL_PASSWORD_GMAIL2;
  } else if (provider === 'ZOHO') {
    hasCredentials = process.env.EMAIL_USER_ZOHO && process.env.EMAIL_PASSWORD_ZOHO;
  }

  if (!hasCredentials) {
    console.error('❌ Error: Email credentials not configured');
    console.error(`\nSetup Instructions:`);
    console.error(`1. Run: bash setup_email.sh`);
    console.error(`2. Or manually update .env file with credentials`);
    console.error(`3. Then run: npm run send-emails\n`);
    process.exit(1);
  }

  try {
    const sender = new EmailSender();
    sender.setupTransporter(provider);
    
    const connected = await sender.verifyConnection();
    if (!connected) {
      process.exit(1);
    }

    const success = await sender.sendAll();
    process.exit(success ? 0 : 1);

  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { EmailSender };
