# Mini-Project-Task-Management-System

## Overview
A simple CLI Task Management System built with Python and SQLite3.  
Supports adding, viewing, updating, completing, and deleting tasks.

## Requirements
- Python 3
- SQLite3

## How to Run
1. Save `task_manager.py` in a folder.
2. Open terminal in that folder.
3. Run `python task_manager.py`.
4. Use the menu to manage tasks.

## Database Schema
Table: tasks
| Column      | Type     | Description                 |
|------------|---------|-----------------------------|
| task_id    | INTEGER | Primary Key, Auto Increment |
| title      | TEXT    | Task title (required)       |
| description| TEXT    | Optional description        |
| status     | TEXT    | Pending/Completed           |
| created_at | TEXT    | Timestamp                   |

## Screenshots

## GitHub Repository
