#!flask/bin/python
import pika
import json
import Events

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

#functie die uitgevoerd wordt als een Event toegevoegd wordt
def eventCallback(ch, method, properties, body):
    message = body.decode('utf-8')   # bytes to string
    message = json.loads(message)   # string to json
    try:
        eventType = message['type']

        if eventType == "loginSuccesEvent":
            print("Succesfull login occured at: "+ message['timestamp'] + " count: "
                  + str(Events.loginSuccesEvent.Succes(Events.loginSuccesEvent)))
        if eventType == "loginFailedEvent":
            print("Failed login occured, trying with: '" + message['triedPassword'] + "' at: "+ message['timestamp'] + " count: "
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
channel.start_consuming() # BEGIN!!! >:D