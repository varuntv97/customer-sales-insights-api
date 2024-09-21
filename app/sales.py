from flask import request, jsonify
from app import app
from db import sales
import uuid

@app.route('/sales', methods=['POST','GET'])
def sales_handler():
        # Get all sales
        if request.method == 'GET':
            try:
                sales_list = list(sales.find({}))
                return jsonify({'message': 'Sales fetched successfully', 'list': sales_list}), 200
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
        
        # Create sales
        if request.method == 'POST':
            try:
                data = request.json
                sales_obj = {}
                sales_obj['_id'] = str(uuid.uuid4())
                sales_obj['sales'] = data['sales']
                sales.insert_one(sales_obj)
                return jsonify({'message': 'Sales added successfully', 'customerId': sales_obj['_id']}), 200
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
 
@app.route('/sales/<id>', methods=['PUT','GET'])    
def sales_by_id_handler(id):
         # Update a sales document
        if request.method == 'PUT':
            try:
                data = request.json  
                sales.find_one_and_update({'_id':id},{'$set':data})
                return jsonify({'message': 'Sales updated successfully', 'salesId': id}), 200
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
        
        # Get a single sales document
        if request.method == 'GET':
            try:
                sale = sales.find_one({'_id':id})
                return jsonify({'message': 'Sale fetched successfully', 'data': sale}), 200   
            except Exception as e:
                return jsonify({'error':'Error occured'}), 500
            
                 