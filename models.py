from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String, unique=True, nullable=False)
    section1 = db.Column(db.String, unique=False, nullable=False)
    section2 = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, dept_name, section1, section2):
        self.dept_name = dept_name
        self.section1 = section1
        self.section2 = section2


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, unique=True, nullable=False)
    lname = db.Column(db.String, unique=False, nullable=False)
    father_name = db.Column(db.String, unique=False, nullable=False)
    mother_name = db.Column(db.String, unique=False, nullable=False)
    dob = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    personal_email = db.Column(db.String, unique=False, nullable=False)
    student_email = db.Column(db.String, unique=False, nullable=False)
    phone_no = db.Column(db.String, unique=False, nullable=False)
    parent_phone_no = db.Column(db.String, unique=False, nullable=False)
    roll_no = db.Column(db.Integer, unique=False, nullable=False)
    registration_no = db.Column(db.Integer, unique=False, nullable=False)
    imei_no = db.Column(db.Integer, unique=False, nullable=False)
    trade = db.Column(db.String, unique=False, nullable=False)
    section = db.Column(db.String, unique=False, nullable=False)
    aadhaar = db.Column(db.Integer, unique=False, nullable=False)
    present_lect = db.Column(db.Integer, unique=False, nullable=False)
    absent_lect = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, fname, lname, father_name, mother_name, dob, gender, personal_email, student_email, phone_no,
                 parent_phone_no, roll_no, registration_no, imei_no, trade, section, aadhaar):
        self.fname, self.lname, self.father_name, self.mother_name, self.dob, self.gender, self.personal_email, self.student_email, self.phone_no, self.parent_phone_no, self.roll_no, self.registration_no, self.imei_no, self.trade, self.section, self.aadhaar = fname, lname, father_name, mother_name, dob, gender, personal_email, student_email, phone_no, parent_phone_no, roll_no, registration_no, imei_no, trade, section, aadhaar
        self.present_lect = 0
        self.absent_lect = 0


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, unique=False, nullable=False)
    exam_name = db.Column(db.String, unique=False, nullable=False)
    detail = db.Column(db.JSON, unique=False, nullable=True)
    subjects = db.Column(db.String, unique=False, nullable=True)

    def __init__(self, class_name, exam_name, subjects):
        self.class_name = class_name
        self.exam_name = exam_name
        self.subjects = subjects


db.create_all()
