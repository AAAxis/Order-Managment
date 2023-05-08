from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from flask import current_app
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import mail_username, mail_password
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
import requests
import json
import string
import os
import secrets
import random
import pytesseract
from PIL import Image


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://polskoydm:)72$K]mp1WDRy$a:}mH+ZZ;rs!WIFiYn@ls-4ff0825bb593ca6500a7d1b7acde152d91e5c0bc.c6hy7e5lwfr3.us-east-1.rds.amazonaws.com:5432/dbmaster'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

Login_manager = LoginManager()
Login_manager.init_app(app)
Login_manager.login_view = "login"



class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    file = db.Column(db.String(120), default='branch.jpg')
    address = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    store = db.Column(db.String(100))



class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    total = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cart = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)



class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    file = db.Column(db.String(120), default="image.jpg")
    email = db.Column(db.String(100), nullable=False, unique=True)


@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/uploads', photo_name)
    photo.save(file_path)
    return photo_name


def get_random_string():
    # choose from all lowercase letter
    characters = string.ascii_uppercase + string.digits
    token = ''.join(random.choice(characters) for i in range(10))
    return token

@app.route('/barcode')
def barcode():
    return render_template('barcode_scanner.html')



@app.route('/scan', methods=['POST'])
def scan_barcode():
    # retrieve form data

    image = request.files['image']

    # save image to disk
    image.save('temp.jpg')

    # extract numeric symbols from image using pytesseract

    img = Image.open('temp.jpg')
    result = pytesseract.image_to_string(img)

    # get product information from barcode lookup API
    barcode = ''.join(c for c in result if c.isnumeric())
    api_key = '4s7a7uk94alxhywl8qisu8ww4il5sl'

    url = f'https://api.barcodelookup.com/v3/products?barcode=3614272049529&formatted=y&key={api_key}'
    response = requests.get(url).json()

    # construct product information dictionary
    if 'products' in response and len(response['products']) > 0:
        product_info = {
            'name': response['products'][0]['brand'],
            'quantity': 1,
            'price': 5,
            'barcode': barcode,
            'image_url': response['products'][0]['images']
        }
    else:
        product_info = {
            'name': 'Unknown',
            'quantity': 1,
            'price': 5,
            'barcode': barcode,
            'image_url': 'None'
        }

    return render_template('scan_result.html', product=product_info)



@app.route('/newchat', methods=['POST', 'GET'])
def newchat():
    if request.method == 'POST':
        data = request.get_json()
        text = data['text']

        email = Message(subject='New Message', body=f'Message - {text}',
                        sender='your_gmail_username@gmail.com', recipients=['polskoydm@gmail.com'])
        mail.send(email)

        response = {'message': 'Message sent successfully!'}
        return jsonify(response)

    else:
        response = {'message': 'Invalid request method!'}
        return jsonify(response)


@app.route('/portfolio', methods=['POST', 'GET'])
def portfolio():

    # Extract the payment information from the link parameters

    name = request.args.get("name")
    text = request.args.get("text")
    email = request.args.get("email")

    msg = Message(subject=f"We handle your request {email}", body=f"Name - {name}\n Message - {text}\n Thank you for testing my app.",
    sender=mail_username)
    msg.recipients = [str(email)]

    mail.send(msg)

    return render_template('subscribe.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    branches = Branch.query.all()
    branch_list = [{'id': branch.id, 'name': branch.name, 'address': branch.address, 'file': branch.file, 'email': branch.email, 'token': branch.token} for branch in branches]
    return jsonify(branch_list)




@app.route('/<path:id>/shop', methods=['POST', 'GET'])
def selectshop(id):
    rows = Product.query.filter_by(store=id).all()
    products = []
    for row in rows:
        product = {
            'id': row.id,
            'name': row.name,
            'description': row.category,
            'price': row.price,
            'image': row.image,
            'store': row.store
        }
        products.append(product)

    return jsonify(products)


@app.route('/checkout', methods=['POST'])
def checkout():
    # Generate a random order ID
    order_id = 'ABC' + str(random.randint(0, 9999999)).zfill(7)

    # Get the items and total from the request
    items = request.form.get('items')
    total = request.form.get('total')

    # Create a list of dictionaries containing the product IDs, quantities, and names
    item_list = []
    for item in json.loads(items):
        product_id = item.get('product_id')
        quantity = item.get('quantity')

        # Fetch the product from the database by its ID
        product = Product.query.get_or_404(product_id)
        product_name = product.name

        item_list.append({
            'product_id': product_id,
            'quantity': quantity,
            'name': product_name
        })

    # Convert the list of dictionaries to a JSON string
    item_json = json.dumps(item_list)

    # Create a new completed schema object
    completed = Order(cart=item_json, id=order_id, total=total)

    # Add the completed object to the session
    db.session.add(completed)

    # Commit the changes to the database
    db.session.commit()

    # Render the checkout template with the order ID and total
    return render_template('checkout.html', order_id=order_id)




@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():

        email = session['email']

        rows = Branch.query.filter_by(email = email)

        return render_template('dashboard.html', rows=rows)






@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        session['email'] = email

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/dashboard')
            else:
                return 'PASSWORD INCORRECT'
        else:
            return 'USER DOES NOT EXIST'

    return render_template('login.html')






@app.route('/<path:id>/item', methods=['POST', 'GET'])
@login_required
def selectitem(id):
    rows = Product.query.filter_by(store=id).all()

    return render_template('item.html', rows=rows, id=id)


@app.route('/drivers', methods=['POST', 'GET'])
@login_required
def selectrider():


    rows = Driver.query.all()

    return render_template('driver.html', rows=rows)



@app.route('/adddriver', methods=['POST', 'GET'])
@login_required
def adddriver():

    if request.method == "POST":

        file = save_images(request.files.get('file'))
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_driver = Driver(username=username, email=email, password=password, file=file)

        db.session.add(new_driver)
        db.session.commit()
        return redirect(request.referrer)

    else:

        return 'ERROR UPLOAD IMAGE'



@app.route('/<path:id>/deletedriver', methods=['POST', 'GET'])
def driverdelete(id):
    if request.method == 'POST':

        driver = Driver.query.get_or_404(id)
        db.session.delete(driver)
        db.session.commit()

        return redirect(request.referrer)
    else:

        return 'ERROR DELETE'







@app.route('/<path:id>/additem', methods=['POST', 'GET'])
@login_required
def additem(id):

    if request.method == "POST":

        image = save_images(request.files.get('file'))
        name = request.form['title']
        price = request.form['price']
        category = request.form['group']

        new_product = Product(name=name, price=price, category=category, image=image, store=id)

        db.session.add(new_product)
        db.session.commit()

        return redirect('/'+id+'/item')
    else:

        return 'ERROR UPLOAD IMAGE'





@app.route('/<path:id>/deleteitem', methods=['POST', 'GET'])
def itemdelete(id):
    if request.method == 'POST':

        item = Product.query.get_or_404(id)

        db.session.delete(item)
        db.session.commit()

        return redirect(request.referrer)

    else:

        return 'ERROR DELETE'









@app.route('/addbranch', methods=['POST', 'GET'])
@login_required
def addbranch():


    if request.method == "POST":
        token = str(get_random_string())
        file = save_images(request.files.get('file'))
        email = session['email']
        title = request.form['title']
        address = request.form['address']


        new_branch = Branch(token=token, title=title, email=email, address=address, file=file)

        db.session.add(new_branch)
        db.session.commit()

        return redirect('/settings')

    else:

        return 'ERROR UPLOAD IMAGE'



@app.route('/settings/<int:id>/delete', methods=['POST', 'GET'])
def branchdelete(id):
    if request.method == 'POST':
        branch = Branch.query.get_or_404(id)
        db.session.delete(branch)
        db.session.commit()


        return redirect('/settings')

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


# define a route to update the order status
@app.route('/orders/<path:order_id>/update_status', methods=['POST'])
def update_order_status(order_id):
    # retrieve the request data
    status = request.form['status']

    # retrieve the order from the database
    order = Order.query.get_or_404(order_id)

    # update the order status
    order.status = status

    # commit the changes to the database
    db.session.commit()


    # redirect to the view order page
    return redirect(url_for('orders'))



@app.route('/orders')
def orders():
    orders = Order.query.filter_by(status='paid').all()
    cart_items = []
    for order in orders:
        cart = json.loads(order.cart)
        item_names = [f"{item['name']} x {item['quantity']}" for item in cart]
        cart_items.append(item_names)
    return render_template('orders.html', orders=orders, cart_items=cart_items)




@app.route('/<path:id>/payment', methods=['POST', 'GET'])
def payment(id):
    # Fetch the order by its ID
    order = Order.query.get_or_404(id)

    if request.method == 'POST':
        # Update the order attributes with the values from the form data
        order.email = request.form.get('email')
        order.name = request.form.get('name')
        order.address = request.form.get('address')


        # Commit the changes to the database
        db.session.commit()

        # Pass the updated order to the payment template
        return render_template('payment.html', order=order)

    # Pass the order to the payment template
    return render_template('payment.html', order=order)





@app.route('/thank-you', methods=['POST', 'GET'])
def thank_you():
    order_id = request.args.get('order')

    # retrieve the order using the order id
    order = Order.query.filter_by(id=order_id).first()

    if order:
        # update the order status to Payment Successful
        order.status = "paid"
        db.session.add(order)
        db.session.commit()


        email = request.args.get('email')
        address = request.args.get('address')
        name = request.args.get('name')

        # send an email to the customer
        msg = Message(subject=f"Hello {name}, your order has been processed",
                      body=f"We have received your payment and your order will be shipped soon. \nOrder Number #{order_id} \nEmail: {email} \nName: {name}\nDelivery Address: {address}\nThank you for shopping with us!",
                      sender=mail_username)
        msg.recipients = [email]
        mail.send(msg)

        # render the thank you template
        return render_template('thank_you.html')
    else:
        return "Error"



if __name__ == "__main__":
    app.run(debug=False)


