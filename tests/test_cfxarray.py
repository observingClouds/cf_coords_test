"""
Test cfxarray's capabilities to understand CF projection information.
"""

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import cf_xarray as cfxr  # noqa
import pytest

from dataset_creator import create_dataset, load_metadata
from dataset_handler import extract_grid_mapping_names

datasets = {
    f: create_dataset(load_metadata(f)) for f in glob.glob("dataset_definitions/*.json")
}


@pytest.mark.parametrize("dataset_name, dataset", datasets.items())
def test_detection_grid_mapping(dataset_name, dataset):
    """
    Test whether the CRS variables are automatically identified based
    on the grid_mapping attributes.
    """
    expected_projection_vars = set()
    for var in dataset.variables:
        if "grid_mapping" in dataset[var].attrs:
            gm = extract_grid_mapping_names(dataset[var].attrs["grid_mapping"])
            expected_projection_vars.update(set(gm))

    infered_projections_dict = dataset.cf.grid_mapping_names
    infered_projections_vars = set(
        proj for sublist in infered_projections_dict.values() for proj in sublist
    )
    assert (
        expected_projection_vars == infered_projections_vars
    ), f"Expected {expected_projection_vars} but got {infered_projections_vars}"
