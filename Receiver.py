#!flask/bin/python
import pika
import json
import Events

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def calculate(message):
    return message+12

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    message = body.decode('utf-8')
    message = eval(message)
    if (message == 1):
        print("message is 1")
        calculate(message)
    elif (message == 2):
        print("message is 2")
    ch.basic_ack(delivery_tag = method.delivery_tag)


def eventCallback(ch, method, properties, body):
    message = body.decode('utf-8')   # bytes to string
    message = json.loads(message)   # string to json
    try:
        eventType = message['type']

        if eventType == "loginSuccesEvent":
            print("Succesfull login occured at: "+ message['timestamp'] + " count: "
                  + str(Events.loginSuccesEvent.Succes(Events.loginSuccesEvent)))
        if eventType == "loginFailedEvent":
            print("Failed login occured at: "+ message['timestamp'] + " count: "
                  + str(Events.loginFailedEvent.Failed(Events.loginFailedEvent)))
        #pageVisitedEvent
        if eventType == "pageVisitedEvent":
            print("Somebody from ip:'" + message['ip'] + "' visited the "+message['pageName']+
                  " page at: " + message['timestamp'] + " count: "
                  + str(Events.pageVisitedEvent.Visited(Events.pageVisitedEvent)))

        #buttonPushedEvent

    except ValueError as error:
        print("eventType not recognized: " + error.args)


    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(eventCallback,
                      queue='task_queue')
channel.start_consuming()


#
#
#
# app = Flask(__name__)
#
# ###Auth
# auth = HTTPBasicAuth()
# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     pw = "$5$rounds=535000$TbjfFguG9yEaDQWS$6joRKlWuiXMBP8dTYoMQ5woWDepmcfcGWBKZtX9vvT0"
#     return username == 'Nergy' and sha256_crypt.verify(password, pw)
#
# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#     'Could not verify your access level for that URL.\n'
#     'You have to login with proper credentials', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated
#
#
# ###RESTFULL
#
# def make_public_tasks(task):
#
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task
#
# def make_public_task(task):
#
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task
#
# ##DB
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
# ### API-Controller
#
#
# @app.route('/', methods=['GET']) # fancy
# def home():
#     return "Welcome to the Home Page"
#
# @app.route('/todo/api/v1.0/tasks', methods=['GET']) # fancy
# @requires_auth
# def get_tasks():
#     return jsonify({'tasks': [make_public_tasks(task) for task in tasks]})
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# @requires_auth
# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         not_found(404)
#     return jsonify({'task': make_public_task(task[0])})
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)
#
# ## Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Page Not found'}), 404)
#
# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bar Request'}), 400)
#
# if __name__ == '__main__':
#     app.run(debug=True)