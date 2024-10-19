from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    

    def __init__(self, name, email, age, date_of_birth):
        self.name = name
        self.email = email
        self.age = age
        self.date_of_birth = date_of_birth
        


    def __repr__(self):
        return f"<Student {self.name}>"