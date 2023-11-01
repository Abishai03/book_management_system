from app import app
from flask import  Flask, render_template, request, redirect, url_for, session, flash
from .db_layer import *
import logging
from datetime import timedelta
 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

logging.basicConfig(filename='app.log', level=logging.INFO)


@app.route('/')
def index():
    books = get_books_from_json()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_book = {
            "title": request.form['title'],
            "author": request.form['author'],
            "ISDN": request.form['ISDN'],
            "price": float(request.form['price']),
            "description": request.form['description']
        }

        result = add_book_to_json(new_book)
        
        if result:
            return render_template('add_book.html', message="Successfully added to database. Return to home.")
        else:
            return render_template('add_book.html', message="Failed to add book to database. Please try again.")
        
    return render_template('add_book.html', message=None)

def authenticate_user(username, password):
    users = get_users()
    user = next((u for u in users if u['username'] == username), None)
    if user and user['password'] == password:
        return user
    return None  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

         
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            
            logging.info('%s logged in successfully', username)
            
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        username = session['username']
        session.pop('user_id')
        session.pop('username')
        session.pop('user_role')
        
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
    results = []
    all_books = get_books_from_json()
    for book in all_books:
        if query.lower() in book['title'].lower(): 
            results.append(book)

    return results

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
  if 'user_id' in session:
    return redirect(url_for('index'))

  error = None  
  if request.method == 'POST':
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']

    error = f'Display date: {username} {password1} {password2}'

    if password1!= password2:
        error = 'Passwords do not match'
    elif len(password1) < 1:
        error = 'Password must be at least 8 characters'
    else:
        # Check if username is already taken
        users = get_users()
        if username in [user['username'] for user in users]:
            error = 'Username already taken. Please choose another username.'
        else:
            # Add new user to database
            if add_user(username, password1):
                error = 'User Added'
                flash('User signed up successfully!')
                return render_template('login.html', error='User Added. Please login.')
            else:
                error = 'Failed to add user to database'

  return render_template('signup.html', error=error)
