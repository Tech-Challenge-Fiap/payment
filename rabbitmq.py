import pika

def get_rabbitmq_connection():
    parameters = pika.ConnectionParameters('my-rabbitmq', 5672)
    return pika.BlockingConnection(parameters)

def get_rabbitmq_channel(connection, queue_name):
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return channel

def publish_message(queue_name, message):
    connection = get_rabbitmq_connection()
    channel = get_rabbitmq_channel(connection, queue_name)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    connection.close()
    print(f" [x] Sent '{message}' to queue '{queue_name}'")