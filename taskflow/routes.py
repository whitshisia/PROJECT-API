from flask import Blueprint, request, jsonify
from .models import db, Task
from sqlalchemy import func
import random
from datetime import datetime, timedelta

taskflow_bp = Blueprint('taskflow', __name__)

@taskflow_bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to TaskFlow API ✅",
        "endpoints": [
            "/tasks (GET, POST)",
            "/tasks/<id> (GET, PUT, DELETE)"
        ]
    })


# --- CREATE ---
@taskflow_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


# --- READ ALL ---
@taskflow_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# --- READ ONE ---
@taskflow_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict())


# --- UPDATE ---
@taskflow_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()

    return jsonify(task.to_dict())


# --- DELETE ---
@taskflow_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} deleted successfully"})

# --- 1. Search tasks by title or description ---
@taskflow_bp.route('/tasks/search')
def search_tasks():
    query = request.args.get('q', '')
    results = Task.query.filter(
        (Task.title.ilike(f"%{query}%")) | (Task.description.ilike(f"%{query}%"))
    ).all()
    return jsonify([task.to_dict() for task in results])


# --- 2. Get all completed tasks ---
@taskflow_bp.route('/tasks/completed')
def completed_tasks():
    tasks = Task.query.filter_by(completed=True).all()
    return jsonify([task.to_dict() for task in tasks])


# --- 3. Get all incomplete tasks ---
@taskflow_bp.route('/tasks/pending')
def pending_tasks():
    tasks = Task.query.filter_by(completed=False).all()
    return jsonify([task.to_dict() for task in tasks])


# --- 4. Toggle task completion ---
@taskflow_bp.route('/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.completed = not task.completed
    db.session.commit()
    return jsonify({
        "message": f"Task {task.id} marked as {'completed' if task.completed else 'incomplete'}",
        "task": task.to_dict()
    })


# --- 5. Delete all completed tasks ---
@taskflow_bp.route('/tasks/clear_completed', methods=['DELETE'])
def clear_completed_tasks():
    deleted = Task.query.filter_by(completed=True).delete()
    db.session.commit()
    return jsonify({"message": f"{deleted} completed tasks deleted"})

# --- 6. Get a random task ---
@taskflow_bp.route('/tasks/random')
def random_task():
    tasks = Task.query.all()
    if not tasks:
        return jsonify({"message": "No tasks found"}), 404
    return jsonify(random.choice(tasks).to_dict())


# --- 7. Get task statistics ---
@taskflow_bp.route('/tasks/stats')
def task_stats():
    total = Task.query.count()
    completed = Task.query.filter_by(completed=True).count()
    pending = total - completed
    return jsonify({
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": f"{(completed/total*100):.1f}%" if total else "0%"
    })


# --- 8. Get tasks created recently (within X days) ---
@taskflow_bp.route('/tasks/recent')
def recent_tasks():
    days = int(request.args.get('days', 7))
    cutoff = datetime.utcnow() - timedelta(days=days)
    tasks = Task.query.filter(Task.id >= 1).order_by(Task.id.desc()).limit(10).all()  # Simulated
    return jsonify([task.to_dict() for task in tasks])


# --- 9. Bulk toggle all tasks (mark all done or undone) ---
@taskflow_bp.route('/tasks/toggle_all', methods=['PUT'])
def toggle_all_tasks():
    flag = request.args.get('completed', 'true').lower() == 'true'
    updated = Task.query.update({Task.completed: flag})
    db.session.commit()
    return jsonify({"message": f"{updated} tasks marked as {'completed' if flag else 'pending'}"})


# --- 10. Export all tasks as JSON ---
@taskflow_bp.route('/tasks/export')
def export_tasks():
    tasks = Task.query.all()
    return jsonify({
        "exported_count": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    })
