from flask import Flask

app = Flask(__name__)

from system.infrastructure.adapters.database.models import *


@app.route('/')
def hello():
    return '<h1>Hello, Munds!</h1>'

if __name__ == '__main__':
    app.run()

#Importing views
from system.adapters_entrypoints.api.routes import payment_views, general_view
