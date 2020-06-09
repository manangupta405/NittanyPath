"""
DESCRIPTION - Flask app to add and delete names to a hospitals database.

AUTHOR - MANAN  GUPTA

LAST MODIFIED -
"""

from flask import Flask, render_template, request, redirect, url_for,flash
from flask_bcrypt import Bcrypt, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, ValidationError, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.fields.html5 import DateTimeLocalField
import datetime, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nittanypathdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
host = 'http://127.0.0.1:5000/'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# User relational mapping
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    user_role =db.Column(db.Integer)

# Student relational mapping
class Student(db.Model):
    SID = db.Column(db.Text, primary_key=True)
    Name = db.Column(db.Text)
    Email = db.Column(db.Text)
    Age = db.Column(db.Text)
    Zip = db.Column(db.Text)
    Phone = db.Column(db.Text)
    Gender = db.Column(db.Text)
    Password = db.Column(db.Text, nullable=False)
    Street = db.Column(db.Text)


# Professor relational mapping
class Professor(db.Model):
    PID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Email = db.Column(db.Text, unique=True, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    Age = db.Column(db.Text)
    Gender = db.Column(db.Text)
    Office = db.Column(db.Text)


class Course(db.Model):
    Course = db.Column(db.Text, primary_key = True)
    CourseName = db.Column(db.Text)
    CourseDetails = db.Column(db.Text)
    Department = db.Column(db.Text)
    DropDeadline = db.Column(db.Date)


class Section(db.Model):
    Course = db.Column(db.Text, primary_key = True)
    Section = db.Column(db.Text, primary_key = True)
    Capacity = db.Column(db.Text)


class TeachingTeam(db.Model):
    TTID = db.Column(db.Text, primary_key = True)


class HeadsTT(db.Model):
    TTID = db.Column(db.Text, primary_key = True)
    PID = db.Column(db.Text, primary_key = True)


class Enroll(db.Model):
    SID = db.Column(db.Text, primary_key = True)
    Course = db.Column(db.Text, primary_key = True)
    Section = db.Column(db.Text, primary_key = True)

class Teaches(db.Model):
    TTID = db.Column(db.Text)
    Course = db.Column(db.Text, primary_key= True)

class Post(db.Model):
    Post_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Course = db.Column(db.Text)
    Post = db.Column(db.Text)
    Post_By = db.Column(db.Text)

class Assignment(db.Model):
    ASSIGN_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Course = db.Column(db.Text)
    Section = db.Column(db.Text)
    Assignment_No = db.Column(db.Text)
    Description = db.Column(db.Text)
    PublishedOn = db.Column(db.DateTime)
    DueDate = db.Column(db.DateTime)

class Exam(db.Model):
    EXAM_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Course = db.Column(db.Text)
    Section = db.Column(db.Text)
    Exam_No = db.Column(db.Text)
    Description = db.Column(db.Text)
    PublishedOn = db.Column(db.DateTime)
    DueDate = db.Column(db.DateTime)

class AssignmentAssigned(db.Model):
    SID = db.Column(db.Text, primary_key=True)
    ASSIGN_ID = db.Column(db.Text, primary_key=True)
    Grade = db.Column(db.Text)

class ExamAssigned(db.Model):
    SID = db.Column(db.Text, primary_key=True)
    EXAM_ID = db.Column(db.Text, primary_key=True)
    Grade = db.Column(db.Text)

class Comment(db.Model):
    Comment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Comment = db.Column(db.Text)
    Comment_By = db.Column(db.Text)
    Post_ID = db.Column(db.Text)

class AssistsTT(db.Model):
    SID = db.Column(db.Text, primary_key=True)
    TTID = db.Column(db.Text)

class Department(db.Model):
    Department = db.Column(db.Text, primary_key=True)
    DepartmentName = db.Column(db.Text)

# Form using the FlaskForm library with validators
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'),Length(min=5, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class SelectCourse(FlaskForm):
    course = SelectField('Course',id="select_field",choices=[], validators=[InputRequired()],)

class PostForm(FlaskForm):
    course = SelectField('Course', id="post_course", choices =[],validators=[InputRequired()])
    post = TextAreaField('Post', id="post_field", validators=[InputRequired()])

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', id="comment_field", validators=[InputRequired()])

class CreateAssign(FlaskForm):
    assignType = RadioField('Type(EXAM/ASSIGNMENT)', choices=[('1','EXAM'),('2','ASSIGNMENT')], validators=[InputRequired()])
    course = SelectField('Course', id="select_course",choices=[], validators=[InputRequired()])
    section = IntegerField('Section',id="select_section", validators=[InputRequired()])
    assignment_No = StringField('Assignment Number', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    #publishedOn = db.Column(db.DateTime)
    dueDate = DateTimeLocalField('Due Date & Time', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])

class DropCourse(FlaskForm):
    course =  SelectField('Course', id="select_drop_course",choices=[], validators=[InputRequired()])

class AssignmentSelect(FlaskForm):
    course = SelectField('Course',id="select_assign_course",choices=[], validators=[InputRequired()],)
    assignType = RadioField('Type(EXAM/ASSIGNMENT)', choices=[('1','EXAM'),('2','ASSIGNMENT')], validators=[InputRequired()])

class PasswordChange(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),EqualTo('confirm', message = 'Passwords Must Match')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),EqualTo('confirm', message = 'Passwords Must Match')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])

class NewCourse(FlaskForm):
    course = StringField('Course',validators=[InputRequired()])
    courseName = StringField('Course Name', validators=[InputRequired()],)
    courseDetails = TextAreaField('Description')
    department = SelectField('Department',id="select_department",choices=[], validators=[InputRequired()],)
    dropDeadline = DateTimeLocalField('Due Date & Time', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])

class NewStudent(FlaskForm):
    sid = StringField('SID',validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    zip_code = StringField('Zip', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    gender = StringField('Gender', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    street = StringField('Street', validators=[InputRequired()])

# Home Page
@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    form = LoginForm()
    return render_template('index.html',form = form)


# CODE INCLUDED IN STARTER

@app.route('/registerUser', methods=['POST','GET'])
def registerUser():
    form = RegisterForm()
    if form.validate_on_submit():
        role = 1;
        if form.email.data == "admin@Nittanystate.edu":
            role = 3
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None:
            return '<h1>User Already Exists</h1><br><h3><a href="'+ url_for('index') +'">Login again!</a></h3>'
        user = User(email = form.email.data, password = bcrypt.generate_password_hash(form.password.data) , user_role = role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('registerUser.html', form=form)
    

# Deciding the redirect page according to the action

@app.route('/action', methods=['POST', 'GET'])
def action():
    error = None
    if request.method == 'POST':
        action_req = request.form['Action']
        if action_req == "checkInfo":
            return redirect(url_for("checkingInfo"))
        elif action_req == "createPosts":
            return redirect(url_for("posts"))
        elif action_req == "createAssign":
            return redirect(url_for("create_assignment"))
        elif action_req == "submitScores":   
            return redirect(url_for("assignments"))
        elif action_req == "dropCourse":   
            return redirect(url_for("dropCourse"))
        elif action_req == "addCourse":   
            return redirect(url_for("addCourse"))
        elif action_req == "addStudent":   
            return redirect(url_for("addStudent"))
        else:
            return "Error <a href='" + url_for("index") + "'>Go Back</a>"
    return "Error <a href='" + url_for("dashboard") + "'>Go Back</a>"


#Loads a user from the user id
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Logging a user into the system
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return '<h1>Invalid username or password</h1><br><h3><a href="'+ url_for('index') +'">Login again!</a></h3>'
    return redirect(url_for('index'))


# Logging a user out of the system
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Redirecting the user to a the dashboard upon login
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
    
    return render_template('dashboard.html', user = user, role = current_user.user_role)


@app.route('/checkingInfo', methods=['GET','POST'])
@login_required
def checkingInfo():
    user = current_user
    form = PasswordChange()
    data = []
    if user.user_role == 1:
        user = Student.query.filter_by(Email=current_user.email).first()
        for enrollment in Enroll.query.filter_by(SID = user.SID).all():
            course = Course.query.filter_by(Course = enrollment.Course).first()
            ttid = Teaches.query.filter_by(Course = enrollment.Course).first().TTID
            heads = HeadsTT.query.filter_by(TTID = ttid).all()
            professors = []
            for p in heads:
                prof = Professor.query.filter_by(PID = p.PID).first()
                professors.append({"Name": prof.Name, "Email":prof.Email, "Office":prof.Office})
                # Grades Yet to implement
            data.append({"Course": course.Course, "Course Name":course.CourseName, "Details":course.CourseDetails, "Department" : course.Department, "Drop Deadline": course.DropDeadline, "Professors" : professors})
    elif user.user_role == 2:
        return '<h1>This page is only for Students.</h1><br><h3><a href="'+url_for('index')+ '"> Login again! </a></h3>'
    if form.validate_on_submit():
        newUser = User.query.filter_by(email = current_user.email).first()
        newUser.password = bcrypt.generate_password_hash(form.password.data)
        student = Student.query.filter_by(Email = current_user.email).first()
        newStudent = student
        newStudent.Password = bcrypt.generate_password_hash(form.password.data)
        db.session.delete(current_user)
        db.session.add(newUser)
        db.session.commit()
        db.session.delete(student)
        db.session.add(newStudent)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('checkInfo.html', user=user, data=data, role = current_user.user_role, form=form)

@app.route('/posts', methods=['POST', 'GET'])
@login_required
def posts():
    form = SelectCourse()
    User.query.filter(User.id != current_user.id).all()
    user = current_user
    post_data =[]
    if user.user_role == 1:
        user = Student.query.filter_by(Email=current_user.email).first()
        enrolled = Enroll.query.filter_by(SID=user.SID).all()
        courses = [course.Course for course in enrolled]
        choices = [(0, 'Please Select A Course')]
        for course in courses:
            entry = Course.query.filter_by(Course=course).first()
            choices.append((course, course + "|" + entry.CourseName))
        form.course.choices = choices
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email=current_user.email).first()
        teams = HeadsTT.query.filter_by(PID=user.PID).all()
        courses = []
        choices = [(0, 'Please Select A Course')]
        for team in teams:
            teaches = Teaches.query.filter_by(TTID=team.TTID).all()
            for entry in teaches:
                course = entry.Course
                if course not in courses:
                    courses.append(course)
        for course in courses:
            entry = Course.query.filter_by(Course=course).first()
            choices.append((course, course + "|" + entry.CourseName))
        form.course.choices = choices
    if form.validate_on_submit():
        get_posts = Post.query.filter_by(Course = form.course.data).all()
        post_data = [Post.query.filter_by(Post_ID = post.Post_ID).first() for post in get_posts]
        return render_template('post.html', form=form, user=user, post_data=post_data,role = current_user.user_role)
    return render_template('post.html', form=form, user=user, post_data = post_data,role = current_user.user_role)

@app.route('/newPost', methods=['POST', 'GET'])
@login_required
def newPost():
    user = current_user
    form = PostForm()
    choices = []
    if user.user_role == 1:
        user = Student.query.filter_by(Email=current_user.email).first()
        enrolled = Enroll.query.filter_by(SID=user.SID).all()
        courses = [course.Course for course in enrolled]
        choices = [(0, 'Please Select A Course')]
        for course in courses:
            entry = Course.query.filter_by(Course=course).first()
            choices.append((course, course + "|" + entry.CourseName))
        form.course.choices = choices
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email=current_user.email).first()
        teams = HeadsTT.query.filter_by(PID=user.PID).all()
        courses = []
        choices = [(0, 'Please Select A Course')]
        for team in teams:
            teaches = Teaches.query.filter_by(TTID=team.TTID).all()
            for entry in teaches:
                course = entry.Course
                if course not in courses:
                    courses.append(course)
        for course in courses:
            entry = Course.query.filter_by(Course=course).first()
            choices.append((course, course + "|" + entry.CourseName))
        form.course.choices = choices
    if form.validate_on_submit():
        newPost = Post(Course=form.course.data, Post=form.post.data, Post_By=user.Email)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('newPost.html', user=user, form=form,role = current_user.user_role)
    
@app.route('/comment/<post_id>', methods=['POST', 'GET'])
@login_required
def comment(post_id):
    user = current_user
    form = CommentForm()
    comments = Comment.query.filter_by(Post_ID = post_id).all()
    comment_data = [Comment.query.filter_by(Comment_ID = comment.Comment_ID).first() for comment in comments]
    if form.validate_on_submit():
        newComment = Comment(Comment = form.comment.data, Comment_By = user.email, Post_ID = post_id)
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for('comment', post_id=post_id))
    return render_template('comments.html', comment_data = comment_data, user = user,form =form, post_id = post_id,role = current_user.user_role)

@app.route('/create_assignment', methods=['POST','GET'])
@login_required
def create_assignment():
    form = CreateAssign()
    user = current_user
    courseChoices = []
    sectionChoices = {}
    choices = [(0, 'Select a Course')]
    if user.user_role == 2:
        user = Professor.query.filter_by(Email = user.email).first()
        heads = HeadsTT.query.filter_by(PID = user.PID).all()
        ttds = [head.TTID for head in heads]
        for teach in ttds:
            courseChoices = [course.Course for course in Teaches.query.filter_by(TTID = teach) if course.Course not in courseChoices]
        for course in courseChoices:
            choices.append((course,course))
            sections = Section.query.filter_by(Course = course).all()
            sectionChoices[course] = []
            for section in sections:
                sectionChoices[course].append(section.Section)
        form.course.choices = choices
        if form.validate_on_submit():
            if form.assignType.data == 1:
                if str(form.section.data) not in sectionChoices[form.course.data]:
                    return '<h1>Section not available.</h1><br><h3><a href="'+url_for('create_assignment')+ '"> GO Back! </a></h3>'
                newAssign = Exam(Course = form.course.data, Section = str(form.section.data), Exam_No = form.assignment_No.data, Description=form.description.data, PublishedOn = datetime.datetime.now(), DueDate = form.dueDate.data)
                db.session.add(newAssign)
                db.session.commit()
            else:
                if str(form.section.data) not in sectionChoices[form.course.data]:
                    return '<h1>Section not available.</h1><br><h3><a href="'+url_for('create_assignment')+ '"> GO Back! </a></h3>'
                newAssign = Assignment(Course = form.course.data, Section = str(form.section.data), Assignment_No = form.assignment_No.data, Description=form.description.data, PublishedOn = datetime.datetime.now(), DueDate = form.dueDate.data)
                db.session.add(newAssign)
                db.session.commit()
            return '<h1>Assignment Created.</h1><br><h3><a href="'+url_for('create_assignment')+ '"> GO Back! </a></h3>'
    else:
        return '<h1>This page is only for Faculty Members.</h1><br><h3><a href="'+url_for('index')+ '"> Login again! </a></h3>' 
    return render_template('createAssign.html', form=form, user=current_user,role = current_user.user_role)

@app.route('/dropCourse', methods=['POST', 'GET'])
@login_required
def dropCourse():
    user = current_user
    form = DropCourse()
    choices = [(0, "Select A Course To DROP")]
    if user.user_role == 1:
        user = Student.query.filter_by(Email = user.email).first()
        getEnrolls = Enroll.query.filter_by(SID = user.SID).all()
        for enroll in getEnrolls:
            choices.append((enroll.Course, enroll.Course))
        form.course.choices = choices
        if form.validate_on_submit():
            enroll = Enroll.query.filter_by(SID = user.SID, Course = form.course.data).first()
            posts = Post.query.filter_by(Post_By = user.Email).all()
            for post in posts:
                db.session.delete(post)
            db.session.delete(enroll)
            db.session.commit()
            return redirect(url_for('dropCourse'))
    else:
        return '<h1>This page is only for Students.</h1><br><h3><a href="'+url_for('index')+ '"> Login again! </a></h3>'
    return render_template('dropCourse.html', form=form, user=user,role = current_user.user_role)

@app.route('/assignments', methods=['POST','GET'])
@login_required
def assignments():
    user = current_user
    form = AssignmentSelect()
    choices = [(0,'Select a Course')]
    type = 0
    length = ""
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
        teachAssist = AssistsTT.query.filter_by(SID = user.SID).first()
        if teachAssist is not None:
            teachTeam = Teaches.query.filter_by(TTID = teachAssist.TTID).all()
            for team in teachTeam:
                choices.append((team.Course,team.Course))
            form.course.choices = choices
        else:
            return '<h1>This page is only for Faculty and Assistants.</h1><br><h3><a href="'+url_for('dashboard')+ '"> Back to Dashboard! </a></h3>'
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
        teams = HeadsTT.query.filter_by(PID = user.PID).all()
        for head in teams:
            teachTeam = Teaches.query.filter_by(TTID = head.TTID).all()
            for team in teachTeam:
                choices.append((team.Course,team.Course))
        form.course.choices = choices
    if form.validate_on_submit():
        type = form.assignType.data
        course = form.course.data
        data = []
        if type == "1":
            length = course
            exams = Exam.query.filter_by(Course = course).all()
            data = [Exam.query.filter_by(EXAM_ID = assignment.EXAM_ID).first() for assignment in exams]
        elif type == "2":
            length = course
            assignments = Assignment.query.filter_by(Course = course).all()
            data = [Assignment.query.filter_by(ASSIGN_ID = assignment.ASSIGN_ID).first() for assignment in assignments]
        return render_template('assignments.html', form=form, user=user, data = data, length = length, type=type,role = current_user.user_role)
    return render_template('assignments.html', form=form, user=user,type=type,role = current_user.user_role)

@app.route('/enterExamGrades/<examId>', methods=['POST', 'GET'])
@login_required
def enterExamGrades(examId):
    user = current_user
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
        teachAssist = AssistsTT.query.filter_by(SID = user.SID).first()
        if teachAssist is None:
            return '<h1>This page is only for Faculty and Assistants.</h1><br><h3><a href="'+url_for('dashboard')+ '"> Back to Dashboard! </a></h3>'
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
    exams = ExamAssigned.query.filter_by(EXAM_ID = str(examId)).all()
    data = [(exam.SID, Student.query.filter_by(SID = exam.SID).first().Name,exam.Grade, exam.EXAM_ID) for exam in exams]
    return render_template('assignGrade.html', user=user, data=data, type = 1,role = current_user.user_role)

@app.route('/enterAssignmentGrades/<assignId>', methods=['POST', 'GET'])
@login_required
def enterAssignmentGrades(assignId):
    user = current_user
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
        teachAssist = AssistsTT.query.filter_by(SID = user.SID).first()
        if teachAssist is None:
            return '<h1>This page is only for Faculty and Assistants.</h1><br><h3><a href="'+url_for('dashboard')+ '"> Back to Dashboard! </a></h3>'
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
    assignments  = AssignmentAssigned.query.filter_by(ASSIGN_ID = assignId).all()
    data = [(assign.SID,Student.query.filter_by(SID = assign.SID).first().Name, assign.Grade, assign.ASSIGN_ID)for assign in assignments]
    return render_template('assignGrade.html', user=user, data=data, type = 2,role = current_user.user_role)

    
@app.route('/updateExamGrade/<examID>', methods=['POST','GET'])
@login_required
def updateExamGrade(examID):
    user = current_user
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
        teachAssist = AssistsTT.query.filter_by(SID = user.SID).first()
        if teachAssist is None:
            return '<h1>This page is only for Faculty and Assistants.</h1><br><h3><a href="'+url_for('dashboard')+ '"> Back to Dashboard! </a></h3>'
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
    if request.method == 'POST':
        studentID = str(request.form.get('SID'))
        grade = str(request.form.get('Grade'))
        assign = ExamAssigned.query.filter_by(SID = studentID, EXAM_ID = examID).first()
        db.session.delete(assign)
        assign.Grade = grade
        db.session.add(assign)
        db.session.commit()
        return redirect(url_for('enterExamGrades', examId=examID))
    return redirect(url_for('enterExamGrades', examId=examID))

@app.route('/updateAssignGrade/<assignID>', methods=['POST','GET'])
@login_required
def updateAssignGrade(assignID):
    user = current_user
    if user.user_role == 1:
        user = Student.query.filter_by(Email = current_user.email).first()
        teachAssist = AssistsTT.query.filter_by(SID = user.SID).first()
        if teachAssist is None:
            return '<h1>This page is only for Faculty and Assistants.</h1><br><h3><a href="'+url_for('dashboard')+ '"> Back to Dashboard! </a></h3>'
    elif user.user_role == 2:
        user = Professor.query.filter_by(Email = current_user.email).first()
    if request.method == 'POST':
        studentID = str(request.form.get('SID'))
        grade = str(request.form.get('Grade'))
        assign = AssignmentAssigned.query.filter_by(SID = studentID, ASSIGN_ID = assignID).first()
        db.session.delete(assign)
        assign.Grade = grade
        db.session.add(assign)
        db.session.commit()
        return redirect(url_for('enterAssignmentGrades', assignId=assignID))
    return redirect(url_for('enterAssignmentGrades', assignId=assignID))

@app.route('/addCourse', methods=['POST','GET'])
@login_required
def addCourse():
    form = NewCourse()
    user = current_user
    if user.user_role != 3:
        return '<h1>Only For Admin</h1><br><h3><a href="'+url_for('index')+ '"> Login! </a></h3>'
    choices = [(0, "Select A Department")] + [(department.Department, department.Department) for department in Department.query.all()]
    form.department.choices = choices
    if form.validate_on_submit():
        oldCourse = Course.query.filter_by(Course = form.course.data).first()
        if oldCourse is not None:
            return '<h1>Course Already Exists</h1><br><h3><a href="'+url_for('addCourse')+ '"> Go Back! </a></h3>'
        else:
            course = Course(Course = form.course.data, CourseName = form.courseName.data, CourseDetails = form.courseDetails.data, Department=form.department.data, DropDeadline = form.dropDeadline.data)
            db.session.add(course)
            db.session.commit()
            return '<h1>Course Added</h1><br><h3><a href="'+url_for('addCourse')+ '"> Add Another! </a></h3>'
    return render_template('newCourse.html', form = form)

@app.route('/addStudent', methods=['POST','GET'])
@login_required
def addStudent():
    form = NewStudent()
    user = current_user
    if user.user_role != 3:
        return '<h1>Only For Admin</h1><br><h3><a href="'+url_for('index')+ '"> Login! </a></h3>'
    if form.validate_on_submit():
        student = Student.query.filter_by(SID = form.sid.data).first()
        if student is not None:
            return '<h1>Student Already Exists</h1><br><h3><a href="'+url_for('addStudent')+ '"> Go Back! </a></h3>'
        else:
            student = Student(SID = form.sid.data, eName = form.name.data, Email = form.email.data, Age=form.age.data, Zip = form.zip_code.data, Phone= form.phone.data, Gender=form.gender.data, Password = bcrypt.generate_password_hash(form.password.data), Street=form.street.data)
            db.session.add(student)
            db.session.commit()
            return '<h1>Student Added</h1><br><h3><a href="'+url_for('addStudent')+ '"> Add Another! </a></h3>'
    return render_template('newStudent.html', form = form)

# Adding name to the database using add_patient method
# Template Name - addName.html
if __name__ == "__main__":
    app.run()


