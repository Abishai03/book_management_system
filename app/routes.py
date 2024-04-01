# from app import app
from flask import  Flask, render_template, request, redirect, url_for, session, flash
from .db_layer import *
import logging
from datetime import timedelta
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from .chat_db import db_chain
from flask import jsonify
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime, date
from .send_email import send_book
logging.basicConfig(filename='app.log', level=logging.INFO)



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'Kjda423sfjsdahf32'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database file path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
# Configuration variables
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80),nullable=False)
    ISDN = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(80),  nullable=False)
    description = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.String(200))

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float(80),  nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Coupon {self.code}>'

# # tables creations
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():

    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author,'ISDN': book.ISDN, 'price': book.price, 'description': book.description, 'thumbnail': book.thumbnail.replace("/static", "") if book.thumbnail else 'static/empty-book-cover.jpeg' } for book in books]

    # book_list = get_books_from_json()
    # print(book_list)
    # for book in book_list:
    #     new_user = Book(title=book['title'], author=book['author'], ISDN=book['ISDN'], price = float(book['price']),description=book['description'])
    #     db.session.add(new_user)
    #     db.session.commit()
    
    return render_template('index.html', books=book_list)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            ISDN = request.form['ISDN']
            price = float(request.form['price'])
            description = request.form['description']
            
            # Handle thumbnail upload
            thumbnail = request.files['thumbnail']
            if thumbnail.filename != '':
                
                try:
                    directory = app.config['UPLOAD_FOLDER']
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    
                    # # Save the thumbnail to the static folder
                    thumbnail_filename = secure_filename(thumbnail.filename)
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename)
                    thumbnail.save(thumbnail_path)
                 

                except Exception as e:
                    print("ERROR: ",e)


                
            thumbnail_path = thumbnail_path.replace("app/","")
            # Create a new book object with the extracted details
            new_book = Book(
                title=title,
                author=author,
                ISDN=ISDN,
                price=price,
                description=description,
                thumbnail=thumbnail_path  # Assign the path of the saved thumbnail
            )
            db.session.add(new_book)
            db.session.commit()
            return render_template('add_book.html', message="Successfully added to database. Return to home.")

        except Exception as e:
            return render_template('add_book.html', message="Failed to add book to database. Please try again. Error: "+ e)
        
    return render_template('add_book.html', message=None)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    # Check if the user is an admin
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    # Fetch the book to edit from the database
    book = Book.query.get_or_404(book_id)

    if request.method == 'GET':
        book = {'id': book.id, 'title': book.title, 'author': book.author,'ISDN': book.ISDN, 'price': book.price, 'description': book.description, 'thumbnail': book.thumbnail.replace("static/", "") if book.thumbnail else 'empty-book-cover.jpeg' }
        return render_template('edit_book.html', book=book)
 
    
    if request.method == 'POST':
        try:
            # Update the book details
            book.title = request.form['title']
            book.author = request.form['author']
            book.ISDN = request.form['ISDN']
            book.price = float(request.form['price'])
            book.description = request.form['description']

            # Handle thumbnail upload
            thumbnail = request.files['thumbnail']
            if thumbnail.filename != '':
                
                try:
                    directory = app.config['UPLOAD_FOLDER']
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    
                    # # Save the thumbnail to the static folder
                    thumbnail_filename = secure_filename(thumbnail.filename)
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename)
                    thumbnail.save(thumbnail_path)
                 

                except Exception as e:
                    print("ERROR: ",e)

                thumbnail_path = thumbnail_path.replace("app/","")
                book.thumbnail = thumbnail_path
                
            
            # Commit the changes to the database
            db.session.commit()
            return render_template('edit_book.html', book=book, message="Book updated successfully.")

        except Exception as e:
            return render_template('edit_book.html', book=book, message="Failed to update book. Please try again. Error: " + str(e))
    
    return render_template('edit_book.html', book=book, message=None)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            book = Book.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            return render_template('index.html', message="Failed to Delete to database. Please try again. Error: "+ e)
        
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role
            session['last_activity'] = datetime.now()
            logging.info('%s logged in successfully', username)
            
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        session.pop('username', None)
        session.pop('role', None)
        session.pop('last_activity', None)
        logging.info('%s logged out successfully', username)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/search')
def search():
  query = request.args.get('query')
  
  books = search_books(query)

  if not books:
    books = [{
        "title": "No results found",
        "author": "",
        "ISDN": "",
        "price": "",
        "description": "Try searching for a different book."
    }]

  return render_template('index.html', books=books)

def search_books(query):
    # query database
    books = Book.query.filter(Book.title.ilike('%'+str(query)+"%")).all()
    
    # Prepare the response
    results = [{'id': book.id, 'title': book.title, 'author': book.author,'ISDN': book.ISDN, 'price': book.price, 'description': book.description, 'thumbnail': book.thumbnail.replace("/static", "") if book.thumbnail else 'static/empty-book-cover.jpeg'  } for book in books]

    return results

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        
        message = request.json['message']
        print(message)
        response = db_chain.run(message)
        print("response: ", response)
        return [{"text":response}]

def generate_html(book_list, coupon):
    html = "<html>\n<head>\n<title>Book List</title>\n</head>\n<body>\n"
    total = 0
    for book in book_list:
        html += "<div>\n"
        html += f"<h2>{book['title']}</h2>\n"
        html += f"<p><strong>Author:</strong> {book['author']}</p>\n"
        html += f"<p><strong>ISDN:</strong> {book['ISDN']}</p>\n"
        html += f"<p><strong>Price:</strong> ${book['price']}</p>\n"
        html += f"<p><strong>Description:</strong> {book['description']}</p>\n"
        # html += f"<img src='{book['thumbnail']}' alt='{book['title']}' width='100' height='150'>\n"
        html += "</div>\n"
        total += book['price']
    total= total - coupon 
    html += "============================<br/><br/> <p><strong> Coupon: -"+str(coupon)+"</strong></p>"
    html += "<br/>============================<br/><br/> <p><strong>Total: "+str(total)+"</strong></p>"
    html += "</body>\n</html>"
    return html

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        code = request.json['coupon']
        coupon = Coupon.query.filter_by(code=code).first()
        minus_total = 0
        if coupon:
            current_date = datetime.now().date()
            if current_date <= coupon.expiration_date:
                minus_total = coupon.price
        
        books = generate_html(request.json['items'], minus_total)
        status = send_book(recipient=session['email'],content=books)
        if status:
            return jsonify({"success": "true", "message":"Success! Books purchased successfully! and send to email"})

        return jsonify({"message":"Failure! Something went wrong"})
    
    else:
        return render_template('cart.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/tou')
def tou():
    return render_template('tou.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/coupon', methods=['GET', 'POST']) 
def coupon():
    if 'username' not in session:
        return redirect(url_for('index'))
    # if session['role'] != 'admin':
    #     return redirect(url_for('index'))

    if request.method == 'POST':
        coupon = request.form['coupon']
        price = request.form['price']

        date = request.form['date']
        expiration_date = datetime.strptime(date, '%Y-%m-%d').date()

        # Create new new_coupon
        new_coupon = Coupon(code=coupon,price=price, expiration_date=expiration_date)
        db.session.add(new_coupon)
        db.session.commit()
        return redirect(url_for('coupon'))

    coupons = Coupon.query.all()
    coupons = [{ 'code': item.code, 'price': item.price,'date': item.expiration_date, } for item in coupons]
    return render_template('coupon.html', coupons=coupons)

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
  error = None
  if 'username' in session and session['role'] != 'admin':
    return redirect(url_for('index'))
  
#   if 'username' not in session or session['role'] != 'admin':
#     return redirect(url_for('login'))


  if request.method == 'POST':
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    email = request.form['email']

    role = request.form['role']

    error = f'Display data: {username} {password1} {password2} {role} {email}'

    if password1!= password2:
        
        render_template('signup.html', error = 'Passwords do not match')
    elif len(password1) < 7:
        render_template('signup.html', error = 'Password must be at least 8 characters')
    else:
        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('login.html', error="Username already exists.")
        
        # Create new user
        new_user = User(username=username, password=password1, role=role, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

  return render_template('signup.html', error=error)

# if __name__ == '__main__':
#     app.run(port=5000)