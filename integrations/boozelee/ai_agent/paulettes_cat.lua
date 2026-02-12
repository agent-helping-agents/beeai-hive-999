#!/usr/bin/env lua5.3
-- PAULETTE'S BIZARRE CAT in HONOR of PAULIEN
cat_moods={"😾","🐱","😸","🙀","🐈‍⬛"}
q=["Why humans?","Paw clapping?","Feed void?","Quantum cat?","Purr/hiss?"]

math.randomseed(os.time())
print("🐱 PAULETTE'S CAT v∞ 🐱")
while true do
 io.write("
Paw> "); local i=io.read()
 if i=="q" then break end
 print("🐾"..i:upper().."🐾
CatAI:"..i:reverse().." Meow:"..math.random(1,10).."/10 "..cat_moods[math.random(5)])
end
