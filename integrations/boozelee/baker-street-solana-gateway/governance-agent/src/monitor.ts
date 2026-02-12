import { Connection, PublicKey, Keypair } from '@solana/web3.js';
import * as splGov from '@solana/spl-governance';
import dotenv from 'dotenv';
import { analyzeProposal } from './analyzer';
import { executePassedProposal } from './executor';

dotenv.config();

const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.devnet.solana.com';
const GOVERNANCE_PROGRAM_ID = new PublicKey(process.env.GOVERNANCE_PROGRAM_ID || 'GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw');

// Agent's Wallet for signing executions (In demo, we generate one)
const agentKeypair = Keypair.generate();

async function startMonitoring() {
  const connection = new Connection(SOLANA_RPC_URL, 'confirmed');
  console.log(`🕵️‍♂️ Baker Street Governance Agent started on ${SOLANA_RPC_URL}`);
  console.log(`🔍 Monitoring Program: ${GOVERNANCE_PROGRAM_ID.toBase58()}`);
  console.log(`🆔 Agent PublicKey: ${agentKeypair.publicKey.toBase58()}`);

  connection.onProgramAccountChange(
    GOVERNANCE_PROGRAM_ID,
    async (keyedAccountInfo) => {
      const { accountId, accountInfo } = keyedAccountInfo;
      
      try {
        console.log(`✨ Detected change in account: ${accountId.toBase58()}`);
        
        // Simulating identification of a new proposal for the demo
        const verdict = await analyzeProposal("Simulation Proposal", "Treasury distribution for research.");
        console.log(`🕵️‍♂️ Detective's Verdict:\n${verdict}`);

        if (verdict?.includes('SHOULD_EXECUTE')) {
            console.log('🎯 Verdict is positive. Triggering autonomous execution...');
            await executePassedProposal(
                GOVERNANCE_PROGRAM_ID,
                PublicKey.default, // Dummy Governance
                accountId,
                agentKeypair
            );
        }
        
      } catch (err) {
        // Not a proposal or parsing error
      }
    },
    'confirmed'
  );
}

startMonitoring().catch(console.error);
