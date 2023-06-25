from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
secret_key = 'qwertyasd'

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
        return jsonify({'message': 'Invalid data'})


if __name__ == '__main__':
    app.run()
