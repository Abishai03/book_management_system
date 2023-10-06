
# Book Management System

This application allows users to view a list of books and provides an admin interface for adding new books to the list.

## User Perspective

### Features:

1. **View Books**: Upon accessing the homepage, users can see a list of books displayed in a table format. This table provides details like the title, author, ISDN, price, and a short description of each book.
2. **Add Books (Admin)**: There's a button labeled "Add Books by Seller" which redirects to a login page. Once logged in with the correct credentials (username: `admin`, password: `pwd`), the user (assumed to be a seller or admin) can add new books to the database.

## Technical / Implementation Details

### Directory Structure:

```
/app
    /templates
        index.html
        login.html
        add_book.html
    /static
        (CSS, JS, images, etc.)
    /data
        books.json
    __init__.py
    routes.py
run.py
```

### Core Implementation:

- **Flask**: This application is built using Flask, a micro web framework written in Python.
- **Data Storage**: Book data is stored in a JSON file (`books.json`) which acts as a simple database.
- **Templates**: Flask's Jinja2 templating engine is used to render the HTML views.
- **Modular Design**: The application follows a modular design with separate files for routes and app initialization.

### Setup & Run:

1. Ensure you have Flask installed: `pip install Flask`.
2. Navigate to the directory containing `run.py`.
3. Run the application with `python run.py`.
4. Access the application in a browser using the URL: `http://127.0.0.1:5000/`.

## To-Do's (Future Improvements)

- [ ] Add a search bar to the homepage to filter the books.
- [ ] Add a filter to the homepage to filter books by title, author, ISBN, price, and description.
- [ ] Add a "add to cart" button to the homepage.
- [ ] Add a "Delete Book" button to the admin interface.
- [ ] Add a "Edit Book" button to the admin interface.
- [ ] Add a filter to the admin interface to filter books by title, author, ISBN, price, and description.
- [ ] Add a "Logout" button to the admin interface.
- [ ] Add a "cart" page to the application.
- [ ] The cart page will list all the books in the cart.
- [ ] Add a "checkout" button to the cart page.
- [ ] Add a "path" field to the database, to store the path to the location of the ebook.
- [ ] Add a "path" field to the database, to store the path to the cover image of the book.
- [ ] Add cover image of the books to the homepage.
- [ ] Add cover image of the books to the admin interface.
- [ ] Add cover image of the books to the cart page.
- [ ] Beautify the application's UI.


---

*Note: This application is for demonstration purposes and shouldn't be used in a production environment without further refinements, especially regarding security and data storage.*
