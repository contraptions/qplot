"""
Created on 19/09/2021
@author barnaby
"""

from .PlotterBase import PlotterBase
from ..helper_functions import load_json


class PlotterRead(PlotterBase):
    def __init__(self, folder, mode="read"):
        meta_data = load_json(folder / "meta_data.json")
        assert "axis" in meta_data, "axis not present within metadata"
        axis = meta_data.pop("axis")

        super().__init__(folder=folder, axis=axis, mode=mode)

        for key, value in meta_data.items():
            self.__setattr__(key, value)
