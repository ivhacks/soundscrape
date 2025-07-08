#!/bin/bash

# Clean up imports and fix other issues
python -m ruff check --select I --fix *.py
python -m ruff check --select I --fix test/*.py
python -m ruff check --fix *.py
python -m ruff check --fix test/*.py

# Format code
python -m ruff format *.py
python -m ruff format test/*.py

# Special formatting for test_integration.py with longer line length
python -m ruff format --line-length 320 test/test_integration.py
