import os
import json

from flask import Response, request

def api_key_required(func):

    def decorator(*args, **kwargs):

        api_key = request.headers.get('x-api-key')

        if not api_key:
            return Response(json.dumps({'message': 'Missing header [x-api-key]'}), status=401, mimetype='application/json')

        if api_key != os.environ['VUE_APP_API_KEY']:
            return Response(json.dumps({'message': 'Invalid api key'}), status=401, mimetype='application/json')

        return func(*args, **kwargs)
    return decorator
