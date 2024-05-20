# tests/features/environment.py

from app import app

def before_all(context):
    context.client = app.test_client()
    app.config['TESTING'] = True