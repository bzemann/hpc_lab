#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


def read_bov_header(fname):
    """Read VisIt BOV file header."""
    with open(fname, "r") as f:
        header = f.readlines()
    time = float(header[0].split()[1])
    data_file = header[1].split()[1]
    data_size = [int(i) for i in header[2].split()[1:]]
    data_format = header[3].split()[1]
    var_names = header[4].split()[1:]
    data_endian = header[5].split()[1]
    centering = header[6].split()[1]
    brick_origin = [float(i) for i in header[7].split()[1:]]
    brick_size = [float(i) for i in header[8].split()[1:]]
    return time, data_file, data_size, data_format, var_names, data_endian, \
           centering, brick_origin, brick_size


def read_bov_data(header):
    """Read VisIt BOV file data."""
    if header[3].lower() == "float":
        dtype = np.float32
    elif header[3].lower() == "double":
        dtype = np.float64
    else:
        raise ValueError(f"Unknown data format: {header[3]}")
    data = np.fromfile(header[1], dtype=dtype)
    data = data.reshape(header[2])
    return data


def plot_data(fname, save=True):
    """Plot data from VisIt BOV file."""
    header = read_bov_header(fname)
    time = header[0]
    res = header[2]
    brick_origin = header[7]
    brick_size = header[8]
    x = np.linspace(brick_origin[0], brick_origin[0] + brick_size[0], res[0])
    y = np.linspace(brick_origin[1], brick_origin[1] + brick_size[1], res[1])
    [X, Y] = np.meshgrid(x, y)
    data = read_bov_data(header)
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_title(f"Time: {time}")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    C = ax.pcolor(X, Y, data[:, :, 0], cmap="jet")
    cbar = fig.colorbar(C, ax=ax)
    cbar.minorticks_on()
    if save:
        fname = fname.split(".")
        fname[-1] = "png"
        plt.savefig(".".join(fname), dpi=300, bbox_inches='tight')
    else:
        plt.show()


if __name__ == "__main__":
    plot_data("output.bov", save=True)
