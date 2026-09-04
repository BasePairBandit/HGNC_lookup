import json
from pathlib import Path
from scripts.process_hgnc import create_lightweight_dataset, save_dataset, build_gene_record

def test_create_light_weight_dataset_not_empty():
    """
    Test that the dataset is not empty.
    """
    dataset = create_lightweight_dataset()

    assert len(dataset) !=0 

def test_create_light_weight_dataset_is_list():
    """
    Test that the dataset created is of type list.
    """
    dataset = create_lightweight_dataset()

    assert type(dataset) == list

def test_create_light_weight_dataset_has_correct_fields():
    """
    Test that the dataset has the expected fields.
    """
    dataset = create_lightweight_dataset()

    expected_fields = {
        "hgnc_id",
        "gene_symbol",
        "gene_name",
        "previous_symbols",
        "previous_names",
        "aliases",
        "mane_select",
        "mane_plus_clinical",
    }

    assert set(dataset[0].keys()) == expected_fields

def test_create_light_weight_dataset_has_correct_types():
    """
    Test that the expected fields contain data of the correct type.
    """
    dataset = create_lightweight_dataset()

    dataset = dataset[0]

    gene_symbol = dataset["gene_symbol"]
    hgnc_id = dataset["hgnc_id"]
    mane_select = dataset["mane_select"]

    assert isinstance(gene_symbol, str)
    assert isinstance(hgnc_id, str)
    assert isinstance(mane_select, list)

def test_create_light_weight_dataset_has_known_genes():
    """
    Test that a known gene exisits and it has the correct hgnc_id.
    """
    dataset = create_lightweight_dataset()
    found_gene = False
    found_hgnc_id = False

    for record in dataset:
        if record["gene_symbol"] == "APOE":
            found_gene = True
            apoe_record = record["hgnc_id"]
            if apoe_record == "HGNC:613":
                found_hgnc_id= True
            else:
                continue
        else:
            continue
    assert found_hgnc_id
    assert found_gene

def test_create_light_weight_dataset_correct_mane_select(): 
    """
    Test that the mane_select is correct for a common gene.
    
    This test is intentionally a bit fragile. If failing consistently,
    check mane_select in dataset. However leaving this here because 
    it can potentially be a trigger for you to check the data structure
    / annotation sometime in the future.
    """
    dataset = create_lightweight_dataset()
    found_gene = False
    found_mane_select = False

    for record in dataset:
        if record["gene_symbol"] == "APOE":
            found_gene = True
            mane_select = str(record["mane_select"][0])
            if mane_select == "ENST00000252486.9":
                found_mane_select= True
            else:
                continue
        else:
            continue
    assert found_mane_select
    assert found_gene

def test_create_light_weight_dataset_check_for_duplicate_hgnc_ids():
    """
    Test that there are no duplicate hgnc_id records.
    """
    dataset = create_lightweight_dataset()

    seen = set()
    duplicates = False

    for record in dataset:
        hgnc_id = record["hgnc_id"]
        if hgnc_id in seen:
            duplicates = True
        else:
            seen.add(hgnc_id)
    assert not duplicates

def test_create_light_weight_dataset_check_for_duplicate_gene_symbol():
    """
    Test that there are no duplicate gene_symbol records.
    """
    dataset = create_lightweight_dataset()

    seen = set()
    duplicates = False

    for record in dataset:
        gene_symbol = record["gene_symbol"]
        if gene_symbol in seen:
            duplicates = True
        else:
            seen.add(gene_symbol)
    assert not duplicates

def test_create_light_weight_dataset_check_for_empty_hgnc_ids(): 
    """
    Test that there are no records with empty hgnc_ids.
    """
    dataset = create_lightweight_dataset()

    empty_hgnc_id = False

    for record in dataset:
        hgnc_id = record["hgnc_id"]
        if len(hgnc_id)==0:
            empty_hgnc_id = True

    assert not empty_hgnc_id

def test_save_dataset_works():
    """
    Test that the lightweight file gets created.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent

    INPUT_FILE = BASE_DIR / "tests" / "test_files" / "test_hgnc_record.txt"
    OUTPUT_FILE = BASE_DIR / "tests" / "test_files" / "test_hgnc_lightweight_dataset.json"
    try:
        dataset = create_lightweight_dataset(INPUT_FILE)

        save_dataset(dataset,output_file=OUTPUT_FILE)
        assert OUTPUT_FILE.exists()

        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        assert saved_data == dataset
    finally:
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()

def test_build_gene_record():
    """
    Test that the json structue is as expected.
    """
    row = {
        "hgnc_id": "HGNC:1",
        "symbol": "TEST",
        "name": "Test Gene",
        "previous_symbols": [],
        "previous_names": [],
        "aliases": "A|B",
        "mane_select": "ENST0001|NM_0001",
        "mane_plus_clinical": "",
    }

    record = build_gene_record(row)

    assert record["hgnc_id"] == "HGNC:1"
    assert record["gene_symbol"] == "TEST"
    assert record["previous_symbols"] == []
    assert record["previous_names"] == []
    assert record["aliases"] == ["A", "B"]
    assert record["mane_select"] == ["ENST0001","NM_0001"]
    assert record["mane_plus_clinical"] == []