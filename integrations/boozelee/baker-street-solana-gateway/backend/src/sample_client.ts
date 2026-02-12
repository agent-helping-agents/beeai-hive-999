import * as web3 from '@solana/web3.js';
import axios from 'axios';

async function requestInvestigation() {
  const connection = new web3.Connection(web3.clusterApiUrl('devnet'), 'confirmed');
  const payer = web3.Keypair.generate(); // In a real app, use a wallet

  console.log('💎 Airdropping SOL for testing...');
  const airdropSignature = await connection.requestAirdrop(payer.publicKey, web3.LAMPORTS_PER_SOL);
  await connection.confirmTransaction(airdropSignature);

  const recipient = new web3.PublicKey('YOUR_GATEWAY_WALLET_ADDRESS');
  
  console.log('💸 Sending payment for investigation...');
  const transaction = new web3.Transaction().add(
    web3.SystemProgram.transfer({
      fromPubkey: payer.publicKey,
      toPubkey: recipient,
      lamports: 0.001 * web3.LAMPORTS_PER_SOL,
    })
  );

  const signature = await web3.sendAndConfirmTransaction(connection, transaction, [payer]);
  console.log('✅ Payment confirmed:', signature);

  console.log('🕵️‍♂️ Sending clue to Baker Street Solana Gateway...');
  const response = await axios.post('http://localhost:3000/investigate', {
    prompt: 'Analyze the recent unusual spikes in SOL liquidity.',
    transactionSignature: signature,
    userPublicKey: payer.publicKey.toBase58()
  });

  console.log('🔍 Investigation Result:', response.data.investigation);
}

requestInvestigation();
