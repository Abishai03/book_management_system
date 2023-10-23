import json
import os

db_file = 'app/data/books.json'

def get_books_from_json() -> dict:
    try:
        with open(db_file, 'r') as file:
            books = json.load(file)
        return books
    except Exception as e:
        return [f"{e}"]

def add_book_to_json(book: dict) -> bool:
    try:
        with open(db_file, 'r') as file:
            books_load = json.load(file)

        books_load.append(book)

        with open(db_file, 'w') as file:
            json.dump(books_load, file)

        return True
    except Exception as e:
        return False

def remove_book_from_json(ISDN: str) -> bool:
    # TODO: Implement this function
    pass

def get_users():
    with open('app/data/users.json') as f:
        return json.load(f)
