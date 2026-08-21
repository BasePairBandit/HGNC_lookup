import pytest
from hgnc_lookup_app.services.gene_search import find_by_symbol, find_by_hgnc_id, validate_search_query, UserInputError
from hgnc_lookup_app.services.data_loader import load_dataset


def test_validate_search_query_normal_case():
    result = validate_search_query("APOE")
    assert result is not None
    assert result[0:4]=="APOE"

def test_validate_search_query_invalid_character(caplog):

    with pytest.raises(UserInputError):
        validate_search_query("APO/")
    assert "User entered invalid input: APO/" in caplog.text

def test_validate_search_query_empty(caplog):

    with pytest.raises(UserInputError):
        validate_search_query("")
    assert "Empty user input" in caplog.text


def test_find_by_symbol_normal_case():

    result = find_by_symbol("APOE")

    assert result is not None
    assert result["gene_symbol"]=="APOE"

def test_find_by_symbol_non_existent_symbol():

    result = find_by_symbol("AAAA")

    assert result is None

def test_find_by_symbol_valid_hyphen():

    result = find_by_symbol("A1BG-AS1")

    assert result is not None
    assert result["gene_symbol"]=="A1BG-AS1"

def test_find_by_symbol_case_insensitive():

    result = find_by_symbol("apoe")

    assert result is not None
    assert result["gene_symbol"] == "APOE"

def test_find_by_symbol_space():

    result = find_by_symbol("ap oe")

    assert result is not None
    assert result["gene_symbol"] == "APOE"

def test_find_by_symbol_not_found():
    result = find_by_symbol("APO")

    assert result is None

def test_find_by_hgnc_id_normal_case():

    result = find_by_hgnc_id("HGNC:613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_case_insensitive():

    result = find_by_hgnc_id("hgnc:613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_space():

    result = find_by_hgnc_id("HGNC :613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_mixed_case():

    result = find_by_hgnc_id("HGnC :613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_non_existent_id():

    result = find_by_hgnc_id("HGnC :000")

    assert result is None
