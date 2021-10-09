from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

app = Flask(__name__)
app.secret_key = "123456"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    date_of_birth = Column(Date)
    date_of_joining = Column(Date)

    def __init__(self, name, date_of_birth, date_of_joining):
        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_joining = date_of_joining


# This is the index route where we are going to
# query on all our student data
@app.route('/')
def Index():
    all_data = Student.query.all()

    return render_template("index.html", students=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        date_of_joining = request.form['date_of_joining']

        my_data = Student(name, date_of_birth,date_of_joining)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our student
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.date_of_birth = request.form['date_of_birth']
        my_data.date_of_joining = request.form['date_of_joining']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our student
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
