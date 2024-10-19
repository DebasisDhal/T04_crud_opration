from flask import Flask, flash, render_template, request, jsonify, url_for, redirect
from models import db, StudentModel
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'xdfjdfkl'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        # Extracting form data from the request
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']

        # Convert the date string from the form to a Python date object
        date_of_birth_str = request.form['date_of_birth']
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()

        # Creating a new student object and adding it to the database
        new_student = StudentModel(name=name, email=email, age=age, date_of_birth=date_of_birth)
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('list_students'))

    except Exception as e:
        # In case of an error, flash an error message and redirect to the form
        flash(f'Error occurred while adding student: {e}', 'error')
        return redirect(url_for('index'))

# Get all students
@app.route('/students', methods=['GET'])
def list_students():
    students = StudentModel.query.all()
    return render_template('student_list.html', students=students)

# Update
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
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
    return redirect(url_for('list_students'))

# Delete
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = StudentModel.query.get(student_id)
    # if student is None:
    #     return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('list_students'))



if __name__ == "__main__":
    app.run(debug = True)

