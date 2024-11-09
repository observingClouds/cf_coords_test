"""
Create pseudo dataset based on provided metadata.
"""

import json

import numpy as np
import xarray as xr


def load_metadata(metadata_file):
    """
    Load metadata from JSON file.
    """
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    return metadata


def create_dataset(metadata):
    """
    Create dataset based on metadata.
    """
    ds = xr.Dataset()

    # Dimensions
    dimensions = metadata["dimensions"]

    # Variables
    variables = metadata["variables"]
    for var, meta in variables.items():
        dims = meta.get("dimensions", [])
        attrs = meta.get("attributes", {})
        if len(dims) == 0:
            data = 0
        else:
            data = np.random.rand(*[dimensions[d] for d in dims])
        ds[var] = xr.DataArray(data, dims=dims, attrs=attrs)

    return ds
