from flask import request, jsonify
from app import app
from db import customers
import uuid
from pymongo.errors import ConnectionFailure, DuplicateKeyError

@app.route('/customer', methods=['POST','GET'])
def customer_handler():
        # Get all the customers
        if request.method == 'GET':
            try:
                customer_list = list(customers.find({}))
                return jsonify({'message': 'Customer fetched successfully', 'list': customer_list}), 200
            except ConnectionFailure as e:
                return jsonify({'error': "Internal server error"}), 500
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500    
    
        # Create a customer
        if request.method == 'POST':
            try:
                data = request.json
                customer = {}
                customer['_id'] = str(uuid.uuid4())
                customer['firstName'] = data['firstName']
                customer['LastName'] = data['lastName']
                customer['company'] = data['company']
                customers.insert_one(customer)
                return jsonify({'message': 'Customer added successfully', 'customerId': customer['_id']}), 200
            except ConnectionFailure as e:
                return jsonify({'error': "Internal server error"}), 500
            except DuplicateKeyError as e:
                return jsonify({'error': "Company already exists"}), 500
            except Exception as e:
                print(e)
                return jsonify({'error':'Error occured'}), 500
    
@app.route('/customer/<id>', methods=['DELETE','PUT','GET'])
def customer_by_id_handler(id):
        # Update a customer
        if request.method == 'PUT':
            try:
                data = request.json
                update_fields={}
                update_fields['firstName'] = data['firstName']
                update_fields['LastName'] = data['lastName']
                update_fields['company'] = data['company']
                customers.find_one_and_update({'_id':id},{'$set':update_fields})
                return jsonify({'message': 'Customer updated successfully', 'customerId': id}), 200
            except ConnectionFailure as e:
                return jsonify({'error': "Internal server error"}), 500
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
        
        # Delete a customer
        if request.method == 'DELETE':
            try:
                customers.find_one_and_delete({'_id':id})
                return jsonify({'message': 'Customer deleted successfully', 'customerId': id}), 200
            except ConnectionFailure as e:
                return jsonify({'error': "Internal server error"}), 500
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
        
        # Get a single customer
        if request.method == 'GET':
            try:
                customer = customers.find_one({'_id':id})
                return jsonify({'message': 'Customer fetched successfully', 'data': customer}), 200
            except ConnectionFailure as e:
                return jsonify({'error': "Internal server error"}), 500
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
        
