import json

from flask import Flask, jsonify, Response, request
from flask_restful import Resource, Api


from jsonschema import validate, ValidationError
import numpy as np

from cwaft.algorithms import kmeans

from .util.json import NpEncoder
from .shared import auth

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env.local')
load_dotenv(dotenv_path)

app = Flask(__name__)
api = Api(app)

class JsonSchema:

    kmeans = {
        'type': 'object',
        'required': ['k', 'points'],
        'properties': {
            'k': {
                'type': 'integer'
            },
            'points': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'required': ['x', 'y'],
                    'properties': {
                        'x': {
                            'type': 'number'
                        },
                        'y': {
                            'type': 'number'
                        }
                    }
                }
            }
        }
    }


class KMeans(Resource):

    @auth.api_key_required
    def post(self):

        data = request.get_json(silent=True)

        try:
            validate(instance=data, schema=JsonSchema.kmeans)
        except ValidationError as e:
            return Response(json.dumps({ 'message': e.message }), status=400, mimetype='application/json')
        except Exception as e:
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

        except Exception as e:
            response = Response(json.dumps({ 'message': f"Something went wrong: {str(e)}" }), status=500, mimetype='application/json')
        
        return response
    
api.add_resource(KMeans, '/api/execute/kmeans')

if __name__ == '__main__':
    app.run(debug=True)
