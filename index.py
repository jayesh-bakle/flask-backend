# import flask
# from pymongo import MongoClient
# from bson.json_util import dumps
# from flask import request
# from flask_cors import CORS 
# import os

# app = flask.Flask(__name__)
# CORS(app)

# def by_id(id):
#     mongodb_url=os.environ.get('MONGODB_URL')
#     db = MongoClient(mongodb_url).zomato
#     collection = db.Finaldata
#     criteria = {"R.res_id": id}
#     data = collection.find_one(criteria)
#     return dumps(data)

# def search_all_restaurants(request):
#     # Retrieving query parameters
#     filter1 = request.args.get('filter1', default=None, type=str)
#     country = request.args.get('country', default=None, type=int)
#     avgSpend = request.args.get('avgSpend', default=None, type=str)
#     cuisines = request.args.get('cuisines', default=None, type=str)
#     lat = request.args.get('lat', default=None, type=float)
#     long = request.args.get('long', default=None, type=float)
#     radius = request.args.get('radius', default=None, type=float)
#     page = request.args.get('page', default=1, type=int)
#     page_size = request.args.get('page_size', default=10, type=int)

#     mongodb_url=os.environ.get('MONGODB_URL')
#     db = MongoClient(mongodb_url).test-data
#     collection = db.Finaldata
#     skip = (page - 1) * page_size  

#     query = {}
#     if filter1:
#         query["name"] = {"$regex": filter1, "$options": "i"}  
#     if country:
#         query["location.country_id"] = country  
#     if avgSpend:
#         query["average_cost_for_two"] = {"$lte": int(avgSpend)}  
#     if cuisines:
#         query["cuisines"] = {"$regex": cuisines, "$options": "i"}  

#     if lat is not None and long is not None and radius is not None:
#         query["location1"] = {
#             "$geoWithin": {
#                 "$centerSphere": [[float(long), float(lat)], radius / 6378.1] 
#             }
#         }

#     data = collection.find(query).skip(skip).limit(page_size)
    
#     total_records = collection.count_documents(query)
#     total_pages = (total_records + page_size - 1) // page_size

#     response = {
#         "data": list(data), 
#         "total_pages": total_pages,
#         "current_page": page,
#         "page_size": page_size
#     }
    
#     return dumps(response)


# @app.route('/')
# def hello():
#     return "Hello World!"

# @app.route('/search/restaurant/<int:id>', methods=['GET'])
# def search_by_id(id):
#     return by_id(id)
    
# @app.route('/search/restaurant/all', methods=['GET'])
# def search_all():
#     return search_all_restaurants(request)



import flask
from pymongo import MongoClient
from bson.json_util import dumps
from flask import request
from flask_cors import CORS 
import os

app = flask.Flask(__name__)
CORS(app)

def by_id(id):
    mongodb_url = os.environ.get('MONGODB_URL')
    db = MongoClient(mongodb_url).test_data
    collection = db.restaurants  # Change to the correct collection
    criteria = {"R.res_id": id}
    data = collection.find_one(criteria)
    return dumps(data)

def search_all_restaurants(request):
    # Retrieving query parameters
    filter1 = request.args.get('filter1', default=None, type=str)
    country = request.args.get('country', default=None, type=int)
    avgSpend = request.args.get('avgSpend', default=None, type=str)
    cuisines = request.args.get('cuisines', default=None, type=str)
    lat = request.args.get('lat', default=None, type=float)
    long = request.args.get('long', default=None, type=float)
    radius = request.args.get('radius', default=None, type=float)
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)

    mongodb_url = os.environ.get('MONGODB_URL')
    db = MongoClient(mongodb_url).test_data
    collection = db.restaurants  # Change to the correct collection
    skip = (page - 1) * page_size  

    query = {}
    if filter1:
        query["name"] = {"$regex": filter1, "$options": "i"}  
    if country:
        query["location.country_id"] = country  # Adjust based on your database's structure
    if avgSpend:
        query["average_cost_for_two"] = {"$lte": int(avgSpend)}  
    if cuisines:
        query["cuisines"] = {"$regex": cuisines, "$options": "i"}  

    if lat is not None and long is not None and radius is not None:
        query["location1"] = {
            "$geoWithin": {
                "$centerSphere": [[float(long), float(lat)], radius / 6378.1] 
            }
        }

    data = collection.find(query).skip(skip).limit(page_size)
    
    total_records = collection.count_documents(query)
    total_pages = (total_records + page_size - 1) // page_size

    response = {
        "data": list(data), 
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size
    }
    
    return dumps(response)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/search/restaurant/<int:id>', methods=['GET'])
def search_by_id(id):
    return by_id(id)
    
@app.route('/search/restaurant/all', methods=['GET'])
def search_all():
    return search_all_restaurants(request)
