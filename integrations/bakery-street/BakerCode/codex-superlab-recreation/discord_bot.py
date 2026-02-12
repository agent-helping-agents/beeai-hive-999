#!/usr/bin/env python3
"""
Codex-SuperLab Discord Auto-Checker Bot
Based on original 8.9K LOC implementation
Commands: !progress, !check, !blueprint
"""

import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class ProgressTracker:
    def __init__(self):
        self.tasks = {}
        self.blueprints = {}
        self.load_data()
    
    def load_data(self):
        """Load tasks and blueprints from storage"""
        try:
            if os.path.exists('tasks.json'):
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
            if os.path.exists('blueprints.json'):
                with open('blueprints.json', 'r') as f:
                    self.blueprints = json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def save_data(self):
        """Save tasks and blueprints to storage"""
        try:
            with open('tasks.json', 'w') as f:
                json.dump(self.tasks, f, indent=2)
            with open('blueprints.json', 'w') as f:
                json.dump(self.blueprints, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def add_task(self, user_id, task_name, description=""):
        """Add a new task for tracking"""
        if user_id not in self.tasks:
            self.tasks[user_id] = {}
        
        self.tasks[user_id][task_name] = {
            'description': description,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'progress': 0,
            'checks': []
        }
        self.save_data()
    
    def update_progress(self, user_id, task_name, progress, check_result=""):
        """Update task progress"""
        if user_id in self.tasks and task_name in self.tasks[user_id]:
            self.tasks[user_id][task_name]['progress'] = progress
            self.tasks[user_id][task_name]['checks'].append({
                'timestamp': datetime.now().isoformat(),
                'progress': progress,
                'result': check_result
            })
            
            if progress >= 100:
                self.tasks[user_id][task_name]['status'] = 'completed'
            elif progress > 0:
                self.tasks[user_id][task_name]['status'] = 'in_progress'
            
            self.save_data()
            return True
        return False

# Initialize progress tracker
tracker = ProgressTracker()

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is ready and monitoring {len(bot.guilds)} servers')

@bot.command(name='progress')
async def show_progress(ctx, task_name=None):
    """Show progress for tasks"""
    user_id = str(ctx.author.id)
    
    if user_id not in tracker.tasks:
        await ctx.send("📊 No tasks found. Use `!check <task_name>` to start tracking!")
        return
    
    if task_name:
        # Show specific task progress
        if task_name in tracker.tasks[user_id]:
            task = tracker.tasks[user_id][task_name]
            embed = discord.Embed(
                title=f"📈 Progress: {task_name}",
                color=0x00ff00 if task['status'] == 'completed' else 0xffaa00
            )
            embed.add_field(name="Status", value=task['status'].title(), inline=True)
            embed.add_field(name="Progress", value=f"{task['progress']}%", inline=True)
            embed.add_field(name="Description", value=task['description'] or "No description", inline=False)
            
            if task['checks']:
                recent_checks = task['checks'][-3:]  # Last 3 checks
                check_text = "\n".join([f"• {check['timestamp'][:19]}: {check['progress']}%" for check in recent_checks])
                embed.add_field(name="Recent Checks", value=check_text, inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Task '{task_name}' not found!")
    else:
        # Show all tasks overview
        embed = discord.Embed(title="📊 All Tasks Progress", color=0x0099ff)
        
        for task_name, task_data in tracker.tasks[user_id].items():
            status_emoji = "✅" if task_data['status'] == 'completed' else "🔄" if task_data['status'] == 'in_progress' else "⏳"
            embed.add_field(
                name=f"{status_emoji} {task_name}",
                value=f"{task_data['progress']}% - {task_data['status']}",
                inline=True
            )
        
        await ctx.send(embed=embed)

@bot.command(name='check')
async def auto_check(ctx, task_name, progress: int = None):
    """Auto-check task progress"""
    user_id = str(ctx.author.id)
    
    if not task_name:
        await ctx.send("❌ Please specify a task name: `!check <task_name> [progress]`")
        return
    
    # Add task if it doesn't exist
    if user_id not in tracker.tasks or task_name not in tracker.tasks[user_id]:
        tracker.add_task(user_id, task_name, f"Auto-tracked task: {task_name}")
        await ctx.send(f"📝 Created new task: **{task_name}**")
    
    # Update progress if provided
    if progress is not None:
        if 0 <= progress <= 100:
            success = tracker.update_progress(user_id, task_name, progress, f"Manual update via Discord")
            if success:
                status_emoji = "✅" if progress >= 100 else "🔄"
                await ctx.send(f"{status_emoji} **{task_name}** updated to {progress}%!")
                
                # Auto-congratulate on completion
                if progress >= 100:
                    await ctx.send(f"🎉 Congratulations! Task **{task_name}** is complete! 🎉")
            else:
                await ctx.send("❌ Failed to update progress!")
        else:
            await ctx.send("❌ Progress must be between 0 and 100!")
    else:
        # Show current status
        task = tracker.tasks[user_id][task_name]
        await ctx.send(f"📊 **{task_name}**: {task['progress']}% ({task['status']})")

@bot.command(name='blueprint')
async def show_blueprint(ctx, blueprint_name=None):
    """Show available blueprints or specific blueprint details"""
    
    # Default blueprints based on original system
    default_blueprints = {
        "web_app": {
            "name": "Web Application Development",
            "tasks": [
                "Setup development environment",
                "Create project structure",
                "Implement backend API",
                "Design frontend interface",
                "Database integration",
                "User authentication",
                "Testing implementation",
                "Deployment setup",
                "Performance optimization",
                "Documentation"
            ]
        },
        "ai_project": {
            "name": "AI/ML Project Blueprint",
            "tasks": [
                "Data collection and preprocessing",
                "Model architecture design",
                "Training pipeline setup",
                "Model training and validation",
                "Hyperparameter optimization",
                "Model evaluation",
                "API development",
                "Frontend integration",
                "Production deployment",
                "Monitoring and maintenance"
            ]
        },
        "discord_bot": {
            "name": "Discord Bot Development",
            "tasks": [
                "Bot setup and configuration",
                "Command framework implementation",
                "Database integration",
                "Event handling system",
                "User permission system",
                "Error handling and logging",
                "Testing and debugging",
                "Hosting and deployment",
                "Documentation and guides",
                "Community feedback integration"
            ]
        }
    }
    
    if blueprint_name:
        if blueprint_name in default_blueprints:
            blueprint = default_blueprints[blueprint_name]
            embed = discord.Embed(
                title=f"📋 Blueprint: {blueprint['name']}",
                color=0x9932cc
            )
            
            task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(blueprint['tasks'])])
            embed.add_field(name="Tasks", value=task_list, inline=False)
            embed.add_field(name="Usage", value=f"Use `!blueprint apply {blueprint_name}` to apply this blueprint", inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Blueprint '{blueprint_name}' not found!")
    else:
        # Show all available blueprints
        embed = discord.Embed(title="📋 Available Blueprints", color=0x9932cc)
        
        for bp_key, bp_data in default_blueprints.items():
            embed.add_field(
                name=bp_data['name'],
                value=f"Key: `{bp_key}` | {len(bp_data['tasks'])} tasks",
                inline=False
            )
        
        embed.add_field(
            name="Usage",
            value="Use `!blueprint <name>` to view details\nUse `!blueprint apply <name>` to apply",
            inline=False
        )
        
        await ctx.send(embed=embed)

@bot.command(name='apply')
async def apply_blueprint(ctx, blueprint_name):
    """Apply a blueprint to create tasks"""
    user_id = str(ctx.author.id)
    
    # This would integrate with the blueprint system
    await ctx.send(f"🚧 Blueprint application feature coming soon! Blueprint: {blueprint_name}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("❌ An error occurred while processing your command.")

async def generate_ai_response(prompt: str) -> str:
    """Generate AI response using Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"AI response unavailable: {str(e)}"

@bot.command(name='ai')
async def ai_help(ctx, *, question):
    """Ask AI for help with tasks"""
    if not question:
        await ctx.send("❌ Please provide a question: `!ai How do I improve my productivity?`")
        return
    
    prompt = f"""
    You are a productivity and project management assistant. 
    Help the user with their question: {question}
    
    Provide practical, actionable advice in a friendly tone.
    Keep responses under 500 characters for Discord.
    """
    
    response = await generate_ai_response(prompt)
    
    # Split long responses
    if len(response) > 1900:
        response = response[:1900] + "..."
    
    await ctx.send(f"🤖 **AI Assistant:**\n{response}")

if __name__ == "__main__":
    # Bot token should be set as environment variable
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not set!")
        print("Please set DISCORD_BOT_TOKEN environment variable")
        print("Get your token from: https://discord.com/developers/applications")
    else:
        logger.info("🚀 Starting Codex-SuperLab Discord Bot...")
        bot.run(token)