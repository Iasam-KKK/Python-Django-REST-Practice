import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": max([task["id"] for task in tasks] + [0]) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task with ID {task_id} not found")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"Task with ID {task_id} not found")

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python testTracker.py <command> [args]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) != 3:
            print("Usage: python testTracker.py add <description>")
            return
        add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) != 4:
            print("Usage: python testTracker.py update <id> <new_description>")
            return
        update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: python testTracker.py delete <id>")
            return
        delete_task(int(sys.argv[2]))

    elif command == "mark-in-progress":
        if len(sys.argv) != 3:
            print("Usage: python testTracker.py mark-in-progress <id>")
            return
        mark_task(int(sys.argv[2]), "in-progress")

    elif command == "mark-done":
        if len(sys.argv) != 3:
            print("Usage: python testTracker.py mark-done <id>")
            return
        mark_task(int(sys.argv[2]), "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3 and sys.argv[2] in ["todo", "in-progress", "done"]:
            list_tasks(sys.argv[2])
        else:
            print("Usage: python testTracker.py list [todo|in-progress|done]")

    else:
        print("Unknown command. Available commands: add, update, delete, mark-in-progress, mark-done, list")

if __name__ == "__main__":
    main()