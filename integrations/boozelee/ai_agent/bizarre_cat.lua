#!/usr/bin/env lua
-- Bizarre Cat Interaction Engine

cat_moods = {"😾", "🐱", "😸", "🙀", "🐈‍⬛"}
questions = {
    "Why humans?", "Paw clapping?", "Feed void?", "Quantum cat?", "Purr/hiss?"
}

math.randomseed(os.time())

function cat_fortune(input)
    local mood = cat_moods[math.random(#cat_moods)]
    return string.format(
        "🐾 %s 🐾
CatAI: %s reversed = %s
Meow: %d/10 %s",
        input:upper(),
        input,
        input:reverse(),
        math.random(1,10),
        mood
    )
end

function cat_menu()
    while true do
        print("
🐱 BIZARRE CAT v∞ 🐱")
        print("1. Random question  2. MEOW  3. Glitch  4. Quit")
        io.write("Paw: ")
        local choice = io.read()
        
        if choice == "1" then
            local q = questions[math.random(#questions)]
            print(cat_fortune(q))
        elseif choice == "2" then
            print(cat_fortune("MEOW MEOW MEOW"))
        elseif choice == "3" then
            print("🐱 GLITCH OVERLOAD 🐱")
            for i=1,5 do print(string.rep("█", 20-i) .. " HISS!") end
        elseif choice == "4" then
            break
        end
    end
end

cat_menu()
