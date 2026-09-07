[![codecov](https://codecov.io/gh/BasePairBandit/HGNC_lookup/graph/badge.svg?token=AI3N488EA6)](https://codecov.io/gh/BasePairBandit/HGNC_lookup)

# HGNC_lookup
HGNC_lookup is a simple Django web application that allows the user to find information about human genes using either the gene symbol or HGNC ID.

User enters gene symbol/HGNC ID and the web app returns the following information:

-	HGNC-approved gene symbol
-	HGNC ID
-	Approved gene name
-	Previous gene symbols
-	Previous gene names
-	Gene aliases/synonyms
-	MANE Select transcript
-	MANE Plus Clinical transcript(s) - if available

# Data source

Original data downloaded from : https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt.
Date downloaded : 27-08-2026

A lightweight dataset (see instructions below) is created to reflect the columns mentioned above and is used by the web application to provide the user with the information.

# Project architecture

The application loads the .txt file into memory once during application startup and the lightweight data set is created from this and performs all gene searches against the lightweight dataset in-memory.

## Download source dataset

If the user would like to use an up-to-date dataset instead of the one provided they can perform the following steps at any point.

wget https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt

Place the downloaded file in:

- data/hgnc_complete_set.txt

Note: the user would need to regenerate the lightweight dataset and restart the server.

# Installation

The project uses a reproducible Conda environment to ensure consistent behaviour across systems.

## Create environment

```bash
conda env create -f environment.yml
```

## Activate environment
```bash
conda activate HGNC_lookup
```

# Install application
```bash
pip install -e .
```

# Generate lightweight dataset

```bash
python -m scripts.process_hgnc
```

# Run application
Run the Django development server:

```bash
python manage.py runserver
```
# Stopping the application

Stop the development server with:

```bash
Ctrl+C
```

Deactivate the Conda environment when finished:

```bash
conda deactivate
```
---

# Run tests

```bash
pytest
```

# Generate coverage report

```bash
pytest --cov=. --cov-report=html
```

The HTML coverage report will be generated in:
- htmlcov/index.html

Open the file in a browser to review coverage.

# Project layout
```text
.
├── data
│   ├── hgnc_complete_set.txt
│   └── hgnc_lightweight_dataset.json
├── environment.yml
├── hgnc_lookup_app
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── services
│   │   ├── data_loader.py
│   │   ├── gene_search.py
│   │   └── __init__.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_data_processing.py
│   │   ├── test_gene_search.py
│   │   └── test_views.py
│   ├── urls.py
│   └── views.py
├── LICENSE
├── manage.py
├── hgnc_lookup
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── scripts
│   └── process_hgnc.py
├── static
│   └── hgnc_lookup_app
│       └── style.css
└── templates
    └── hgnc_lookup_app
        ├── results.html
        └── search.html
```

# Logging

Logging is configured centrally within :

hgnc_lookup/settings.py

# Purpose 

This web app is made as part of the UoM STP-2025 cohort software engineering project requirement demonstrating data processing, testing, documentation and web application development using Django. 
