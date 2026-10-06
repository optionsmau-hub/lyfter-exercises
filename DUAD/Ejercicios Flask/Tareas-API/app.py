"""
REST API for managing tasks (CRUD) using Flask.
Data is persisted in a JSON file (tasks.json).
"""

import json
import os
from threading import Lock

from flask import Flask, jsonify, request

app = Flask(__name__)

# Path to the file where tasks are stored.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

# Valid status values for a task.
VALID_STATUSES = ["To Do", "In Progress", "Completed"]

# Lock to avoid race conditions when reading/writing the file.
file_lock = Lock()


# ---------------------------------------------------------------------------
# JSON read / write helpers
# ---------------------------------------------------------------------------

def read_tasks():
    """Reads and returns the list of tasks stored in the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return []
        return json.loads(content)


def write_tasks(tasks):
    """Writes the list of tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)


def find_task(tasks, task_id):
    """Returns the task with the given id, or None if it doesn't exist."""
    for task in tasks:
        if str(task.get("id")) == str(task_id):
            return task
    return None


# ---------------------------------------------------------------------------
# Validations
# ---------------------------------------------------------------------------

def validate_task_data(data, is_creation, current_tasks=None):
    """
    Validates the data for a task (create or update).
    Returns a list of errors. If the list is empty, the data is valid.
    """
    errors = []

    if not isinstance(data, dict):
        return ["The request body must be a JSON object."]

    # --- id (only validated on creation) ---
    if is_creation:
        task_id = data.get("id")
        if task_id is None or str(task_id).strip() == "":
            errors.append("The 'id' field is required.")
        elif current_tasks is not None and find_task(current_tasks, task_id):
            errors.append(f"A task with id '{task_id}' already exists.")

    # --- title ---
    title = data.get("title")
    if title is None or not str(title).strip():
        errors.append("The 'title' field is required and cannot be empty.")

    # --- description ---
    description = data.get("description")
    if description is None or not str(description).strip():
        errors.append("The 'description' field is required and cannot be empty.")

    # --- status ---
    status = data.get("status")
    if status is None or not str(status).strip():
        errors.append("The 'status' field is required and cannot be empty.")
    elif status not in VALID_STATUSES:
        errors.append(
            f"'{status}' is not a valid status. Allowed statuses are: "
            f"{', '.join(VALID_STATUSES)}."
        )

    return errors


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Gets all tasks. Optionally filters them by status."""
    with file_lock:
        tasks = read_tasks()

    status_filter = request.args.get("status")

    if status_filter is not None:
        if status_filter not in VALID_STATUSES:
            return jsonify({
                "error": f"'{status_filter}' is not a valid status. Allowed statuses are: "
                         f"{', '.join(VALID_STATUSES)}."
            }), 400
        tasks = [t for t in tasks if t.get("status") == status_filter]

    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Creates a new task."""
    data = request.get_json(silent=True)

    with file_lock:
        tasks = read_tasks()
        errors = validate_task_data(data, is_creation=True, current_tasks=tasks)

        if errors:
            return jsonify({"errors": errors}), 400

        new_task = {
            "id": data["id"],
            "title": data["title"],
            "description": data["description"],
            "status": data["status"],
        }

        tasks.append(new_task)
        write_tasks(tasks)

    return jsonify(new_task), 201


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates an existing task."""
    data = request.get_json(silent=True)

    with file_lock:
        tasks = read_tasks()
        task = find_task(tasks, task_id)

        if task is None:
            return jsonify({"error": f"No task found with id '{task_id}'."}), 404

        errors = validate_task_data(data, is_creation=False)
        if errors:
            return jsonify({"errors": errors}), 400

        task["title"] = data["title"]
        task["description"] = data["description"]
        task["status"] = data["status"]

        write_tasks(tasks)

    return jsonify(task), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes a task by its id."""
    with file_lock:
        tasks = read_tasks()
        task = find_task(tasks, task_id)

        if task is None:
            return jsonify({"error": f"No task found with id '{task_id}'."}), 404

        tasks = [t for t in tasks if str(t.get("id")) != str(task_id)]
        write_tasks(tasks)

    return jsonify({"message": f"Task '{task_id}' deleted successfully."}), 200


if __name__ == "__main__":
    app.run(debug=True)
