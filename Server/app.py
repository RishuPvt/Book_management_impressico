
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
CORS(app)


# JWT Config
app.config["JWT_SECRET_KEY"] = "asdfghjkl"
jwt = JWTManager(app)

db_config = {
    'host' :"host.docker.internal",
    'user': 'postgres',
    'password': 'Rishu@raj27',
    'dbname': 'flask_demo'
}

def get_db_connection():
    connection = psycopg2.connect(**db_config)
    return connection



# =============================
# 🔐 REGISTER
# =============================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return jsonify({"message": "Email already registered"}), 400

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "User registered successfully"}), 201



# =============================
# 🔐 LOGIN
# =============================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # Search by email
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    # Check password
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "username": user['username'],
            "email": user['email']
        })

    return jsonify({"message": "Invalid email or password"}), 401




@app.route('/', methods=['GET'])
@jwt_required()
def get_books():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM book")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    print("Current User:", get_jwt_identity())
    return jsonify(result)

@app.route('/create', methods=['POST'])
@jwt_required()
def create_books():
    new_book = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO book (publisher, name, date, cost, edition) VALUES (%s, %s, %s, %s ,%s)", (new_book['publisher'], new_book['name'], new_book['date'],new_book['cost'],  new_book['edition']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(new_book), 201

@app.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    updated_book = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE book SET publisher=%s, name=%s, date=%s , cost=%s , edition=%s WHERE id=%s ", (updated_book['publisher'], updated_book['name'], updated_book['date'], updated_book['cost'],  updated_book['edition'],id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(updated_book)

@app.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM book WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'result': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0", port=5000 )