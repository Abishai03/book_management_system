from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="DESKTOP-04BA3ME",
    user="root",
    password="Abi1989",
    database="perfecto"
)
cursor = db.cursor()

# ...

@app.route('/search')
def search():
    query = request.args.get('query')

    cursor.execute("SELECT name FROM your_table WHERE name LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()

    search_results = [{'name': result[0]} for result in results]

    return jsonify(search_results)

# ...

if __name__ == '__main__':
    app.run(debug=True)
