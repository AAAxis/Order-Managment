import os
import secrets


from flask import Flask, render_template, request, redirect, send_from_directory
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from config import mail_username, mail_password


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'key'


app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password


mail = Mail(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


Login_manager = LoginManager()
Login_manager.init_app(app)
Login_manager.login_view = "login"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)




class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    text = db.Column(db.String(100), default=None)
    photo = db.Column(db.String(120), default="image.jpg")
    email = db.Column(db.String(100), default=None)
    isActive = db.Column(db.Boolean, default=True)




    def __repr__(self):
        return f'<Student {self.username}>'

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/students', photo_name)
    photo.save(file_path)
    return photo_name



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username "})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Student.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")



@Login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))





@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nMessage: {message}",
                      sender=mail_username, recipients=['devacademyspace@outlook.com'])
        mail.send(msg)
        return render_template('contact.html', success=True)

    return render_template('contact.html')








@app.route('/', methods=['POST', 'GET'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/dashboard')
    return render_template('index.html', form=form)



@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
        student = Student.query.get_or_404(id)

        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            text = request.form['text']
            photo = save_images(request.files.get('file'))
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')



            student.password = hashed_password
            student.username = username
            student.email = email
            student.text = text
            student.photo = photo

            db.session.add(student)
            db.session.commit()

            return redirect('/dashboard')

        return render_template('edit.html', student=student)


        user = Student.query.get_or_404(id)

        if request.method == 'POST':
            about = request.form['about']
            username = request.form['username']
            email = request.form['email']


            user.about = about
            user.username = username
            user.email = email


            db.session.add(user)
            db.session.commit()

            return render_template('register.html', success=True)

        return render_template('edit.html', user=user)








@app.route('/admin/<int:id>/delete')
def itemdelete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/admin')
    except:
        return "Error"

    return render_template("admin.html", data=item)


@app.route('/homepage/<int:id>/delete')
def carddelete(id):
    card = Card.query.get_or_404(id)
    try:
        db.session.delete(card)
        db.session.commit()
        return redirect('/homepage')
    except:
        return "Error"

    return render_template("homepage.html", data=card)


@app.route('/adduser/<int:id>/delete')
def userdelete(id):
    user = Student.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/adduser')
    except:
        return "Error"

    return render_template("adduser.html", userlist=user)


@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    items = Item.query.all()

    return render_template('dashboard.html', data=items)



@app.route('/cards', methods=['POST', 'GET'])

def cards():
    cards = Card.query.all()

    return render_template('cards.html', data=cards)




@app.route('/homepage', methods=['POST', 'GET'])
@login_required
def homepage():
    cards = Card.query.all()
    if request.method=="POST":
        title = request.form.get('title')
        link = request.form.get('link')
        text = request.form.get('text')


    try:
        card = Card(title=title, link=link, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/homepage')

    except: "Error"

    return render_template('homepage.html', data=cards)






@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    items = Item.query.all()
    if request.method=="POST":
        title = request.form.get('title')
        link = request.form.get('link')
        text = request.form.get('text')


    try:
        item = Item(title=title, link=link, text=text)
        db.session.add(item)
        db.session.commit()
        return redirect('/admin')

    except: "Error"

    return render_template('admin.html', data=items)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nPassword: {message}",
                      sender=mail_username, recipients=['devacademyspace@outlook.com'])
        mail.send(msg)
        return render_template('register.html', success=True)


    return render_template('register.html')


@app.route('/adduser', methods=['POST', 'GET'])

def adduser():
    users = Student.query.all()
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Student(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/adduser')

    return render_template('adduser.html', form=form, userlist=users)








if __name__ == "__main__":
    app.run(debug=False)

