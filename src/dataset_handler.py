"""
Helper functions to extract projections from datasets
"""


def extract_grid_mapping_names(grid_mapping_attr):
    """
    Extract grid mapping names from the grid_mapping attribute.

    Parameters
    ----------
    grid_mapping_attr : str
        The grid_mapping attribute.

    Returns
    -------
    list
        List of grid mapping names.

    Examples
    --------
    >>> m1 = "crsOSGB: x y crsWGS84: lat lon"
    >>> extract_grid_mapping_names(m1)
    ['crsOSGB', 'crsWGS84']
    >>> m2 = "crsOSGB"
    >>> extract_grid_mapping_names(m2)
    ['crsOSGB']
    """
    if ":" not in grid_mapping_attr:
        return grid_mapping_attr.split(" ")
    else:
        return [
            key.split(":")[0].strip()
            for key in grid_mapping_attr.split(" ")
            if ":" in key
        ]
