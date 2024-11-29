name: Documentation Build

on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install sphinx

      - name: Build Documentation
        run: |
          cd docs
          make html

      - name: Upload Documentation Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: documentation
          path: docs/_build/html
