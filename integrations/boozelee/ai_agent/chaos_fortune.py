#!/usr/bin/env python3
import curses, random, time, os
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
math.randomseed(os.time())
function fortune(user_input, glitches)
    return "Lua says: '"..user_input:reverse().."' = "..math.random(1,100).."% chaos ["..glitches.."]"
end
""")

def main(stdscr):
    curses.curs_set(0)
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.addstr(0, 0, "Type (ESC=quit): ", curses.A_BOLD)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 27: break
        
        inp = chr(ch) if 32 <= ch <= 126 else "?"
        fortune = lua.globals().fortune(inp, random.randint(0, 99))
        stdscr.addstr(2, 0, str(fortune)[:w])
        stdscr.refresh()
        time.sleep(1)

curses.wrapper(main)
