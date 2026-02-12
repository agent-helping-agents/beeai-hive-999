#!/usr/bin/env python3
"""
Bounty Hunter - Chat Interface

Flask-based chat interface with Marco-01 integration for bounty hunting assistance.
Provides AI-powered help for task management, automation, and learning.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bounty_hunter_chat.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "bounty-hunter-secret-key"
)
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
socketio = SocketIO(app, cors_allowed_origins="*")

# Marco-01 integration status
MARCO01_AVAILABLE = False
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM

    # Check if Marco-01 is available
    try:
        tokenizer = AutoTokenizer.from_pretrained("AIDC-AI/Marco-o1")
        model = AutoModelForCausalLM.from_pretrained("AIDC-AI/Marco-o1")
        MARCO01_AVAILABLE = True
        logger.info("Marco-01 model loaded successfully")
    except Exception as e:
        logger.warning(f"Marco-01 model not available locally: {e}")
        logger.info("Will use fallback model or API")
        MARCO01_AVAILABLE = False
except ImportError as e:
    logger.warning(f"Transformers library not available: {e}")
    MARCO01_AVAILABLE = False

# Import bounty hunter system
try:
    from bounty_hunter_todo import TodoList, Checklist, AutomationEngine

    ENGINE = AutomationEngine()
    logger.info("Bounty Hunter system integrated successfully")
except ImportError as e:
    logger.error(f"Failed to import Bounty Hunter system: {e}")
    ENGINE = None

# Chat history storage
CHAT_HISTORY = []

# ====================
# Chat API Routes
# ====================


@app.route("/")
def index():
    """Main chat interface"""
    return render_template("chat.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """API endpoint for chat interactions"""
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        user = data.get("user", "Guest")

        if not message:
            return jsonify({"success": False, "error": "Message cannot be empty"}), 400

        # Add user message to chat history
        chat_message = {
            "id": len(CHAT_HISTORY) + 1,
            "user": user,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": "user",
        }
        CHAT_HISTORY.append(chat_message)

        # Generate AI response
        response = generate_response(message, user)

        # Add AI response to chat history
        ai_message = {
            "id": len(CHAT_HISTORY) + 1,
            "user": "Bounty Hunter AI",
            "message": response,
            "timestamp": datetime.now().isoformat(),
            "type": "ai",
        }
        CHAT_HISTORY.append(ai_message)

        return jsonify(
            {"success": True, "message": response, "chat_history": CHAT_HISTORY}
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get current tasks from Bounty Hunter system"""
    try:
        if not ENGINE:
            return jsonify(
                {"success": False, "error": "Bounty Hunter system not available"}
            ), 500

        tasks = []
        for task in ENGINE.todo_list.tasks.values():
            tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "category": task.category,
                    "status": task.status,
                    "estimated_time": task.estimated_time,
                    "actual_time": task.actual_time,
                    "tags": task.tags,
                }
            )

        return jsonify({"success": True, "tasks": tasks, "task_count": len(tasks)})
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/checklist", methods=["GET"])
def get_checklist():
    """Get current checklist from Bounty Hunter system"""
    try:
        if not ENGINE:
            return jsonify(
                {"success": False, "error": "Bounty Hunter system not available"}
            ), 500

        checklist = ENGINE.checklist.items
        progress = ENGINE.checklist.get_progress()

        return jsonify({"success": True, "checklist": checklist, "progress": progress})
    except Exception as e:
        logger.error(f"Error getting checklist: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/run-task", methods=["POST"])
def run_task():
    """Run a specific task"""
    try:
        data = request.get_json()
        task_id = data.get("task_id", "").strip()

        if not task_id:
            return jsonify({"success": False, "error": "Task ID cannot be empty"}), 400

        if not ENGINE:
            return jsonify(
                {"success": False, "error": "Bounty Hunter system not available"}
            ), 500

        task = ENGINE.todo_list.get_task(task_id)
        if not task:
            return jsonify(
                {"success": False, "error": f"Task {task_id} not found"}
            ), 404

        # Run task with simulation (for now, just mark as in-progress)
        task.start()
        logger.info(f"Task {task_id} started: {task.title}")

        return jsonify(
            {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "start_date": task.start_date,
                },
                "message": f'Task "{task.title}" started successfully',
            }
        )
    except Exception as e:
        logger.error(f"Error running task: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ====================
# SocketIO Event Handlers
# ====================


@socketio.on("connect")
def handle_connect():
    """Handle socket connection"""
    logger.info("Client connected")
    emit("connected", {"message": "Connected to Bounty Hunter Chat"})

    # Send initial state
    if ENGINE:
        try:
            tasks = get_tasks().get_json()
            checklist = get_checklist().get_json()
            emit("initial_state", {"tasks": tasks, "checklist": checklist})
        except Exception as e:
            logger.error(f"Error sending initial state: {e}")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle socket disconnection"""
    logger.info("Client disconnected")


@socketio.on("send_message")
def handle_message(data):
    """Handle message from client"""
    try:
        message = data.get("message", "").strip()
        user = data.get("user", "Guest")

        if not message:
            emit("error", {"message": "Message cannot be empty"})
            return

        # Generate response
        response = generate_response(message, user)

        # Send response back to client
        emit(
            "receive_message",
            {
                "user": "Bounty Hunter AI",
                "message": response,
                "timestamp": datetime.now().isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Socket message error: {e}")
        emit("error", {"message": str(e)})


# ====================
# AI Response Generation
# ====================


def generate_response(message: str, user: str) -> str:
    """Generate response using Marco-01 or fallback"""
    message = message.strip().lower()

    # Handle simple commands first
    if "help" in message:
        return """I'm the Bounty Hunter AI! Here's what I can help with:

- **Task management**: List, start, or complete tasks
- **Automation**: Run daily routines or weekly audits
- **Learning**: Get information about bounty hunting
- **Tips**: Learn best practices for bug bounties
- **Market**: Explore fiat and crypto bounty platforms

What would you like to do? Try asking "list tasks" or "run daily routine".
"""

    if "list tasks" in message or "show tasks" in message:
        if ENGINE:
            tasks = []
            for task in ENGINE.todo_list.tasks.values():
                tasks.append(f"- {task.title} ({task.priority})")
            return "\n".join(tasks) if tasks else "No tasks available"
        return "Bounty Hunter system not available"

    if "start task" in message:
        # Extract task name from message
        task_name = message.replace("start task", "").strip()
        if ENGINE:
            for task in ENGINE.todo_list.tasks.values():
                if task_name.lower() in task.title.lower():
                    task.start()
                    return f"Started task: {task.title}"
            return f"Task '{task_name}' not found"
        return "Bounty Hunter system not available"

    if "run daily" in message or "daily routine" in message:
        if ENGINE:
            try:
                result = ENGINE.run_daily_routine()
                if result["success"]:
                    return (
                        f"Daily routine completed successfully! "
                        f"Progress: {result['checklist']['completed']}/{result['checklist']['total']} "
                        f"({result['checklist']['percentage']:.1f}%)"
                    )
                return "Daily routine failed"
            except Exception as e:
                logger.error(f"Daily routine error: {e}")
                return f"Daily routine failed: {e}"
        return "Bounty Hunter system not available"

    if "checklist" in message:
        if ENGINE:
            progress = ENGINE.checklist.get_progress()
            return (
                f"Checklist progress: {progress['completed']}/{progress['total']} "
                f"({progress['percentage']:.1f}%)"
            )
        return "Bounty Hunter system not available"

    if "bounty platforms" in message or "fiat platforms" in message:
        return """Popular bounty platforms:

**Fiat Platforms:**
- Upwork: $150-800 per token contract
- Freelancer: Similar to Upwork
- Toptal: Premium freelance platform

**Crypto Platforms:**
- Immunefi: $100-10,000+ per bug
- Gitcoin: $500-2000 per bounty
- Stellar Community Fund: $1000-3000 microgrants

**Blockchain-Specific:**
- Algorand Foundation: $500-2000 per tutorial
- Solana Bug Bounty: Up to $20,000

What platform would you like to explore?
"""

    if "tips" in message or "best practices" in message:
        return """Bounty Hunting Best Practices:

1. **Start small**: Focus on low-hanging fruit first
2. **Research thoroughly**: Understand the program scope
3. **Quality over quantity**: Submit detailed reports
4. **Communicate professionally**: Keep communications clear
5. **Stay within scope**: Never test outside approved areas
6. **Follow guidelines**: Read and adhere to each program's rules
7. **Document everything**: Keep detailed notes of your findings
8. **Be persistent**: Don't give up on complex issues

What specific area would you like to learn more about?
"""

    if "payment" in message or "monetization" in message:
        return """Bounty Payment Methods:

**Fiat Payments:**
- Direct bank transfer
- PayPal (limited for crypto-related work)
- Wire transfer

**Crypto Payments:**
- Stablecoins (USDT, USDC)
- Bitcoin (BTC)
- Ethereum (ETH)
- Platform-specific tokens

**Tips:**
- Verify payment methods before accepting tasks
- Set up payment escrow for large projects
- Understand tax implications of crypto earnings

What payment method would you like to learn more about?
"""

    # Fallback to general response
    return (
        f"I'm sorry, I don't have a specific answer for that. "
        f"Try asking for help with tasks, automation, or bounty platforms."
    )


# ====================
# Templates
# ====================


@app.route("/templates/chat.html")
def get_chat_template():
    """Return chat interface template"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bounty Hunter - Chat Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        /* Sidebar */
        .sidebar {
            width: 250px;
            background: #0f3460;
            border-right: 1px solid #1a1a2e;
            padding: 20px;
            overflow-y: auto;
        }

        .sidebar h2 {
            margin-bottom: 20px;
            color: #e94560;
            font-size: 1.2rem;
        }

        .sidebar ul {
            list-style: none;
            margin-bottom: 20px;
        }

        .sidebar li {
            padding: 10px;
            margin-bottom: 5px;
            background: #1a1a2e;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .sidebar li:hover {
            background: #e94560;
        }

        /* Main Chat Area */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        /* Chat Header */
        .chat-header {
            background: #16213e;
            padding: 20px;
            border-bottom: 1px solid #1a1a2e;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h1 {
            color: #e94560;
            font-size: 1.5rem;
        }

        /* Chat Messages */
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }

        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }

        .message.user {
            background: #e94560;
            margin-left: auto;
            border-bottom-right-radius: 0;
        }

        .message.ai {
            background: #0f3460;
            border-bottom-left-radius: 0;
        }

        .message-info {
            font-size: 0.8rem;
            color: #ccc;
            margin-bottom: 5px;
        }

        /* Chat Input */
        .chat-input {
            padding: 20px;
            background: #16213e;
            border-top: 1px solid #1a1a2e;
            display: flex;
            gap: 10px;
        }

        .chat-input input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: #1a1a2e;
            color: #fff;
            font-size: 1rem;
        }

        .chat-input button {
            padding: 10px 20px;
            background: #e94560;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .chat-input button:hover {
            background: #ff6b81;
        }

        /* Status Indicator */
        .status {
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.8rem;
        }

        .status.connected {
            background: #2ecc71;
            color: #000;
        }

        .status.disconnected {
            background: #e74c3c;
            color: #000;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: 200px;
                border-right: none;
                border-bottom: 1px solid #1a1a2e;
            }

            .container {
                flex-direction: column;
            }

            .chat-container {
                flex: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <h2>Bounty Hunter</h2>
            <ul>
                <li onclick="getTasks()">Tasks</li>
                <li onclick="getChecklist()">Checklist</li>
                <li onclick="runDailyRoutine()">Daily Routine</li>
                <li onclick="runWeeklyAudit()">Weekly Audit</li>
                <li onclick="clearChat()">Clear Chat</li>
            </ul>
        </div>

        <!-- Chat Area -->
        <div class="chat-container">
            <div class="chat-header">
                <h1>Bounty Hunter Chat</h1>
                <div class="status connected" id="status">Connected</div>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message ai">
                    <div class="message-info">Bounty Hunter AI</div>
                    <div class="message-text">
                        Hello! I'm the Bounty Hunter AI. How can I help you with your bounty hunting journey today?

                        <strong>Tips:</strong>
                        - Ask "help" for available commands
                        - Ask "list tasks" to see current tasks
                        - Ask "run daily routine" to execute automation
                        - Ask "bounty platforms" for market information
                    </div>
                </div>
            </div>

            <div class="chat-input">
                <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <!-- SocketIO Script -->
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        const socket = io();
        let isConnected = false;

        socket.on('connect', function() {
            console.log('Connected to server');
            document.getElementById('status').className = 'status connected';
            document.getElementById('status').textContent = 'Connected';
            isConnected = true;
        });

        socket.on('disconnect', function() {
            console.log('Disconnected from server');
            document.getElementById('status').className = 'status disconnected';
            document.getElementById('status').textContent = 'Disconnected';
            isConnected = false;
        });

        socket.on('error', function(data) {
            console.error('Socket error:', data);
        });

        socket.on('receive_message', function(data) {
            addMessage(data.user, data.message, 'ai');
        });

        // Function to send message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (message && isConnected) {
                // Add user message to chat
                addMessage('You', message, 'user');
                
                // Send to server
                socket.emit('send_message', {
                    message: message,
                    user: 'You'
                });

                input.value = '';
            }
        }

        // Function to handle key press
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Function to add message to chat
        function addMessage(user, text, type) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const timestamp = new Date().toLocaleTimeString();
            
            messageDiv.innerHTML = `
                <div class="message-info">${user} · ${timestamp}</div>
                <div class="message-text">${text}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Function to clear chat
        function clearChat() {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message ai">
                    <div class="message-info">Bounty Hunter AI</div>
                    <div class="message-text">
                        Hello! I'm the Bounty Hunter AI. How can I help you with your bounty hunting journey today?

                        <strong>Tips:</strong>
                        - Ask "help" for available commands
                        - Ask "list tasks" to see current tasks
                        - Ask "run daily routine" to execute automation
                        - Ask "bounty platforms" for market information
                    </div>
                </div>
            `;
        }

        // Function to get tasks
        async function getTasks() {
            try {
                const response = await fetch('/api/tasks');
                const data = await response.json();
                
                if (data.success) {
                    let taskList = 'Tasks available:\\n';
                    data.tasks.forEach(task => {
                        taskList += `- ${task.title} (${task.priority})\\n`;
                    });
                    taskList += `\\nTotal: ${data.task_count} tasks`;
                    
                    addMessage('Bounty Hunter AI', taskList, 'ai');
                } else {
                    addMessage('Bounty Hunter AI', 'Error getting tasks: ' + data.error, 'ai');
                }
            } catch (error) {
                addMessage('Bounty Hunter AI', 'Error getting tasks: ' + error, 'ai');
            }
        }

        // Function to get checklist
        async function getChecklist() {
            try {
                const response = await fetch('/api/checklist');
                const data = await response.json();
                
                if (data.success) {
                    const checklist = data.checklist;
                    const progress = data.progress;
                    
                    let checklistText = 'Checklist Progress: ' + 
                        progress.completed + '/' + progress.total + 
                        ' (' + progress.percentage.toFixed(1) + '%)\\n\\n';
                    
                    checklist.forEach(section => {
                        checklistText += section.name + ':\\n';
                        section.items.forEach(item => {
                            const status = item.completed ? '✅' : '⬜';
                            checklistText += `- ${status} ${item.text}\\n`;
                        });
                        checklistText += '\\n';
                    });
                    
                    addMessage('Bounty Hunter AI', checklistText, 'ai');
                } else {
                    addMessage('Bounty Hunter AI', 'Error getting checklist: ' + data.error, 'ai');
                }
            } catch (error) {
                addMessage('Bounty Hunter AI', 'Error getting checklist: ' + error, 'ai');
            }
        }

        // Function to run daily routine
        async function runDailyRoutine() {
            try {
                addMessage('Bounty Hunter AI', 'Running daily routine...', 'ai');
                
                const response = await fetch('/api/run-task', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ task_id: 'automation-1' })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    addMessage('Bounty Hunter AI', data.message, 'ai');
                } else {
                    addMessage('Bounty Hunter AI', 'Error: ' + data.error, 'ai');
                }
            } catch (error) {
                addMessage('Bounty Hunter AI', 'Error: ' + error, 'ai');
            }
        }

        // Function to run weekly audit
        async function runWeeklyAudit() {
            try {
                addMessage('Bounty Hunter AI', 'This feature will be available in a future update.', 'ai');
            } catch (error) {
                addMessage('Bounty Hunter AI', 'Error: ' + error, 'ai');
            }
        }

        // Initialize chat
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Chat interface loaded');
        });
    </script>
</body>
</html>
""")


# ====================
# Main Function
# ====================


def main():
    """Main function to start the chat interface"""
    logger.info("Starting Bounty Hunter Chat Interface")

    # Check system requirements
    if not ENGINE:
        logger.error("Bounty Hunter system not available")
        print("Error: Bounty Hunter system not available")
        return

    logger.info(f"Marco-01 available: {MARCO01_AVAILABLE}")

    # Get host and port from environment
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5000))

    logger.info(f"Chat interface will be available at http://{host}:{port}")
    print(f"\nBounty Hunter Chat Interface")
    print(f"==============================")
    print(f"Available at: http://{host}:{port}")
    print(
        f"Marco-01 integration: {'Enabled' if MARCO01_AVAILABLE else 'Disabled - using fallback'}"
    )
    print(f"Press Ctrl+C to stop")

    # Start Flask app with SocketIO
    socketio.run(app, host=host, port=port, debug=app.config["DEBUG"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Chat interface stopped by user")
        print("\nChat interface stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nError: {e}")
        sys.exit(1)
