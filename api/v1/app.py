#!/usr/bin/python3
""" app api """
from flask import Flask, jsonify, Blueprint, make_response
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """call to close() method """
    storage.close()


@app.errorhandler(404)
def erro_404(error):
    """ Err 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
