
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
        base.html
        help.html
        tou.html
        contact_us.html
    /data
        books.json
        users.json
    __init__.py
    routes.py
run.py
.env
```

### Core Implementation:

- **Flask**: This application is built using Flask, a micro web framework written in Python.
- **Data Storage**: 
  All data[books, user and coupon] are saved in SQLite database.
- **Templates**: Flask's Jinja2 templating engine is used to render the HTML views.
- **Modular Design**: The application follows a modular design with separate files for routes and app initialization.
- **Routes and Views**:
-   Home Page (/): Displays a list of available books.
- Signup (/signup): Allows new users to register for an account.
- Login (/login): Provides user authentication functionality.
- Logout (/logout): Logs out the current user.
- Add Book (/add_book): Allows administrators to add new books to the database.
- Edit Book (/edit_book/<int:book_id>): Allows administrators to edit details of existing books.
- Delete Book (/delete_book/<int:book_id>): Allows administrators to delete books from the database.
- Search (/search): Allows users to search for books by title.
- Chat (/chat): Provides a chat interface for interacting with a chatbot (not implemented in the provided code).
- Cart (/cart): Allows users to view and purchase books in their cart.
- Help (/help): Displays help information.
- Terms of Use (/tou): Displays terms of use.
- Contact Us (/contact_us): Displays contact information.
- Coupon Management (/coupon): Allows administrators to manage coupons.


### Setup & Run:

1. Ensure you have Flask installed: `pip install -r requirement.txt`.
2. create .env file and values of openai key, gmail and password
```
OpenAI = ''
email = ''
password = ''
```
2. Navigate to the directory containing `run.py`.
3. Run the application with `python run.py`.
4. Access the application in a browser using the URL: `http://127.0.0.1:5000/`.

## Database Schema
All the data is stored in SQLite.
- **User**: Represents a user of the application, with attributes such as username, password, email, and role.
- **Book**: Represents a book available in the bookstore, with attributes including title, author, ISDN, price, description, and thumbnail.
- **Coupon**: Represents a coupon that users can apply for discounts, with attributes such as code, price, and expiration date.

Only the admin user can add new books to the database.

## To-Do's (Future Improvements)

- [✓] Add a search bar to the homepage to filter the books.
- [✓] Add a filter to the homepage to filter books by title, author, ISBN, price, and description.
- [✓] Add a "add to cart" button to the homepage.
- [✓] Add a "Delete Book" button to the admin interface.
- [✓] Add a "Edit Book" button to the admin interface.
- [✓] Add a filter to the admin interface to filter books by title, author, ISBN, price, and description.
- [✓] Add a "Logout" button to the admin interface.
- [✓] Add a "cart" page to the application.
- [✓] The cart page will list all the books in the cart.
- [ ] Add a "checkout" button to the cart page.
- [ ] Add a "path" field to the database, to store the path to the location of the ebook.
- [ ] Add a "path" field to the database, to store the path to the cover image of the book.
- [✓] Add cover image of the books to the homepage.
- [✓] Add cover image of the books to the admin interface.
- [✓] Add cover image of the books to the cart page.
- [✓] Beautify the application's UI.
- [✓] Chat system to talk about listedbooks.

---

*Note: This application is for demonstration purposes and shouldn't be used in a production environment without further refinements, especially regarding security and data storage.*
