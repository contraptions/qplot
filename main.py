"""
Created on 11/03/2022
@author jdh
"""


from pathlib import Path

import numpy as np
from qplot import PlotterWrite
from qplot import qplot_variable


w, h = 64, 64
folder = Path('./example_data_dir')

_plot_axes = ['x', 'y', 'z']

x_data = np.linspace(0, 10, w)
y_data = np.linspace(0, 10, h)

z_data = np.full(shape=(x_data.size, y_data.size), fill_value=np.nan)

variables = [
    qplot_variable(
        name=variable,
        unit='',
        data=data
    )
    for variable, data in zip(_plot_axes, [x_data, y_data, z_data])
]

plotter = PlotterWrite(
    folder=folder,
    variables=variables,
    axis=[_plot_axes],
    set_variable_names=['x', 'y']

)

plotter.plot()

from qplot import TwoDLive

# w, h = 64, 64
#
# plot = TwoDLive(folder=folder)
# plot.set_axes(
#     x_data=np.linspace(0, 10, w),
#     y_data=np.linspace(0, 10, h)
# )

# while True:
#     plot.data(np.random.rand(w, h))
#
#




"""
plot = qplot.2d_live_plot(folder=folder) 

plot.axes(
    x_data=np.linspace(0, 10, 100), 
    y_data=np.linspace(0, 10, 100)
)

while True: 
    plot.data(np.random.rand(100, 100))
    
"""

"""
Want the syntax to look something like above. If y_data is not given then the plot can be assumed to be
1d and then plot.data() plots a 1d plot. 

Get rid of the variables - this is useful for qgor but maybe not useful here? 
"""