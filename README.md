# Kunde-Service

Kunde-Service is a Flask-based microservice that handles customer management. It includes endpoints for creating customers, retrieving customer details, updating credit status, and generating customer reports. The service uses SQLite for database management and provides API documentation via Swagger.

## Features
	•	Create Customers: Add new customers with details like name, address, phone number, and CPR number.
	•	Retrieve Customer Details: Fetch customer details by their unique ID.
	•	Update Credit Status: Update the credit status of a customer (e.g., "RKI" or "Godkendt").
	•	Generate Reports: Summarize customer data, including total customers and credit status breakdown.
	•	API Documentation: Integrated Swagger UI for exploring and testing endpoints.

## Requirements

### Python Packages
	•	Python 3.7 or higher
	•	Flask
	•	Flasgger
	•	Python-Dotenv
	•	SQLite (built into Python)

### Python Dependencies

Install the required dependencies using:
```Pip install -r requirements.txt```

### Environment Variables

Create a .env file in the root directory and specify the following:
```FLASK_DEBUG=1```
```DATABASE=kunde-database.db```

## Getting Started

1. Initialize the Database

The service uses SQLite to store customer data. The database is automatically initialized when the service starts.
If reinitialization is needed, you can modify the init_db() function in kunde.app.py.

2. Start the Service

Run the Flask application:
```python kunde.app.py```
The service will be available at: http://127.0.0.1:5004

## API Endpoints

1. GET /

Provides a list of available endpoints in the service.

#### Response Example:
```
{
  "service": "Kunde-Service",
  "available_endpoints": [
    {"path": "/create_customer", "method": "POST", "description": "Create a new customer"},
    {"path": "/get_customer/<int:kunde_id>", "method": "GET", "description": "Retrieve customer details by ID"},
    {"path": "/update_status/<int:kunde_id>", "method": "PUT", "description": "Update customer credit status"},
    {"path": "/report", "method": "GET", "description": "Generate customer report"}
  ]
}
```

2. POST /create_customer

Creates a new customer in the system.

#### Request Body:
```
{
  "navn": "John Doe",
  "adresse": "Nørrebrogade 12, København",
  "telefon": 12345678,
  "email": "johndoe@example.com",
  "cprnummer": "123456-7890"
}

```

#### Response Example:
```
{
  "message": "Customer created",
  "kunde_id": 1
}
```

3. GET /get_customer/<int:kunde_id>

Fetches details for a specific customer by ID.

#### Response Example:
```
{
  "kunde_id": 1,
  "navn": "John Doe",
  "adresse": "Nørrebrogade 12, København",
  "telefon": 12345678,
  "email": "johndoe@example.com",
  "cprnummer": "123456-7890",
  "kreditvurdering_status": "Godkendt",
  "oprettelsesdato": "2024-06-01 12:00:00"
}
```

4. PUT /update_status/<int:kunde_id>

Updates the credit status of an existing customer.

#### Request Body:
```
{
  "kreditvurdering_status": "RKI"
}
```

#### Response Example:
```
{
  "message": "Credit status updated"
}
```

5. GET /report

Generates a summary report of all customers, including credit statuses.

#### Response Example:
```
{
  "TotalCustomers": 25,
  "RKICustomers": 5,
  "ApprovedCustomers": 20
}
```
## Project Structure
```
.
├── kunde.app.py            # Main Flask application
├── data/
│   └── kunde-database.db   # SQLite database (created automatically)
├── swagger/                # YAML files for Swagger documentation
│   ├── home.yaml
│   ├── create_customer.yaml
│   ├── get_customer.yaml
│   ├── update_status.yaml
│   └── report.yaml
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md               # Project documentation
```

## Development Notes

### Swagger Documentation
	•	Swagger is available at /apidocs.
	•	API specifications are written in YAML and stored in the swagger/ folder.

### Database Management
####	•	Initialization: Automatically initializes the database on start.
####	•	Schema:
	•	kunde_id: Unique ID for the customer (Primary Key).
	•	navn: Customer's name.
	•	adresse: Customer's address.
	•	telefon: Customer's phone number.
	•	email: Customer's email address.
	•	cprnummer: Customer's CPR number.
	•	kreditvurdering_status: Credit status ("RKI" or "Godkendt").
	•	oprettelsesdato: Timestamp when the customer was created.

## Contributions

Feel free to fork the repository and submit pull requests. For major changes, open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License. See LICENSE for more information.
