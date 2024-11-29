name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run flake8
        run: |
          flake8 .

  # test:
  #   runs-on: ubuntu-latest
  #   # This job requires the lint job to finish successfully
  #   needs: lint
  #   steps:
  #     - uses: actions/checkout@v2
  #     - name: Set up Python
  #       # Set up the Python version specified in the cookiecutter template
  #       uses: actions/setup-python@v2
  #       with: 
  #         python-version: '3.x'
          
  #     - name: Install dependencies
  #       # Install the dependencies specified in the requirements file
  #       run: |
  #         python -m pip install --upgrade pip
  #         pip install -r requirements-dev.txt
  #     - name: Run tests
  #       # Run the tests using pytest
  #       run: |
  #         pytest
