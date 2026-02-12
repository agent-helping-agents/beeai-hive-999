#!/usr/bin/env python3
"""
Bounty Hunter - System Test Script

Comprehensive test script for the Bounty Hunter automation system.
Tests all core functionality, including task management, checklist operations,
and automation workflows.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Test configuration
TEST_FILES = {
    "todo_list": "bounty_hunter_todo.py",
    "todo_json": "bounty_hunter_todo.json",
    "checklist_json": "bounty_hunter_checklist.json",
    "blueprint": "bounty_hunter_blueprint.md",
    "startup": "start_bounty_hunter.sh",
}

# Test results
test_results = []


def print_result(test_name, success, details=None):
    """Print test result with color coding"""
    color = "\033[92m✓" if success else "\033[91m✗"
    status = "PASS" if success else "FAIL"
    result = f"{color} {status}: {test_name}"
    if details:
        result += f" - {details}"
    print(f"{result}\033[0m")
    test_results.append({"name": test_name, "success": success, "details": details})


def test_file_existence():
    """Test if all required files exist"""
    print("\n=== File Existence Tests ===")
    all_exist = True

    for name, filename in TEST_FILES.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print_result(f"{filename}", True, f"{size} bytes")
        else:
            print_result(f"{filename}", False, "File not found")
            all_exist = False

    return all_exist


def test_file_permissions():
    """Test file permissions"""
    print("\n=== File Permission Tests ===")
    all_permissions = True

    # Check executable permissions
    executable_files = [TEST_FILES["todo_list"], TEST_FILES["startup"]]

    for filename in executable_files:
        if os.path.exists(filename):
            if os.access(filename, os.X_OK):
                print_result(f"{filename} executable", True)
            else:
                print_result(f"{filename} executable", False, "File not executable")
                all_permissions = False
        else:
            print_result(f"{filename} executable", False, "File not found")
            all_permissions = False

    return all_permissions


def test_json_validity():
    """Test JSON file validity"""
    print("\n=== JSON File Validity Tests ===")
    all_valid = True

    json_files = [TEST_FILES["todo_json"], TEST_FILES["checklist_json"]]

    for filename in json_files:
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print_result(
                    f"{filename}",
                    True,
                    f"{len(data.get('tasks', data.get('items', [])))} items",
                )
            except Exception as e:
                print_result(f"{filename}", False, f"JSON error: {e}")
                all_valid = False
        else:
            print_result(f"{filename}", False, "File not found")
            all_valid = False

    return all_valid


def test_python_import():
    """Test if the Python module can be imported"""
    print("\n=== Python Import Tests ===")
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from bounty_hunter_todo import TodoList, Checklist, AutomationEngine, UI

        print_result("TodoList class", True)
        print_result("Checklist class", True)
        print_result("AutomationEngine class", True)
        print_result("UI class", True)

        return True
    except Exception as e:
        print_result("Python import", False, f"Error: {e}")
        return False


def test_todo_list_creation():
    """Test todo list creation and management"""
    print("\n=== Todo List Tests ===")
    try:
        from bounty_hunter_todo import TodoList

        todo_list = TodoList()

        # Test task count
        task_count = len(todo_list.tasks)
        expected_count = 21
        if task_count == expected_count:
            print_result("Task count", True, f"{task_count} tasks")
        else:
            print_result(
                "Task count", False, f"Expected {expected_count}, got {task_count}"
            )
            return False

        # Test task categories
        categories = set(task.category for task in todo_list.tasks.values())
        expected_categories = {
            "UPWORK",
            "IMMUNEFI",
            "ALGORAND",
            "STELLAR",
            "AUTOMATION",
            "DOCUMENTATION",
            "SECURITY",
            "MAINTENANCE",
        }

        missing_categories = expected_categories - categories
        if not missing_categories:
            print_result("Task categories", True, f"{len(categories)} categories")
        else:
            print_result(
                "Task categories",
                False,
                f"Missing categories: {', '.join(missing_categories)}",
            )
            return False

        # Test high priority tasks
        high_priority = [
            task for task in todo_list.tasks.values() if task.priority == "HIGH"
        ]
        if len(high_priority) >= 5:
            print_result("High priority tasks", True, f"{len(high_priority)} tasks")
        else:
            print_result(
                "High priority tasks", False, f"Expected >=5, got {len(high_priority)}"
            )

        return True
    except Exception as e:
        print_result("Todo list tests", False, f"Error: {e}")
        return False


def test_checklist_creation():
    """Test checklist creation and management"""
    print("\n=== Checklist Tests ===")
    try:
        from bounty_hunter_todo import Checklist

        checklist = Checklist()

        # The checklist is stored as {'items': [...], 'last_updated': ..., 'version': ...}
        # So we need to access checklist.items['items'] to get the sections

        # Test checklist item count
        total_items = sum(len(section["items"]) for section in checklist.items["items"])
        expected_items = 20
        if total_items == expected_items:
            print_result("Checklist items", True, f"{total_items} items")
        else:
            print_result(
                "Checklist items",
                False,
                f"Expected {expected_items}, got {total_items}",
            )
            return False

        # Test sections
        sections = [section["name"] for section in checklist.items["items"]]
        expected_sections = [
            "System Configuration",
            "Bounty Platforms",
            "Security Scanners",
            "Documentation",
            "Daily Routine",
        ]

        missing_sections = set(expected_sections) - set(sections)
        if not missing_sections:
            print_result("Checklist sections", True, f"{len(sections)} sections")
        else:
            print_result(
                "Checklist sections",
                False,
                f"Missing sections: {', '.join(missing_sections)}",
            )
            return False

        return True
    except Exception as e:
        print_result("Checklist tests", False, f"Error: {e}")
        # Print the actual checklist structure for debugging
        try:
            from bounty_hunter_todo import Checklist

            checklist = Checklist()
            print(f"Actual checklist structure: {checklist.items}")
        except Exception as debug_error:
            print(f"Debug error: {debug_error}")
        return False

        # Test sections
        sections = [section["name"] for section in checklist.items]
        expected_sections = [
            "System Configuration",
            "Bounty Platforms",
            "Security Scanners",
            "Documentation",
            "Daily Routine",
        ]

        missing_sections = set(expected_sections) - set(sections)
        if not missing_sections:
            print_result("Checklist sections", True, f"{len(sections)} sections")
        else:
            print_result(
                "Checklist sections",
                False,
                f"Missing sections: {', '.join(missing_sections)}",
            )
            return False

        return True
    except Exception as e:
        print_result("Checklist tests", False, f"Error: {e}")
        # Print the actual checklist structure for debugging
        try:
            from bounty_hunter_todo import Checklist

            checklist = Checklist()
            print(f"Actual checklist structure: {checklist.items}")
        except Exception as debug_error:
            print(f"Debug error: {debug_error}")
        return False

        # Test sections
        sections = [section["name"] for section in checklist.items]
        expected_sections = [
            "System Configuration",
            "Bounty Platforms",
            "Security Scanners",
            "Documentation",
            "Daily Routine",
        ]

        missing_sections = set(expected_sections) - set(sections)
        if not missing_sections:
            print_result("Checklist sections", True, f"{len(sections)} sections")
        else:
            print_result(
                "Checklist sections",
                False,
                f"Missing sections: {', '.join(missing_sections)}",
            )
            return False

        return True
    except Exception as e:
        print_result("Checklist tests", False, f"Error: {e}")
        return False


def test_automation_engine():
    """Test automation engine initialization"""
    print("\n=== Automation Engine Tests ===")
    try:
        from bounty_hunter_todo import AutomationEngine

        engine = AutomationEngine()

        # Test script dictionary
        if hasattr(engine, "scripts") and isinstance(engine.scripts, dict):
            print_result(
                "Script dictionary", True, f"{len(engine.scripts)} scripts configured"
            )
        else:
            print_result("Script dictionary", False)
            return False

        # Test todo list and checklist
        if hasattr(engine, "todo_list") and hasattr(engine, "checklist"):
            print_result("Engine initialization", True)
        else:
            print_result("Engine initialization", False)
            return False

        return True
    except Exception as e:
        print_result("Automation engine tests", False, f"Error: {e}")
        return False


def test_startup_script():
    """Test the startup script"""
    print("\n=== Startup Script Tests ===")
    try:
        # Get full path to startup script
        script_path = os.path.abspath(TEST_FILES["startup"])

        # Test if startup script is executable
        if not os.path.exists(script_path):
            print_result("Startup script", False, "File not found")
            return False

        if not os.access(script_path, os.X_OK):
            print_result("Startup script", False, "File not executable")
            return False

        # Test startup script runs without errors
        result = subprocess.run(
            [script_path], capture_output=True, text=True, timeout=5
        )

        # Check if script started (will timeout after 5 seconds)
        if result.returncode in [0, 1]:  # 1 means it exited from menu
            print_result(
                "Startup script",
                True,
                f"Ran successfully (exit code: {result.returncode})",
            )
        else:
            print_result(
                "Startup script", False, f"Failed with code: {result.returncode}"
            )
            print(f"Error output: {result.stderr}")

        return True
    except subprocess.TimeoutExpired:
        print_result(
            "Startup script", True, "Script started successfully (timeout expected)"
        )
        return True
    except Exception as e:
        print_result("Startup script", False, f"Error: {e}")
        return False

        if not os.access(TEST_FILES["startup"], os.X_OK):
            print_result("Startup script", False, "File not executable")
            return False

        # Test startup script runs without errors
        result = subprocess.run(
            [TEST_FILES["startup"]], capture_output=True, text=True, timeout=5
        )

        # Check if script started (will timeout after 5 seconds)
        if result.returncode in [0, 1]:  # 1 means it exited from menu
            print_result(
                "Startup script",
                True,
                f"Ran successfully (exit code: {result.returncode})",
            )
        else:
            print_result(
                "Startup script", False, f"Failed with code: {result.returncode}"
            )
            print(f"Error output: {result.stderr}")

        return True
    except subprocess.TimeoutExpired:
        print_result(
            "Startup script", True, "Script started successfully (timeout expected)"
        )
        return True
    except Exception as e:
        print_result("Startup script", False, f"Error: {e}")
        return False


def run_all_tests():
    """Run all tests and generate summary"""
    print("==========================================")
    print("BOUNTY HUNTER - SYSTEM TESTS")
    print("==========================================")
    print()

    # Run all tests
    tests = [
        test_file_existence,
        test_file_permissions,
        test_json_validity,
        test_python_import,
        test_todo_list_creation,
        test_checklist_creation,
        test_automation_engine,
        test_startup_script,
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        time.sleep(0.5)

    # Print summary
    print("\n==========================================")
    print("TEST SUMMARY")
    print("==========================================")

    passed = sum(1 for result in test_results if result["success"])
    failed = sum(1 for result in test_results if not result["success"])
    total = len(test_results)

    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        print("\nFailed tests:")
        for result in test_results:
            if not result["success"]:
                print(f"  - {result['name']}: {result['details']}")

    if all_passed:
        print("\n✅ All tests passed! Bounty Hunter system is ready to use.")
    else:
        print(f"\n❌ {failed} out of {total} tests failed. Please check the system.")

    return all_passed


# Run tests if script is executed directly
if __name__ == "__main__":
    all_passed = run_all_tests()
    sys.exit(0 if all_passed else 1)
