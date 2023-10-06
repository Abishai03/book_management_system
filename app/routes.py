import json
from app import app
from flask import render_template, request, redirect, url_for, jsonify
import os



@app.route('/')
def index():
    with open('app/data/books.json', 'r') as file:
        books = json.load(file)
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


@app.route('/logged_in')
def logged_in():
    return 'Logged In'

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
        try:
            with open('app/data/books.json', 'r') as file:
                books = json.load(file)

            books.append(new_book)

            with open('app/data/books.json', 'w') as file:
                json.dump(books, file)

            return render_template('add_book.html', message="Successfully added to database. Return to home.")
        except Exception as e:
            return render_template('add_book.html', message="Failed to add book to database. Please try again.")
    return render_template('add_book.html', message=None)
