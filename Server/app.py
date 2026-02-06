
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '12345',
    'dbname': 'demo_flask'
}

def get_db_connection():
    connection = psycopg2.connect(**db_config)
    return connection

@app.route('/', methods=['GET'])
def get_books():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM book")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)

@app.route('/create', methods=['POST'])
def create_books():
    new_book = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO book (publisher, name, date, cost) VALUES (%s, %s, %s, %s)", (new_book['publisher'], new_book['name'], new_book['date'],new_book['cost']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(new_book), 201

@app.route('/update/<int:id>', methods=['PUT'])
def update_book(id):
    updated_book = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE book SET publisher=%s, name=%s, date=%s , cost=%s WHERE id=%s", (updated_book['publisher'], updated_book['name'], updated_book['date'], updated_book['cost'],id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(updated_book)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM book WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'result': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)