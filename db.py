from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# DB Name
db = client['flask-app']

# Customers collection
customers = db['customers']

# Sales collection
sales = db['sales']

# Sales value by customer report collection
salesValueByCustomer = db['salesValueByCustomer']

# create index function
def create_index_if_not_exists(collection, index):
    try:
        # Get all indexes
        indexes = list(collection.list_indexes())
        concatinated_index_name = index + '_1' # Assuming ASCENDING index
        existing_index_names = [index['name'] for index in indexes]
    except Exception as e:
        print(f'Error occured')
        return    
    
    try:
        # Create index if not exists
        if concatinated_index_name not in existing_index_names:
            collection.create_index(index, unique=True)
            print(f'Index {concatinated_index_name} created successfully')
        else:
            print(f'Index {concatinated_index_name} already exists')
    except Exception as e:
        print(f'Error occured')
        return
    
    