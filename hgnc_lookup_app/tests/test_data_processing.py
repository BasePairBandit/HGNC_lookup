import pytest
from hgnc_lookup_app.services.data_loader import DATA_FILE, load_dataset


def test_data_file_exists():
    assert DATA_FILE.exists

def test_load_dataset():
    result = load_dataset()
    assert result is not None
    assert isinstance(result, list)
    assert len(result)>0
