from flask import Blueprint, request, jsonify
from .models import db, Note
from sqlalchemy import func
from datetime import datetime, timedelta
import random 

notenest_bp = Blueprint('notenest', __name__)

@notenest_bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to NoteNest API 📝",
        "endpoints": [
            "/notes (GET, POST)",
            "/notes/<id> (GET, PUT, DELETE)"
        ]
    })


# --- CREATE ---
@notenest_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Both title and content are required"}), 400

    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201


# --- READ ALL ---
@notenest_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])


# --- READ ONE ---
@notenest_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note.to_dict())


# --- UPDATE ---
@notenest_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()

    return jsonify(note.to_dict())


# --- DELETE ---
@notenest_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": f"Note {note_id} deleted successfully"})

# --- 1. Search notes by title or content ---
@notenest_bp.route('/notes/search')
def search_notes():
    query = request.args.get('q', '')
    results = Note.query.filter(
        (Note.title.ilike(f"%{query}%")) | (Note.content.ilike(f"%{query}%"))
    ).all()
    return jsonify([note.to_dict() for note in results])


# --- 2. Get recent notes (created in last X days) ---
@notenest_bp.route('/notes/recent')
def recent_notes():
    days = int(request.args.get('days', 7))
    cutoff = datetime.utcnow() - timedelta(days=days)
    notes = Note.query.filter(Note.created_at >= cutoff).order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])


# --- 3. Sort notes (asc or desc) ---
@notenest_bp.route('/notes/sorted')
def sorted_notes():
    order = request.args.get('order', 'desc')
    if order == 'asc':
        notes = Note.query.order_by(Note.created_at.asc()).all()
    else:
        notes = Note.query.order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])


# --- 4. Get word count for all notes ---
@notenest_bp.route('/notes/wordcount')
def note_wordcount():
    notes = Note.query.all()
    total_words = sum(len(note.content.split()) for note in notes)
    return jsonify({
        "note_count": len(notes),
        "total_words": total_words,
        "average_words": total_words / len(notes) if notes else 0
    })


# --- 5. Delete all notes ---
@notenest_bp.route('/notes/clear_all', methods=['DELETE'])
def clear_all_notes():
    deleted = Note.query.delete()
    db.session.commit()
    return jsonify({"message": f"{deleted} notes deleted"})


# --- 6. Get a random note ---
@notenest_bp.route('/notes/random')
def random_note():
    notes = Note.query.all()
    if not notes:
        return jsonify({"message": "No notes found"}), 404
    return jsonify(random.choice(notes).to_dict())


# --- 7. Get notes summary (count + average length) ---
@notenest_bp.route('/notes/summary')
def note_summary():
    notes = Note.query.all()
    count = len(notes)
    total_chars = sum(len(note.content) for note in notes)
    avg_length = total_chars / count if count else 0
    return jsonify({
        "note_count": count,
        "avg_characters": avg_length,
        "total_characters": total_chars
    })


# --- 8. Get notes containing a keyword ---
@notenest_bp.route('/notes/contains/<string:keyword>')
def notes_containing(keyword):
    results = Note.query.filter(Note.content.ilike(f"%{keyword}%")).all()
    return jsonify([note.to_dict() for note in results])


# --- 9. Delete notes older than X days ---
@notenest_bp.route('/notes/cleanup', methods=['DELETE'])
def cleanup_old_notes():
    days = int(request.args.get('days', 30))
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted = Note.query.filter(Note.created_at < cutoff).delete()
    db.session.commit()
    return jsonify({"message": f"{deleted} old notes deleted"})


# --- 10. Export all notes as JSON ---
@notenest_bp.route('/notes/export')
def export_notes():
    notes = Note.query.all()
    return jsonify({
        "exported_count": len(notes),
        "notes": [note.to_dict() for note in notes]
    })
