import colorsys
import os
import time
from contextlib import ContextDecorator
from typing import List, Tuple, Union, Optional

import matplotlib.colors as mc
import numpy as np
import xarray as xr
from cartopy import util as cutil
from matplotlib.figure import Figure

Color = Tuple[float, float, float]
IMAGE_DIR = os.getenv("SAVED_FIG_DIR", default=".")


def set_image_dir(image_dir):
    global IMAGE_DIR
    IMAGE_DIR = image_dir


def cyclitize(dataset: xr.DataArray) -> xr.DataArray:
    """
    Take a dataarray and add cyclic longitude points for easy plotting. Return
    a new dataarray to make life easier for everyone.
    """
    cyclic_data, cyclic_lon = cutil.add_cyclic_point(dataset, coord=dataset.lon)
    new_dataset = xr.DataArray(
        cyclic_data,
        coords={
            **dataset.coords,
            "lon": cyclic_lon,
        },
        dims=dataset.dims,
        attrs=dataset.attrs,
        name=dataset.name,
    )
    return new_dataset


def to_lower_snake_case(*args: List[str]) -> str:
    """
    Convenience function for converting one or more strings to lower snake case. Useful
    for creating filenames.
    """
    return "_".join([input_str.lower().replace(" ", "_") for input_str in args])


def get_max_colormap_value(data: xr.DataArray) -> float:
    """
    Get the maximum absolute value from a dataset. Useful for setting the vmax and vmin
    values when creating a colormap for plotting in matplotlib.
    """
    return max(np.abs(np.max(data)), np.abs(np.min(data)))


def adjust_lightness(color: Union[Color, str], amount: float = 1.5) -> Color:
    """
    Change the lightness of the provided color. The second optional color determines
    how much to lighten the color. The higher the value, the lighter it will be.

    Adapted from: https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib/49601444
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def savefig(
    fig: Figure, filename: str, dpi: int = 100, version: Optional[int] = None
) -> None:
    """
    Save a figure to a specified directory and version it to ensure that it doesn't overwrite any
    previously saved figures.
    """
    figure_path = os.path.join(
        IMAGE_DIR, f"{filename}-v{str(version or 1).zfill(3)}.png"
    )
    if version is None:
        version = 1
        while os.path.exists(figure_path):
            version += 1
            if version > 100:
                raise Exception(
                    f"To many files named {filename} in directory, tried up to version {version}"
                )
            figure_path = os.path.join(
                IMAGE_DIR, f"{filename}-v{str(version or 1).zfill(3)}.png"
            )
    fig.savefig(figure_path, dpi=dpi)


class timer(ContextDecorator):
    """
    Use as an annotation to wrap a function and create a timer for that function
    to measure wall clock timing. Can also be used as a contextmanager:

    with timer(name="potato"):
        time.sleep(2) # do stuff

    @timer(name="funcname")
    def test():
        time.sleep(3) # do stuff
    """

    def __init__(self, name="timer", format="s"):
        self.name = name
        self.format = format

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *exc):
        elapsed = time.time() - self.start

        if format == "ms":
            elapsed *= 1000

        print(f"{self.name} took {elapsed:.2f}{self.format}")
        return False