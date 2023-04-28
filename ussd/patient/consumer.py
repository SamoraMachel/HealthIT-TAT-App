import pika
from threading import Thread
from .models import Patient

credentials = pika.PlainCredentials('guest', 'guest')

def callBackFunctionForQueueA(ch, method, properties, body: bytes):
    attr_byte = body.decode('utf-8')
    attr = attr_byte.split(";")
    patient = Patient(
        id=attr[0],
        messageId=attr[-1],
        dispatch_time=attr[5],
        username=attr[1],
        phone_number=attr[2],
        age=attr[3],
        gender=attr[4]
    )
    patient.save()

def startConsumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port='5672', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare('patient', durable=True, exchange_type='topic')
    
    channel.basic_consume(
        queue='dispatch', 
        on_message_callback=callBackFunctionForQueueA,
        auto_ack=True
    )
    channel.start_consuming()
    # channel.close()