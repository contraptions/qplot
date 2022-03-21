"""
Created on 11/03/2022
@author jdh
"""


from .PlotWindows.PlotterWrite import PlotterWrite
from .Dataclass import qplot_variable

import numpy as np

class TwoDLive:

    def __init__(self, folder):
        self.folder = folder

        self._plot_axes = ['x', 'y', 'z']

    def set_axes(self, x_data, y_data):
        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)

        self.z_data = np.full(shape=(x_data.size, y_data.size), fill_value=np.nan)

        self.make_plotter()

    def data(self, data):

        self.plotter.mm_w.z[...] = data

    def make_plotter(self):

        self.variables= [
            qplot_variable(
            name=variable,
            unit='',
            data=data
            )
        for variable, data in zip(self._plot_axes, [self.x_data, self.y_data, self.z_data])
        ]

        self.plotter = PlotterWrite(
            folder=self.folder,
            variables=self.variables,
            axis=[self._plot_axes],
            set_variable_names=['x', 'y']
        )

        self.plotter.plot()














