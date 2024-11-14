from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # MySQL server
        user='root',       # MySQL username
        password='1234',   # MySQL password
        database='food_ordering'  # Database name
    )
    return connection

# Route to serve the homepage (with menu items)
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch menu items from the database
@app.route('/get_menu', methods=['GET'])
def get_menu():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu")  # Assuming your menu is stored in a 'menu' table
    menu_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(menu_items)

# Route to handle order placement
@app.route('/place_order', methods=['POST'])
def place_order():
    order_data = request.get_json()
    if not order_data:
        return jsonify({"message": "No data provided"}), 400
    
    # Extract the order details
    order_items = order_data.get('order', [])
    
    # Open a database connection
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert each order item into the database (order history)
    for item in order_items:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        
        cursor.execute('''
            INSERT INTO orders (item_name, quantity, price)
            VALUES (%s, %s, %s)
        ''', (name, quantity, price))
    
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Order placed successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
