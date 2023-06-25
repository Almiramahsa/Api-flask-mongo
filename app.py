from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
import jwt
import os
from dotenv import load_dotenv


app = Flask(__name__)
secret_key = os.getenv('SECRET_KEY')

app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo'

mongo = PyMongo(app)


@app.route("/api/auth/register", methods=['POST'])
def register():
    data = request.form.to_dict()

    if mongo.db.user.find_one({'username': data['username']}):
        return jsonify({'message': 'Username already exists!'})
    elif data['username'] and data['password']:
        user_id = mongo.db.user.insert_one(
            {'username': data['username'], 'password': generate_password_hash(data['password'])})
        return jsonify({'message': "User registered successfully!"})
    else:
        return jsonify({'message': 'Data Empty'})


@app.route("/api/auth/login", methods=['POST'])
def login():
    data = request.form.to_dict()
    user = mongo.db['user'].find_one({'username': data['username']})

    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    payload = {'_id': str(user['_id']),
               'exp': datetime.utcnow() + timedelta(minutes=30)}
    access_token = jwt.encode(
        payload, secret_key, algorithm='HS256')
    return jsonify({'token': access_token}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
