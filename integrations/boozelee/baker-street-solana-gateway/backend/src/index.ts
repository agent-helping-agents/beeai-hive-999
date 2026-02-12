import express from 'express';
import * as web3 from '@solana/web3.js';
import dotenv from 'dotenv';
import { OpenAI } from 'openai';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Initialize Solana Connection
const connection = new web3.Connection(
  process.env.SOLANA_RPC_URL || web3.clusterApiUrl('devnet'),
  'confirmed'
);

// Initialize OpenAI (or your preferred local LLM endpoint)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.LLM_BASE_URL // e.g., http://localhost:11434/v1 for Ollama
});

app.post('/investigate', async (req, res) => {
  const { prompt, transactionSignature, userPublicKey } = req.body;

  if (!prompt || !transactionSignature || !userPublicKey) {
    return res.status(400).json({ error: 'Missing prompt, signature, or public key.' });
  }

  try {
    // 1. Verify Transaction
    console.log(`🔍 Verifying transaction: ${transactionSignature}`);
    const tx = await connection.getTransaction(transactionSignature, {
      commitment: 'confirmed',
      maxSupportedTransactionVersion: 0
    });

    if (!tx) {
      return res.status(402).json({ error: 'Transaction not found. Payment required.' });
    }

    // TODO: Add logic to verify recipient and amount matches the prompt cost

    // 2. Process AI Request
    console.log(`🧠 Processing investigation for ${userPublicKey}...`);
    const completion = await openai.chat.completions.create({
      model: process.env.LLM_MODEL || 'marco-o1',
      messages: [
        { role: 'system', content: 'You are the Psychedelic Detective of Baker Street Laboratory. Analyze the following clue.' },
        { role: 'user', content: prompt }
      ]
    });

    const answer = completion.choices[0].message.content;

    // 3. Return Result
    res.json({
      status: 'SOLVED',
      investigation: answer,
      evidence: transactionSignature
    });

  } catch (error: any) {
    console.error('❌ Investigation failed:', error.message);
    res.status(500).json({ error: 'Internal Detective Error' });
  }
});

app.listen(port, () => {
  console.log(`🕵️‍♂️ Baker Street Solana Gateway listening at http://localhost:${port}`);
});
