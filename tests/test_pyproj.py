"""
Test xarray's capabilities to understand CF projection information.
"""

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pyproj
import pytest

from dataset_creator import create_dataset, load_metadata
from dataset_handler import extract_grid_mapping_names

datasets = [
    create_dataset(load_metadata(f)) for f in glob.glob("dataset_definitions/*.json")
]


@pytest.mark.parametrize("dataset", datasets)
def test_from_cf(dataset):
    """
    Test the pasting of each projection that is referenced by at least one variable.
    """
    projections = set()
    for var in dataset.variables:
        if "grid_mapping" in dataset[var].attrs:
            gm = extract_grid_mapping_names(dataset[var].attrs["grid_mapping"])
            projections.update(set(gm))

    for proj in projections:
        pyproj.CRS.from_cf(dataset[proj].attrs)


@pytest.mark.parametrize("dataset", datasets)
def test_from_wkt(dataset):
    """
    Test the pasting of each projection that is referenced by at least one variable.
    """
    projections = set()
    for var in dataset.variables:
        if "grid_mapping" in dataset[var].attrs:
            gm = extract_grid_mapping_names(dataset[var].attrs["grid_mapping"])
            projections.update(set(gm))

    for proj in projections:
        if "crs_wkt" in dataset[proj].attrs:
            pyproj.CRS.from_wkt(dataset[proj].attrs["crs_wkt"])


@pytest.mark.parametrize("dataset", datasets)
def test_roundtrip_cf(dataset):
    """
    Test if projection can be created from CF attributes and then converted back to CF attributes.
    """
    projections = set()
    for var in dataset.variables:
        if "grid_mapping" in dataset[var].attrs:
            gm = extract_grid_mapping_names(dataset[var].attrs["grid_mapping"])
            projections.update(set(gm))

    for proj in projections:
        crs = pyproj.CRS.from_cf(dataset[proj].attrs)
        attrs_orig = dataset[proj].attrs
        attrs_gen = crs.to_cf()
        assert (
            attrs_orig == attrs_gen
        ), f"Attributes missmatch! \n\nNew:\n {attrs_gen} \n\nold:\n{attrs_orig}"
