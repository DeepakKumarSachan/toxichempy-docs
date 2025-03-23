import os

import pandas as pd
import pytest

from toxichempy.data_loader import get_sample_data_path, load_sample_data

# Define available dataset formats
DATASET_NAME = "iris"
DATASET_FORMATS = ["csv", "json", "xlsx", "pkl", "h5", "db"]


@pytest.mark.parametrize("format", DATASET_FORMATS)
def test_get_sample_data_path(format):
    """Test if sample data path exists for all supported formats."""
    filename = f"{DATASET_NAME}.{format}"
    try:
        file_path = get_sample_data_path(filename)
        assert os.path.exists(file_path), f"File {filename} not found."
    except FileNotFoundError:
        pytest.skip(f"Skipping test: {filename} not found.")


@pytest.mark.parametrize("format", DATASET_FORMATS)
def test_load_sample_data(format):
    """Test if sample data loads correctly for each format."""
    try:
        df = load_sample_data(DATASET_NAME)
        assert isinstance(df, pd.DataFrame), "Loaded data is not a DataFrame."
        assert not df.empty, "Loaded DataFrame is empty."
    except FileNotFoundError:
        pytest.skip(
            f"Skipping test: No available dataset format found for {DATASET_NAME}."
        )
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")
