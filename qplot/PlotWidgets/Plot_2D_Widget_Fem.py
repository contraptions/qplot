"""
Created on 17/09/2021
@author barnaby
@author jdh
"""

import pyqtgraph as pg
import PyQt5
from PyQt5 import QtCore
from .Custom_Dock import Dock
from .colour_map import load_colour_map
import pyqtgraph.exporters
import logging
import numpy as np
from time import time

logger = logging.getLogger(__name__)


class Plot_2D_Widget_Fem:
    def __init__(
        self,
        x_mm,
        y_mm,
        z_mm,
        axis=None,
        colour_map: str = "hot",
        colour_map_downsampling: int = 10,
        closeable: bool = True,
        auto_range: bool = True,
        auto_level: bool = True,
        lock_aspect: bool = False,
        size: tuple = (500, 500),
        **kwargs
    ):

        if axis is None:
            axis = {
                "x": {"name": "x", "unit": ""},
                "y": {"name": "y", "unit": ""},
                "z": {"name": "z", "unit": ""},
            }

        self.x_axis = axis.get("x")
        self.y_axis = axis.get("y")
        self.z_axis = axis.get("z")

        self.dock = Dock(self.z_axis.get("name"), size=tuple(size), closable=closeable)

        self.x_mm, self.y_mm, self.z_mm = x_mm, y_mm, z_mm

        self.auto_range = auto_range
        self.auto_level = auto_level

        self.plot_area = pg.PlotItem()

        # make sure the aspect ratio of the plot area is not locked
        self.plot_area.setAspectLocked(lock=False)

        # set the PlotItem's axis labels
        self.plot_area.getAxis("bottom").setLabel(
            text=self.x_axis.get("name"), units=self.x_axis.get("unit")
        )
        self.plot_area.getAxis("left").setLabel(
            text=self.y_axis.get("name"), units=self.y_axis.get("unit")
        )

        # create the imageview object that displays the data inside the plotitem
        self.plot = pg.ImageView(view=self.plot_area)

        # plot so the y axis is the right way around
        self.plot.view.invertY(False)

        # Lock the aspect ratio of the image, set to False to have a dynamic ratio
        self.plot.view.setAspectLocked(lock_aspect)

        cmap = load_colour_map(colour_map, downsampling=colour_map_downsampling)
        self.plot.setColorMap(cmap)
        self.dock.addWidget(self.plot)

        # self.plot.imageItem.mousePressEvent = lambda event: self.imageHoverEvent(event)

        self.plot.imageItem.hoverEvent = lambda event: self.imageHoverEvent(event)
        self.plot.imageItem.mouseClickEvent = lambda event: self.mouseClickEvent(event)

        self.init_copies()

        self.click_location_list = []
        self.click_times = [0]

        # create an empty region of interest and add it to the plot area
        self.lineROI = pg.PolyLineROI(positions=[], closed=True)
        self.plot_area.addItem(self.lineROI)
        self.ROI_bool = False



    def init_copies(self):
        self.x = np.full_like(self.x_mm, fill_value=np.nan)
        self.y = np.full_like(self.y_mm, fill_value=np.nan)
        self.z = np.full_like(self.z_mm, fill_value=np.nan)

    def create_copies(self):
        # creating copies of the memory maps
        self.x = self.x_mm.__array__().copy()
        self.y = self.y_mm.__array__().copy()
        self.z = self.z_mm.__array__().copy()

    def imageHoverEvent(self, event):

        try:
            x = self.x_mm
            y = self.y_mm
            z = self.z_mm

            if x is not None and y is not None:
                if event.isExit():
                    self.dock.setTitle(self.z_axis.get("name"))
                    return

            pos = event.pos()
            i, j = pos.x(), pos.y()

            i = int(np.clip(i, 0, z.shape[0] - 1))
            j = int(np.clip(j, 0, z.shape[1] - 1))

            x = x[i]
            y = y[j]

            # prevents 'None' being set as the unit on the image
            x_unit = self.x_axis.get("unit")
            y_unit = self.y_axis.get("unit")

            x_unit = "" if x_unit is None else x_unit
            y_unit = "" if y_unit is None else y_unit

            self.dock.setTitle(
                "x,y = ({:0.3f}{}, {:0.3f}{})".format(
                    x,
                    x_unit,
                    y,
                    y_unit,
                )
            )
        except AttributeError as e:
            logger.debug(
                "Attribute error: hover event means nothing outside of view image"
            )

    def mouseClickEvent(self, event):

        x = self.x_mm
        y = self.y_mm
        z = self.z_mm
        pos = event.pos()
        i, j = pos.x(), pos.y()

        i = int(np.clip(i, 0, z.shape[0] - 1))
        j = int(np.clip(j, 0, z.shape[1] - 1))

        x = x[i]
        y = y[j]

        print(
            "{}: {:0.3f}\n{}: {:0.3f}\n".format(
                self.x_axis.get("name"), x, self.y_axis.get("name"), y
            )
        )

        self.click_location_list.append(
            {self.x_axis.get("name"): x, self.y_axis.get("name"): y}
        )

        # if the time between two clicks is less than 0.3, it is a double click.
        self.click_times.append(time())
        time_diff = self.click_times[-1] - self.click_times[-2]
        if time_diff < 0.3:
            self.on_double_click(x, y)
            self.ROI_bool = True

        return x, y

    def coords_dict(self):
        # creates a dictionary with all of the existing handle coordinates
        coords = {}
        # once a handle is moved it becomes a QPointF object, check typing of coordinate.
        for i in self.lineROI.getLocalHandlePositions():
            if isinstance(i[1], PyQt5.QtCore.QPointF) is True:
                coords[self.lineROI.getLocalHandlePositions().index(i)] = [i[1].x(), i[1].y()]
            else:
                coords[self.lineROI.getLocalHandlePositions().index(i)] = i[1]
        return coords

    def clear_handles(self):
        self.lineROI.setPoints(points=[])

    def on_double_click(self, x, y):

        # create an info dictionary for each handle
        info = {'name': None, 'type': 'f', 'pos': [x, y], 'item': None, 'lockAspect': False}
        self.lineROI.addHandle(info=info)

        # depending on the number of handles existing, a different number of segments will be added to connect handles.
        if self.lineROI.handles.__len__() > 3:
            self.lineROI.addSegment(self.lineROI.handles[-2]['item'], self.lineROI.handles[-1]['item'])
            self.lineROI.addSegment(self.lineROI.handles[-1]['item'], self.lineROI.handles[0]['item'])
            self.lineROI.removeSegment(self.lineROI.segments[-3])
        elif self.lineROI.handles.__len__() > 2:
            self.lineROI.addSegment(self.lineROI.handles[-2]['item'], self.lineROI.handles[-1]['item'])
            self.lineROI.addSegment(self.lineROI.handles[-1]['item'], self.lineROI.handles[0]['item'])
        elif self.lineROI.handles.__len__() > 1:
            self.lineROI.addSegment(self.lineROI.handles[-2]['item'], self.lineROI.handles[-1]['item'])
        else:
            pass

    def update(self):

        data_changed = False
        for mm, copy in zip(
            [self.x_mm, self.y_mm, self.z_mm], [self.x, self.y, self.z]
        ):
            if not np.array_equal(mm, copy):
                data_changed = True

        if data_changed and not np.all(np.isnan(self.z_mm)):
            # pos is the new location of the lower left corner of the plot
            pos = (np.min(self.x_mm), np.min(self.y_mm))

            # scale from pixel index values to x/y values
            scale = (
                np.max(self.x_mm) - np.min(self.x_mm),
                np.max(self.y_mm) - np.min(self.y_mm),
            ) / np.array(self.z_mm.shape)

            self.plot.setImage(
                self.z_mm,
                autoRange=False,
                autoLevels=self.auto_level,
                pos=pos,
                scale=scale,
            )

            # creating copies of the memory maps
            self.create_copies()
