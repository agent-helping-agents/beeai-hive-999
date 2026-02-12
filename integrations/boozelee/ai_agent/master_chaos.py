#!/usr/bin/env python3
import curses, subprocess, os

APPS = {
    '1': './chaos_fortune.py',
    '2': './lua_glitch_tui.py', 
    '3': './chaos_menu.py',
    '4': './lua_state_engine.py'
}

def main(stdscr):
    curses.curs_set(0)
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.addstr(2, 2, "LUA + NCURSES CHAOS SUITE", curses.A_BOLD)
        stdscr.addstr(5, 2, "1. Chaos Fortune")
        stdscr.addstr(6, 2, "2. Glitch Art TUI")
        stdscr.addstr(7, 2, "3. Lua Menu System")
        stdscr.addstr(8, 2, "4. State Engine")
        stdscr.addstr(10, 2, "q=quit")
        stdscr.refresh()
        
        k = chr(stdscr.getch())
        if k == 'q': break
        if k in APPS and os.path.exists(APPS[k]):
            subprocess.run(['python3', APPS[k]])
        stdscr.clear()

curses.wrapper(main)
