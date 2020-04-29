#!/usr/bin/python3
<<<<<<< HEAD
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
=======
""" Module Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

>>>>>>> 53b4c3511c83a85299b5ec04fd6ab247850ea70b
from api.v1.views.index import *
