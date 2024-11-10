"""
Test xarray's capabilities to understand CF projection information.
"""

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pytest
import xarray as xr

from dataset_creator import create_dataset, load_metadata
from dataset_handler import extract_grid_mapping_names

datasets = {
    f: create_dataset(load_metadata(f)) for f in glob.glob("dataset_definitions/*.json")
}


@pytest.mark.parametrize("dataset_name, dataset", datasets.items())
def test_coords_from_ds(dataset_name, dataset, tmp_path):
    """
    Test whether the CRS matching the variable can be retrieved automatically
    without knowing the grid_mapping variable name.

    See also:
    https://github.com/pydata/xarray/issues/9761
    """
    projections = set()
    for var in dataset.variables:
        if "grid_mapping" in dataset[var].attrs:
            gm = extract_grid_mapping_names(dataset[var].attrs["grid_mapping"])
            projections.update(set(gm))

    fn = "test_dataset.nc"
    dataset.to_netcdf(tmp_path / fn)
    ds_reopen = xr.open_dataset(tmp_path / fn, decode_coords="all")

    for projection in projections:
        assert (
            projection in ds_reopen.coords
        ), f"Projection {projection} not found in reopened dataset coordinates"
