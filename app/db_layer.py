import json
import os

db_file = 'data/books.json'

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
            json.dump(books_load, file, indent=4)

        return True
    except Exception as e:
        return False

def remove_book_from_json(ISDN: str) -> bool:
    # TODO: Implement this function
    pass

def get_users():
    with open('app/data/users.json') as f:
        return json.load(f)

# Add new user to database
def add_user(username, password):
    if username == None or password == None:
        return False
    
    try:
        with open('app/data/users.json', 'r') as file:
            users = json.load(file)
        
        user_id = max(users, key=lambda user: user['id'])['id'] + 1
        
        users.append({
            "id": user_id,
            "username": username,
            "password": password,
            "role": "user"})
        
        with open('app/data/users.json', 'w') as file:
            json.dump(users, file, indent=4)
            return True
    
    except Exception as e:
        return False
