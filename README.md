# Test handling of CF convention projection information

This repo is for test purposes only.

- folder `dataset_defintions` contains dataset definitions based on dataset examples given in the [CF conventions documentation](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html#coordinate-system).
- folder `src` contains code to create xarray datasets from the dataset definitions by using random data.
- folder `tests` contains tests to check if the coordinate and projection information given in those datasets can be read by different libraries (e.g. xarray, pyproj, metpy)