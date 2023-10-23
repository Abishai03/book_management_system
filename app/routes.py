from app import app
from flask import render_template, request, redirect, url_for, session
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

        import os
        print(os.path.abspath('app/data/users.json'))
        
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
