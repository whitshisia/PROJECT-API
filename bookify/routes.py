from flask import Blueprint, request, jsonify
from .models import db, Book
from sqlalchemy import func
import random

bookify_bp = Blueprint('bookify', __name__)

@bookify_bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to Bookify API 📚",
        "endpoints": [
            "/books (GET, POST)",
            "/books/<id> (GET, PUT, DELETE)"
        ]
    })

# --- CREATE ---
@bookify_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    status = data.get('status', 'Not Read')

    if not title or not author:
        return jsonify({"error": "Title and author are required"}), 400

    new_book = Book(title=title, author=author, status=status)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201


# --- READ ALL ---
@bookify_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


# --- READ ONE ---
@bookify_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())


# --- UPDATE ---
@bookify_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.status = data.get('status', book.status)
    db.session.commit()

    return jsonify(book.to_dict())


# --- DELETE ---
@bookify_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book {book_id} deleted successfully"})

# --- 1. Search books by title or author ---
@bookify_bp.route('/books/search')
def search_books():
    query = request.args.get('q', '')
    results = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
    ).all()
    return jsonify([book.to_dict() for book in results])


# --- 2. Get all books by a specific author ---
@bookify_bp.route('/books/author/<string:author_name>')
def books_by_author(author_name):
    books = Book.query.filter(Book.author.ilike(f"%{author_name}%")).all()
    return jsonify([book.to_dict() for book in books])


# --- 3. Get all books with a specific status (e.g. Read, Not Read) ---
@bookify_bp.route('/books/status/<string:status>')
def books_by_status(status):
    books = Book.query.filter(Book.status.ilike(status)).all()
    return jsonify([book.to_dict() for book in books])


# --- 4. Bulk mark all books as "Read" ---
@bookify_bp.route('/books/mark_all_read', methods=['PUT'])
def mark_all_books_read():
    updated = Book.query.update({Book.status: "Read"})
    db.session.commit()
    return jsonify({"message": f"{updated} books marked as Read"})


# --- 5. Get book statistics (total, read, unread) ---
@bookify_bp.route('/books/stats')
def book_stats():
    total = Book.query.count()
    read_count = Book.query.filter(Book.status == "Read").count()
    unread_count = total - read_count
    return jsonify({
        "total_books": total,
        "read": read_count,
        "not_read": unread_count
    })


# --- 6. Get a random book ---
@bookify_bp.route('/books/random')
def random_book():
    books = Book.query.all()
    if not books:
        return jsonify({"message": "No books available"}), 404
    book = random.choice(books)
    return jsonify(book.to_dict())


# --- 7. Get top authors by number of books ---
@bookify_bp.route('/books/top-authors')
def top_authors():
    from sqlalchemy import func
    data = db.session.query(Book.author, func.count(Book.id)).group_by(Book.author).all()
    return jsonify([{"author": a, "book_count": c} for a, c in data])


# --- 8. Delete all books by a given author ---
@bookify_bp.route('/books/author/<string:author_name>', methods=['DELETE'])
def delete_books_by_author(author_name):
    deleted = Book.query.filter(Book.author.ilike(f"%{author_name}%")).delete()
    db.session.commit()
    return jsonify({"message": f"{deleted} books deleted for author '{author_name}'"})


# --- 9. Update all books by an author (e.g. mark as read) ---
@bookify_bp.route('/books/author/<string:author_name>/mark_read', methods=['PUT'])
def mark_author_books_read(author_name):
    updated = Book.query.filter(Book.author.ilike(f"%{author_name}%")).update({Book.status: "Read"})
    db.session.commit()
    return jsonify({"message": f"{updated} books by '{author_name}' marked as Read"})


# --- 10. Export all books as JSON (for backup) ---
@bookify_bp.route('/books/export')
def export_books():
    books = Book.query.all()
    return jsonify({
        "exported_count": len(books),
        "books": [book.to_dict() for book in books]
    })
