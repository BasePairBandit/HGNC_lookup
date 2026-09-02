
from django.urls import reverse


def test_search_page_loads(client):
    """
    Tests that the search URL:
    - returns HTTP 200
    - Renders search template
    """
    response = client.get(reverse("search"))

    assert response.status_code == 200
    assert "hgnc_lookup_app/search.html" in [
        template.name
        for template in response.templates
    ]


def test_valid_symbol_search(client):
    """
    Tests a valid gene symbol works
    """
    response = client.get(
        reverse("search"),
        {"query": "APOE"},
    )

    assert response.status_code == 200
    assert response.context["gene"]["gene_symbol"]=="APOE"
    assert response.context["error"] is None

def test_valid_hgnc_id_search(client):
    """
    Test that the search view finds a gene using a valid HGNC ID.
    """
    response = client.get(
        reverse("search"),
        {"query": "HGNC:613"},
    )

    assert response.status_code == 200
    assert response.context["error"] is None
    assert response.context["gene"] is not None
    assert response.context["gene"]["hgnc_id"] == "HGNC:613"
    assert response.context["gene"]["gene_symbol"] == "APOE"


def test_unknown_hgnc_id_displays_not_found_error(client):
    """
    Test that an unknown HGNC ID produces a clear error.
    """
    response = client.get(
        reverse("search"),
        {"query": "HGNC:999999999"},
    )

    assert response.status_code == 200
    assert response.context["gene"] is None
    assert response.context["error"] == "Gene not found."
    assert b"Gene not found." in response.content

def test_invalid_query_displays_validation_error(client):
    """
    Test that invalid characters produce a user-friendly error.
    """
    response = client.get(
        reverse("search"),
        {"query": "APO/"},
    )

    assert response.status_code == 200
    assert response.context["gene"] is None
    assert (
        response.context["error"]
        == "Please enter a vald HGNC ID or gene symbol"
    )

def test_lowercase_hgnc_id_uses_hgnc_search(client):
    """
    Test that lowercase HGNC IDs use the HGNC ID search.
    """
    expected_gene = {
        "hgnc_id": "HGNC:613",
        "gene_symbol": "APOE",
        "gene_name": "apolipoprotein E",
        "previous_symbols": [],
        "previous_names": [],
        "aliases": [],
        "mane_select": ['ENST00000252486.9','NM_000041.4',],
        "mane_plus_clinical": [],
    }
    response = client.get(
        reverse("search"),
        {"query": "hgnc:613"},
    )

    assert response.status_code == 200
    assert response.context["gene"] == expected_gene