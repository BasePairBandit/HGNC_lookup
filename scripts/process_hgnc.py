"""
This script converts the full hgnc_complete_set.txt file into a smaller JSON dataset 
containing only the fields required by the app while handling missing values and 
formatting the data into dictionaries that are easy for the Django app to search.

Input:
    data/hgnc_complete_set.txt

Output:
    data/hgnc_lightweight_dataset.json
"""

import csv
import json
import logging
from pathlib import Path


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "hgnc_complete_set.txt"
OUTPUT_FILE = BASE_DIR / "data" / "hgnc_lightweight_dataset.json"


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

logger = logging.getLogger("hgnc_lookup")


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def split_field(value: str) -> list:
    """
    Convert pipe-delimited HGNC fields into a list. Inspecting original dataset showed that some cells have information seperated by a pipe.
    """

    if not value:
        return []

    return value.split("|")


def build_gene_record(row: dict) -> dict:
    """
    Build a lightweight gene dictionary by only extracting the fields specified in the assignment.
    """

    return {
        "hgnc_id": row.get("hgnc_id", ""),
        "gene_symbol": row.get("symbol", ""),
        "gene_name": row.get("name", ""),

        "previous_symbols":
            split_field(row.get("previous_symbols", "")),

        "previous_names":
            split_field(row.get("previous_names", "")),

        "aliases":
            split_field(row.get("aliases", "")),

        "mane_select":
            split_field(row.get("mane_select", "")),

        "mane_plus_clinical": #Empty column when inspecting but included as assignment specified.
            split_field(row.get("mane_plus_clinical", ""))
    }


# ------------------------------------------------------------------
# Main processing
# ------------------------------------------------------------------

def create_lightweight_dataset() -> list:
    """
    Read the hgnc_complete_set.txt and create a lightweight dataset.
    """

    logger.info("Reading HGNC data from %s", INPUT_FILE)

    dataset = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        reader = csv.DictReader(
            file,
            delimiter="\t"
        )

        for row in reader:
            dataset.append(
                build_gene_record(row)
            )

    logger.info(
        "Processed %d gene records",
        len(dataset)
    )

    return dataset


def save_dataset(dataset: list[dict]) -> None:
    """
    Write lightweight dataset to JSON.
    """

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            dataset,
            outfile,
            indent=4
        )

    logger.info(
        "Saved lightweight dataset to %s",
        OUTPUT_FILE
    )


def main() -> None:

    dataset = create_lightweight_dataset()

    save_dataset(dataset)

    logger.info("Dataset generation complete")


if __name__ == "__main__":
    main()