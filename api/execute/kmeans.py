from ..index import app, api, request

class KMeans(Resource):
    def post(self, ):
        body = request.json
        
        print(body)
        
        return None # response
    
api.add_resource(KMeans, '/api/execute/kmeans')
