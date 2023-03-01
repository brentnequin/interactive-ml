import json

from flask import Response, request
from flask_restful import Resource
from flask_cors import cross_origin

from jsonschema import validate, ValidationError
import numpy as np

from cwaft.algorithms import kmeans

from .util.json import NpEncoder, read_json_file
from .shared import auth


class APIStatus(Resource):

    @auth.api_key_required
    def get(self):
        return Response(json.dumps({'message': 'ok'}), mimetype='application/json')


class KMeans(Resource):

    @auth.api_key_required
    @cross_origin()
    def post(self):

        data = request.get_json(silent=True)

        if not data:
            return Response(json.dumps({'message': 'Missing request body'}), status=400, mimetype='application/json')

        try:
            schema = read_json_file('src/api/schema/kmeans.json')
            validate(instance=data, schema=schema)
        except ValidationError as e:
            return Response(json.dumps({'message': e.message}), status=400, mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'message': f'Something went wrong: {str(e)}'}), status=400, mimetype='application/json')

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
            return Response(json.dumps({'message': f'Something went wrong: {str(e)}'}), status=500, mimetype='application/json')
        
        return response
