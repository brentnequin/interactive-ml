from flask import Flask, jsonify, Response, request
from flask_restful import Resource, Api

import numpy as np
import json

from sklearn import cluster
# from sklearn_extra.cluster import KMedoids

app = Flask(__name__)
api = Api(app)

class KMeans(Resource):
    def post(self):

        data = request.get_json(silent=True)

        if not data:
            return Response(json.dumps({ 'message': 'Missing or incorrect payload' }), status=400, mimetype='application/json')

        try:

            X = np.array([(point['x'], point['y']) for point in data['points']])
            kmeans = cluster.KMeans(n_clusters=data.get('k'), random_state=0, n_init="auto").fit(X)

            cluster_centers = [{ 'x': float(x), 'y': float(y), 'label': index} for index, (x, y) in enumerate(list(map(tuple, kmeans.cluster_centers_)))]
            points_labeled = [{ 'x': point['x'], 'y': point['y'], 'cluster_center': int(label) } for point, label in zip(data['points'], kmeans.labels_)]

            response_data = {
                'k': data['k'],
                'cluster_centers': cluster_centers,
                'points': points_labeled
            }

            response = Response(json.dumps(response_data), mimetype='application/json')

        except KeyError as e:

            response = Response(json.dumps({ 'message': f"Missing data in payload: {str(e)}" }), status=500, mimetype='application/json')
        
        return response
    
api.add_resource(KMeans, '/api/execute/kmeans')

if __name__ == '__main__':
    app.run(debug=True)
