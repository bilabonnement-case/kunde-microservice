from flask import Flask, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
import sqlite3

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Swagger Configuration
app.config['SWAGGER'] = {
    'title': 'Kunde Microservice API',
    'uiversion': 3,
    'openapi': '3.0.0'
}
swagger = Swagger(app)

# Database Configuration
DATABASE = "kunde-database.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Drop table if it exists (optional during development)
        ##cursor.execute("DROP TABLE IF EXISTS customers")
        # Create the customers table if it doesn't already exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            kunde_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique customer ID
            navn TEXT NOT NULL,                        -- Customer name
            adresse TEXT NOT NULL,                     -- Customer address
            telefon INTEGER NOT NULL,                  -- Customer phone number
            email TEXT NOT NULL,                       -- Customer email
            cprnummer TEXT NOT NULL,                   -- CPR number
            kreditvurdering_status TEXT NOT NULL,      -- Credit status (e.g., RKI)
            oprettelsesdato TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Creation timestamp
        )
        """)
        conn.commit()


init_db()

# Enum for Kreditvurdering Status
class KreditStatus:
    RKI = "RKI"
    GODKENDT = "Godkendt"


@app.route('/')
@swag_from('swagger/home.yaml')
def home():
    return jsonify({
        "service": "Kunde-Service",
        "available_endpoints": [
            {"path": "/create_customer", "method": "POST", "description": "Create a new customer"},
            {"path": "/get_customer/<int:kunde_id>", "method": "GET", "description": "Retrieve customer details by ID"},
            {"path": "/update_status/<int:kunde_id>", "method": "PUT", "description": "Update customer credit status"},
            {"path": "/report", "method": "GET", "description": "Generate customer report"},
        ]
    })


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/create_customer', methods=['POST'])
@swag_from('swagger/create_customer.yaml')
def create_customer():
    try:
        data = request.get_json()
        navn = data.get("navn")
        adresse = data.get("adresse")
        telefon = data.get("telefon")
        email = data.get("email")
        cprnummer = data.get("cprnummer")
        kreditvurdering_status = KreditStatus.GODKENDT

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO customers (navn, adresse, telefon, email, cprnummer, kreditvurdering_status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (navn, adresse, telefon, email, cprnummer, kreditvurdering_status))
            conn.commit()

            kunde_id = cursor.lastrowid

        return jsonify({"message": "Customer created", "kunde_id": kunde_id}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route('/get_customer/<int:kunde_id>', methods=['GET'])
@swag_from('swagger/get_customer.yaml')
def get_customer(kunde_id):
    with get_db_connection() as conn:
        customer = conn.execute("SELECT * FROM customers WHERE kunde_id = ?", (kunde_id,)).fetchone()

    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(dict(customer)), 200


@app.route('/update_status/<int:kunde_id>', methods=['PUT'])
@swag_from('swagger/update_status.yaml')
def update_status(kunde_id):
    try:
        data = request.get_json()
        kreditvurdering_status = data.get("kreditvurdering_status")

        if kreditvurdering_status not in [KreditStatus.RKI, KreditStatus.GODKENDT]:
            return jsonify({"error": "Invalid credit status"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()
            result = cursor.execute("""
            UPDATE customers SET kreditvurdering_status = ? WHERE kunde_id = ?
            """, (kreditvurdering_status, kunde_id))
            conn.commit()

            if result.rowcount == 0:
                return jsonify({"error": "Customer not found"}), 404

        return jsonify({"message": "Credit status updated"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route('/report', methods=['GET'])
@swag_from('swagger/report.yaml')
def report():
    with get_db_connection() as conn:
        total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        rki_customers = conn.execute("SELECT COUNT(*) FROM customers WHERE kreditvurdering_status = ?", (KreditStatus.RKI,)).fetchone()[0]
        approved_customers = conn.execute("SELECT COUNT(*) FROM customers WHERE kreditvurdering_status = ?", (KreditStatus.GODKENDT,)).fetchone()[0]

    report_data = {
        "TotalCustomers": total_customers,
        "RKICustomers": rki_customers,
        "ApprovedCustomers": approved_customers
    }

    return jsonify(report_data)


if __name__ == '__main__':
    app.run(debug=bool(int(os.getenv('FLASK_DEBUG', 0))), host='0.0.0.0', port=5004)