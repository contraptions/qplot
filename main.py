"""
Created on 11/03/2022
@author jdh
"""

from qplot import PlotterWrite


folder = './example_data_dir'

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