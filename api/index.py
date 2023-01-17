from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
import numpy as np

app = Flask(__name__)
api = Api(app)

class KMeans(Resource):
    def post(self, ):
        body = request.json
        
        print(body)
        
        return None # response
    
api.add_resource(KMeans, '/api/execute/kmeans')

if __name__ == '__main__':
    app.run(debug=True)