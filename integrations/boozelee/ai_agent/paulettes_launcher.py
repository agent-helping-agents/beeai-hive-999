#!/usr/bin/env python3
import curses, subprocess, os, random
APPS={'1':'paulettes_chaoscat.py','2':'paulettes_cat.lua','3':'rust_cat'}

PAULIEN_ART="""
   /_/    PAULETTE'S    ( o.o )
  ( 😸 )   CHAOS SUITE    > ^ <
   > ^ <     v∞ 2026     /_/  
🐱               🐱          🐱
In HONOR of PAULIEN - Terminal Sorcery
"""

def main(stdscr):
    curses.curs_set(0)
    while 1:
        h,w=stdscr.getmaxyx(); stdscr.clear()
        for i,line in enumerate(PAULIEN_ART.split('
')): 
            stdscr.addstr(1+i,w//2-len(line)//2,line,curses.color_pair(i%7+1)|curses.A_BOLD)
        curses.start_color(); [curses.init_pair(i,random.randint(1,7),0) for i in range(1,8)]
        
        stdscr.addstr(12,2,"1. ChaosCat+TinyLlama",curses.color_pair(1)|curses.A_BOLD)
        stdscr.addstr(13,2,"2. Lua Cat",curses.color_pair(2)|curses.A_BOLD)
        stdscr.addstr(14,2,"3. Rust Cat (install)",curses.color_pair(3)|curses.A_BOLD)
        stdscr.addstr(16,2,"Q=Quit",curses.color_pair(7))
        stdscr.refresh()
        
        k=stdscr.getch()
        if k==ord('q'): break
        elif k==ord('1') and os.path.exists('paulettes_chaoscat.py'): subprocess.run(['python3','paulettes_chaoscat.py'])
        elif k==ord('2'): subprocess.run(['lua5.3','paulettes_cat.lua'])
        elif k==ord('3'): print("Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")

curses.wrapper(main)
