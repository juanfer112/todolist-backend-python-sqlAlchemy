# """
# This module takes care of starting the API Server, Loading the DB and Adding the endpoints
# """
# import os
# from flask import Flask, request, jsonify, url_for
# from flask_migrate import Migrate
# from flask_swagger import swagger
# from flask_cors import CORS
# from utils import APIException, generate_sitemap
# from models import db
# #from models import Person

# app = Flask(__name__)
# app.url_map.strict_slashes = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# MIGRATE = Migrate(app, db)
# db.init_app(app)
# CORS(app)

# # Handle/serialize errors like a JSON object
# @app.errorhandler(APIException)
# def handle_invalid_usage(error):
#     return jsonify(error.to_dict()), error.status_code

# # generate sitemap with all your endpoints
# @app.route('/')
# def sitemap():
#     return generate_sitemap(app)

# @app.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "hello": "world"
#     }

#     return jsonify(response_body), 200

# # this only runs if `$ python src/main.py` is executed
# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3000))
#     app.run(host='0.0.0.0', port=PORT, debug=False)

from flask import Flask, jsonify, request, json
from models import db, Todo, engine

app = Flask(__name__)

todos=[{ "label": "Sample todo1", "done": True }, { "label": "Sample todo2", "done": True,}]

@app.route('/todos', methods=['GET'])

def get_todos():
    body=jsonify(todos)
    return body

@app.route('/todos', methods=['POST'])

def add_new_todo():
    request_body= request.get_json()
    label = request.json['label'] 
    done = request.json['done'] 
    new_task = Todo(label,done)
    db.session.add(new_task)
    # decoded_object=json.loads(request_body)
    print("Incoming request with the following body", request_body)
    return request_body

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

