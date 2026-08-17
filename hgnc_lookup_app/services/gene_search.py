from .data_loader import load_dataset
import re
import logging
logger = logging.getLogger("hgnc_lookup")

# ------------------------------------------------------------------
# Validate user input
# ------------------------------------------------------------------
class UserInputError(Exception):
    """
    Raised when a gene symbol/hgnc_ID is invalid.
    """
    pass

def validate_search_query(query: str) -> str:
    """
    Validate a gene symbol or HGNC ID
    """
    query = query.replace(" ","")
    if not query:
        logger.exception("Empty user input")
        raise UserInputError(
            "Invalid input, please enter a valid gene/HGNC_ID."
        )
    hgnc_pattern = r"^HGNC:\d+$"
    symbol_pattern = r"^[A-Za-z0-9-]+$"

    if re.match(hgnc_pattern, query):
        return query
    if re.match(symbol_pattern, query):
        return query
    logger.warning("User entered invalid input: %s",query)
    raise UserInputError(
        "Please enter a vald HGNC ID or gene symbol"
    )
    
    




# ------------------------------------------------------------------
# Search using user input
# ------------------------------------------------------------------

def find_by_symbol(symbol):

    dataset = load_dataset()

    for gene in dataset:
        if gene["gene_symbol"].upper() == symbol.upper():
            return gene

    return None


def find_by_hgnc_id(hgnc_id):

    dataset = load_dataset()

    for gene in dataset:
        if gene["hgnc_id"].upper() == hgnc_id.upper():
            return gene

    return None