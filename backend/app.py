from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import sqlite3
from config import Config
from routes import auth, debug
from models.users import db

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

# General debugging API, response verifies API host is running
app.add_url_rule('/api/debug', view_func=debug.debug, methods=['GET'])

# Handle user login call
app.add_url_rule('/api/login', view_func=auth.login, methods=['POST'])

# Handle user forgot password request
app.add_url_rule('/api/forgot_password', view_func=auth.forgot_password, methods=['POST'])

def get_db_connection():
    database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'products.db')
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/products', methods=['GET'])
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    products_list = []
    for product in products:
        product_dict = dict(product)
        if product_dict['image']:
            product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')
        products_list.append(product_dict)
    conn.close()
    return jsonify(products_list)


if __name__ == '__main__':
    app.run(debug=True)