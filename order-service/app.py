# order-service/app.py
from flask import Flask, jsonify, request
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment or defaults.
DB_NAME = os.getenv('POSTGRES_DB', 'ecommerce')
DB_USER = os.getenv('POSTGRES_USER', 'myuser')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT)
    return conn

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Get product info
        cur.execute("SELECT id, name, price FROM products WHERE id = %s;", (product_id,))
        product = cur.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        total_price = product['price'] * quantity
        # Insert order record.
        cur.execute(
            "INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s) RETURNING id, created_at;",
            (product_id, quantity, total_price)
        )
        order_info = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        order = {
            'order_id': order_info['id'],
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
            'created_at': order_info['created_at'].isoformat()
        }
        return jsonify(order), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders', methods=['GET'])
def list_orders():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT o.id as order_id, o.quantity, o.total_price, o.created_at, "
                    "p.id as product_id, p.name, p.price FROM orders o "
                    "JOIN products p ON o.product_id = p.id ORDER BY o.id;")
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)