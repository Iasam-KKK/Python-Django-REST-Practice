# Task Tracker CLI

A simple command-line interface (CLI) application to track and manage your tasks.

## Features

- Add, update, and delete tasks
- Mark tasks as in-progress or done
- List all tasks
- List tasks by status (todo, in-progress, done)

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository or download the `testTracker.py` file.
2. Ensure you have Python installed on your system.

## Usage

Run the script from the command line using Python:

### Available Commands

1. Add a new task:

   ```
   python testTracker.py add "Task description"
   ```

2. Update a task:

   ```
   python testTracker.py update <task_id> "New task description"
   ```

3. Delete a task:

   ```
   python testTracker.py delete <task_id>
   ```

4. Mark a task as in-progress:

   ```
   python testTracker.py mark-in-progress <task_id>
   ```

5. Mark a task as done:

   ```
   python testTracker.py mark-done <task_id>
   ```

6. List all tasks:

   ```
   python testTracker.py list
   ```

7. List tasks by status:
   ```
   python testTracker.py list todo
   python testTracker.py list in-progress
   python testTracker.py list done
   ```

## Data Storage

Tasks are stored in a JSON file named `tasks.json` in the same directory as the script. The file is created automatically if it doesn't exist.

## Task Properties

Each task has the following properties:

- id: A unique identifier for the task
- description: A short description of the task
- status: The status of the task (todo, in-progress, done)
- createdAt: The date and time when the task was created
- updatedAt: The date and time when the task was last updated

## Error Handling

The script includes basic error handling for invalid commands or missing arguments. It will display usage instructions if the command is not used correctly.
