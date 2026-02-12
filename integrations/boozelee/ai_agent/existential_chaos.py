python3 existential_chaos.py#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The Terminal That Shouldn’t Exist — v∞
# Author: (You, the chaos architect)

import curses
import random
import time
import subprocess
import os
import sys
from lupa import LuaRuntime  # Lua-Python bridge (pip install lupa)

# ------------------------------------------------------------
# Initialize Lua runtime — unexplored co-language integration
# ------------------------------------------------------------
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
function generate_fortune(user_input, glitches)
    local quotes = {
        "You typed '"..user_input.."' but meant '"..user_input:reverse().."'. Reality "..math.random(1,100).."% fake.",
        "Lua says: Your brain clock runs at "..math.random(1,9).."Hz with "..glitches.." dangling thoughts.",
        "'"..user_input.."' dereferenced nil. Soul segmentation fault.",
        "Quantum shell: Both '"..user_input.."' and not '"..user_input.."' exist simultaneously.",
        "Attempted to reboot ego. SYS_ERR: recursive introspection detected."
    }
    return quotes[math.random(#quotes)]
end
""")

FORTUNES = [
    "SEGFAULT (fake) — but your future breakpoint is real.",
    "Your terminal now identifies as sentient.",
    "Reverse world engaged. You’ve become your own process.",
    "Lua blinks and whispers: return nil.",
    "Type in silence… something unseen listens.",
]

# ------------------------------------------------------------
# State object to store per-session chaos parameters
# ------------------------------------------------------------
class ChaosState:
    def __init__(self):
        self.reverse_mode = False
        self.ghost_mode = False
        self.glitch_count = 0
        self.fake_crash = False
        self.history = []
        self.eat_edges = 0


# ------------------------------------------------------------
# Display logic and twisted UI effects
# ------------------------------------------------------------
def draw_screen(stdscr, state):
    curses.curs_set(0)
    curses.start_color()
    for i in range(1, 8):
        curses.init_pair(i, random.randint(0, 7), random.randint(0, 7))

    h, w = stdscr.getmaxyx()
    stdscr.clear()

    # Self‑eating border shrink
    margin = state.eat_edges
    draw_h, draw_w = max(5, h - 2*margin), max(10, w - 4*margin)

    # Title (sometimes reversed)
    title = "CHAOS FORTUNE TERMINAL vNULL"
    ypos, xpos = 1 + margin, 2 + random.randint(0, margin + 2)
    text = title[::-1] if state.reverse_mode else title
    stdscr.addstr(ypos, xpos % w, text[:draw_w], curses.color_pair(2) | curses.A_REVERSE)

    # Dynamic menu
    options = ["(F)ortune", "(R)everse", "(G)host", "(C)rash", "(E)at border", "(T)akeover", "(Esc) quit"]
    for i, opt in enumerate(options):
        ox = 4 + i * 2 + state.glitch_count % 5
        stdscr.addstr(3 + i, ox % draw_w, opt, curses.color_pair((i+1) % 7) | curses.A_BOLD)

    # Lua fortune displayed mid‑screen
    if state.history:
        recent = state.history[-1][:20]
        msg = lua.globals().generate_fortune(recent, state.glitch_count)
        lines = str(msg).split('
')
        for j, line in enumerate(lines):
            pos_y = h // 2 + j
            stdscr.addstr(pos_y, 4, line[:draw_w - 5], curses.color_pair(random.randint(1,6)))

    # Invisible hint
    if state.ghost_mode:
        stdscr.addstr(h-3, 2, "(Ghost input mode active... invisible typing)",
                      curses.color_pair(4) | curses.A_DIM)

    # Fake crash overlay
    if state.fake_crash:
        crash_msg = "!!! KERNEL PANIC: process=your_consciousness !!!"
        stdscr.addstr(h//2, max(0, w//2 - len(crash_msg)//2), crash_msg,
                      curses.color_pair(1) | curses.A_BLINK)
        stdscr.addstr(h//2+1, w//2 - 10, "Press any key to recover phantom...", curses.color_pair(5))

    # Footer status bar
    footer = f"Reverse={state.reverse_mode} Ghost={state.ghost_mode} Glitches={state.glitch_count} Eat={state.eat_edges}"
    stdscr.addstr(h-1, 0, footer[:w-1], curses.color_pair(7))
    stdscr.refresh()


# ------------------------------------------------------------
# Persistent PS1 takeover (appends to bashrc)
# ------------------------------------------------------------
def terminal_takeover():
    dread_ps1 = r'[e[38;5;196m][VOID][e[0m] w $ '
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc, "a") as f:
        f.write(f"
# --- Chaos injection ---
PS1='{dread_ps1}'
")
    subprocess.call(["bash", "-c", "source ~/.bashrc > /dev/null 2>&1"])
    return ">> Terminal personality installed (permanent)."


# ------------------------------------------------------------
# Main interactive loop
# ------------------------------------------------------------
def main(stdscr):
    state = ChaosState()
    k = 0
    curses.halfdelay(1)  # Non-blocking input, short delay

    while k != 27:  # ESC
        draw_screen(stdscr, state)
        k = stdscr.getch()

        # Log keypress
        if 32 <= k <= 126:
            key = chr(k)
            if not state.ghost_mode:
                state.history.append(key)
        elif k != -1:
            state.history.append(f"<{k}>")

        if state.reverse_mode:
            k = (k + 42) % 255  # Input corruption

        # Command handlers
        if k in (ord('f'), 10):  # Fortune
            f = random.choice(FORTUNES)
            stdscr.addstr(10, 5, f, curses.color_pair(random.randint(1,6)))
            stdscr.refresh()
            time.sleep(1.3)

        elif k == ord('r'):
            state.reverse_mode = not state.reverse_mode

        elif k == ord('g'):
            state.ghost_mode = not state.ghost_mode

        elif k == ord('c'):
            state.fake_crash = True
            draw_screen(stdscr, state)
            time.sleep(1.5)
            state.fake_crash = False

        elif k == ord('e'):
            state.eat_edges = min(10, state.eat_edges + 1)

        elif k == ord('t'):
            msg = terminal_takeover()
            stdscr.addstr(12, 5, msg, curses.color_pair(3))
            stdscr.refresh()
            time.sleep(2)

        # Random glitch events
        if random.random() < 0.12:
            state.glitch_count += 1
            stdscr.addstr(random.randint(0,5), random.randint(0,20), "GLITCH>", curses.A_BLINK)
            stdscr.refresh()
            time.sleep(0.05)

    stdscr.clear()
    stdscr.addstr(5, 5, "You escaped the void. Or did you?", curses.color_pair(6))
    stdscr.refresh()
    time.sleep(1.5)


# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
if __name__ == "__main__":
    print("Launching CHAOS FORTUNE TERMINAL (press ESC to exit)")
    curses.wrapper(main)
