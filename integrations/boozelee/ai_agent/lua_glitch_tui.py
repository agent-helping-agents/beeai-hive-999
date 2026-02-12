#!/usr/bin/env python3
import curses, random, time
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
function glitch_art(width, eat_level)
    local art = {}
    for i = 1, 5 do
        art[i] = string.rep("█", width-eat_level*2) .. " GLITCH["..eat_level.."]"
    end
    return table.concat(art, "
")
end
""")

def main(stdscr):
    eat = 0
    curses.curs_set(0)
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        
        art = lua.globals().glitch_art(w//2, eat)
        for i, line in enumerate(str(art).split('
')):
            stdscr.addstr(3+i, 2, line[:w-5])
        
        stdscr.addstr(10, 2, f"EAT LEVEL: {eat} (e=more, q=quit)")
        stdscr.refresh()
        
        k = stdscr.getch()
        if k == ord('q'): break
        if k == ord('e'): eat = min(20, eat + 1)
        time.sleep(0.1)

curses.wrapper(main)
