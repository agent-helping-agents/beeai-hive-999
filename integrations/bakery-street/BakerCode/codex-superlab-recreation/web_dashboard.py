#!/usr/bin/env python3
"""
Codex-SuperLab Web Dashboard
Flask web interface for task management and progress tracking
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database setup
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('codex_superlab.db')
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            task_name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            progress INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Progress checks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            progress INTEGER,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT,
            subscription_tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks for a user"""
    user_id = request.args.get('user_id', 'default')
    
    conn = sqlite3.connect('codex_superlab.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, task_name, description, status, progress, created_at, updated_at
        FROM tasks 
        WHERE user_id = ?
        ORDER BY updated_at DESC
    ''', (user_id,))
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append({
            'id': row[0],
            'task_name': row[1],
            'description': row[2],
            'status': row[3],
            'progress': row[4],
            'created_at': row[5],
            'updated_at': row[6]
        })
    
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.json
    user_id = data.get('user_id', 'default')
    task_name = data.get('task_name')
    description = data.get('description', '')
    
    if not task_name:
        return jsonify({'error': 'Task name is required'}), 400
    
    conn = sqlite3.connect('codex_superlab.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (user_id, task_name, description)
        VALUES (?, ?, ?)
    ''', (user_id, task_name, description))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': task_id, 'message': 'Task created successfully'})

@app.route('/api/tasks/<int:task_id>/progress', methods=['POST'])
def update_progress():
    """Update task progress"""
    data = request.json
    progress = data.get('progress', 0)
    notes = data.get('notes', '')
    
    conn = sqlite3.connect('codex_superlab.db')
    cursor = conn.cursor()
    
    # Update task progress
    cursor.execute('''
        UPDATE tasks 
        SET progress = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (progress, task_id))
    
    # Add progress check record
    cursor.execute('''
        INSERT INTO progress_checks (task_id, progress, notes)
        VALUES (?, ?, ?)
    ''', (task_id, progress, notes))
    
    # Update status based on progress
    if progress >= 100:
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    elif progress > 0:
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('in_progress', task_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Progress updated successfully'})

@app.route('/api/ai/suggest', methods=['POST'])
def ai_suggest():
    """Get AI suggestions for task improvement"""
    data = request.json
    task_name = data.get('task_name', '')
    current_progress = data.get('progress', 0)
    
    prompt = f"""
    Task: {task_name}
    Current Progress: {current_progress}%
    
    Provide 3 specific, actionable suggestions to help complete this task.
    Focus on practical next steps and productivity tips.
    Keep each suggestion under 100 characters.
    
    Format as JSON array: ["suggestion1", "suggestion2", "suggestion3"]
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Try to parse as JSON, fallback to simple list
        try:
            suggestions = json.loads(response.text)
        except:
            # Fallback parsing
            suggestions = [
                "Break the task into smaller, manageable steps",
                "Set a specific deadline and work backwards",
                "Remove distractions and focus for 25-minute blocks"
            ]
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        return jsonify({'error': f'AI suggestion failed: {str(e)}'}), 500

@app.route('/api/analytics')
def analytics():
    """Get analytics data"""
    user_id = request.args.get('user_id', 'default')
    
    conn = sqlite3.connect('codex_superlab.db')
    cursor = conn.cursor()
    
    # Task statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_tasks,
            AVG(progress) as avg_progress
        FROM tasks 
        WHERE user_id = ?
    ''', (user_id,))
    
    stats = cursor.fetchone()
    
    # Recent activity
    cursor.execute('''
        SELECT task_name, progress, updated_at
        FROM tasks 
        WHERE user_id = ?
        ORDER BY updated_at DESC
        LIMIT 5
    ''', (user_id,))
    
    recent_activity = []
    for row in cursor.fetchall():
        recent_activity.append({
            'task_name': row[0],
            'progress': row[1],
            'updated_at': row[2]
        })
    
    conn.close()
    
    return jsonify({
        'total_tasks': stats[0] or 0,
        'completed_tasks': stats[1] or 0,
        'in_progress_tasks': stats[2] or 0,
        'avg_progress': round(stats[3] or 0, 1),
        'recent_activity': recent_activity
    })

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Create templates directory and basic HTML templates
def create_templates():
    """Create basic HTML templates"""
    os.makedirs('templates', exist_ok=True)
    
    # Dashboard template
    dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codex-SuperLab Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .task-form { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .task-list { background: white; padding: 20px; border-radius: 8px; }
        .task-item { border-bottom: 1px solid #eee; padding: 10px 0; }
        .progress-bar { width: 100%; height: 20px; background: #eee; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: #27ae60; transition: width 0.3s; }
        button { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Codex-SuperLab Dashboard</h1>
            <p>AI-Powered Progress Tracking & Task Management</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3>Total Tasks</h3>
                <div id="total-tasks">0</div>
            </div>
            <div class="stat-card">
                <h3>Completed</h3>
                <div id="completed-tasks">0</div>
            </div>
            <div class="stat-card">
                <h3>In Progress</h3>
                <div id="in-progress-tasks">0</div>
            </div>
            <div class="stat-card">
                <h3>Avg Progress</h3>
                <div id="avg-progress">0%</div>
            </div>
        </div>
        
        <div class="task-form">
            <h3>Add New Task</h3>
            <input type="text" id="task-name" placeholder="Task name" required>
            <textarea id="task-description" placeholder="Task description (optional)"></textarea>
            <button onclick="createTask()">Create Task</button>
        </div>
        
        <div class="task-list">
            <h3>Your Tasks</h3>
            <div id="tasks-container">
                Loading tasks...
            </div>
        </div>
    </div>

    <script>
        // Load dashboard data
        async function loadDashboard() {
            try {
                // Load analytics
                const analyticsResponse = await fetch('/api/analytics?user_id=default');
                const analytics = await analyticsResponse.json();
                
                document.getElementById('total-tasks').textContent = analytics.total_tasks;
                document.getElementById('completed-tasks').textContent = analytics.completed_tasks;
                document.getElementById('in-progress-tasks').textContent = analytics.in_progress_tasks;
                document.getElementById('avg-progress').textContent = analytics.avg_progress + '%';
                
                // Load tasks
                const tasksResponse = await fetch('/api/tasks?user_id=default');
                const tasks = await tasksResponse.json();
                
                const container = document.getElementById('tasks-container');
                if (tasks.length === 0) {
                    container.innerHTML = '<p>No tasks yet. Create your first task above!</p>';
                } else {
                    container.innerHTML = tasks.map(task => `
                        <div class="task-item">
                            <h4>${task.task_name}</h4>
                            <p>${task.description || 'No description'}</p>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${task.progress}%"></div>
                            </div>
                            <p>Progress: ${task.progress}% - Status: ${task.status}</p>
                            <button onclick="updateProgress(${task.id}, ${task.progress + 10})">+10% Progress</button>
                            <button onclick="getSuggestions('${task.task_name}', ${task.progress})">AI Suggestions</button>
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        // Create new task
        async function createTask() {
            const taskName = document.getElementById('task-name').value;
            const taskDescription = document.getElementById('task-description').value;
            
            if (!taskName) {
                alert('Please enter a task name');
                return;
            }
            
            try {
                const response = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: 'default',
                        task_name: taskName,
                        description: taskDescription
                    })
                });
                
                if (response.ok) {
                    document.getElementById('task-name').value = '';
                    document.getElementById('task-description').value = '';
                    loadDashboard(); // Reload dashboard
                } else {
                    alert('Error creating task');
                }
            } catch (error) {
                console.error('Error creating task:', error);
                alert('Error creating task');
            }
        }
        
        // Update task progress
        async function updateProgress(taskId, newProgress) {
            newProgress = Math.min(100, Math.max(0, newProgress));
            
            try {
                const response = await fetch(`/api/tasks/${taskId}/progress`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        progress: newProgress,
                        notes: `Progress updated to ${newProgress}%`
                    })
                });
                
                if (response.ok) {
                    loadDashboard(); // Reload dashboard
                } else {
                    alert('Error updating progress');
                }
            } catch (error) {
                console.error('Error updating progress:', error);
                alert('Error updating progress');
            }
        }
        
        // Get AI suggestions
        async function getSuggestions(taskName, progress) {
            try {
                const response = await fetch('/api/ai/suggest', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        task_name: taskName,
                        progress: progress
                    })
                });
                
                const data = await response.json();
                if (data.suggestions) {
                    alert('AI Suggestions:\\n\\n' + data.suggestions.join('\\n\\n'));
                } else {
                    alert('Error getting AI suggestions');
                }
            } catch (error) {
                console.error('Error getting suggestions:', error);
                alert('Error getting AI suggestions');
            }
        }
        
        // Load dashboard on page load
        loadDashboard();
    </script>
</body>
</html>
    '''
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)

if __name__ == '__main__':
    create_templates()
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')