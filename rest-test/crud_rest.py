from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import datetime

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add():
  user = mongo.db.user
  request_json = request.get_json()
  name = request_json.get('name')
  status = request_json.get('status')
  activity = request_json.get('activity')
  now = datetime.datetime.now()
  user_id = user.insert({'name': name, 'date_created':now , 'activity':activity, 'status': status})
  new_user = user.find_one({'_id': user_id })
  output = {'activity' : new_user['activity'], 'name': new_user['name'], 'status' : new_user['status']}
  return jsonify({'result' : output})

@app.route('/getAll', methods=['GET'])
def get_all():
  user = mongo.db.user
  output = []
  for s in user.find():
    output.append({'name' : s['name'],'date_created': s['date_created'] , 'activity': s['activity'],'status' : s['status']})
  return jsonify({'result' : output})

@app.route('/get/<name>', methods=['GET'])
def get_name(name):
  user = mongo.db.user
  s = user.find_one({'name' : name})
  if s:
    output = {'name' : s['name'],'date_created': s['date_created'] , 'activity': s['activity'],'status' : s['status']}
  else:
    output = "No such name"
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)