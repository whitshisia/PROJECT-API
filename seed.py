# seed.py
import os
from faker import Faker
from app import app, db
from bookify.models import Book
from taskflow.models import Task
from notenest.models import Note

fake = Faker()

def seed_books(n=10):
    for _ in range(n):
        book = Book(
            title=fake.sentence(nb_words=3),
            author=fake.name(),
            status=fake.random_element(elements=["Not Read", "Reading", "Completed"])
        )
        db.session.add(book)
    db.session.commit()
    print(f"✅ Added {n} fake books")


def seed_tasks(n=15):
    for _ in range(n):
        task = Task(
            title=fake.sentence(nb_words=4),
            description=fake.text(max_nb_chars=150),
            completed=fake.boolean(chance_of_getting_true=30)
        )
        db.session.add(task)
    db.session.commit()
    print(f"✅ Added {n} fake tasks")


def seed_notes(n=12):
    for _ in range(n):
        note = Note(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3)
        )
        db.session.add(note)
    db.session.commit()
    print(f"✅ Added {n} fake notes")


if __name__ == "__main__":
    with app.app_context():
        print("🌱 Seeding database...")

        # ⚠️ Only drop tables in local dev, not in Render
        if os.environ.get("RENDER") == "true":
            print("⚠️ Running in Render environment — skipping db.drop_all() to protect production data.")
        else:
            db.drop_all()
            print("🧹 Dropped all tables (local environment).")

        # ✅ Ensure tables exist
        db.create_all()

        # ✅ Add fake data
        seed_books()
        seed_tasks()
        seed_notes()

        print("🌳 Done seeding!")
