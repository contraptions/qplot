"""
Created on 15/09/2021
@author barnaby, jdh
"""

import numpy as np
from pprint import pformat
import logging

from ..helper_functions import create_directory_structure


logger = logging.getLogger(__name__)

class MemoryMapWrite:
    """
    A class to write a list of arrays to a folder as memory maps. The name, associated units and shape of the arrays
    are encode in the file_name.
    """

    def __init__(self, folder, variables):
        self.folder = folder

        # checking if the folder exists
        if not self.folder.is_dir():
            # creating the directories necessary to save to folder
            create_directory_structure(self.folder)
        else:
            logger.warning(
                "writing data to folder already exists, it is possible that the wrong data is loaded - {}".format(
                    self.folder.resolve()
                )
            )

        # asserting to avoid indecipherable errors later
        for variable in variables:

            # not sure if this is necessary because the variable dataclass has to have these or will
            # error on init
            #
            # assert hasattr(variable, "name"), "variable must have attribute name"
            # assert hasattr(variable, "unit"), "variable must have attribute unit"
            # assert hasattr(variable, "data"), "variable must have attribute data"

            assert isinstance(variable.get('data'), np.ndarray)

            # constructing the file name
            file_name = "./{}-{}-{}-{}.dat".format(
                variable.get("name"),
                variable.get("unit"),
                variable.get("data").dtype.name,
                variable.get("data").shape,
            )

            data = variable.get("data")

            memory_map = np.memmap(
                self.folder / file_name, dtype=data.dtype, shape=data.shape, mode="w+"
            )
            # assigning all values in the memmap to the values in the arrays passed
            memory_map[...] = data[...]

            self.__setattr__(variable.get("name"), memory_map)

    def __repr__(self):
        return pformat(self.__dict__)

    def get(self, name):
        assert hasattr(self, name), "this memory map has no attribute {}".format(name)
        return self.__getattribute__(name)

