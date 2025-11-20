
# Mini Project- Task Management System (Python + SQLite3)

import sqlite3
import datetime
import sys

x = "task.db"

def connect():
    return sqlite3.connect(x)

def database():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def add_task(title, description=""):

    if not title.strip():
        print("Error: task title cannot be empty.")
        return
    conn = connect()
    cur = conn.cursor()
    created_at = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    cur.execute(
        "INSERT INTO tasks (title, description, status, created_at) VALUES (?, ?, ?, ?);",
        (title.strip(), description.strip(), "Pending", created_at)
    )
    conn.commit()
    conn.close()
    print("Task added successfully.")

def list_tasks(show_all=True):
    """List tasks. If show_all is False, show only Pending tasks."""
    conn = connect()
    cur = conn.cursor()
    if show_all:
        cur.execute("SELECT task_id, title, description, status, created_at FROM tasks ORDER BY task_id;")
    else:
        cur.execute("SELECT task_id, title, description, status, created_at FROM tasks WHERE status = 'Pending' ORDER BY task_id;")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No tasks found.")
        return

    print("\n{:<6} {:<30} {:<10} {:<19} {}".format("ID", "Title", "Status", "Created At", "Description"))
    print("-" * 90)
    for r in rows:
        tid, title, desc, status, created_at = r
        print("{:<6} {:<30} {:<10} {:<19} {}".format(tid, title[:28], status, created_at, (desc[:40] if desc else "")))
    print()

def get_task_by_id(task_id):
    """Return a task tuple or None."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT task_id, title, description, status, created_at FROM tasks WHERE task_id = ?;", (task_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_task(task_id, new_title=None, new_description=None):

    existing = get_task_by_id(task_id)
    if not existing:
        print("No task found with that ID.")
        return
    title = new_title.strip() if new_title is not None and new_title.strip() else existing[1]
    desc = new_description.strip() if new_description is not None else existing[2]
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET title = ?, description = ? WHERE task_id = ?;", (title, desc, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully.")

def mark_task_complete(task_id):

    if not get_task_by_id(task_id):
        print("No task found with that ID.")
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status = 'Completed' WHERE task_id = ?;", (task_id,))
    conn.commit()
    conn.close()
    print("Task marked as Completed.")

def delete_task(task_id):

    if not get_task_by_id(task_id):
        print("No task found with that ID.")
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE task_id = ?;", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully.")


def prompt_add_task():
    title = input("Enter task title: ").strip()
    description = input("Enter description (optional): ").strip()
    add_task(title, description)

def prompt_update_task():
    try:
        tid = int(input("Enter task ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    task = get_task_by_id(tid)
    if not task:
        print("Task not found.")
        return
    print(f"Current title: {task[1]}")
    new_title = input("New title (leave blank to keep current): ")
    print(f"Current description: {task[2]}")
    new_description = input("New description (leave blank to keep current): ")
    update_task(tid, new_title if new_title != "" else None, new_description if new_description != "" else None)

def prompt_mark_complete():
    try:
        tid = int(input("Enter task ID to mark as completed: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    mark_task_complete(tid)

def prompt_delete_task():
    try:
        tid = int(input("Enter task ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    confirm = input("Are you sure you want to delete this task? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_task(tid)
    else:
        print("Delete cancelled.")

def main_menu():
    database()
    while True:
        print("\n--- Task Management System ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. Update Task")
        print("5. Mark Task as Completed")
        print("6. Delete Task")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == '1':
            prompt_add_task()
        elif choice == '2':
            list_tasks(show_all=True)
        elif choice == '3':
            list_tasks(show_all=False)
        elif choice == '4':
            prompt_update_task()
        elif choice == '5':
            prompt_mark_complete()
        elif choice == '6':
            prompt_delete_task()
        elif choice == '7':
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main_menu()
