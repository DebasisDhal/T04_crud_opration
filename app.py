from flask import Flask, render_template, request, jsonify
from models import db, StudentModel
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'xdfjdfkl'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/', methods = ['GET', 'POSt'])
def create():
     if request.method == 'GET':
          return render_template('create.html')

# Add student    
@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        date_of_birth_str = data.get('date_of_birth')

        if not all([name, email, age, date_of_birth_str]):
            return jsonify({"error": "All fields are required"}), 400

        try:
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

        new_student = StudentModel(name=name, email=email, age=age, date_of_birth=date_of_birth)
        db.session.add(new_student)
        db.session.commit()

        return jsonify({"message": "Student added successfully", "id": new_student.id}), 201

    except Exception as e:
        app.logger.error(f"Error occurred while adding student: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    students = StudentModel.query.all()
    return jsonify([{"id": student.id, "name": student.name, "email": student.email, "age": student.age, "date_of_birth": student.date_of_birth.strftime('%Y-%m-%d')} for student in students]), 200

# Update
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = StudentModel.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.age = data.get('age', student.age)
    student.date_of_birth = data.get('date_of_birth', student.date_of_birth)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"}), 200

# Delete
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = StudentModel.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200



if __name__ == "__main__":
    app.run(debug = True)

