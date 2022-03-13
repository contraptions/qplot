"""
Created on 15/09/2021
@author barnaby
"""
import numpy as np
from pprint import pformat
from pathlib import Path


def open_memmap(file_path: Path, mode="r"):
    """
    A function to open a memory map, while also parsing its name to retrieve the name, units, data_type and array shape.
    @param file_path: pathlib path to the folder.
    @param mode: the mode with which to open the memmap.
    @return: name, unit, memmap.
    """
    name, unit, data_type, shape_string = file_path.stem.split("-", 3)
    # clipping the brackets off
    shape_string = shape_string[1:-1]

    # parsing the shape string
    shape = tuple(shape_string.split(",", shape_string.count(",")))
    shape = tuple(filter(lambda x: x != "", shape))
    shape = tuple(int(i) for i in shape)

    # loading the memmaps
    memmap = np.memmap(filename=file_path, dtype=data_type, mode=mode, shape=shape)

    return name, unit, memmap


class MemoryMapRead:
    """
    A load all of the memmaps in a particular folder the assign them to class attributes.
    """

    def __init__(self, folder: [Path, str], mode: str = "read"):
        folder = folder if isinstance(folder, Path) else Path(folder)

        self.folder = folder
        self.units = {}

        assert mode in ["read", "copy"], "invalid mode {}".format(mode)

        for file in folder.glob("*.dat"):
            if "modified" not in file.name:
                name, unit, memmap = open_memmap(file_path=file)

                if mode == "read":
                    self.__setattr__(name, memmap)
                if mode == "copy":
                    file = file.parent / "modified_{}".format(file.name)

                    memmap_copy = np.memmap(
                        file, dtype=memmap.dtype, shape=memmap.shape, mode="w+"
                    )
                    memmap_copy[...] = memmap[...]
                    self.__setattr__(name, memmap_copy)

                self.units.__setitem__(name, unit)

    def __repr__(self):
        return pformat(self.__dict__)

    def get(self, name):
        assert hasattr(self, name), "this memory map has no attribute {}".format(name)
        return self.__getattribute__(name)
