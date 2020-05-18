import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all() # This command creates the table in sqlite

def get_error_message(error, default_text):
    try:
        # Return message contained in error, if possible
        return error['description']
    except TypeError:
        # otherwise, return given default text
        return default_text


def getJSON(obj):
    if not isinstance(obj, list):
        obj = [obj]
    jsonList = json.dumps(obj)
    return jsonList

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    all_drinks = Drink.query.order_by(Drink.id).all()
    all_drinks_formatted = [drink.short() for drink in all_drinks]

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'No drinks found in Database.'})    
    
    return jsonify({
        'success': True,
        'drinks': all_drinks_formatted
    }), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    all_drinks = Drink.query.order_by(Drink.id).all()
    all_drinks_formatted = [drink.long() for drink in all_drinks]

    return jsonify({
        'success': True,
        'drinks': all_drinks_formatted
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',  methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    data = request.get_json()
    if 'title' and 'recipe' not in data:
        abort(422)

    title = data['title']
    recipe = data['recipe']
    recipeJSON = getJSON(recipe)
    drink = Drink(title=title, recipe=recipeJSON)
    drink.insert()

    return jsonify({
        'success': True,
        'drinks': drink.long()
    }), 200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',  methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)

    body = request.get_json()

    if not body:
      abort(400, {'message': 'Request doesnot contain valid JSON body'})

    drink_to_update = Drink.query.filter(Drink.id == drink_id).one_or_none()

    updated_title = body.get('title', None)
    updated_recipe = body.get('recipe', None)

    if updated_title:
        drink_to_update.title = body['title']

    if updated_recipe:
        drink_to_update.recipe = """{}""".format(body['recipe'])

    drink_to_update.update()
    return jsonify({
        'success': True,
        'drinks': [Drink.long(drink_to_update)]
    }), 200
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    drink.delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    })

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message":  get_error_message(error, "unprocessable")
    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": get_error_message(error, "bad request")
    }), 400

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": get_error_message(error, "resource not found")
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def processAuthError(AuthError):
    status_code = AuthError.status_code
    error_message = AuthError.error

    return jsonify({
        "success": False,
        "error": status_code,
        "message": get_error_message(error_message, "authentification fails")
    }), status_code
