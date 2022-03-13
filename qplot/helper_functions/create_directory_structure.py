"""
Created on 15/09/2020
@author bvs
"""

import os
from pathlib import Path

def create_directory(folder_path):
    """
    a function to create a directory and folder path
    @param folder_path: where to create the directory
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def create_directory_structure(path):
    """
    a function to create the directory structure. Such that if you call it to create ./a/b/c. And ./a/ does not exist
    it will create it
    @param path:
    """
    for path_parent in reversed(Path(path).parents):
        create_directory(path_parent)
    create_directory(path)
