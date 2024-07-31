from faker import Faker
from models import db,Student, Books
from app import app

faker = Faker()
print ('start seeding.......')
def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        for i in range(6):
            student = Student(
                name = faker.name(),
                age = faker.random_int(min=18, max=60),
                email = faker.email()
            )
            db.session.add(student)
            db.session.commit()
        for i in range(6):
            book = Books(
                title = faker.word(),
                author = faker.name(),
                description = faker.sentence(),
                student_id = faker.random_int(min=1, max=6) 
            )  
            db.session.add(book)
            db.session.commit()  
seed_data()        
print ("done ")