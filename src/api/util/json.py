import json
import numpy as np

def read_json_file(path: str) -> dict:

    with open(path) as file:
        data = json.load(file)

    return data


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

if __name__ == "__main__":

    import os

    print(os.getcwd())

    schema = read_json_file('api/schema/kmeans.json')
    print('.')