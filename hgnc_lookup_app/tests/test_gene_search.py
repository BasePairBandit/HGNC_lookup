import pytest
from hgnc_lookup_app.services.gene_search import find_by_symbol, find_by_hgnc_id, validate_search_query, UserInputError
from hgnc_lookup_app.services.data_loader import load_dataset

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                    # Testing validation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def test_validate_search_query_normal_case():
    """
    Testing that a normal entry is passing validation
    """
    result = validate_search_query("APOE")
    assert result is not None
    assert result[0:4]=="APOE"

def test_validate_search_query_invalid_character(caplog):
    """
    Tesing that an invalid character is flagged, raises error and logs it.
    """
    with pytest.raises(UserInputError):
        validate_search_query("APO/")
    assert "User entered invalid input: APO/" in caplog.text

def test_validate_search_query_empty(caplog):
    """
    Tesing that an empty entry is logged.
    """
    with pytest.raises(UserInputError):
        validate_search_query("")
    assert "Empty user input" in caplog.text

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                    # Testing find_by_symbol()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def test_find_by_symbol_normal_case():
    """
    Tesing that it can find by gene symbol.
    """
    result = find_by_symbol("APOE")

    assert result is not None
    assert result["gene_symbol"]=="APOE"

def test_find_by_symbol_non_existent_symbol():
    """
    Tesing that it returns no result if gene symbol is not real.
    """
    result = find_by_symbol("AAAA")

    assert result is None

def test_find_by_symbol_valid_hyphen():
    """
    Tesing that it allows hyphens (-) in gene symbol as some genes have it.
    """
    result = find_by_symbol("A1BG-AS1")

    assert result is not None
    assert result["gene_symbol"]=="A1BG-AS1"

def test_find_by_symbol_case_insensitive():
    """
    Tesing that it works with upper and lower case gene symbols.
    """
    result = find_by_symbol("apoe")

    assert result is not None
    assert result["gene_symbol"] == "APOE"

def test_find_by_symbol_space():
    """
    Tesing that it can get rid of white spaces and still find the gene.
    """
    result = find_by_symbol("ap oe")

    assert result is not None
    assert result["gene_symbol"] == "APOE"

def test_find_by_symbol_leading_space():
    """
    Tesing that it can get rid of leading spaces and still find the gene.
    """
    result = find_by_symbol(" APOE")

    assert result is not None
    assert result["gene_symbol"] == "APOE"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                    # Testing find_by_hgnc_id
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def test_find_by_hgnc_id_normal_case():
    """
    Tesing that it can find by hgnc_id.
    """
    result = find_by_hgnc_id("HGNC:613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_case_insensitive():
    """
    Tesing that it can work with upper and lowercase hgnc_ids.
    """
    result = find_by_hgnc_id("hgnc:613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_space():
    """
    Tesing that it can get rid of whitespaces and still find the gene.
    """
    result = find_by_hgnc_id("HGNC :613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_mixed_case():
    """
    Tesing that it can find even when upper and lower cases are mixed.
    """
    result = find_by_hgnc_id("HGnC :613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"

def test_find_by_hgnc_id_non_existent_id():
    """
    Tesing that it returns none with non-existent hgnc_ids.
    """
    result = find_by_hgnc_id("HGnC :000")

    assert result is None

def test_find_by_hgnc_id_leading_space():
    """
    Tesing that it can get rid of leading spaces and still find the gene.
    """
    result = find_by_hgnc_id(" HGNC:613")

    assert result is not None
    assert result["hgnc_id"]=="HGNC:613"