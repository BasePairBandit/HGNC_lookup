from django.shortcuts import render

from .services.gene_search import (
    validate_search_query,
    UserInputError,
    find_by_symbol,
    find_by_hgnc_id,
)

def search_gene(request):
    """
    Validate the user input.
    Decide if HGNC_ID or gene symbol.
    Make context result available for use in html. 
    """

    query = request.GET.get("query", "")

    result = None
    error = None

    if query:

        try:
            query = validate_search_query(query)

            if query.upper().startswith("HGNC:"):
                result = find_by_hgnc_id(query)
            else:
                result = find_by_symbol(query)

            if result is None:
                error = "Gene not found."

        except UserInputError as exc:
            error = str(exc)

    return render(
        request,
        "hgnc_lookup_app/search.html",
        {
            "gene": result,
            "error": error,
        }
    )