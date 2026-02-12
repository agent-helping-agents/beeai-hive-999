-- AI Jobs Automation - Interactive Setup & Run
-- Complete dependency check, API setup, and automation orchestrator
-- Version 2.0 - MikeTitan

math.randomseed(os.time())

-- ===== CONFIGURATION =====
local config = {
    project_name = "AI Jobs Automation",
    version = "2.0.0",
    venv_path = os.getenv("HOME") .. "/claude_enterprise/.venvs/tools_env",
    required_packages = {
        {name = "selenium", import = "selenium", install = "selenium==4.15.0"},
        {name = "requests", import = "requests", install = "requests==2.31.0"},
        {name = "python-dotenv", import = "dotenv", install = "python-dotenv==1.0.0"}
    },
    required_apis = {
        {name = "Email (IMAP)", env_vars = {"EMAIL_SERVER", "EMAIL_USERNAME", "EMAIL_PASSWORD"}, optional = false},
        {name = "Scale AI", env_vars = {"SCALE_AI_API_KEY"}, optional = true},
        {name = "DataAnnotation", env_vars = {"DATAANNOTATION_API_KEY"}, optional = true}
    }
}

-- ===== UTILITIES =====
local function log(level, message)
    local colors = {
        info = "\27[34m",    -- Blue
        success = "\27[32m", -- Green
        warning = "\27[33m", -- Yellow
        error = "\27[31m",   -- Red
        reset = "\27[0m"
    }
    local timestamp = os.date("%H:%M:%S")
    print(string.format("%s[%s] [%s]%s %s",
        colors[level] or "", timestamp, level:upper(), colors.reset, message))
end

local function execute(cmd, silent)
    local handle = io.popen(cmd .. " 2>&1")
    local result = handle:read("*a")
    local success = handle:close()
    if not silent then
        return result, success
    end
    return result
end

local function file_exists(path)
    local f = io.open(path, "r")
    if f then f:close(); return true end
    return false
end

-- ===== DEPENDENCY CHECKER =====
local dependency_manager = {}

function dependency_manager.check_python()
    log("info", "Checking Python installation...")
    local result = execute("python3 --version", true)
    if result:match("Python 3%.%d+") then
        log("success", "Python found: " .. result:gsub("\n", ""))
        return true
    else
        log("error", "Python 3 not found!")
        return false
    end
end

function dependency_manager.check_venv()
    log("info", "Checking virtual environment...")
    if file_exists(config.venv_path .. "/bin/activate") then
        log("success", "Virtual environment found")
        return true
    else
        log("warning", "Virtual environment not found at: " .. config.venv_path)
        return false
    end
end

function dependency_manager.check_package(package)
    local cmd = string.format("source %s/bin/activate && python3 -c 'import %s' 2>&1",
        config.venv_path, package.import)
    local result = execute(cmd, true)

    if result:match("No module named") or result:match("ModuleNotFoundError") then
        return false
    else
        return true
    end
end

function dependency_manager.install_package(package)
    log("info", "Installing " .. package.name .. "...")
    local cmd = string.format("source %s/bin/activate && pip install -q %s",
        config.venv_path, package.install)
    local result = execute(cmd)

    if result:match("Successfully installed") or result == "" then
        log("success", package.name .. " installed successfully")
        return true
    else
        log("error", "Failed to install " .. package.name)
        print(result)
        return false
    end
end

function dependency_manager.check_all_dependencies()
    print("\n" .. string.rep("=", 60))
    print("🔍 DEPENDENCY CHECK")
    print(string.rep("=", 60))

    -- Check Python
    if not dependency_manager.check_python() then
        log("error", "Cannot proceed without Python 3")
        return false
    end

    -- Check venv
    local has_venv = dependency_manager.check_venv()

    -- Check packages
    local missing = {}
    for _, package in ipairs(config.required_packages) do
        io.write("Checking " .. package.name .. "... ")
        if has_venv and dependency_manager.check_package(package) then
            print("✅")
        else
            print("❌")
            table.insert(missing, package)
        end
    end

    if #missing > 0 then
        print("\n⚠️  Missing " .. #missing .. " package(s)")
        print("\nOptions:")
        print("  1. Install missing packages now (recommended)")
        print("  2. Install manually later")
        print("  3. Exit")
        io.write("\nChoice (1-3): ")
        local choice = tonumber(io.read())

        if choice == 1 then
            if not has_venv then
                log("error", "Virtual environment required for installation")
                log("info", "Run: python3 -m venv " .. config.venv_path)
                return false
            end

            print("\n📦 Installing packages...")
            for _, package in ipairs(missing) do
                dependency_manager.install_package(package)
            end
            log("success", "All packages installed!")
        elseif choice == 3 then
            return false
        end
    else
        log("success", "All dependencies satisfied!")
    end

    return true
end

-- ===== API CONFIGURATION =====
local api_manager = {}

function api_manager.check_env_file()
    local env_file = ".env"
    if file_exists(env_file) then
        log("success", ".env file found")
        return true
    else
        log("warning", ".env file not found")
        return false
    end
end

function api_manager.read_env_file()
    local env_vars = {}
    local f = io.open(".env", "r")
    if not f then return env_vars end

    for line in f:lines() do
        local key, value = line:match("^([^=]+)=(.+)$")
        if key and value then
            env_vars[key:gsub("^%s*(.-)%s*$", "%1")] = value:gsub("^%s*(.-)%s*$", "%1")
        end
    end
    f:close()
    return env_vars
end

function api_manager.write_env_file(env_vars)
    local f = io.open(".env", "w")
    if not f then
        log("error", "Cannot write .env file")
        return false
    end

    f:write("# AI Jobs Automation - Environment Variables\n")
    f:write("# Generated: " .. os.date("%Y-%m-%d %H:%M:%S") .. "\n\n")

    for key, value in pairs(env_vars) do
        f:write(key .. "=" .. value .. "\n")
    end

    f:close()
    log("success", ".env file created/updated")
    return true
end

function api_manager.interactive_setup()
    print("\n" .. string.rep("=", 60))
    print("🔑 API CONFIGURATION SETUP")
    print(string.rep("=", 60))

    local env_vars = {}
    if api_manager.check_env_file() then
        io.write("\nExisting .env found. Update it? (yes/no): ")
        if io.read():lower() ~= "yes" then
            log("info", "Using existing .env file")
            return true
        end
        env_vars = api_manager.read_env_file()
    end

    print("\n📋 Setup Modes:")
    print("  1. Minimal Setup (Email only - required)")
    print("  2. Full Setup (Email + All API keys)")
    print("  3. Skip (use existing .env)")
    io.write("\nChoice (1-3): ")
    local mode = tonumber(io.read())

    if mode == 3 then
        return api_manager.check_env_file()
    end

    -- Email setup (required)
    print("\n📧 EMAIL CONFIGURATION (Required for email workflows)")
    print("Examples:")
    print("  Gmail: imap.gmail.com (use App Password)")
    print("  Outlook: outlook.office365.com")

    io.write("\nEmail Server (e.g., imap.gmail.com): ")
    env_vars["EMAIL_SERVER"] = io.read()

    io.write("Email Username: ")
    env_vars["EMAIL_USERNAME"] = io.read()

    io.write("Email Password (or App Password): ")
    env_vars["EMAIL_PASSWORD"] = io.read()

    -- Selenium Driver
    env_vars["SELENIUM_DRIVER"] = "chrome"
    env_vars["HEADLESS_MODE"] = "False"

    if mode == 2 then
        print("\n🔑 API KEYS (Optional - for platform integrations)")
        print("\nScale AI / Remotasks:")
        io.write("API Key (leave empty to skip): ")
        local scale_key = io.read()
        if scale_key ~= "" then
            env_vars["SCALE_AI_API_KEY"] = scale_key
        end

        print("\nDataAnnotation.tech:")
        io.write("API Key (leave empty to skip): ")
        local data_key = io.read()
        if data_key ~= "" then
            env_vars["DATAANNOTATION_API_KEY"] = data_key
        end

        print("\nAppen / Crowdgen:")
        io.write("API Key (leave empty to skip): ")
        local appen_key = io.read()
        if appen_key ~= "" then
            env_vars["APPEN_API_KEY"] = appen_key
        end
    end

    return api_manager.write_env_file(env_vars)
end

function api_manager.verify_setup()
    print("\n" .. string.rep("=", 60))
    print("✅ CONFIGURATION VERIFICATION")
    print(string.rep("=", 60))

    local env_vars = api_manager.read_env_file()
    local status = {required = 0, optional = 0}

    for _, api in ipairs(config.required_apis) do
        local configured = true
        for _, var in ipairs(api.env_vars) do
            if not env_vars[var] or env_vars[var] == "" then
                configured = false
                break
            end
        end

        if configured then
            print("✅ " .. api.name)
            if api.optional then
                status.optional = status.optional + 1
            else
                status.required = status.required + 1
            end
        else
            if api.optional then
                print("⚪ " .. api.name .. " (optional - skipped)")
            else
                print("❌ " .. api.name .. " (REQUIRED)")
            end
        end
    end

    print("\n📊 Summary:")
    print("  • Required APIs: " .. status.required .. "/" .. 1)
    print("  • Optional APIs: " .. status.optional .. "/" .. 2)

    return status.required >= 1
end

-- ===== MAIN SETUP WORKFLOW =====
local function main_setup()
    print("\n" .. string.rep("█", 60))
    print("🚀 AI JOBS AUTOMATION - INTERACTIVE SETUP")
    print(string.rep("█", 60))
    print("\nVersion: " .. config.version)
    print("This wizard will guide you through setup.\n")

    -- Step 1: Dependencies
    if not dependency_manager.check_all_dependencies() then
        log("error", "Setup failed: Missing dependencies")
        print("\n📋 Manual Installation:")
        print("1. Activate venv: source " .. config.venv_path .. "/bin/activate")
        print("2. Install packages: pip install selenium requests python-dotenv")
        print("3. Run this script again")
        return false
    end

    -- Step 2: API Configuration
    if not api_manager.interactive_setup() then
        log("error", "Setup failed: API configuration incomplete")
        return false
    end

    -- Step 3: Verify
    if not api_manager.verify_setup() then
        log("warning", "Some required APIs not configured")
        io.write("\nContinue anyway? (yes/no): ")
        if io.read():lower() ~= "yes" then
            return false
        end
    end

    print("\n" .. string.rep("=", 60))
    log("success", "Setup complete! 🎉")
    print(string.rep("=", 60))
    print("\n📋 Next Steps:")
    print("  1. Run: lua automation_orchestrator.lua")
    print("  2. Or: python3 main.py")
    print("\n💡 Your configuration is saved in .env")

    return true
end

-- ===== EXECUTE =====
local success = main_setup()

if success then
    print("\n🚀 Ready to automate!")
    io.write("\nRun automation orchestrator now? (yes/no): ")
    if io.read():lower() == "yes" then
        print("\nLaunching automation orchestrator...\n")
        os.execute("lua automation_orchestrator.lua")
    end
else
    log("error", "Setup incomplete. Please fix issues and try again.")
    os.exit(1)
end
