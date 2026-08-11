import pytest
from main import main
from src.client import BreweryClientError


def test_main_returns_zero_on_success(monkeypatch, tmp_path):
    expected_raw_data = [
        {"id": "1", "name": "Test Brewery", "brewery_type": "micro", "street": "Street 1", "city": "Lisbon", "state": "Lisbon", "postal_code": "1000-000", "country": "Portugal", "longitude": "-9.142683", "latitude": "38.736946", "phone": "(21) 1234-5678", "website_url": "http://example.com"}
    ]

    class DummyClient:
        def fetch_all_breweries(self, max_pages=3):
            return expected_raw_data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    class DummyStorage:
        def __init__(self, output_dir=None):
            self.saved_csv = None
            self.saved_parquet = None

        def save_to_csv(self, df, filename):
            self.saved_csv = filename
            return tmp_path / filename

        def save_to_parquet(self, df, filename):
            self.saved_parquet = filename
            return tmp_path / filename

    monkeypatch.setattr("main.BreweryClient", lambda: DummyClient())
    monkeypatch.setattr("main.LocalStorage", lambda: DummyStorage())

    result = main()

    assert result == 0


def test_main_returns_one_on_brewery_error(monkeypatch):
    class DummyClient:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def fetch_all_breweries(self, max_pages=3):
            raise BreweryClientError("failed")

    monkeypatch.setattr("main.BreweryClient", lambda: DummyClient())

    result = main()

    assert result == 1


def test_main_returns_two_on_unexpected_error(monkeypatch):
    class DummyClient:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def fetch_all_breweries(self, max_pages=3):
            return [{
                "id": "1",
                "name": "Test Brewery",
                "brewery_type": "micro",
                "street": "Street 1",
                "city": "Lisbon",
                "state": "Lisbon",
                "postal_code": "1000-000",
                "country": "Portugal",
                "longitude": "-9.142683",
                "latitude": "38.736946",
                "phone": "(21) 1234-5678",
                "website_url": "http://example.com",
            }]

    class DummyCleaner:
        def __init__(self, raw_data):
            pass

        def process(self):
            raise RuntimeError("unexpected failure")

    monkeypatch.setattr("main.BreweryClient", lambda: DummyClient())
    monkeypatch.setattr("main.DataCleaner", DummyCleaner)

    result = main()

    assert result == 2
