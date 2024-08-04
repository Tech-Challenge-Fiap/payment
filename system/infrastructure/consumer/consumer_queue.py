import pika
import logging
from rabbitmq import get_rabbitmq_connection, get_rabbitmq_channel
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.usecase import payment_usecase

logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body, app):
    with app.app_context():
        message = body.decode('utf-8')
        print(f"Received {message}")
        # Suponha que a mensagem seja um JSON contendo os dados necessários
        import json
        try:
            data = json.loads(message)
            order_id = data.get('order_id')
            new_status = data.get('status')
            payment_value = data.get('payment_value')

            # Chame o use case updateOrder com os dados extraídos
            if order_id and new_status and payment_value:
                try:
                    request_json = {"value": payment_value}
                    payment = payment_usecase.CreatePayment.execute(request_json)

                except InfrastructureError:
                    return {"error": "Internal Error"}, 500
                return payment.response
            else:
                print("Invalid message format")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON message: {e}")

def start_consuming(app):
    try:
        connection = get_rabbitmq_connection()
        channel = get_rabbitmq_channel(connection, 'fila-pagamentos')
        channel.queue_declare(queue='fila-pagamentos', durable=True)

        def on_message(ch, method, properties, body):
            callback(ch, method, properties, body, app)

        # Configuração do consumidor
        channel.basic_consume(queue='fila-pagamentos', on_message_callback=on_message, auto_ack=True)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f'Failed to connect to RabbitMQ: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')