#!/usr/bin/python3
<<<<<<< HEAD
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
=======
""" Modules """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
@app.teardown_appcontext
def teardown_appcontext(error):
    """
        Close Error
    """
    storage.close()


if __name__ == "__main__":
    host_d = environ.get('HBNB_API_HOST')
    port_d = environ.get('HBNB_API_PORT')
    if (not host_d):
        host_d = '0.0.0.0'

    if (not port_d):
        port_d = '5000'
    app.run(host=host_d, port=port_d, threaded=True)
>>>>>>> 53b4c3511c83a85299b5ec04fd6ab247850ea70b
