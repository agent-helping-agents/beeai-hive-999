import React from 'react';
import { Search, Shield, Zap, Brain } from 'lucide-react';

const AISoulCard = ({ name, role, price, description }) => (
  <div className="bg-gray-900 border-2 border-purple-500 rounded-lg p-6 hover:shadow-[0_0_20px_rgba(168,85,247,0.5)] transition-all">
    <div className="flex justify-between items-start mb-4">
      <h3 className="text-2xl font-bold text-white uppercase tracking-tighter">{name}</h3>
      <span className="bg-purple-600 text-white px-3 py-1 rounded text-sm font-bold">{price} SOL</span>
    </div>
    <p className="text-purple-300 text-sm mb-4 italic">{role}</p>
    <p className="text-gray-400 text-sm mb-6 line-clamp-3">{description}</p>
    <button className="w-full bg-transparent border-2 border-purple-500 text-purple-500 hover:bg-purple-500 hover:text-white py-2 font-black transition-colors uppercase italic">
      Capture Soul
    </button>
  </div>
);

const App = () => {
  const souls = [
    {
      name: "The Investigator",
      role: "Pattern Recognition Specialist",
      price: "2.5",
      description: "A soul forged in the fires of Baker Street. Specializes in finding hidden links between disparate on-chain events."
    },
    {
      name: "The Cryptographer",
      role: "Zero-Knowledge Analyst",
      price: "5.0",
      description: "An expert in reading between the blocks. This soul provides unparalleled insights into protocol vulnerabilities."
    },
    {
      name: "The Alchemist",
      role: "Liquidity Transformer",
      price: "3.2",
      description: "Masters the art of swapping. The Alchemist soul identifies optimal yield opportunities before they manifest."
    }
  ];

  return (
    <div className="min-h-screen bg-black text-white p-8 font-mono uppercase">
      <header className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center mb-16 border-b-4 border-purple-900 pb-8">
        <div>
          <h1 className="text-6xl font-black italic tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-500 mb-2">
            Baker Street Souls
          </h1>
          <p className="text-purple-400 tracking-widest">Agentic NFT Market - Trade AI Personalities</p>
        </div>
        <div className="flex gap-4 mt-8 md:mt-0">
          <div className="flex items-center gap-2 bg-gray-900 px-4 py-2 border-2 border-purple-500">
            <Search size={20} className="text-purple-500" />
            <input type="text" placeholder="Scan for souls..." className="bg-transparent border-none outline-none text-sm w-48" />
          </div>
          <button className="bg-purple-600 px-6 py-2 font-bold hover:bg-purple-700 transition-colors">
            Connect Wallet
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {souls.map((soul, i) => (
            <AISoulCard key={i} {...soul} />
          ))}
        </div>
      </main>

      <footer className="max-w-6xl mx-auto mt-24 pt-8 border-t-2 border-gray-800 text-gray-600 text-xs flex justify-between">
        <p>Decentralized Personality Proxy v1.0</p>
        <p>&copy; 2026 Baker Street Laboratory</p>
      </footer>
    </div>
  );
};

export default App;
