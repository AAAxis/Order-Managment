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
import stripe


stripe.api_key = 'sk_test_51LXRaMDoWGog1gVBRii0ef0AgNCWInoqHcQXkGkyqF6Uwh7k7pfHq0AwFhuIFg0dcALX3boKoQsYLqvzNd7tcFQh0024Q8SGnM'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://polskoydm:)72$K]mp1WDRy$a:}mH+ZZ;rs!WIFiYn@ls-4ff0825bb593ca6500a7d1b7acde152d91e5c0bc.c6hy7e5lwfr3.us-east-1.rds.amazonaws.com:5432/dbmaster'
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

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.String(100), default=False)


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), default=False)


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

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    total = db.Column(db.String(100))
    transaction = db.Column(db.String(100))
    status = db.Column(db.String(100))




class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    total = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(50), nullable=True)
    start_point = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    driver_phone = db.Column(db.String(50), nullable=True)
    store_name = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    cart = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    file = db.Column(db.String(120), default="https://static.vecteezy.com/system/resources/previews/000/439/863/original/vector-users-icon.jpg")
    email = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=True, default='333 17th Ave SW, Calgary')
    mobile = db.Column(db.String(100), nullable=True, default='+16474784250')


class Driver(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bank = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    money = db.Column(db.Integer, default='0')



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



Login_manager = LoginManager()
Login_manager.init_app(app)
Login_manager.login_view = "login"

@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():

        email = session['email']

        rows = Branch.query.filter_by(email = email)

        return render_template('dashboard.html', rows=rows, email=email)



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



@app.route("/merchant_login", methods=['GET', 'POST'])
def merchant_login():
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

    return render_template('merchant_login.html')


@app.route('/submit', methods=['POST'])
def apply():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    # Check if the verification code is correct
    application = Application.query.filter_by(email=email, verified=code).first()
    if application:
        # Update the application record to mark it as verified
        application.verified = 'Email Sent'
        db.session.commit()

        # Send email
        email_body = render_template('email_template.html', name=application.name, title=application.title, type=application.type)
        sbm = Message(subject='Thank you for applying at Wheels Works', sender=mail_username, recipients=[email])
        sbm.body = email_body
        sbm.html = email_body
        with app.open_resource(f'static/uploads/{application.resume}') as resume_file:
            sbm.attach(application.resume, 'application/pdf', resume_file.read())
        mail.send(sbm)


        msg = Message(subject='New Job Application', sender=mail_username, recipients=['polskoydm@outlook.com'])
        msg.body = f"New Job Application {email} \nLink: https://polskoydm.pythonanywhere.com/applications"
        with app.open_resource(f'static/uploads/{application.resume}') as resume_file:
            msg.attach(application.resume, 'application/pdf', resume_file.read())
        mail.send(msg)

        return jsonify({'message': 'Application submitted successfully'})
    else:
        return jsonify({'message': f'Invalid verification code: {code}'})


@app.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    name = request.form.get('name')
    email = request.form.get('email')
    resume_name = save_images(request.files.get('resume'))
    cover = request.form.get('cover')
    type = request.form.get('type')
    title = request.form.get('title')



    # Generate and send the verification code via email
    verification_code = '613245'

    # Send email
    ver = Message(subject='Verification Code', sender=mail_username, recipients=[email])
    ver.body = f"Your verification code is {verification_code}"
    mail.send(ver)



    # Create a new unverified application record in the database
    application = Application(
        name=name,
        email=email,
        resume=resume_name,
        cover=cover,
        title=title,
        type=type,
        verified=verification_code
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Verification code sent'})




@app.route('/applications', methods=['GET', 'POST'])
def applications():
    if request.method == 'POST':
        # Handle the POST request to clear the table
        Application.query.delete()
        db.session.commit()
        return jsonify({'message': 'Table cleared successfully'})
    else:
        # Handle the GET request to fetch and render the applications
        applications = Application.query.all()
        return render_template('applications.html', applications=applications)



@app.route('/jobs_edit')
def get_jobs_html():
    jobs = Jobs.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/jobs')
def get_jobs_json():
    jobs = Jobs.query.all()
    job_list = [{"id": job.id, "title": job.title, "location": job.location, "salary": job.salary, "description": job.description, "type": job.type} for job in jobs]
    return jsonify(jobs=job_list)



@app.route('/jobs/add', methods=['POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        salary = request.form['salary']
        description = request.form['description']
        job_type = request.form['type']
        link = request.form['link']

        new_job = Jobs(title=title, location=location, salary=salary, description=description, type=job_type, link=link)
        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('get_jobs'))

@app.route('/jobs/delete/<int:id>')
def delete_job(id):
    job_to_delete = Jobs.query.get(id)
    db.session.delete(job_to_delete)
    db.session.commit()

    return redirect(url_for('get_jobs'))


@app.route('/barcode')
def barcode():
    return render_template('barcode_scanner.html')

@app.route('/privacy')
def organaizer():
    return render_template('privacy.html')



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
                        sender='polskoydm@gmail.com', recipients=['polskoydm@gmail.com'])
        mail.send(email)

        response = {'message': 'Message sent successfully!'}
        return jsonify(response)

    else:
        response = {'message': 'Invalid request method!'}
        return jsonify(response)


@app.route('/subscribe', methods=['POST', 'GET'])
def subscribe():

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



@app.route('/<path:id>/item', methods=['POST', 'GET'])
@login_required
def selectitem(id):
    rows = Product.query.filter_by(store=id).all()

    return render_template('edit_items.html', rows=rows, id=id)


@app.route('/drivers', methods=['POST', 'GET'])
def selectrider():

    rows = Driver.query.all()

    return render_template('driver_status.html', rows=rows)




@app.route('/approve_driver/<int:driver_id>', methods=['POST'])
def approve_driver(driver_id):
    if request.method == 'POST':
        driver = Driver.query.get(driver_id)

        email = driver.email

        msg = Message(subject=f"Application was Approved, Thank You {email}", body=f"Hello {email},\nThank you for interesting at Driver Position.",
        sender=mail_username)
        msg.recipients = [str(email)]

        mail.send(msg)
        # Change the verified status to 'approved'
        driver.status = 'approved'
        db.session.commit()

        return redirect(request.referrer)
    else:

            return 'ERROR UPDATE'


@app.route('/delete_driver/<int:id>', methods=['POST', 'GET'])
def driver_delete(id):
    if request.method == 'POST':
        driver = Driver.query.get_or_404(id)

        # Delete the driver record
        db.session.delete(driver)
        db.session.commit()

        return redirect(request.referrer)
    else:
        return 'ERROR DELETE'


@app.route('/global_auth', methods=['GET'])
def global_auth():
    # Handle GET request to initiate login with a phone number
    email = request.args.get('email')

    if email:
        # Generate a random verification code (password)
        generate_random_password = ''.join(random.choices('0123456789', k=6))

        # Send an email with the verification code
        msg = Message(
            subject='Holy Labs - Verification Code',
            body=f'Your verification code is: {generate_random_password}',
            sender='your_mail_username',  # Replace with your sender email address
        )
        msg.recipients = [email]

        mail.send(msg)

        # Include the verification code in the response data
        response_data = {"message": "Verification code sent successfully", "verification_code": generate_random_password}
        return jsonify(response_data), 200

    else:
        return jsonify({'message': 'Missing email query parameter in GET request'}), 400






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
        name = request.form['title']
        address = request.form['address']


        new_branch = Branch(token=token, name=name, email=email, address=address, file=file)

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









@app.route('/<path:email>/profile', methods=['POST', 'GET'])
def profile(email):

    # Query the user using the email
        profile = User.query.filter_by(email=email).first()

        if request.method == 'POST':

            username = request.form['username']
            mobile = request.form['mobile']
            address = request.form['address']
            photo = request.form['file']
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

            profile.password = hashed_password
            profile.username = username
            profile.photo = photo
            profile.mobile = mobile
            profile.address = address

            db.session.add(profile)
            db.session.commit()

            return "Update Success"

        return render_template('edit_profile.html', profile=profile)




@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')




@app.route('/merchant_register', methods=['POST', 'GET'])
def merchant_register():

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email, type="merchant")

        db.session.add(new_user)
        db.session.commit()

        return redirect('/merchant_login')


    return render_template('merchant_register.html')


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


@app.route('/assign_driver', methods=['GET'])
def assign_driver():
    user_phone = request.args.get('user_phone')
    order_id = request.args.get('orderId')

    order = Order.query.filter_by(id=order_id).first()
    if order:
        order.driver_phone = user_phone
        order.status = "assigned"
        db.session.commit()  # Make sure to commit changes to the database

        # Send a success response
        return jsonify({'message': 'Driver assigned successfully'})
    else:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'error': 'Invalid parameters'}), 400


@app.route("/orderpickup/<path:order_id>", methods=["GET"])
def mark_pickedup(order_id):
    # Update the 'driver_name' column in the 'order' table
    order = Order.query.filter_by(id=order_id).first()
    if order:
        order.status = "pickedup"
        db.session.commit()  # Make sure to commit changes to the database

        return jsonify({"message": "Order marked as picked up"}), 200
    return jsonify({"error": "Order not found or already picked up"}), 404

@app.route("/orderdone/<path:order_id>", methods=["GET"])
def mark_done(order_id):
    email = request.args.get('email')

    driver = Driver.query.filter_by(email=email).first()  # Assuming 'Driver' has an 'email' attribute
    order = Order.query.filter_by(id=order_id).first()

    if order and driver:
        if order.status != "done":
            order.status = "done"
            db.session.commit()

            # Add $10 to the 'money' column of the driver
            driver.money += 10
            db.session.commit()

            return jsonify({"message": "Order marked as Done, $10 added to driver's money"}), 200

        return jsonify({"error": "Order already marked as Done"}), 400

    return jsonify({"error": "Order not found or driver not found"}), 404



@app.route('/history', methods=['GET'])
def history():
    email = request.args.get('email')  # Retrieve the email from the query parameters

    if email:
    # If the 'email' parameter is provided, fetch orders for that specific email
        orders = Order.query.filter(Order.email == email, Order.status.in_(['assigned','paid', 'pickedup', 'done'])).all()
    else:
        return "error"

    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'total': order.total,
            'address': order.address,
            'email': order.email,
            'user_phone': order.phone,
            'name': order.name,
            'store_name': order.store_name,
             'start_point': order.start_point,
              'driver_phone': order.driver_phone,
            'cart': json.loads(order.cart),
            'status': order.status,

        }
        order_list.append(order_data)

    return jsonify(order_list)

@app.route('/online', methods=['GET'])
def online():

    orders = Order.query.filter(Order.status.in_(['paid'])).all()

    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'total': order.total,
            'address': order.address,
            'email': order.email,
            'name': order.name,
            'store_name': order.store_name,
             'start_point': order.start_point,
              'driver_phone': order.driver_phone,
            'cart': json.loads(order.cart),
            'status': order.status,



        }
        order_list.append(order_data)

    return jsonify(order_list)


@app.route('/my_chats', methods=['GET'])
def my_chats():
    phone = request.args.get('phone')  # Retrieve the email from the query parameters

    if phone:
    # If the 'email' parameter is provided, fetch orders for that specific email
        orders = Order.query.filter(Order.driver_phone == phone, Order.status.in_(['assigned', 'pickedup', 'done'])).all()
    else:
        return "error"

    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'total': order.total,
            'address': order.address,
            'email': order.email,
            'user_phone': order.phone,
            'name': order.name,
            'store_name': order.store_name,
             'start_point': order.start_point,
              'driver_phone': order.driver_phone,
            'cart': json.loads(order.cart),
            'status': order.status,

        }
        order_list.append(order_data)

    return jsonify(order_list)






@app.route('/driver_info', methods=['GET'])
def driver_info():
    email = request.args.get('email')  # Retrieve the email from the query parameters
    driver = Driver.query.filter_by(email=email).first()

    if driver is not None:

        profile_dict = {
            'money': driver.money,
            'email': driver.email,
             'status': driver.status,

        }
        return jsonify(profile_dict)
    else:
        if email != "N/A":

                new_driver = Driver(
                    email=email,
                    status="disabled",
                    bank="Add Payment Method",
                    money=0
                )

                db.session.add(new_driver)
                db.session.commit()

                admin = "polskoydm@outlook.com"

                msg = Message(subject=f"New Driver Application {email} ", body=f"Tap this link to approve {email},  \nhttps://polskoydm.pythonanywhere.com/drivers",
                sender=mail_username)
                msg.recipients = [str(admin)]

                mail.send(msg)


    return jsonify({'error': 'Driver not found'}), 404



@app.route('/assigned', methods=['GET'])
def assigned():
    email = request.args.get('email')  # Retrieve the email from the query parameters

    if email:
    # If the 'email' parameter is provided, fetch orders for that specific email
        orders = Order.query.filter(Order.email == email, Order.status.in_(['assigned', 'pickedup'])).all()
    else:
    # If 'email' parameter is not provided, fetch all orders with 'assigned', 'pickedup', or 'done' status
        orders = Order.query.filter(Order.status.in_(['assigned', 'pickedup'])).all()

    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'total': order.total,
            'address': order.address,
            'email': order.email,
            'name': order.name,
            'store_name': order.store_name,
             'start_point': order.start_point,
              'driver_phone': order.driver_phone,
            'cart': json.loads(order.cart),
            'status': order.status
        }
        order_list.append(order_data)

    return jsonify(order_list)






@app.route('/store/<path:token>', methods=['GET'])
def get_store(token):
    store = Branch.query.filter_by(token=token).first()  # Find the store by the provided token

    if not store:
        return jsonify({'error': 'Store not found'}), 404

    store_data = {
        'id': store.id,
        'name': store.name,
        'email': store.email,
        'file': store.file,
        'address': store.address,
        'token': store.token
    }

    return jsonify(store_data)



@app.route('/orders')
def orders():

    orders = Order.query.filter(Order.status.in_(['assigned','paid', 'pickedup', 'done'])).all()
    cart_items = []
    for order in orders:
        cart = json.loads(order.cart)
        item_names = [f"{item['name']} x {item['quantity']}" for item in cart]
        cart_items.append(item_names)
    return render_template('my_orders.html', orders=orders, cart_items=cart_items)


@app.route('/checkout', methods=['POST'])
def checkout():
    # Generate a random order ID
    order_id = 'ABC' + str(random.randint(0, 9999999)).zfill(7)


    # Get the items and total from the request
    data = request.get_json()
    items = data.get('items')
    total = data.get('total')

    # Create a list of dictionaries containing the product IDs, quantities, and names
    item_list = []
    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity')

        # Fetch the product from the database by its ID
        product = Product.query.get_or_404(product_id)
        product_store = product.store
        product_name = product.name
        product_price = product.price
        product_image = product.image


        store = Branch.query.filter_by(token=product_store).first()
        store_name = store.name
        store_address = store.address


        item_list.append({
            'product_id': product_id,
            'quantity': quantity,
            'name': product_name,
            'price': product_price,
            'image': product_image
        })

    # Convert the list of dictionaries to a JSON string
    item_json = json.dumps(item_list)

    # Create a new completed schema object
    completed = Order(cart=item_json, id=order_id, total=total, address='None', name='None', email='None', store_name = store_name, start_point = store_address)

    # Add the completed object to the session
    db.session.add(completed)

    # Commit the changes to the database
    db.session.commit()



    return jsonify({'message': 'Order placed successfully', 'order_id': order_id, 'total': total})

@app.route('/taxi', methods=['POST'])
def taxi():
    # Generate a random order ID
    order_id = 'ABC' + str(random.randint(0, 9999999)).zfill(7)

    # Get the items and total from the request
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    total = data.get('total')
    distance = data.get('distance')
    start = data.get('start_point')
    address = data.get('address')

    # Create a list of dictionaries containing the product IDs, quantities, and names
    item_list = []

    item_list.append({
         'id': "1",
        'quantity': distance +"KM",
        'name': name,
        'price': "2$",
        'image': "user.png"
    })

    # Convert the list of dictionaries to a JSON string
    item_json = json.dumps(item_list)

    # Create a new completed schema object
    completed = Order(cart=item_json, id=order_id, total=total, phone=phone, address=address, name=name, email=email, store_name="Billa Taxi", start_point=start)

    # Add the completed object to the session
    db.session.add(completed)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Order placed successfully', 'order_id': order_id, 'total': total})





@app.route('/payment/<path:id>', methods=['POST', 'GET'])
def payment(id):
    # Fetch the order by its ID
    order = Order.query.get(id)

    cart = json.loads(order.cart)
    cart_items = []
    for item in cart:
        item_data = {
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'image': item['image'],
            'id': item['product_id']
        }
        cart_items.append(item_data)

    if request.method == 'POST':
        # Extract the JSON data from the request
        data = request.get_json()

        # Update the order attributes with the values from the JSON data
        order.phone = data.get('phone')
        order.email = data.get('email')
        order.name = data.get('name')
        order.address = data.get('address')

        # Commit the changes to the database
        db.session.commit()



    # Return the order and cart items as JSON
    return jsonify(cart_items=cart_items, total=order.total)




@app.route('/addmoney', methods=['POST', 'GET'])
def addmoney():
    email = request.args.get('email')
    total_amount = float(request.args.get('total'))  # Parse total_amount as a float

    transaction = 'DEP' + str(random.randint(0, 9999999)).zfill(7)

    # Convert total_amount to cents (integer)
    total_amount_cents = int(total_amount * 100)

    # Create a new completed schema object
    completed = Payment(total=total_amount, email=email, status="pending", transaction=transaction)

    # Add the completed object to the session
    db.session.add(completed)

    # Commit the changes to the database
    db.session.commit()

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Self-Service',
                },
                'unit_amount': total_amount_cents,  # Use total_amount_cents as the unit amount
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'https://polskoydm.pythonanywhere.com/deposit?transaction={transaction}',
        cancel_url='https://polskoydm.pythonanywhere.com/error',
    )

    return redirect(session.url, code=303)

@app.route('/deposit', methods=['GET'])
def deposit():
    # Extract the payment ID from the query parameters
    transaction = request.args.get('transaction')

    if transaction:
        # Update the payment status to "done" in the database based on the payment ID
        payment = Payment.query.filter_by(transaction=transaction).first()
        if payment:
            payment.status = "done"
            db.session.commit()
        return f"Deposit Successful for Payment ID: {transaction}"

    return "Invalid Payment ID"


@app.route('/transactions', methods=['GET'])
def transactions():
    # Query all payment records from the database
    payments = Payment.query.all()

    return render_template('transactions.html', payments=payments)


@app.route('/balance', methods=['GET'])
def get_balance():
    email = request.args.get('email')

    # Find all records with the specified email and "status" set to "done"
    payments = Payment.query.filter_by(email=email, status='done').all()

    if payments:
        # Calculate the balance by summing the "total" field of all matching records
        balance = sum(float(payment.total) for payment in payments)
        return jsonify({"balance": balance})
    else:
        return jsonify({"balance": 0})  # Return 0 if no records were found for the email


@app.route('/billapay/<path:id>', methods=['POST', 'GET'])
def billapay(id):
    transaction = 'PAY' + str(random.randint(0, 9999999)).zfill(7)
    order = Order.query.get(id)
    total_amount = order.total  # Replace with your own logic to calculate the total amount
    email = order.email
    name = order.name
    address = order.address
    # Create a new Payment record
    new_payment = Payment(email=email, total=-total_amount, status='pending', transaction=transaction)
    db.session.add(new_payment)
    db.session.commit()

    # Find all records with the specified email and "status" set to "done"
    payments = Payment.query.filter_by(email=email, status='done').all()

    if payments:
        # Calculate the balance by summing the "total" field of all matching records
        balance = sum(float(payment.total) for payment in payments)

        # Check if the balance is enough to cover the total_amount
        if balance >= total_amount:
            # Update the status of the newly created payment record to "done"
            new_payment.status = 'done'
            db.session.commit()

            # Update the order status to Payment Successful
            order.status = "paid"
            db.session.add(order)
            db.session.commit()

            # send an email to the customer
            msg = Message(subject=f"Hello {name}, your order has been processed",
                          body=f"We have received your payment and your order will be shipped soon. \nNew Order  \nEmail: {email} \nName: {name}\nDelivery Address: {address}\nThank you for shopping with us!",
                          sender=mail_username)
            msg.recipients = [email]
            mail.send(msg)
            return jsonify({"message": "Payment successful!"})
        else:
            return jsonify({"message": "Insufficient balance to make the payment."})

    return jsonify({"message": "No previous payments found for this email."})


@app.route('/create-checkout-session/<path:id>', methods=['POST', 'GET'])
def create_checkout_session(id):

    order = Order.query.get(id)

    total_amount = order.total  # Replace with your own logic to calculate the total amount

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Self-Service',
                },
                'unit_amount': int(total_amount * 100),  # Stripe expects the amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
       success_url=f'https://polskoydm.pythonanywhere.com/thank-you/{id}',  # Include the order ID in the URL
        cancel_url='https://polskoydm.pythonanywhere.com/error',
    )

    return redirect(session.url, code=303)





@app.route('/error', methods=['GET'])
def error():
    return "An error occurred during the payment process. Please try again later."

@app.route('/thank-you/<path:id>', methods=['POST', 'GET'])
def thankyou(id):
    order = Order.query.get(id)

    if order:
        name = order.name
        email = order.email
        address = order.address

        # Update the order status to Payment Successful
        order.status = "paid"
        db.session.add(order)
        db.session.commit()


        # send an email to the customer
        msg = Message(subject=f"Hello {name}, your order has been processed",
                      body=f"We have received your payment and your order will be shipped soon. \nNew Order  \nEmail: {email} \nName: {name}\nDelivery Address: {address}\nThank you for shopping with us!",
                      sender=mail_username)
        msg.recipients = [email]
        mail.send(msg)

        return render_template('thank_you.html', order_id=id, success=True)
    else:
        # Return a JSON response indicating error
        return jsonify({'status': 'error', 'message': 'Error occurred'})




if __name__ == "__main__":
    app.run(debug=False)


