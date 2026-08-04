# Open Brewery Data Pipeline

A lightweight ETL (Extract, Transform, Load) pipeline built in Python to consume data from the Open Brewery DB API, process it into a structured schema, and persist it in analytical formats.

🌐 *Read this in [Português (Brasil)](README.pt-br.md).* 

## Features

- **Automated Extraction:** Robust HTTP client fetching data from Open Brewery DB with automatic retries and failure handling.
- **Data Transformation:** Cleans, sanitizes, and schemas raw API responses using `pandas` DataFrames.
- **Dual Persistence:** Export pipeline results simultaneously to CSV and Parquet formats for BI tool consumption (Power BI/Streamlit).
- **Unit Tested:** Full test suite covering client requests, transformation rules, storage handlers, and main orchestration.

## Technologies & Concepts Applied

- **Python 3.11+**
- **Pandas & PyArrow:** Data wrangling, schema enforcement, and columnar Parquet serialization.
- **Requests:** Resilient HTTP communication with custom error management.
- **Pytest:** Comprehensive unit and integration test coverage.
- **Clean Architecture & PEP 8:** Decoupled execution layers (client, cleaner, storage) with explicit type hints and docstrings.

## Installation & Usage

### Quickstart

Clone the repository and enter the project directory:
```bash
git clone https://github.com/YOUR_USERNAME/open-brewery-pipeline.git
cd open-brewery-pipeline
```

### Create and activate a virtual environment

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Linux/macOS (Bash):
```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the ETL pipeline

```bash
python main.py
```

### Output

Processed datasets will be written to `data/processed/`:

- `breweries_clean.csv` — UTF-8-sig CSV for easy Excel/Power BI import
- `breweries_clean.parquet` — columnar Parquet for performant BI queries

Tip: open the directory after running to verify generated files:

Windows PowerShell:
```powershell
explorer.exe .\data\processed
```

Linux/macOS:
```bash
xdg-open data/processed || open data/processed
```

## Testing
Execute the test suite via `pytest`:

```bash
pytest
```

## Project Structure

```
open-brewery-pipeline/
├── data/
│   └── processed/         # Generated output datasets (.csv, .parquet)
├── src/
│   ├── client.py          # API interaction layer
│   ├── cleaner.py         # Data transformation routines
│   └── storage.py         # File persistence handlers
├── tests/
│   ├── test_cleaner.py
│   ├── test_client.py
│   ├── test_main.py
│   └── test_storage.py
├── main.py                # Pipeline entry point
├── requirements.txt
└── README.md
