#!/usr/bin/env python3
import curses, subprocess, os, time, random
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="tinyllama")

AGENTS = {
    '1': {'name': '🐱 PAULETTE CODER', 'cmd': 'python3 paulettes_agents/python_agent/coder_agent.py'},
    '2': {'name': '⚙️ RUST TUI AGENT', 'cmd': './rust_agent/target/release/rust_agent'},
    '3': {'name': '🌌 LUA CHAOS AGENT', 'cmd': 'lua5.3 paulettes_agents/lua_agent/chaos.lua'},
    '4': {'name': '🔗 LANGCHAIN RAG', 'cmd': 'python3 paulettes_agents/python_agent/rag_agent.py'},
    '5': {'name': '🧠 MULTI-AGENT ORCH', 'cmd': 'python3 paulettes_agents/python_agent/multi_agent.py'}
}

PAULIEN_ART = """ 
  /_/\\     PAULETTE'S     ( o.o )  
 ( 😸 )   AI AGENTS v∞     > ^ <  
  > ^ <  LangChain+Rust    /_/\\   
🐱 5 CODING AGENTS 🐱 2026 🐱
LANGCHAIN • TINYLLAMA • RUST • LUA • RAG"""

class AgentHub:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.start_color()
        [curses.init_pair(i, i, 0) for i in range(1, 8)]
        self.selected = 0
    
    def draw(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.clear()
        
        # PAULIEN ASCII ART
        for i, line in enumerate(PAULIEN_ART.splitlines()):
            self.stdscr.addstr(1 + i, (w - len(line)) // 2, line, 
                             curses.color_pair((i % 7) + 1) | curses.A_BOLD)
        
        # AGENT SELECTION
        self.stdscr.addstr(10, 2, "🤖 SELECT AI CODING AGENT:", 
                          curses.color_pair(1) | curses.A_BOLD)
        for i, (k, agent) in enumerate(AGENTS.items()):
            color = curses.color_pair(2) | curses.A_BOLD if i == self.selected else curses.color_pair(4)
            status = "✓ READY" if os.path.exists(agent['cmd'].split()[0]) else "✗ BUILD"
            self.stdscr.addstr(12 + i, 4, f"{k}. {agent['name']} {status}", color)
        
        self.stdscr.addstr(h - 3, 2, "↑↓=Select ENTER=Run Q=Quit", curses.color_pair(7))
        self.stdscr.addstr(h - 2, 2, f"TinyLlama: {llm.model_id.split(':')[-1]}", curses.color_pair(3))
        self.stdscr.refresh()
    
    def run(self):
        while True:
            self.draw()
            key = self.stdscr.getch()
            if key == ord('q'): break
            elif key == curses.KEY_UP: self.selected = max(0, self.selected - 1)
            elif key == curses.KEY_DOWN: self.selected = min(len(AGENTS) - 1, self.selected + 1)
            elif key == 10:  # ENTER
                agent_key = list(AGENTS.keys())[self.selected]
                cmd = AGENTS[agent_key]['cmd']
                if os.path.exists(cmd.split()[0]):
                    self.stdscr.addstr(20, 2, f"🚀 LAUNCHING {AGENTS[agent_key]['name']}...", 
                                     curses.color_pair(1) | curses.A_BLINK)
                    self.stdscr.refresh()
                    subprocess.run(cmd, shell=True)
                else:
                    self.stdscr.addstr(20, 2, "❌ BUILD AGENT FIRST", curses.color_pair(2))

if __name__ == '__main__':
    print("🐱 PAULETTE'S AI AGENTS HUB 🐱")
    curses.wrapper(AgentHub)
