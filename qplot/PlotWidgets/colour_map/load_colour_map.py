"""
Created on 17/09/2021
@author barnaby
"""

import numpy as np
from matplotlib import cm
from .colour_maps import colour_maps
from pyqtgraph import ColorMap


def load_colour_map(name, downsampling):

    if name in colour_maps.keys():
        colours = colour_maps.get(name)
        colours = 255 * colours[::downsampling]
    else:
        colormap = cm.get_cmap(name)
        colormap._init()
        # Convert matplotlib colormap from 0-1 to 0-255 for PyQtGraph
        colours = (colormap._lut * 255).view(np.ndarray)[: colormap.N]
        colours = colours[::downsampling]

    pos = np.linspace(0, 1, colours.shape[0])
    return ColorMap(pos=pos, color=colours)
