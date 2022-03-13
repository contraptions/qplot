"""
Created on 19/09/2021
@author barnaby
@author jdh
"""

from .PlotterBase import PlotterBase
from qplot.MemoryMaps import MemoryMapWrite
from qplot.helper_functions import check_list_in_list_of_lists
import numpy as np
from qplot.Dataclass import qplot_variable

class PlotterWrite(PlotterBase):
    def __init__(self, folder, variables, axis, set_variable_names, processors=[]):

        self.variables = variables

        self.data_shape = self.variables[-1].get('data').shape

        # set variable names are needed for the processors
        self.set_variable_names = set_variable_names

        self.axis = axis
        self.processors = processors

        if processors:
            self.set_up_processors()

        self.mm_w = MemoryMapWrite(folder=folder, variables=self.variables)
        super().__init__(folder=folder, axis=self.axis)

        if processors:
            self.process_data()

        super().save()


    def process_data(self):

        for processor in self.processors:
            mm = self.mm_w.__getattribute__(
                processor.name
            )

            mm[...] = processor(*[self.mm_r.__getattribute__(
                variable
            ) for variable in processor.variables])[...]

    def set_up_processors(self):

        # set up a variable
        processed_variables = [
            qplot_variable(
                name=processor.name,
                unit=processor.unit,
                data=np.full(shape=self.data_shape, fill_value=np.nan)
            )
            for processor in self.processors
        ]

        processed_axis = [
            (*self.set_variable_names, processor.name)
            for processor in self.processors
        ]

        variable_keys = [var.get('name') for var in self.variables]
        for variable in processed_variables:
            if variable.get('name') not in variable_keys:
                self.variables.append(variable)


        for axis in processed_axis:
            if not check_list_in_list_of_lists(list(axis), self.axis):
                self.axis += [axis]
