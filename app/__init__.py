from flask import Flask, render_template
from db import create_index_if_not_exists, customers      

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

from app import customer
from app import sales
from app import aggregation 

# create index
create_index_if_not_exists(customers, 'company')