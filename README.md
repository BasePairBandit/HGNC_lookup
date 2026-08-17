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
-	MANE Plus Clinical transcript(s)

# Data source

Original data downloaded from : https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt.
Date downloaded :

A lightweight dataset is created to reflects the columns mentioned above and is used by the web application to provide the user with the information.

# Project architecture

The application loads a TSV file into memory once during application startup the lightweight data set is created from this and performs all gene searches against the lightweight dataset in-memory.

# Installation

The project uses a reproducible Conda environment to ensure consistent behaviour across systems.

# Create environment
conda env create -f environment.yml

# Activate environment
conda activate HGNC_lookup

# Install application
pip install -e .

# Run application
python manage.py runserver

# Run tests
pytest

# Generate coverage report
pytest --cov=. --cov-report=html

# Project layout
├── data
│   ├── hgnc_complete_set.tsv
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
├── project
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── settings.cpython-312.pyc
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

# Logging

Logging is configured centrally within:

project/settings.py

# Stopping the application

Stop the development server with:

```text
Ctrl+C
```

Deactivate the Conda environment when finished:

conda deactivate
---

# Purpose 

This web app is made as part of the UoM STP-2025 cohort software engineering project requirement demonstrating data processing, testing, documentation and web application development using Django. 
