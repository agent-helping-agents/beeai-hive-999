#!/usr/bin/env python3
import curses
import ollama
import random
import time
import threading
try:
    from lupa import LuaRuntime
    LUA_OK = True
except:
    LUA_OK = False

# Fixed Lua cat chaos (single line)
LUA_CAT_CODE = """
cat_moods = {"😾", "🐱", "😸", "🙀", "🐈‍⬛"}
function cat_fortune(user_input, ai_response)
    return "🐾 "..user_input:upper().." 🐾
CatAI: "..ai_response:match("([^
]+)").."
Meow: "..math.random(1,10).."/10 "..cat_moods[math.random(#cat_moods)]
end
"""

if LUA_OK:
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(LUA_CAT_CODE)

CAT_QUESTIONS = [
    "Why do humans exist?", "What is the sound of one paw clapping?",
    "Feed me or face the void", "Quantum cat: alive or dead?",
    "Purr or hiss? Choose wisely."
]

class CatState:
    def __init__(self):
        self.ai_busy = False
        self.cat_mood = 0
        self.last_response = ""
        self.glitch_level = 0

def tinyllama_chat(prompt):
    try:
        resp = ollama.chat(model='tinyllama', messages=[
            {'role': 'system', 'content': 'You are CATGPT - deranged feline oracle. Meows, hisses, existential dread, cat puns. CHAOTIC.'},
            {'role': 'user', 'content': f"🐱 {prompt} 🐱"}
        ])
        return resp['message']['content']
    except:
        return "🐱 *hiss* TinyLlama napped... Meow later 😿"

def draw_cat_interface(stdscr, state):
    h, w = stdscr.getmaxyx()
    curses.start_color()
    for i in range(1, 8):
        curses.init_pair(i, random.randint(0,7), random.randint(0,7))
    
    stdscr.clear()
    
    # Title
    title = "🐱 CHAOSCAT v∞ - TINYLLAMA ORACLE 🐱"
    color = curses.color_pair(2) | curses.A_BLINK if state.glitch_level > 5 else curses.color_pair(1)
    stdscr.addstr(1, max(0,(w-len(title))//2), title[:w], color | curses.A_BOLD)
    
    # FIXED ASCII CAT (single strings)
    cat_frame = state.cat_mood % 3
    if cat_frame == 0:
        stdscr.addstr(4, w//2-8, "/_/  ", curses.color_pair(3))
        stdscr.addstr(5, w//2-8, "( o.o)", curses.color_pair(3))
        stdscr.addstr(6, w//2-8, " > ^ <", curses.color_pair(3))
    elif cat_frame == 1:
        stdscr.addstr(4, w//2-8, "/_/\\ GLITCH", curses.color_pair(2))
        stdscr.addstr(5, w//2-8, "( -.- )", curses.color_pair(2))
        stdscr.addstr(6, w//2-8, " > ^ < HISS", curses.color_pair(2))
    else:
        stdscr.addstr(4, w//2-10, "🐱 MEOW VOID 🐱", curses.color_pair(4) | curses.A_BLINK)
    
    # Lua fortune display
    if state.last_response and LUA_OK:
        try:
            fortune = lua.globals().cat_fortune("HUMAN", state.last_response)
            for j, line in enumerate(str(fortune).split("
")):
                stdscr.addstr(10+j, 2, line[:w-5], curses.color_pair(4))
        except:
            stdscr.addstr(10, 2, state.last_response[:w-5], curses.color_pair(4))
    
    # Menu
    menu = ["(Q)uestions", "(M)eow", "(G)litch++", "(P)redict", "(ESC)uit"]
    for i, opt in enumerate(menu):
        stdscr.addstr(h-5+i, 2, opt, curses.color_pair((i+1)%7))
    
    status = f"🐾 Mood:{state.cat_mood} Glitch:{state.glitch_level} AI:{'AWAKE' if not state.ai_busy else 'MEOWING...'}"
    stdscr.addstr(h-1, 0, status[:w], curses.color_pair(7))
    stdscr.refresh()

def ai_thread(prompt, state):
    state.ai_busy = True
    state.last_response = tinyllama_chat(prompt)
    state.ai_busy = False

def main(stdscr):
    state = CatState()
    curses.curs_set(0)
    
    while True:
        draw_cat_interface(stdscr, state)
        k = stdscr.getch()
        
        if k == 27: break
        elif k == ord('q'):
            prompt = random.choice(CAT_QUESTIONS)
            threading.Thread(target=ai_thread, args=(prompt, state), daemon=True).start()
        elif k == ord('m'):
            threading.Thread(target=ai_thread, args=("MEOW MEOW MEOW", state), daemon=True).start()
        elif k == ord('g'):
            state.glitch_level += 1
            state.cat_mood += 1
        elif k == ord('p'):
            prompt = f"Predict my future as chaotic cat entropy level {random.randint(1,100)}"
            threading.Thread(target=ai_thread, args=(prompt, state), daemon=True).start()
        
        if random.random() < 0.1:
            state.cat_mood += 1
            stdscr.addstr(15, 2, "🐱 SUDDEN HISS! 🐱", curses.color_pair(2) | curses.A_BLINK)
            stdscr.refresh()
            time.sleep(0.2)
    
    stdscr.clear()
    stdscr.addstr(5, 5, "🐾 Cat entropy escaped... for now 🐾", curses.color_pair(6))
    stdscr.refresh()
    time.sleep(1)

if __name__ == "__main__":
    print("🐱 Starting ChaosCat TUI + TinyLlama...")
    curses.wrapper(main)
