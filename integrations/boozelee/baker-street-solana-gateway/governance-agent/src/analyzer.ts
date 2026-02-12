import { OpenAI } from 'openai';
import dotenv from 'dotenv';

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || 'local',
  baseURL: process.env.LLM_BASE_URL || 'http://localhost:11434/v1'
});

export async function analyzeProposal(name: string, description: string) {
  console.log(`🧠 Psychedelic Detective is analyzing proposal: ${name}`);
  
  const prompt = `
    You are the Psychedelic Detective of Baker Street Laboratory. 
    Analyze the following Solana DAO proposal and determine its impact on the ecosystem.
    Provide a verdict: SHOULD_EXECUTE or SHOULD_REJECT.
    
    Proposal Name: ${name}
    Description: ${description}
    
    Maintain your 2D comic book art style persona. Focus on unconventional pattern analysis.
  `;

  try {
    const completion = await openai.chat.completions.create({
      model: process.env.LLM_MODEL || 'marco-o1',
      messages: [{ role: 'user', content: prompt }]
    });

    return completion.choices[0].message.content;
  } catch (error: any) {
    console.error('❌ AI Analysis failed:', error.message);
    return 'Analysis failed. Detective is thinking...';
  }
}
