from app import app, db, allowed_file
from flask import url_for, redirect, render_template, request, jsonify, session, flash
from werkzeug.utils import secure_filename
import os
from form import LoginForm
from methods import add_user, login_user, user_logged
from models import User, Department, Student, Exam
import smtplib


@app.route('/', methods=['post', 'get'])
def home_page():
    form = LoginForm()
    if request.method == "GET":
        if user_logged():
            return redirect("/dashboard ")
        else:
            return render_template("index.html", form=form)
    else:
        if form.validate_on_submit():
            data = request.form.to_dict()
            user = User.query.filter_by(username=data['username'], password=data['password']).first()
            if user:
                flash(f'User has been successfully logged in', 'success')
                login_user(data['username'])
                return redirect("/dashboard")
            else:
                flash(f'Incorrect User/Password', 'danger')
                return redirect("/")
        else:
            return render_template("index.html", form=form)


@app.route("/dashboard")
def dashboard():
    if user_logged():

        mcount = len([x for x in Student.query.filter_by(gender="male")])
        fcount = len([x for x in Student.query.filter_by(gender="female")])
        return render_template("dashboard.html", no_of_student=len([x for x in Student.query.filter_by()]),
                               no_of_admin=len([x for x in User.query.filter_by()]),
                               no_of_exam=len([x for x in Exam.query.filter_by()]), mcount=mcount, fcount=fcount)
    else:
        return redirect("/")


@app.route("/users", methods=['post', 'get'])
def users():
    if request.method == "POST":
        print(request.form.to_dict())
    if user_logged():
        return render_template("users.html", users=User.query.filter_by())
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    if user_logged():
        del session['username']
        del session['logged_in']
    return redirect("/")


@app.route("/adduser", methods=['get'])
def adduser():
    if user_logged():
        username = request.args.get("username")
        pwd = request.args.get("password")
        if request.args.get("action") == "update":
            selected_user = User.query.filter_by(id=request.args.get("id")).first()
            selected_user.username = username
            selected_user.password = pwd
            db.session.commit()
        elif request.args.get("action") == "delete":
            obj = User.query.filter_by(username=username).one()
            db.session.delete(obj)
            db.session.commit()
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                flash(f'User already exist!', 'danger')
            else:
                flash(f"Sucessfully added user", "success")
                user = User(username, pwd)
                db.session.add(user)
                db.session.commit()
        return redirect("/users")

    else:
        return redirect("/")


@app.route("/managestudent", methods=['get', 'post'])
def manage_student():
    if request.method == "POST":
        data = request.form.to_dict()
        student = Student(data['fname'], data['lname'], data['ffname'], data['mfname'], data['dob'], data['gender'],
                          data['personal_email'], data['student_email'], data['phno'], data['pphno2'], data['rollno'],
                          data['registerno'], data['imeino'],
                          data['trade'], data['section'], data['aadhaar'])
        db.session.add(student)
        db.session.commit()
        return redirect("/managestudent")
    else:
        depts = [x for x in Department.query.filter_by()]
        students = [x for x in Student.query.filter_by()]
        if request.args.get("delete"):
            id_del = request.args.get("delete")
            obj = Student.query.filter_by(id=id_del).first()
            db.session.delete(obj)
            db.session.commit()
            return redirect("/managestudent")

        return render_template("managestudent.html", depts=depts, students=students)


@app.route("/department", methods=['get', 'post'])
def department():
    if request.method == 'POST':
        data = request.form.to_dict()
        selected_dept = Department.query.filter_by(dept_name=data['trade']).first()
        if selected_dept:
            flash("Department Already Exists!", "danger")
        else:
            dept = Department(data['trade'], data['section1'], data['section2'])
            db.session.add(dept)
            db.session.commit()
            flash("Department has been added!", "success")
        return redirect("/department")
    else:
        if request.args.get("del"):
            obj = Department.query.filter_by(id=request.args.get("del")).one()
            if obj:
                db.session.delete(obj)
                db.session.commit()
            return redirect("/department")
        depts = [x for x in Department.query.filter_by()]
        if request.args.get("show"):
            sel_dept = Department.query.filter_by(dept_name=request.args.get("show")).first()
            return f"<option>{sel_dept.section1}</option>" \
                   f"<option>{sel_dept.section2}</option>"

        return render_template("department.html", depts=depts)


@app.route("/attendance", methods=['POST', 'GET'])
def attendance_page():
    students = [x for x in Student.query.filter_by()]
    if request.args.get("id"):
        selected_user = Student.query.filter_by(id=request.args.get("id")).first()
        if request.args.get("present_lect"):
            selected_user.present_lect = request.args.get("present_lect")
        if request.args.get("absent_lect"):
            selected_user.absent_lect = request.args.get("absent_lect")
        db.session.commit()
        return redirect("/attendance")
    else:
        return render_template("/attendance.html", students=students)


@app.route("/marks", methods=['POST', 'GET'])
def marks():
    exams = [x for x in Exam.query.filter_by()]
    students = [x for x in Student.query.filter_by()]
    depts = [x for x in Department.query.filter_by()]
    if request.args.get("exam"):
        obj = Exam.query.filter_by(id=request.args.get("exam")).one()
        roll = [x[0] for x in obj.detail] if obj.detail else []
        hidden = 0
        if len(roll) > 0 and roll.index("") != 0:
            hidden = roll.index("")
        return render_template("marks.html", exams=exams, students=students, depts=depts,
                               current_exam=Exam.query.filter_by(id=request.args.get("exam")).first(), hidden=hidden)
    return render_template("marks.html", exams=exams, students=students, depts=depts, hidden=80)


@app.route("/addexam", methods=["POST", "GET"])
def addexam():
    if request.method == "POST":
        form = request.form.to_dict()
        exam = Exam(form['class_name'], form['exam_name'], form['subjects'])
        db.session.add(exam)
        db.session.commit()
        return redirect("/marks")
    else:
        obj = Exam.query.filter_by(id=request.args.get("del")).one()
        db.session.delete(obj)
        db.session.commit()
        return redirect("/marks")


@app.route("/updateExam", methods=["POST", "GET"])
def updateExam():
    if request.method == "POST":

        data = request.get_json()
        exam_id = request.headers.get("Referer").split("=")[-1]
        obj = Exam.query.filter_by(id=exam_id).one()
        obj.detail = data
        db.session.commit()
        return "True"
    else:
        exam_id = request.args.get("id")
        obj = Exam.query.filter_by(id=exam_id).one()
        return jsonify(obj.detail)


@app.route("/send_email", methods=['POST', 'GET'])
def send_email():
    if request.method == "POST":
        form = request.form.to_dict()
        emails = [x.strip() for x in form['emaillist'].split("\n") if x.strip()]
        msg = Message(emails, form['subject'], form['body'])
        if msg:
            flash(f"Email sent to {len(emails)} Emails", "success")
        else:
            flash(f"Failed to send Email, contact administrator", "danger")
        return render_template("send_email.html", students=[x for x in Student.query.filter_by()])
    else:
        return render_template("send_email.html", students=[x for x in Student.query.filter_by()])


@app.route("/temp", methods=['POST', 'GET'])
def temp():
    return render_template("home.html")


def Message(email, subject, body):
    FROM = "gauravverma64786@gmail.com"
    TO = email if isinstance(email, list) else [email]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        print(email, subject, body)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("gauravverma64786@gmail.com", "tshkqvxigzfgibuy")
        server.sendmail(FROM, TO, message)
        server.close()

        return True
    except Exception as e:
        print(e)
        return False


db.create_all()
