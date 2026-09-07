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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                            # Paths
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "hgnc_complete_set.txt"
OUTPUT_FILE = BASE_DIR / "data" / "hgnc_lightweight_dataset.json"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                            # Logging
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger("hgnc_lookup")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                        # Helper functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def split_field(value: str) -> list:
    """
    Convert pipe-delimited HGNC fields into a list. Inspecting original dataset showed that some cells have information seperated by a pipe.
    """

    if not value:
        return []

    return value.split("|")


def build_gene_record(row: dict) -> dict:
    """
    Build a lightweight json dictionary by only extracting the fields specified in the assignment.
    """

    return {
        "hgnc_id": row.get("hgnc_id", ""),
        "gene_symbol": row.get("symbol", ""),
        "gene_name": row.get("name", ""),

        "previous_symbols":
            split_field(row.get("prev_symbol", "")),

        "previous_names":
            split_field(row.get("prev_name", "")),

        "aliases":
            split_field(row.get("alias_symbol", "")),

        "mane_select":
            split_field(row.get("mane_select", "")),

        "mane_plus_clinical": #Empty column when inspecting but included as assignment specified.
            split_field(row.get("mane_plus_clinical", ""))
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                        # Main processing
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def create_lightweight_dataset(input_file=INPUT_FILE) -> list:
    """
    Read the hgnc_complete_set.txt and create a lightweight 
    dataset using the helper functions above.
    """

    logger.info("Reading HGNC data from %s", input_file)

    dataset = []

    with open(input_file, "r", encoding="utf-8") as file:

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


def save_dataset(dataset: list[dict], output_file=OUTPUT_FILE) -> None:
    """
    Write lightweight dataset to JSON.
    """

    with open(
        output_file,
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
        output_file
    )


def main() -> None:

    dataset = create_lightweight_dataset()

    save_dataset(dataset)

    logger.info("Dataset generation complete")


if __name__ == "__main__":
    main()