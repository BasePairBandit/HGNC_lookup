import pytest
from hgnc_lookup_app.services.data_loader import DATA_FILE, load_dataset


def test_data_file_exists():
    """
    Testing if the file exists
    """
    assert DATA_FILE.exists

def test_load_dataset():
    """
    Testing that the dataset is not empty and is a list
    """
    result = load_dataset()
    assert result is not None
    assert isinstance(result, list)
    assert len(result)>0
