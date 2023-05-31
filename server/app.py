#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime

from models import db, Activity, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET', 'POST'])
def get_campers():
    if request.method == 'GET':
        campers = Camper.query.all() 
        return {'campers': [camper.to_dict() for camper in campers]}
    else:
        campers = request.form['campers']


@app.route('/campers/<int:id>', methods=['GET', 'DELETE'])
def get_camper_by_id(id):
    camper = Camper.query.get(1)
    return camper.to_dict() 


@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all() 
    return {'activities': [activity.to_dict() for activity in activities]}


@app.route('/signups', methods=['POST'])
def new_signup():
    request_data = request.get_json()
    time = request.form.get('time')
    camper_id = request.form.get('camper_id')
    activity_id = request.form.get('activity_id')
    if request_data:
        if 'time' in request_data:
            time = request_data['time'] 
        if 'camper_id' in request_data:
            camper_id = request_data['camper_id']
        if 'activity_id' in request_data: 
            activity_id = request_data['activity_id']
    return '''
           The time value is: {}
           The camper_id value is: {}
           The activity_id value is: {}
            '''.format(time, camper_id, activity_id)


    

if __name__ == '__main__':
    app.run(port=5555, debug=True)

"""
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        time = request.form.get('time')
        camper_id = request.form.get('camper_id')
        activity
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

"""