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
        }, 404)

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })
