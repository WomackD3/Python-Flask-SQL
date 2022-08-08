from flask import Flask, request, jsonify;
from peewee import *;
from playhouse.shortcuts import model_to_dict, dict_to_model;


app = Flask(__name__)

db = PostgresqlDatabase(
    'people', 
    user='mack', 
    password='',
    host='localhost',
    port=5432
   )

class BaseModel(Model):
    class Meta:
      database = db
    
class Person(BaseModel):
    name = CharField()
    age = IntegerField()

db.connect()
db.drop_tables([Person])
db.create_tables([Person])

Person(name='Mario', age=30).save()
Person(name='Mack', age=18).save()

@app.route('/person/', methods=['GET', 'POST'])
@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET': 
      if id:
          return jsonify(
              model_to_dict(
                  Person.get(
                     Person.id == id
                  )
              )
          )
      else:
          people_list = []
          for person in Person.select():
              people_list.append(model_to_dict(person))
          return jsonify(people_list)

    if request.method == 'PUT':
          return 'PUT request'

    if request.method == 'POST' :
          new_person = dict_to_model(Person, request.get_json())
          new_person.save()
          return jsonify({'great success': True})

    if request.method == 'DELETE':
          return 'DELETE request'

# @app.route('/')
# def index():
#     return 'Hello, world!' 

# @app.route('/Say-hello/<name>')
# def say_hello(name):
#     return f'hello, {name}!'

# @app.route('/endpoint', methods=['GET','PUT', 'POST', 'DELETE'])
# def endpoint():
#     if request.method == 'GET':
#       return 'GET request'
#     if request.method == 'PUT':
#       return 'PUT request'
#     if request.method == 'POST':
#       return 'POST request'
#     if request.method == 'DELETE':
#       return 'DELETE request'

# @app.route('/get-json')
# def get_json():
#   return jsonify({
#     'name': 'Mack'
#     'coolerThanGarfield': True,
#     'isAtHome': 'True, today'
#     })

app.run(port=3030, debug=True)