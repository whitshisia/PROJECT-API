from flask import Flask,jsonify,request
from flask_migrate import Migrate
app = Flask(__name__)
app.config ["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///libarary.db'
from models import db , Student, Books
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/student", methods=["GET"])
def fetch_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_list.append({
            "id":student.id,
            "name":student.name,
            "age":student.age,
            "email":student.email
        })
    return jsonify(student_list),200

@app.route("/students/<int:id>",methods=["GET"])
def get_student_by_id(student_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)