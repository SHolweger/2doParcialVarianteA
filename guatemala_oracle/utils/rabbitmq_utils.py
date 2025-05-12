# rabbitmq_utils.py
import pika
import json

def publicar_cliente(cliente_data, action="create"):
    try:
        # Estructuramos el mensaje correctamente
        mensaje = {
            "model": "cliente",
            "action": action,
            "data": cliente_data
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'sebas123')
        ))
        channel = connection.channel()
        channel.queue_declare(queue='replicacion_clientes', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='replicacion_clientes',
            body=json.dumps(mensaje),
            properties=pika.BasicProperties(delivery_mode=2)  # mensaje persistente
        )
        connection.close()
        print(f"[✔] Cliente publicado a RabbitMQ: {mensaje}")
    except Exception as e:
        print(f"[✖] Error publicando en RabbitMQ: {e}")