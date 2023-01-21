from flask import Flask, jsonify, Response, request
from flask_restful import Resource, Api

import numpy as np
import json

from cwaft.algorithms import kmeans

from .util.json import NpEncoder
from .shared import auth

# from sklearn import cluster
# from sklearn_extra.cluster import KMedoids

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env.local')
load_dotenv(dotenv_path)

app = Flask(__name__)
api = Api(app)

class KMeans(Resource):

    @auth.api_key_required
    def post(self):

        data = request.get_json(silent=True)

        if not data:
            return Response(json.dumps({ 'message': 'Missing or incorrect payload' }), status=400, mimetype='application/json')

        try:

            X = np.array([(point['x'], point['y']) for point in data['points']])
            model = kmeans.KMeans()
            model.fit(X)
            result = {
                "centeroids": [dict(x=x, y=y, id=id) for id, [x, y] in enumerate(model.centeroids)],
                "points": [dict(x=x, y=y, centeroid_id=label) for [x, y, label] in np.column_stack([X, model.labels])]
            }
            response = Response(json.dumps(result, cls=NpEncoder), mimetype='application/json')

        except KeyError as e:

            response = Response(json.dumps({ 'message': f"Invalid data in payload: {str(e)}" }), status=500, mimetype='application/json')
        
        return response
    
api.add_resource(KMeans, '/api/execute/kmeans')

if __name__ == '__main__':
    app.run(debug=True)
