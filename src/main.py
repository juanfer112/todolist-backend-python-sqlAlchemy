"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db,Todos
import mysql.connector


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)

CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos', methods=['GET'])
def get_task():
    tasks=Todos.query.all()
    todo_list=list(map(lambda task: task.serialize(),tasks))
    return jsonify(todo_list),200

@app.route('/todos', methods=['POST'])
def post_task():
    body = request.get_json() 

    if 'done' not in body:
        return 'please specify true or false in done',400
    if 'label' not in body:
        return 'please specify the label', 400
    todo_list=Todos(done=body['done'], label=body['label'])
    db.session.add(todo_list)
    db.session.commit()
    return jsonify(todo_list.serialize()), 200

@app.route('/todos/<id>', methods=['DELETE'])
def delete_task(id):
    todo_list=Todos.query.filter_by(id=id).first_or_404()
    db.session.delete(todo_list)
    db.session.commit()
    return jsonify(todo_list.serialize()),200

@app.route('/todos', methods=['PUT'])
def update_task():
    body = request.get_json()
    todo_list=Todos.query.filter_by(id=body['id']).first_or_404()
    todo_list.done=body['done']
    todo_list.label=body['label']
    db.session.commit()
    return jsonify(todo_list.serialize()),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

