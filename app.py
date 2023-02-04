import os
import secrets
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import random
import string
import paypalrestsdk
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





class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(120), default='branch.jpg')
    operation = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return self.title


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(120), default='product.jpg')
    group = db.Column(db.String(100), nullable=False)
    store = db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return self.title




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(120), default="image.jpg")
    email = db.Column(db.String(100), nullable=False, unique=True)
    isActive = db.Column(db.Boolean, default=True)





def __repr__(self):
    return f'<User {self.username}>'



def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/images/users', photo_name)
    photo.save(file_path)
    return photo_name


def get_random_string():
    # choose from all lowercase letter
    characters = string.ascii_uppercase + string.digits
    token = ''.join(random.choice(characters) for i in range(10))
    return token




@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        name = request.form.get('username')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\n{message}",
                      sender=mail_username, recipients=['polskoydm@gmail.com'])
        mail.send(msg)
        return render_template('contact.html', success=True)

    return render_template('contact.html')



@app.route('/payment', methods=['POST', 'GET'])
def payment():

    # Extract the payment information from the link parameters

    token = request.args.get("token")
    order = request.args.get("order")
    email = request.args.get("email")

    msg = Message(subject=f"We handle your order {email}", body=f"Order #{order}\nJoin order status here https://wheelsworks.000webhostapp.com/email-done.php?order={order}&token={token}",
    sender=mail_username)
    msg.recipients = [str(email)]

    mail.send(msg)

    return render_template('payment.html')





@app.route('/newchat', methods=['POST', 'GET'])
def newchat():

        token = request.args.get("token")
        email = request.args.get("email")

        msg = Message(subject=f"New Message from {email}", body=f"Join Chat https://wheelsworks.000webhostapp.com/messages.php?token={token}&email={email}",
        sender=mail_username, recipients=['polskoydm@gmail.com'])

        mail.send(msg)
        return redirect('https://wheelsworks.000webhostapp.com/messages.php?token='+token+'&email='+email)




@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('index.html')

@app.route('/cart', methods=['POST', 'GET'])
def demo():

    return redirect('https://wheelsworks.000webhostapp.com/shopping-cart.php?token=8ZLL5LKCF4')


# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        session['email'] = email

        user = User.query.filter_by(email = email).first()
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        else:
            return 'PASSWORD INCORRECT'


    return render_template('login.html')






@app.route('/<path:id>/item', methods=['POST', 'GET'])
@login_required
def selectitem(id):


    rows = Product.query.filter_by(store=id)

    return render_template('item.html', rows=rows, token=id)



@app.route('/<path:id>/additem', methods=['POST', 'GET'])
@login_required
def additem(id):

    if request.method == "POST":

        logo = save_images(request.files.get('file'))
        item = request.form['title']
        value = request.form['price']
        group = request.form['group']
        token = str(id)

        new_product = Product(item=item, value=value, group=group, store=token, logo=logo)

        db.session.add(new_product)
        db.session.commit()

        return redirect('https://wheelsworks.000webhostapp.com/additem.php?store='+token+'&file='+logo+'&group='+group+'&value='+value+'&item='+item)

    else:

        return 'ERROR UPLOAD IMAGE'





@app.route('/<path:id>/deleteitem', methods=['POST', 'GET'])
def itemdelete(id):
    if request.method == 'POST':
        store = request.form['delete']
        prod = request.form['prod']

        item = Product.query.get_or_404(id)
        token = str(store)
        db.session.delete(item)
        db.session.commit()


        return redirect('https://wheelsworks.000webhostapp.com/deleteitem.php?prod='+prod+'&token='+token)

    else:

        return 'ERROR DELETE'






@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():

        email = session['email']

        rows = Branch.query.filter_by(email = email)

        return render_template('dashboard.html', rows=rows)


@app.route('/addbranch', methods=['POST', 'GET'])
@login_required
def addbranch():


    if request.method == "POST":
        token = str(get_random_string())
        logo = save_images(request.files.get('file'))
        email = session['email']
        title = request.form['title']
        operation = request.form['operation']
        address = request.form['address']


        new_branch = Branch(token=token, title=title, operation=operation, email=email, address=address, logo=logo)

        db.session.add(new_branch)
        db.session.commit()

        return redirect('https://wheelsworks.000webhostapp.com/addbranch.php?title='+title+'&operation='+operation+'&address='+address+'&logo='+logo+'&email='+email+'&token='+token)

    else:

        return 'ERROR UPLOAD IMAGE'



@app.route('/settings/<int:id>/delete', methods=['POST', 'GET'])
def branchdelete(id):
    if request.method == 'POST':
        delete = request.form['delete']
        branch = Branch.query.get_or_404(id)
        db.session.delete(branch)
        db.session.commit()


        return redirect('https://wheelsworks.000webhostapp.com/deletebranch.php?delete='+delete)

    else:

        return 'ERROR DELETE'




@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():

    email = session['email']
    rows = Branch.query.filter_by(email = email)

    return render_template('settings.html', rows=rows)







@app.route('/<int:id>/profile', methods=['POST', 'GET'])
@login_required
def profile(id):
        profile = User.query.get_or_404(id)

        if request.method == 'POST':

            username = request.form['username']
            photo = save_images(request.files.get('file'))
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

            profile.password = hashed_password
            profile.username = username
            profile.photo = photo

            db.session.add(profile)
            db.session.commit()

            return redirect('/settings')

        return render_template('profile.html', profile=profile)




@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')





@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')


    return render_template('register.html')







if __name__ == "__main__":
    app.run(debug=False)
