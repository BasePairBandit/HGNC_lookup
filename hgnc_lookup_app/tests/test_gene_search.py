import pytest
from hgnc_lookup_app.services.gene_search import find_by_symbol, find_by_hgnc_id
from hgnc_lookup_app.services.data_loader import load_dataset

def test_find_by_symbol_normal_case():

    result = find_by_symbol("APOE")

    assert result is not None
    assert result["gene_symbol"]=="APOE"

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
