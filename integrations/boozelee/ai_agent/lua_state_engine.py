#!/usr/bin/env python3
import curses, time
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
chaos_state = {glitches = 0, mood = "calm", inputs = {}}
moods = {"calm", "angry", "ecstatic", "void"}

function log_input(input)
    table.insert(chaos_state.inputs, input)
    chaos_state.glitches = chaos_state.glitches + 1
    if chaos_state.glitches > 5 then
        chaos_state.mood = moods[math.random(#moods)]
    end
    return chaos_state
end
""")

def main(stdscr):
    curses.curs_set(0)
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        
        state = lua.globals().log_input("KEYPRESS")
        stdscr.addstr(2, 2, f"Glitches: {state.glitches}")
        stdscr.addstr(4, 2, f"Mood: {state.mood}")
        stdscr.addstr(6, 2, f"History: {len(state.inputs)} entries")
        
        stdscr.addstr(h-2, 2, "q=quit")
        stdscr.refresh()
        
        if stdscr.getch() == ord('q'): break
        time.sleep(0.5)

curses.wrapper(main)
