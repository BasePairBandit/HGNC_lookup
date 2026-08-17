import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_FILE = (
    BASE_DIR /
    "data" /
    "hgnc_lightweight_dataset.json"
)

def load_dataset():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)