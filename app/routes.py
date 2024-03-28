# from app import app
from flask import  Flask, render_template, request, redirect, url_for, session, flash
# from db_layer import *
import logging
from datetime import timedelta
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
# from chat_db import db_chain
from flask import jsonify

# logging.basicConfig(filename='app.log', level=logging.INFO)



app = Flask(__name__)
app.secret_key = 'Kjda423sfjsdahf32'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database file path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80),nullable=False)
    ISDN = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(80),  nullable=False)
    description = db.Column(db.String(200), nullable=False)


# # tables creations
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():

    books = Book.query.all()
    book_list = [{'title': book.title, 'author': book.author,'ISDN': book.ISDN, 'price': book.price, 'description': book.description } for book in books]
    # print(book_list)

    # books = get_books_from_json()
    # for book in books:
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
            new_user = Book(title=request.form['title'], author=request.form['author'], ISDN=request.form['ISDN'], price = float(request.form['price']),description=request.form['description'])
            db.session.add(new_user)
            db.session.commit()
            return render_template('add_book.html', message="Successfully added to database. Return to home.")

        except Exception as e:
            return render_template('add_book.html', message="Failed to add book to database. Please try again. Error: "+ e)
        
    return render_template('add_book.html', message=None)


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
            session['role'] = user.role
            session['last_activity'] = datetime.now()
            logging.info('%s logged in successfully', username)
            
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
    results = [{'title': book.title, 'author': book.author,'ISDN': book.ISDN, 'price': book.price, 'description': book.description } for book in books]

    return results

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        message = request.json['msg']
        response = db_chain.run(message)
    
        return jsonify({"message":response})
    
    return render_template('chat.html', message=None)

@app.route('/cart')
def cart():
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
    role = request.form['role']

    error = f'Display date: {username} {password1} {password2} {role}'

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
        new_user = User(username=username, password=password1, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

  return render_template('signup.html', error=error)

if __name__ == '__main__':
    app.run(port=5000)