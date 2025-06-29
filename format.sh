#!/bin/bash

# Clean up imports and fix other issues
python -m ruff check --fix *.py
python -m ruff check --fix test/*.py

# Format code
python -m ruff format *.py
python -m ruff format test/*.py
