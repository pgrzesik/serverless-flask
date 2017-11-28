import os

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
dynamo_client = boto3.client('dynamodb')


@app.route('/')
def hello():
    return 'Hello'


@app.route('/users/<string:user_id>')
def get_user(user_id):
    resp = dynamo_client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        })
    item = resp.get('item')

    if not item:
        return jsonify({
            'error': 'User does not exist'
        }), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provider userId and name'}), 400

    resp = dynamo_client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name}
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })
