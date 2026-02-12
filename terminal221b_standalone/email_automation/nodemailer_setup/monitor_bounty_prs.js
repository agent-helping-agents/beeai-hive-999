#!/usr/bin/env node

/**
 * Bounty PR Monitor - Terminal 221B
 * Tracks GitHub PR status for bounty claims
 * 
 * Monitors:
 * - PR #8254 (OAuth v2) - $50
 * - PR #8253 (Alpine Linux) - TBD
 * - PR #8228 (Debian 13) - $6,900
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const BOUNTY_PRS = [
  { number: 8254, title: 'OAuth v2', repo: 'coollabsio/coolify', bounty: '$50' },
  { number: 8253, title: 'Alpine Linux', repo: 'coollabsio/coolify', bounty: 'TBD' },
  { number: 8228, title: 'Debian 13', repo: 'coollabsio/coolify', bounty: '$6,900' }
];

const LOG_FILE = path.expandUser('~/terminal221b/logs/bounty_monitor.log');
const STATUS_FILE = path.expandUser('~/terminal221b/logs/bounty_status.json');

class BountyMonitor {
  constructor() {
    this.results = [];
    this.statuses = {};
  }

  log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}`;
    console.log(logMessage);
    
    // Append to log file
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
    fs.appendFileSync(LOG_FILE, logMessage + '\n');
  }

  checkPRStatus(prNumber, repo) {
    try {
      // Get PR status from GitHub CLI
      const cmd = `gh pr view ${prNumber} --repo ${repo} --json state,statusCheckRollup,mergeable,mergedAt,mergedBy --jq '.state + "|" + .statusCheckRollup[0].conclusion + "|" + (.mergeable // "unknown") + "|" + (.mergedAt // "null") + "|" + (.mergedBy.login // "null")'`;
      
      const output = execSync(cmd, { encoding: 'utf8' }).trim();
      const [state, ciStatus, mergeable, mergedAt, mergedBy] = output.split('|');
      
      return {
        state,
        ciStatus: ciStatus || 'PENDING',
        mergeable,
        mergedAt: mergedAt === 'null' ? null : mergedAt,
        mergedBy: mergedBy === 'null' ? null : mergedBy,
        isMerged: mergedAt !== 'null'
      };

    } catch (error) {
      this.log(`⚠️  Error checking PR #${prNumber}: ${error.message}`);
      return null;
    }
  }

  async monitorAll() {
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║  🎯 BOUNTY PR MONITOR - Terminal 221B                      ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');

    this.log('Starting bounty PR status check...');

    for (const pr of BOUNTY_PRS) {
      console.log(`\n📋 Checking: ${pr.title} (PR #${pr.number}) - ${pr.bounty}`);
      this.log(`Checking PR #${pr.number}: ${pr.title}`);

      const status = this.checkPRStatus(pr.number, pr.repo);
      
      if (status) {
        this.statuses[pr.number] = {
          ...pr,
          status,
          timestamp: new Date().toISOString()
        };

        // Display status
        const stateEmoji = status.state === 'MERGED' ? '✅' : status.state === 'OPEN' ? '📖' : '❌';
        const ciEmoji = status.ciStatus === 'SUCCESS' ? '✅' : status.ciStatus === 'PENDING' ? '⏳' : '❌';
        
        console.log(`  State: ${stateEmoji} ${status.state}`);
        console.log(`  CI: ${ciEmoji} ${status.ciStatus}`);
        console.log(`  Mergeable: ${status.mergeable}`);
        
        if (status.isMerged) {
          console.log(`  ✅ MERGED by ${status.mergedBy}`);
          console.log(`  Bounty Status: 🎉 CLAIMED!`);
          this.log(`✅ PR #${pr.number} MERGED - Bounty ${pr.bounty} ready to claim!`);
        } else if (status.state === 'OPEN') {
          console.log(`  Status: Awaiting merge`);
          this.log(`⏳ PR #${pr.number} still open - monitoring...`);
        }
      }
    }

    // Save status snapshot
    this.saveStatus();
    this.displaySummary();
  }

  saveStatus() {
    const statusDir = path.dirname(STATUS_FILE);
    if (!fs.existsSync(statusDir)) fs.mkdirSync(statusDir, { recursive: true });
    
    fs.writeFileSync(STATUS_FILE, JSON.stringify(this.statuses, null, 2));
    this.log(`Status snapshot saved: ${STATUS_FILE}`);
  }

  displaySummary() {
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║  📊 BOUNTY STATUS SUMMARY                                  ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');

    let totalBounty = 0;
    let mergedCount = 0;
    let openCount = 0;

    for (const [prNum, data] of Object.entries(this.statuses)) {
      const bountyAmount = parseInt(data.bounty.replace(/[$,]/g, '')) || 0;
      
      if (data.status.isMerged) {
        console.log(`✅ PR #${prNum} (${data.title}): MERGED - ${data.bounty}`);
        totalBounty += bountyAmount;
        mergedCount++;
      } else if (data.status.state === 'OPEN') {
        console.log(`📖 PR #${prNum} (${data.title}): OPEN - ${data.bounty}`);
        openCount++;
      } else {
        console.log(`❌ PR #${prNum} (${data.title}): ${data.status.state}`);
      }
    }

    console.log(`\n📊 Metrics:`);
    console.log(`  Merged: ${mergedCount}/${BOUNTY_PRS.length}`);
    console.log(`  Open: ${openCount}/${BOUNTY_PRS.length}`);
    console.log(`  Claimed: $${totalBounty.toLocaleString()}`);
    console.log(`  Potential: $6,950+`);
    
    this.log(`Summary - Merged: ${mergedCount}, Open: ${openCount}, Claimed: $${totalBounty}`);
  }
}

// Path helper
Object.defineProperty(path, 'expandUser', {
  value: (p) => p.replace('~', process.env.HOME || '.')
});

async function main() {
  const monitor = new BountyMonitor();
  await monitor.monitorAll();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { BountyMonitor };
