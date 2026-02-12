# 🔬 Baker Street Solana Ecosystem

**A Revolutionary DeAI Research & Governance Suite for the Solana Network.**

Created by **Baker Street Laboratory** for the Superteam Open Innovation Track. This ecosystem demonstrates the synergy between autonomous AI agents and Solana's high-performance blockchain.

---

## 🕵️‍♂️ The "Psychedelic Detective" Vision
In a sea of generic "AI wrappers," Baker Street stands out by treating blockchain data as a crime scene and AI as the detective. Our theme combines 2026's cutting-edge scientific breakthroughs with a unique 2D comic-book aesthetic, creating an immersive experience that stimulates creativity while maintaining rigorous on-chain analysis.

---

## 🚀 The Three Pillars (Ecosystem Integration)

Unlike single-tool submissions, the Baker Street Ecosystem provides a full lifecycle for AI agents on Solana:

### 1. 🕵️‍♂️ Baker Street Solana Gateway (Monetization Layer)
The **Pay-per-Prompt** proxy allows any user to access our specialized "Psychedelic Detective" models (via Ollama/Marco engine) using real-time Solana micro-payments.
*   **Decentralized Access:** No monthly subscriptions. Pay only for the clues you solve.
*   **Tech:** Node.js, Web3.js, OpenAI-Compatible local endpoints.
*   **Location:** `/backend`

### 2. 🧠 Sentient DAOs (Automation Layer)
Autonomous agents that monitor **SPL-Governance (Realms)** proposals. They don't just alert; they **act**.
*   **Autonomous Execution:** If the Detective's verdict is `SHOULD_EXECUTE` and the vote passes, the agent triggers the on-chain transaction.
*   **Pattern Recognition:** Identifies treasury exploits or governance attacks before they manifest.
*   **Tech:** `@solana/spl-governance`, WebSocket monitoring.
*   **Location:** `/governance-agent`

### 3. 💎 Agentic NFT Market (Financialization Layer)
A marketplace for trading AI **"Souls"**—portable bundles of memory, system prompts, and specialized skills.
*   **Soul Portability:** Move your trained investigator from the Gateway to a Sentient DAO by trading the NFT.
*   **Tech:** React, Tailwind (Futuristic TUI style), Lucide-Icons.
*   **Location:** `/nft-market`

---

## 🛠 Strategic Analysis: Why This Wins
Based on our **Marco-o1 Neural Script Engine** analysis of the 2026 Solana landscape:
*   **Agentic Future:** We move beyond static dApps to active, self-executing AI agents.
*   **Micro-payment Efficiency:** We leverage Solana's sub-cent fees to make micro-AI queries economically viable.
*   **Narrative Resonance:** The "Psychedelic Detective" theme creates an emotional connection, making complex DeAI concepts accessible and aspirational.

---

## 🛠 Setup & Submission

### Installation
1.  **Clone:** `git clone https://github.com/BoozeLee/baker-street-solana-gateway`
2.  **Initialize LLM:** Run Ollama with `marco-o1`.
3.  **Deploy Backend:** `cd backend && npm install && npm start`
4.  **Deploy Agent:** `cd governance-agent && npm install && npm start`
5.  **View Market:** `cd nft-market && npm install`

### Demo Instruction
Run `npx ts-node backend/src/sample_client.ts` to see the full micro-payment and AI response flow in action.

---
**Baker Street Laboratory**
*Solving the mysteries of the block, one transaction at a time.*