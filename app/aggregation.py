from flask import jsonify
from app import app
from db import sales

# Sales Value by Customer
@app.route('/report/salesValueByCustomer', methods=['GET'])
def generate_sales_value_by_customer():
    try:
        aggregated_data = list(sales.aggregate([
            {
                "$unwind": "$sales"
            },
            {
              "$lookup": {
                "from": "customers",
                "localField": "sales.customer",
                "foreignField": "_id",
                "as": "customer"
              } 
            },
            {
                "$unwind": "$customer"
            },
            {
                "$group": {
                    "_id": "$sales.customer",
                    "customer": {
                        "$first": "$customer.company"
                    },
                    "totalSalesValue": {
                        "$sum": "$sales.value"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer": 1,
                    "totalSalesValue": 1
                }
            }
        ]))
        return jsonify({'message': 'Sales value by customer generated successfully', 'list': aggregated_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    
# Total Sales Value 
@app.route('/report/totalSales', methods=['GET'])
def generate_total_sales():
    try:
        aggregated_data = list(sales.aggregate([
            {
                "$unwind": "$sales"
            },
            {
                "$group": {
                    "_id": None,
                    "totalSalesValue": {
                        "$sum": "$sales.value"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "totalSalesValue": 1
                } 
            }
        ]))
        return jsonify({'message': 'Total sales value generated successfully', 'list': aggregated_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Sales Value by Each Sales
@app.route('/report/salesValueByEachSales', methods=['GET'])
def generate_sales_by_each_sales():
    try:
        aggregated_data = list(sales.aggregate([
            {
                "$unwind": "$sales"
            },
            {
                "$group": {
                    "_id": "$_id",
                    "totalSalesValue": {
                        "$sum": "$sales.value"
                    }
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "totalSalesValue": 1
                }
            }
        ]))
        return jsonify({'message': 'Sales value by each sales generated successfully', 'list': aggregated_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500    