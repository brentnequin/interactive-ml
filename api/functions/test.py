import json

def handler(request, context):
    return json.dumps({'message': 'success'})
    

if __name__ == '__main__':
    handler({}, {})
