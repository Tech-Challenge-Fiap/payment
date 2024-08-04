from flask import Flask
import threading
from system.infrastructure.consumer.consumer_queue import start_consuming

app = Flask(__name__)

from system.infrastructure.adapters.database.models import *


@app.route('/')
def hello():
    return '<h1>Hello, Munds!</h1>'

# Start the consumer thread
def start_consumer_thread(app):
    consumer_thread = threading.Thread(target=start_consuming, args=(app,))
    consumer_thread.daemon = True  # Ensures the thread will exit when the main program exits
    consumer_thread.start()

# Start the consumer thread
with app.app_context():
    start_consumer_thread(app)

if __name__ == '__main__':
    app.run()

#Importing views
from system.adapters_entrypoints.api.routes import payment_views, general_view
