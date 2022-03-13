"""
Created on 18/09/2020
@author bvs
"""

import json
from .load_json import load_json

def save_json(path, dict):
    """
    a function to load a json
    @param path: the path of the json to load
    @return: the json as a dict
    """
    # if the file already exists, load it and add to the dict to be saved
    if path.is_file():
        dict = {**load_json(path=path), **dict}

    with open(path, "w") as f:
        json.dump(dict, f, indent=4, sort_keys=False)
