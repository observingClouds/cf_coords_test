"""
Test xarray's capabilities to understand CF projection information.
"""

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pytest

from dataset_creator import create_dataset, load_metadata

datasets = [
    create_dataset(load_metadata(f)) for f in glob.glob("dataset_definitions/*.json")
]


@pytest.mark.parametrize("dataset", datasets)
def test_coords_from_ds(dataset):
    """
    Test whether the CRS matching the variable can be retrieved automatically
    without knowing the grid_mapping variable name.
    """
    variables_w_crs = [
        var for var in dataset.variables if "grid_mapping" in dataset[var].attrs
    ]

    ds_crs = dataset.metpy.parse_cf()
    for var in variables_w_crs:
        assert ds_crs[var].metpy.cartopy_crs is not None
        assert ds_crs[var].metpy.pyproj_crs is not None
