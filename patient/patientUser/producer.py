import pika
from .models import PatientUser

credentials = pika.PlainCredentials('guest', 'guest')


def dispatchMessage(patient: PatientUser, messageId: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port='5672', credentials=credentials))

    channel = connection.channel()
    channel.exchange_declare('patient', durable=True, exchange_type='topic')

    channel.queue_declare(queue="dispatch")
    channel.queue_bind(exchange='patient', queue='dispatch', routing_key='A')
    
    str_patient = patient.toString() + f";{messageId}"
    channel.basic_publish(exchange="patient", routing_key='A', body=str_patient)
    # channel.close()
    
    