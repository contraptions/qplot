"""
Created on 18/09/2020
@author bvs
"""

import json

def load_json(path):
    """
    a function to load a json
    @param path: the path of the json to load
    @return: the json as a dict
    """
    with open(path) as f:
        return json.load(f)
