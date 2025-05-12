import pika
import json
from sqlalchemy.orm import sessionmaker
from models import Cliente
from config.config import engine

# Crea la sesión de base de datos
SessionLocal = sessionmaker(bind=engine)

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if data.get("model") == "cliente":
            action = data.get("action", "create")
            cliente_data = data.get("data")
            session = SessionLocal()
            try:
                existente = session.query(Cliente).filter_by(id_cliente=cliente_data["id_cliente"]).first()
                if action == "delete":
                    if existente:
                        session.delete(existente)
                        session.commit()
                        print(f"Cliente eliminado: {cliente_data['id_cliente']}")
                    else:
                        print(f"Cliente a eliminar no existe: {cliente_data['id_cliente']}")
                elif action == "update":
                    if existente:
                        for campo, valor in cliente_data.items():
                            setattr(existente, campo, valor)
                        session.commit()
                        print(f"Cliente actualizado: {cliente_data['id_cliente']}")
                    else:
                        print(f"Cliente a actualizar no existe: {cliente_data['id_cliente']}")
                else:  # create
                    if not existente:
                        nuevo_cliente = Cliente(**cliente_data)
                        session.add(nuevo_cliente)
                        session.commit()
                        print(f"Cliente replicado en base de datos local: {cliente_data['id_cliente']}")
                    else:
                        print(f"Cliente ya existe: {cliente_data['id_cliente']}")
            except Exception as e:
                session.rollback()
                print(f"Error al replicar cliente: {e}")
            finally:
                session.close()
    except Exception as e:
        print(f"[ERROR] Fallo en el callback: {e}")

def iniciar_consumidor():
    try:
        print("[DEBUG] Intentando conectar a RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'sebas123'),
            heartbeat=600,
            blocked_connection_timeout=300
        ))
        print("[DEBUG] Conexión a RabbitMQ exitosa.")
        channel = connection.channel()
        print("[DEBUG] Canal creado.")
        channel.queue_declare(queue='replicacion_clientes', durable=True)
        print("[DEBUG] Cola declarada.")
        print("[*] Esperando mensajes. Para salir presiona CTRL+C")
        channel.basic_consume(queue='replicacion_clientes', on_message_callback=callback, auto_ack=True)
        print("[DEBUG] Consumidor registrado.")
        channel.start_consuming()
        print("[!] El consumidor dejó de consumir (start_consuming terminó)")
    except Exception as e:
        print(f"[ERROR] Fallo en iniciar_consumidor: {e}")


if __name__ == "__main__":
    iniciar_consumidor()
