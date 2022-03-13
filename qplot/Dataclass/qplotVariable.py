"""
Created on 22/11/2021
@author jdh
"""

from dataclasses import dataclass
import numpy as np

@dataclass
class qplot_variable:
    """
    variables have a name, unit and data associated with them
    """
    name: str
    unit: str
    data: np.ndarray

    # this class replaces dictionaries for storing data. The .get() method provides backwards compatibility.
    def get(self, attribute):
        return self.__getattribute__(attribute)

    def data_shape(self):
        return self.data.shape
