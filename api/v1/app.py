#!/usr/bin/python3
""" app api """
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(self):
    """call to close() method """
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
