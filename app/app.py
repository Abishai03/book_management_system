from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Define a route for the Contact Us page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission here (e.g., save data to a database)
        # For this example, we'll just print the submitted data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Name: {name}, Email: {email}, Message: {message}")
        return redirect('/contact')  # Redirect to the same page after submission

    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
