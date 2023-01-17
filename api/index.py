from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
import numpy as np

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)