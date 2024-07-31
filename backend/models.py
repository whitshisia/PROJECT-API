from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    books = db.relationship("Books", backref='student')
class Books(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20),nullable=False)
    
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'), nullable=False)