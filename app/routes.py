from app import app
from flask import render_template, request, redirect, url_for
from .db_layer import *


@app.route('/')
def index():
    books = get_books_from_json()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'pwd':
            return redirect(url_for('add_book'))  # Redirect to add_book on successful login
        else:
            error = 'Incorrect username or password. Please try again.'
    return render_template('login.html', error=error)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
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
