from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import os
from dotenv import load_dotenv

from .resources import APIStatus, KMeans

dotenv_path = os.path.join(os.getcwd(), '.env.local')
load_dotenv(dotenv_path)

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api.add_resource(APIStatus, '/api')
api.add_resource(KMeans, '/api/execute/kmeans')

if __name__ == '__main__':
    app.run(debug=True)
