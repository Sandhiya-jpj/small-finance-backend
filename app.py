from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import os

app = Flask(__name__)

# Sample static loan data for testing
loans = [
    {"borrower_name": "John Doe", "amount": 1000, "interest_rate": 5.5, "term_months": 12},
    {"borrower_name": "Jane Smith", "amount": 2000, "interest_rate": 6.0, "term_months": 24},
]

CORS(app)

# Supabase connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sandhiyasuchi%4024@db.ywxtpsuxljfjdobrmftm.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

@app.route('/')
def home():
    return "Flask backend is connected to Supabase!"

@app.route('/api/loans', methods=['GET'])
def get_loans():
    # For now, return static loans list
    return jsonify(loans)

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    try:
        new_customer = Customer(name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-users', methods=['GET'])
def get_users():
    try:
        users = db.session.execute(text('SELECT * FROM customers')).fetchall()
        user_list = [{'id': user[0], 'name': user[1], 'email': user[2]} for user in users]
        return jsonify({'users': user_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email} for c in customers])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
