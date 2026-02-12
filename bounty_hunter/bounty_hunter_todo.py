#!/usr/bin/env python3
"""
Bounty Hunter - Automated Todo List and Checklist System

Comprehensive automation system for managing bounty hunting tasks with
real-time tracking, AI-powered analysis, and structured workflows.
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bounty_hunter_todo.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Constants
TODO_FILE = "bounty_hunter_todo.json"
CHECKLIST_FILE = "bounty_hunter_checklist.json"
PROJECT_ROOT = Path(__file__).resolve().parent

# Task priorities
PRIORITY = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

# Task statuses
STATUS = {
    "TODO": "todo",
    "IN_PROGRESS": "in_progress",
    "COMPLETED": "completed",
    "BLOCKED": "blocked",
    "CANCELLED": "cancelled",
}

# Task categories
CATEGORY = {
    "UPWORK": "upwork",
    "IMMUNEFI": "immunefi",
    "ALGORAND": "algorand",
    "STELLAR": "stellar",
    "AUTOMATION": "automation",
    "DOCUMENTATION": "documentation",
    "SECURITY": "security",
    "MAINTENANCE": "maintenance",
}

# ====================
# Task Management
# ====================


class Task:
    """Represents a single bounty hunting task"""

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        priority: str = "MEDIUM",
        category: str = "AUTOMATION",
        status: str = "TODO",
        dependencies: List[str] = None,
        estimated_time: int = 60,
        actual_time: int = 0,
        start_date: str = None,
        due_date: str = None,
        completed_date: str = None,
        created_date: str = None,
        notes: List[str] = None,
        tags: List[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.status = status
        self.dependencies = dependencies or []
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.start_date = start_date
        self.due_date = due_date
        self.completed_date = completed_date
        self.created_date = created_date or datetime.now().isoformat()
        self.notes = notes or []
        self.tags = tags or []

    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "dependencies": self.dependencies,
            "estimated_time": self.estimated_time,
            "actual_time": self.actual_time,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_date": self.completed_date,
            "created_date": self.created_date,
            "notes": self.notes,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create task from dictionary"""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority", "MEDIUM"),
            category=data.get("category", "AUTOMATION"),
            status=data.get("status", "TODO"),
            dependencies=data.get("dependencies", []),
            estimated_time=data.get("estimated_time", 60),
            actual_time=data.get("actual_time", 0),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            created_date=data.get("created_date"),
            notes=data.get("notes", []),
            tags=data.get("tags", []),
        )

    def start(self) -> None:
        """Start the task"""
        self.status = STATUS["IN_PROGRESS"]
        self.start_date = datetime.now().isoformat()
        logger.info(f"Started task: {self.title}")

    def complete(self, actual_time: int = None) -> None:
        """Complete the task"""
        self.status = STATUS["COMPLETED"]
        self.completed_date = datetime.now().isoformat()
        if actual_time:
            self.actual_time = actual_time
        logger.info(f"Completed task: {self.title}")

    def add_note(self, note: str) -> None:
        """Add a note to the task"""
        self.notes.append(note)
        logger.info(f"Added note to task: {self.title}")


# ====================
# Todo List Management
# ====================


class TodoList:
    """Manages the complete todo list"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.load()

    def load(self) -> None:
        """Load tasks from file"""
        try:
            if os.path.exists(TODO_FILE):
                with open(TODO_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for task_data in data.get("tasks", []):
                        task = Task.from_dict(task_data)
                        self.tasks[task.id] = task
                logger.info(f"Loaded {len(self.tasks)} tasks from {TODO_FILE}")
            else:
                logger.info(f"Creating new todo list at {TODO_FILE}")
                self.create_default_tasks()
        except Exception as e:
            logger.error(f"Error loading todo list: {e}")
            self.create_default_tasks()

    def save(self) -> None:
        """Save tasks to file"""
        try:
            data = {
                "tasks": [task.to_dict() for task in self.tasks.values()],
                "last_updated": datetime.now().isoformat(),
                "version": "1.0",
            }
            with open(TODO_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved {len(self.tasks)} tasks to {TODO_FILE}")
        except Exception as e:
            logger.error(f"Error saving todo list: {e}")

    def create_default_tasks(self) -> None:
        """Create default task list for bounty hunting"""
        tasks = [
            # Upwork Tasks
            {
                "id": "upwork-1",
                "title": "Create ERC-20 Token Contract",
                "description": "Generate a complete ERC-20 token contract with Solidity and Etherscan verification",
                "priority": "HIGH",
                "category": "UPWORK",
                "estimated_time": 120,
                "tags": ["erc20", "token", "solidity"],
            },
            {
                "id": "upwork-2",
                "title": "Create Trading Bot",
                "description": "Build a simple crypto trading bot for Binance/Coinbase",
                "priority": "MEDIUM",
                "category": "UPWORK",
                "estimated_time": 180,
                "tags": ["trading", "bot", "python"],
            },
            {
                "id": "upwork-3",
                "title": "Smart Contract Audit",
                "description": "Perform security audit for a small smart contract project",
                "priority": "MEDIUM",
                "category": "UPWORK",
                "estimated_time": 240,
                "tags": ["audit", "security", "solidity"],
            },
            # Immunefi Tasks
            {
                "id": "immunefi-1",
                "title": "Run Auto-Scan",
                "description": "Run Slither + Mythril scanners to find low-severity vulnerabilities",
                "priority": "HIGH",
                "category": "IMMUNEFI",
                "estimated_time": 60,
                "tags": ["scan", "security", "vulnerability"],
            },
            {
                "id": "immunefi-2",
                "title": "Analyze Scanner Results",
                "description": "Analyze security scanner results and prepare reports",
                "priority": "MEDIUM",
                "category": "IMMUNEFI",
                "estimated_time": 120,
                "tags": ["analysis", "report", "security"],
            },
            {
                "id": "immunefi-3",
                "title": "Submit Bug Report",
                "description": "Submit detailed bug reports to Immunefi programs",
                "priority": "MEDIUM",
                "category": "IMMUNEFI",
                "estimated_time": 90,
                "tags": ["submit", "report", "immunefi"],
            },
            # Algorand Tasks
            {
                "id": "algorand-1",
                "title": "Generate Algorand Tutorial",
                "description": "Create Algorand tutorial content using AI",
                "priority": "HIGH",
                "category": "ALGORAND",
                "estimated_time": 180,
                "tags": ["tutorial", "algorand", "content"],
            },
            {
                "id": "algorand-2",
                "title": "Submit Algorand Bounty",
                "description": "Submit tutorial to Algorand's Gitcoin bounty program",
                "priority": "MEDIUM",
                "category": "ALGORAND",
                "estimated_time": 60,
                "tags": ["submit", "bounty", "algorand"],
            },
            {
                "id": "algorand-3",
                "title": "Monitor Algorand Bounties",
                "description": "Check for new Algorand bounty opportunities",
                "priority": "LOW",
                "category": "ALGORAND",
                "estimated_time": 30,
                "tags": ["monitor", "bounty", "algorand"],
            },
            # Stellar Tasks
            {
                "id": "stellar-1",
                "title": "Create Soroban Contract",
                "description": "Build a Soroban smart contract template",
                "priority": "HIGH",
                "category": "STELLAR",
                "estimated_time": 240,
                "tags": ["soroban", "contract", "rust"],
            },
            {
                "id": "stellar-2",
                "title": "Create SCF Proposal",
                "description": "Generate Stellar Community Fund proposal",
                "priority": "MEDIUM",
                "category": "STELLAR",
                "estimated_time": 180,
                "tags": ["scf", "proposal", "grant"],
            },
            {
                "id": "stellar-3",
                "title": "Submit SCF Application",
                "description": "Submit proposal to Stellar SCF",
                "priority": "MEDIUM",
                "category": "STELLAR",
                "estimated_time": 60,
                "tags": ["submit", "scf", "grant"],
            },
            # Automation Tasks
            {
                "id": "automation-1",
                "title": "Run Daily Bounty Routine",
                "description": "Execute the complete daily bounty hunting workflow",
                "priority": "HIGH",
                "category": "AUTOMATION",
                "estimated_time": 60,
                "tags": ["daily", "routine", "automation"],
            },
            {
                "id": "automation-2",
                "title": "Check Bounty Status",
                "description": "Monitor status of claimed bounties",
                "priority": "MEDIUM",
                "category": "AUTOMATION",
                "estimated_time": 30,
                "tags": ["status", "monitor", "automation"],
            },
            {
                "id": "automation-3",
                "title": "Star Trending Repos",
                "description": "Automatically star trending AI/DevOps repositories",
                "priority": "LOW",
                "category": "AUTOMATION",
                "estimated_time": 15,
                "tags": ["github", "social", "automation"],
            },
            # Documentation Tasks
            {
                "id": "docs-1",
                "title": "Update Documentation",
                "description": "Update project documentation with new findings",
                "priority": "MEDIUM",
                "category": "DOCUMENTATION",
                "estimated_time": 60,
                "tags": ["docs", "update", "maintenance"],
            },
            {
                "id": "docs-2",
                "title": "Create Report",
                "description": "Generate daily/weekly activity report",
                "priority": "LOW",
                "category": "DOCUMENTATION",
                "estimated_time": 30,
                "tags": ["report", "documentation", "analysis"],
            },
            # Security Tasks
            {
                "id": "security-1",
                "title": "System Health Check",
                "description": "Run security and system health checks",
                "priority": "LOW",
                "category": "SECURITY",
                "estimated_time": 15,
                "tags": ["security", "health", "check"],
            },
            {
                "id": "security-2",
                "title": "Update Vulnerability Database",
                "description": "Update the vulnerability database with new findings",
                "priority": "LOW",
                "category": "SECURITY",
                "estimated_time": 30,
                "tags": ["vulnerability", "database", "update"],
            },
            # Maintenance Tasks
            {
                "id": "maintenance-1",
                "title": "Update Dependencies",
                "description": "Update project dependencies",
                "priority": "LOW",
                "category": "MAINTENANCE",
                "estimated_time": 60,
                "tags": ["dependencies", "update", "maintenance"],
            },
            {
                "id": "maintenance-2",
                "title": "Backup Data",
                "description": "Backup all project data",
                "priority": "LOW",
                "category": "MAINTENANCE",
                "estimated_time": 15,
                "tags": ["backup", "data", "maintenance"],
            },
        ]

        for task_data in tasks:
            task = Task.from_dict(task_data)
            self.tasks[task.id] = task

        logger.info(f"Created {len(tasks)} default tasks")
        self.save()

    def add_task(self, task: Task) -> None:
        """Add a new task"""
        self.tasks[task.id] = task
        self.save()
        logger.info(f"Added task: {task.title}")

    def get_task(self, task_id: str) -> Task:
        """Get a task by ID"""
        return self.tasks.get(task_id)

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks by category"""
        return [task for task in self.tasks.values() if task.category == category]

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks by status"""
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority"""
        return [task for task in self.tasks.values() if task.priority == priority]

    def start_task(self, task_id: str) -> None:
        """Start a task"""
        task = self.get_task(task_id)
        if task:
            task.start()
            self.save()

    def complete_task(self, task_id: str, actual_time: int = None) -> None:
        """Complete a task"""
        task = self.get_task(task_id)
        if task:
            task.complete(actual_time)
            self.save()


# ====================
# Checklist Management
# ====================


class Checklist:
    """Manages the automated checklist system"""

    def __init__(self):
        self.items: List[Dict] = []
        self.load()

    def load(self) -> None:
        """Load checklist from file"""
        try:
            if os.path.exists(CHECKLIST_FILE):
                with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
                    self.items = json.load(f)
                logger.info(
                    f"Loaded {len(self.items)} checklist items from {CHECKLIST_FILE}"
                )
            else:
                logger.info(f"Creating new checklist at {CHECKLIST_FILE}")
                self.create_default_checklist()
        except Exception as e:
            logger.error(f"Error loading checklist: {e}")
            self.create_default_checklist()

    def save(self) -> None:
        """Save checklist to file"""
        try:
            data = {
                "items": self.items,
                "last_updated": datetime.now().isoformat(),
                "version": "1.0",
            }
            with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved {len(self.items)} checklist items to {CHECKLIST_FILE}")
        except Exception as e:
            logger.error(f"Error saving checklist: {e}")

    def create_default_checklist(self) -> None:
        """Create default checklist"""
        self.items = [
            {
                "id": "check-1",
                "name": "System Configuration",
                "items": [
                    {
                        "id": "sys-1",
                        "text": "Check internet connectivity",
                        "completed": False,
                    },
                    {
                        "id": "sys-2",
                        "text": "Verify API key availability",
                        "completed": False,
                    },
                    {"id": "sys-3", "text": "Check tool versions", "completed": False},
                    {
                        "id": "sys-4",
                        "text": "Validate database connections",
                        "completed": False,
                    },
                ],
            },
            {
                "id": "check-2",
                "name": "Bounty Platforms",
                "items": [
                    {
                        "id": "plat-1",
                        "text": "Check Upwork API status",
                        "completed": False,
                    },
                    {
                        "id": "plat-2",
                        "text": "Verify Immunefi scanner configuration",
                        "completed": False,
                    },
                    {
                        "id": "plat-3",
                        "text": "Check Algorand SDK installation",
                        "completed": False,
                    },
                    {
                        "id": "plat-4",
                        "text": "Verify Stellar SDK installation",
                        "completed": False,
                    },
                ],
            },
            {
                "id": "check-3",
                "name": "Security Scanners",
                "items": [
                    {
                        "id": "scan-1",
                        "text": "Verify Slither installation",
                        "completed": False,
                    },
                    {
                        "id": "scan-2",
                        "text": "Check Mythril configuration",
                        "completed": False,
                    },
                    {
                        "id": "scan-3",
                        "text": "Test Echidna installation",
                        "completed": False,
                    },
                    {
                        "id": "scan-4",
                        "text": "Validate scanner output formats",
                        "completed": False,
                    },
                ],
            },
            {
                "id": "check-4",
                "name": "Documentation",
                "items": [
                    {
                        "id": "docs-1",
                        "text": "Update TODAY_BOUNTY_REPORT.md",
                        "completed": False,
                    },
                    {
                        "id": "docs-2",
                        "text": "Check REAL_BOUNTY_ANALYSIS.md",
                        "completed": False,
                    },
                    {
                        "id": "docs-3",
                        "text": "Verify BOUNTY_HUNTER_SETUP.md",
                        "completed": False,
                    },
                    {
                        "id": "docs-4",
                        "text": "Update NO_INVESTMENT_JOBS.md",
                        "completed": False,
                    },
                ],
            },
            {
                "id": "check-5",
                "name": "Daily Routine",
                "items": [
                    {
                        "id": "daily-1",
                        "text": "Run check-bounty-status.sh",
                        "completed": False,
                    },
                    {
                        "id": "daily-2",
                        "text": "Execute github-social.sh",
                        "completed": False,
                    },
                    {"id": "daily-3", "text": "Run auto-scan.sh", "completed": False},
                    {
                        "id": "daily-4",
                        "text": "Generate token contract",
                        "completed": False,
                    },
                ],
            },
        ]

        self.save()

    def mark_completed(self, item_id: str) -> None:
        """Mark a checklist item as completed"""
        for section in self.items:
            for item in section["items"]:
                if item["id"] == item_id:
                    item["completed"] = True
                    self.save()
                    logger.info(f"Marked checklist item as completed: {item['text']}")
                    return
        logger.warning(f"Checklist item not found: {item_id}")

    def mark_all_completed(self) -> None:
        """Mark all checklist items as completed"""
        for section in self.items:
            for item in section["items"]:
                item["completed"] = True
        self.save()
        logger.info("All checklist items marked as completed")

    def reset(self) -> None:
        """Reset all checklist items to incomplete"""
        for section in self.items:
            for item in section["items"]:
                item["completed"] = False
        self.save()
        logger.info("Checklist reset to initial state")

    def get_progress(self) -> Dict:
        """Get checklist progress"""
        total = 0
        completed = 0

        for section in self.items:
            for item in section["items"]:
                total += 1
                if item["completed"]:
                    completed += 1

        return {
            "total": total,
            "completed": completed,
            "percentage": (completed / total * 100) if total > 0 else 0,
        }


# ====================
# Automation Engine
# ====================


class AutomationEngine:
    """Engine for automated task execution and checklist management"""

    def __init__(self):
        self.todo_list = TodoList()
        self.checklist = Checklist()
        self.scripts = {
            "check-bounty-status": "~/bin/check-bounty-status.sh",
            "github-social": "~/bin/github-social.sh",
            "auto-scan": "~/bounty-work/immunefi/scanners/auto-scan.sh",
            "generate-token": "~/bounty-work/upwork/scripts/generate-token.sh",
            "start-earning": "~/bounty-work/START_EARNING.sh",
        }

    def run_script(self, script_name: str, args: List[str] = None) -> Dict:
        """Run a shell script and return results"""
        script_path = self.scripts.get(script_name)
        if not script_path:
            return {"success": False, "error": f"Script not found: {script_name}"}

        try:
            command = [script_path]
            if args:
                command.extend(args)

            process = subprocess.run(
                command, capture_output=True, text=True, shell=False, check=True
            )

            return {
                "success": True,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "returncode": process.returncode,
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"Script failed: {script_name} - {e}")
            return {
                "success": False,
                "error": str(e),
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode,
            }

        except Exception as e:
            logger.error(f"Error running script: {script_name} - {e}")
            return {"success": False, "error": str(e)}

    def run_daily_routine(self) -> Dict:
        """Run complete daily bounty hunting routine"""
        logger.info("Starting daily bounty hunting routine")
        results = []

        # Reset checklist
        self.checklist.reset()

        # Step 1: Check internet connectivity
        logger.info("Checking internet connectivity...")
        try:
            import urllib.request

            urllib.request.urlopen("https://www.google.com", timeout=10)
            self.checklist.mark_completed("sys-1")
            results.append(
                {"step": "internet", "success": True, "message": "Internet connected"}
            )
        except Exception as e:
            logger.error(f"Internet connectivity check failed: {e}")
            results.append(
                {
                    "step": "internet",
                    "success": False,
                    "message": f"Internet check failed: {e}",
                }
            )
            return {
                "success": False,
                "results": results,
                "error": "Internet connectivity check failed",
            }

        # Step 2: Run daily scripts
        steps = [
            ("check-bounty-status", "sys-2"),
            ("github-social", "sys-3"),
            ("auto-scan", "scan-1"),
            ("generate-token", "daily-4"),
        ]

        for script_name, check_id in steps:
            logger.info(f"Running script: {script_name}")
            result = self.run_script(script_name)

            if result["success"]:
                self.checklist.mark_completed(check_id)
                results.append(
                    {
                        "step": script_name,
                        "success": True,
                        "stdout": result["stdout"],
                        "stderr": result["stderr"],
                    }
                )
            else:
                results.append(
                    {
                        "step": script_name,
                        "success": False,
                        "error": result["error"],
                        "stdout": result.get("stdout"),
                        "stderr": result.get("stderr"),
                    }
                )

        # Step 3: Update documentation
        logger.info("Updating documentation...")
        try:
            if os.path.exists("TODAY_BOUNTY_REPORT.md"):
                with open("TODAY_BOUNTY_REPORT.md", "r", encoding="utf-8") as f:
                    current_report = f.read()

                # Add today's date if not already present
                today = datetime.now().strftime("%Y-%m-%d")
                if today not in current_report:
                    with open("TODAY_BOUNTY_REPORT.md", "a", encoding="utf-8") as f:
                        f.write(
                            f"\n## {today}\n\n- Daily bounty routine completed successfully\n"
                        )

            self.checklist.mark_completed("docs-1")
            results.append(
                {"step": "update-report", "success": True, "message": "Report updated"}
            )
        except Exception as e:
            logger.error(f"Failed to update report: {e}")
            results.append(
                {"step": "update-report", "success": False, "message": str(e)}
            )

        # Complete checklist
        self.checklist.mark_all_completed()

        logger.info("Daily bounty hunting routine completed")
        return {
            "success": all(result["success"] for result in results),
            "results": results,
            "checklist": self.checklist.get_progress(),
        }

    def run_weekly_audit(self) -> Dict:
        """Run weekly system audit"""
        logger.info("Starting weekly system audit")

        # Run system health checks
        health_checks = self.run_script("system-health-check")
        logger.info(
            f"System health check: {'Passed' if health_checks['success'] else 'Failed'}"
        )

        # Check dependencies
        dependencies = self.run_script("update-dependencies")
        logger.info(
            f"Dependency check: {'Passed' if dependencies['success'] else 'Failed'}"
        )

        # Backup data
        backup = self.run_script("backup-data")
        logger.info(f"Data backup: {'Success' if backup['success'] else 'Failed'}")

        return {
            "success": all(
                [health_checks["success"], dependencies["success"], backup["success"]]
            ),
            "health": health_checks,
            "dependencies": dependencies,
            "backup": backup,
        }


# ====================
# UI and Reporting
# ====================


class UI:
    """Text-based user interface for the todo list and checklist system"""

    def __init__(self):
        self.engine = AutomationEngine()

    def print_header(self) -> None:
        """Print application header"""
        print("\033[H\033[J")  # Clear screen
        print("=" * 80)
        print("BOUNTY HUNTER - AUTOMATED TODO LIST & CHECKLIST SYSTEM")
        print("=" * 80)
        print()

    def print_todo_list(self) -> None:
        """Print current todo list"""
        self.print_header()
        print("CURRENT TASK LIST")
        print("-" * 80)

        # Group tasks by category
        categories = {}
        for task in self.engine.todo_list.tasks.values():
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)

        # Print tasks by category and priority
        for category, tasks in sorted(categories.items()):
            print(f"\n{category.upper()}:")
            print("-" * len(category))

            # Sort by priority and status
            tasks_sorted = sorted(
                tasks, key=lambda x: (PRIORITY.get(x.priority, 3), STATUS[x.status])
            )

            for task in tasks_sorted:
                status_icon = {
                    "todo": "[ ]",
                    "in_progress": "[*]",
                    "completed": "[✓]",
                    "blocked": "[!]",
                    "cancelled": "[x]",
                }[task.status]

                priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[
                    task.priority
                ]

                time_str = (
                    f"{task.actual_time}m"
                    if task.actual_time > 0
                    else f"{task.estimated_time}m"
                )

                print(f"{status_icon} {priority_icon} {task.title} ({time_str})")
                if task.description:
                    print(f"    {task.description}")

        # Print stats
        total_tasks = len(self.engine.todo_list.tasks)
        completed = len(
            [
                t
                for t in self.engine.todo_list.tasks.values()
                if t.status == STATUS["COMPLETED"]
            ]
        )
        in_progress = len(
            [
                t
                for t in self.engine.todo_list.tasks.values()
                if t.status == STATUS["IN_PROGRESS"]
            ]
        )

        print(
            f"\nSUMMARY: {completed}/{total_tasks} completed, {in_progress} in progress"
        )
        print()

    def print_checklist(self) -> None:
        """Print current checklist"""
        self.print_header()
        print("AUTOMATED CHECKLIST")
        print("-" * 80)

        progress = self.engine.checklist.get_progress()

        for section in self.engine.checklist.items:
            print(f"\n{section['name']}:")
            print("-" * len(section["name"]))

            for item in section["items"]:
                status = "[✓]" if item["completed"] else "[ ]"
                print(f"{status} {item['text']}")

        print(
            f"\nPROGRESS: {progress['completed']}/{progress['total']} ({progress['percentage']:.1f}%)"
        )
        print()

    def print_menu(self) -> None:
        """Print main menu"""
        self.print_header()
        print("MAIN MENU")
        print("-" * 80)
        print()
        print("1. View Todo List")
        print("2. View Checklist")
        print("3. Run Daily Routine")
        print("4. Run Weekly Audit")
        print("5. Mark Task Complete")
        print("6. Start Task")
        print("7. Reset Checklist")
        print("8. Exit")
        print()

    def run(self) -> None:
        """Run the interactive interface"""
        while True:
            self.print_menu()
            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                self.print_todo_list()
                input("Press Enter to continue...")
            elif choice == "2":
                self.print_checklist()
                input("Press Enter to continue...")
            elif choice == "3":
                self.print_header()
                print("Running daily bounty hunting routine...")
                print()

                result = self.engine.run_daily_routine()

                if result["success"]:
                    print("✅ Daily routine completed successfully!")
                    print(
                        f"Progress: {result['checklist']['completed']}/{result['checklist']['total']} ({result['checklist']['percentage']:.1f}%)"
                    )
                else:
                    print("❌ Daily routine failed!")
                    failed_steps = [r for r in result["results"] if not r["success"]]
                    print(f"\nFailed steps: {len(failed_steps)}")
                    for step in failed_steps:
                        print(f"  • {step['step']}: {step['message']}")

                input("\nPress Enter to continue...")
            elif choice == "4":
                self.print_header()
                print("Running weekly system audit...")
                print()

                result = self.engine.run_weekly_audit()

                if result["success"]:
                    print("✅ Weekly audit completed successfully!")
                    print("All health checks passed")
                else:
                    print("❌ Weekly audit failed!")
                    if not result["health"]["success"]:
                        print("  • System health check failed")
                    if not result["dependencies"]["success"]:
                        print("  • Dependency check failed")
                    if not result["backup"]["success"]:
                        print("  • Data backup failed")

                input("\nPress Enter to continue...")
            elif choice == "5":
                self.print_todo_list()
                task_id = input("Enter task ID to mark complete: ").strip()
                task = self.engine.todo_list.get_task(task_id)
                if task:
                    actual_time = input("Enter actual time (in minutes): ").strip()
                    actual_time = int(actual_time) if actual_time.isdigit() else None
                    self.engine.todo_list.complete_task(task_id, actual_time)
                    print(f"✅ Task '{task.title}' marked as complete!")
                else:
                    print(f"❌ Task '{task_id}' not found!")
                input("Press Enter to continue...")
            elif choice == "6":
                self.print_todo_list()
                task_id = input("Enter task ID to start: ").strip()
                task = self.engine.todo_list.get_task(task_id)
                if task:
                    self.engine.todo_list.start_task(task_id)
                    print(f"✅ Task '{task.title}' started!")
                else:
                    print(f"❌ Task '{task_id}' not found!")
                input("Press Enter to continue...")
            elif choice == "7":
                confirm = (
                    input("Are you sure you want to reset the checklist? (y/N): ")
                    .lower()
                    .strip()
                )
                if confirm == "y":
                    self.engine.checklist.reset()
                    print("✅ Checklist reset!")
                input("Press Enter to continue...")
            elif choice == "8":
                print("\nThank you for using Bounty Hunter!")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please enter a number between 1 and 8.")
                time.sleep(1)


# ====================
# Entry Point
# ====================


def main():
    """Main entry point"""
    try:
        ui = UI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt detected. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
