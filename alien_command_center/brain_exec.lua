-- Alien Lua Sandbox
function execute_snippet(code)
    print("🛸 BOOTING LUA CORE...")
    local chunk, err = load(code)
    if not chunk then
        return "LUA SYNTAX ERR: " .. err
    end
    
    local status, res = pcall(chunk)
    if not status then
        return "LUA RUNTIME ERR: " .. res
    end
    return "RESULT: " .. tostring(res)
end
