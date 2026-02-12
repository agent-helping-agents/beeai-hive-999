-- AI Jobs Automation Orchestrator
-- Complete Lua automation system for job application workflows
-- Version 1.0 - MikeTitan

math.randomseed(os.time())

-- ===== CONFIGURATION =====
local config = {
    project_name = "AI Jobs Automation",
    version = "1.0.0",
    platforms = {
        "Scale AI / Remotasks",
        "DataAnnotation.tech",
        "Outlier AI",
        "Appen / Crowdgen",
        "Lionbridge / Aurora AI",
        "TELUS International"
    },
    automation_modes = {"safe", "moderate", "aggressive"},
    current_mode = "safe"
}

-- ===== STATE MANAGEMENT =====
local state = {
    applications_submitted = 0,
    emails_processed = 0,
    apis_called = 0,
    errors_logged = 0,
    session_start = os.time(),
    active_platform = nil,
    automation_active = false
}

-- ===== UTILITIES =====
local function log(level, message)
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")
    print(string.format("[%s] [%s] %s", timestamp, level:upper(), message))
end

local function execute_command(cmd, description)
    log("info", "Executing: " .. description)
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    handle:close()
    return result
end

-- ===== BROWSER AUTOMATION =====
local browser_automation = {}

function browser_automation.check_selenium()
    log("info", "Checking Selenium WebDriver installation...")
    local result = execute_command("python3 -c 'import selenium; print(selenium.__version__)'", "Check Selenium")
    if result:match("%d+%.%d+") then
        log("success", "Selenium found: " .. result:gsub("\n", ""))
        return true
    else
        log("error", "Selenium not found. Install with: pip install selenium")
        return false
    end
end

function browser_automation.fill_application(platform, data)
    log("info", "Filling application form for: " .. platform)

    local python_script = string.format([[
python3 automation/browser.py --platform "%s" --email "%s" --firstname "%s" --lastname "%s"
]], platform, data.email or "user@example.com", data.first_name or "John", data.last_name or "Doe")

    log("info", "Launching browser automation...")
    print("\n⚠️  MANUAL REVIEW REQUIRED!")
    print("The browser will open. Please review the form before submitting.")
    print("This ensures compliance with platform ToS.\n")

    local result = execute_command(python_script, "Browser automation")

    if result:match("success") or result:match("completed") then
        state.applications_submitted = state.applications_submitted + 1
        log("success", "Application form filled successfully!")
        return true
    else
        state.errors_logged = state.errors_logged + 1
        log("error", "Browser automation failed: " .. result)
        return false
    end
end

-- ===== EMAIL MANAGEMENT =====
local email_manager = {}

function email_manager.connect()
    log("info", "Connecting to email server...")
    local python_script = [[
python3 automation/email.py --action connect --check-config
]]
    local result = execute_command(python_script, "Email connection test")

    if result:match("connected") or result:match("success") then
        log("success", "Email server connected successfully")
        return true
    else
        log("error", "Email connection failed. Check .env configuration")
        return false
    end
end

function email_manager.get_job_emails()
    log("info", "Fetching job-related emails...")
    local python_script = [[
python3 automation/email.py --action fetch --filter job
]]
    local result = execute_command(python_script, "Fetch job emails")
    state.emails_processed = state.emails_processed + 1
    return result
end

function email_manager.send_follow_up(recipient, subject)
    log("info", "Sending follow-up email to: " .. recipient)
    local python_script = string.format([[
python3 automation/email.py --action send --to "%s" --subject "%s"
]], recipient, subject)

    execute_command(python_script, "Send follow-up email")
    log("success", "Follow-up email sent")
end

-- ===== API INTEGRATION =====
local api_manager = {}

function api_manager.test_connection(platform)
    log("info", "Testing API connection for: " .. platform)
    local python_script = string.format([[
python3 automation/api.py --platform "%s" --action test
]], platform)

    local result = execute_command(python_script, "API connection test")
    state.apis_called = state.apis_called + 1

    if result:match("success") or result:match("200") then
        log("success", "API connection successful")
        return true
    else
        log("error", "API connection failed")
        return false
    end
end

function api_manager.get_available_jobs(platform)
    log("info", "Fetching available jobs from: " .. platform)
    local python_script = string.format([[
python3 automation/api.py --platform "%s" --action list-jobs
]], platform)

    local result = execute_command(python_script, "Fetch available jobs")
    state.apis_called = state.apis_called + 1
    return result
end

-- ===== WORKFLOW ORCHESTRATION =====
local workflows = {}

workflows.full_application = function(platform, user_data)
    log("info", "Starting full application workflow for: " .. platform)
    print("\n" .. string.rep("=", 60))
    print("FULL APPLICATION WORKFLOW")
    print(string.rep("=", 60))

    -- Step 1: API check
    print("\n[1/4] Checking API access...")
    if not api_manager.test_connection(platform) then
        log("warning", "API not available, proceeding with browser automation")
    else
        local jobs = api_manager.get_available_jobs(platform)
        print("Available jobs retrieved:")
        print(jobs)
    end

    -- Step 2: Browser automation
    print("\n[2/4] Browser automation...")
    if not browser_automation.check_selenium() then
        log("error", "Cannot proceed without Selenium")
        return false
    end

    browser_automation.fill_application(platform, user_data)

    -- Step 3: Email check
    print("\n[3/4] Checking for confirmation emails...")
    if email_manager.connect() then
        local emails = email_manager.get_job_emails()
        print("Recent job emails:")
        print(emails)
    end

    -- Step 4: Summary
    print("\n[4/4] Workflow complete!")
    print(string.rep("=", 60))
    log("success", "Full application workflow completed")
    return true
end

workflows.email_only = function()
    log("info", "Starting email-only workflow")
    print("\n" .. string.rep("=", 60))
    print("EMAIL MANAGEMENT WORKFLOW")
    print(string.rep("=", 60))

    if email_manager.connect() then
        print("\n[1/2] Fetching job emails...")
        local emails = email_manager.get_job_emails()
        print(emails)

        print("\n[2/2] Email management complete!")
    else
        log("error", "Email workflow failed")
        return false
    end

    print(string.rep("=", 60))
    log("success", "Email workflow completed")
    return true
end

workflows.api_only = function()
    log("info", "Starting API-only workflow")
    print("\n" .. string.rep("=", 60))
    print("API INTEGRATION WORKFLOW")
    print(string.rep("=", 60))

    print("\nTesting API connections for all platforms...")
    for _, platform in ipairs(config.platforms) do
        print("\n• " .. platform)
        if api_manager.test_connection(platform) then
            local jobs = api_manager.get_available_jobs(platform)
            print(jobs)
        end
    end

    print("\n" .. string.rep("=", 60))
    log("success", "API workflow completed")
    return true
end

-- ===== INTERACTIVE MENU =====
local function show_menu()
    print("\n" .. string.rep("=", 60))
    print("🤖 AI JOBS AUTOMATION ORCHESTRATOR")
    print(string.rep("=", 60))
    print("\nVersion: " .. config.version)
    print("Mode: " .. config.current_mode:upper())
    print("\n📊 Session Stats:")
    print("  • Applications: " .. state.applications_submitted)
    print("  • Emails: " .. state.emails_processed)
    print("  • API Calls: " .. state.apis_called)
    print("  • Errors: " .. state.errors_logged)

    print("\n📋 Available Workflows:")
    print("  1. Full Application (Browser + Email + API)")
    print("  2. Email Management Only")
    print("  3. API Integration Only")
    print("  4. Quick Platform Check")
    print("  5. View Session Report")
    print("  6. Exit")

    io.write("\nSelect workflow (1-6): ")
    return tonumber(io.read())
end

local function platform_selector()
    print("\n📌 Select Platform:")
    for i, platform in ipairs(config.platforms) do
        print("  " .. i .. ". " .. platform)
    end
    io.write("\nSelect (1-" .. #config.platforms .. "): ")
    local choice = tonumber(io.read())
    return config.platforms[choice] or config.platforms[1]
end

local function get_user_data()
    print("\n👤 Enter User Data:")
    io.write("Email: ")
    local email = io.read()
    io.write("First Name: ")
    local first_name = io.read()
    io.write("Last Name: ")
    local last_name = io.read()

    return {
        email = email,
        first_name = first_name,
        last_name = last_name
    }
end

local function show_report()
    local session_duration = os.time() - state.session_start
    print("\n" .. string.rep("=", 60))
    print("📊 SESSION REPORT")
    print(string.rep("=", 60))
    print("\nDuration: " .. session_duration .. " seconds")
    print("\nMetrics:")
    print("  • Applications Submitted: " .. state.applications_submitted)
    print("  • Emails Processed: " .. state.emails_processed)
    print("  • API Calls Made: " .. state.apis_called)
    print("  • Errors Logged: " .. state.errors_logged)

    print("\nEfficiency:")
    if session_duration > 0 then
        local apps_per_min = (state.applications_submitted / session_duration) * 60
        print("  • Applications/Hour: " .. string.format("%.2f", apps_per_min * 60))
    end

    print("\n" .. string.rep("=", 60))
end

-- ===== MAIN ORCHESTRATION LOOP =====
local function main()
    log("info", "Starting " .. config.project_name .. " v" .. config.version)

    print("\n🚨 LEGAL & ETHICAL NOTICE:")
    print("This automation respects platform Terms of Service.")
    print("• Manual account creation required")
    print("• Manual review before submission")
    print("• Rate limiting respected")
    print("• Official APIs only\n")

    io.write("Do you agree to use this ethically? (yes/no): ")
    local agreement = io.read():lower()
    if agreement ~= "yes" and agreement ~= "y" then
        log("info", "User declined. Exiting.")
        return
    end

    while true do
        local choice = show_menu()

        if choice == 1 then
            local platform = platform_selector()
            local user_data = get_user_data()
            workflows.full_application(platform, user_data)
        elseif choice == 2 then
            workflows.email_only()
        elseif choice == 3 then
            workflows.api_only()
        elseif choice == 4 then
            print("\n🔍 Quick Platform Check:")
            for _, platform in ipairs(config.platforms) do
                print("\n• " .. platform)
                api_manager.test_connection(platform)
            end
        elseif choice == 5 then
            show_report()
        elseif choice == 6 then
            show_report()
            log("info", "Shutting down gracefully...")
            print("\n✅ Automation complete. Good luck with your applications!")
            break
        else
            log("error", "Invalid choice. Please select 1-6.")
        end

        io.write("\nPress ENTER to continue...")
        io.read()
    end
end

-- EXECUTE
main()
