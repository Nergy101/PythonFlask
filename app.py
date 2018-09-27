#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request, Response
from flask import url_for
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from passlib.hash import sha256_crypt
import pika
import Events
import json
import datetime
import time

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

# message = "2"
# channel.basic_publish(exchange='',
#                       routing_key='task_queue',
#                       body=message,
#                       properties=pika.BasicProperties(
#                          delivery_mode = 2, # make message persistent
#                       ))

#print(" [x] Sent %r" % message)
#        connection.close()

###Auth
auth = HTTPBasicAuth()
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    pw = "$5$rounds=535000$TbjfFguG9yEaDQWS$6joRKlWuiXMBP8dTYoMQ5woWDepmcfcGWBKZtX9vvT0"

    return username == 'Nergy' and sha256_crypt.verify(password, pw)

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            payload = Events.loginFailedEvent(date, "geheim")  # maak loginSuccesEvent
            message = json.dumps(payload.__dict__)  # naar json
            channel.basic_publish(exchange='',
                                  routing_key='task_queue',
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
            return authenticate()

        payload = Events.loginSuccesEvent(date)  # maak loginSuccesEvent
        message = json.dumps(payload.__dict__)  # naar json
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return f(*args, **kwargs)


    return decorated


###RESTFULL

def make_public_tasks(task):

    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

def make_public_task(task):

    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

##DB
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
### API-Controller

@app.route('/', methods=['GET']) # fancy
def home():
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    payload = Events.pageVisitedEvent(date, "homepage")  # maak loginSuccesEvent
    message = json.dumps(payload.__dict__)  # naar json
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    return "Welcome to the Home Page"

@app.route('/todo/api/v1.0/tasks', methods=['GET']) # fancy
@requires_auth
def get_tasks():
    return jsonify({'tasks': [make_public_tasks(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        not_found(404)
    return jsonify({'task': make_public_task(task[0])})

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@requires_auth
def create_task():
    if not request.json or not 'title' in request.json:
        not_found(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        not_found(404)
    if not request.json:
        bad_request(400)
    # if 'title' in request.json and type(request.json['title']):
    #     not_found(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     not_found(400)
    # if 'done' in request.json and type(request.json['done']) is not bool:
    #     not_found(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@requires_auth
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        not_found(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


## Error handlers
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Page Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bar Request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)