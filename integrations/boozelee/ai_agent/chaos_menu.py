#!/usr/bin/env python3
import curses, random
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
menu_items = {"FORTUNE", "GLITCH", "REVERSE", "CRASH", "VOID"}
function get_menu_item(index)
    return menu_items[index % #menu_items + 1]
end
function process_choice(choice)
    return "Lua processed: "..choice.." -> CHAOS LEVEL "..math.random(1,10)
end
""")

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    menu_idx = 0
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        
        # Lua menu rendering
        for i in range(5):
            item = lua.globals().get_menu_item(i)
            color = curses.color_pair(1) if i == menu_idx else 0
            stdscr.addstr(5+i, w//2-10, item, color)
        
        stdscr.addstr(15, 2, "↑↓=move ENTER=select q=quit")
        stdscr.refresh()
        
        k = stdscr.getch()
        if k == ord('q'): break
        if k == curses.KEY_UP: menu_idx = (menu_idx - 1) % 5
        if k == curses.KEY_DOWN: menu_idx = (menu_idx + 1) % 5
        if k == 10:  # ENTER
            choice = lua.globals().get_menu_item(menu_idx)
            result = lua.globals().process_choice(choice)
            stdscr.addstr(18, 2, result[:w-5], curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()

curses.wrapper(main)
