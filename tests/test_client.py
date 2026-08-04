import pytest
from requests.exceptions import ConnectionError, HTTPError, Timeout

from src.client import BreweryClient, BreweryRequestError, BreweryResponseParseError


class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise HTTPError(f"HTTP {self.status_code}", response=self)

    def json(self):
        return self._json_data



def test_request_raises_brewery_request_error_on_non_transient_http_error(monkeypatch):
    client = BreweryClient()

    def fake_get(url, params, timeout):
        return DummyResponse(status_code=404)

    monkeypatch.setattr(client._session, "get", fake_get)

    with pytest.raises(BreweryRequestError):
        client.fetch_breweries_page(page=1, per_page=1)


def test_request_retries_on_connection_error(monkeypatch):
    client = BreweryClient(max_retries=2, backoff_factor=0)
    call_count = {"count": 0}

    def fake_get(url, params, timeout):
        call_count["count"] += 1
        raise ConnectionError("network down")

    monkeypatch.setattr(client._session, "get", fake_get)

    with pytest.raises(BreweryRequestError):
        client.fetch_breweries_page(page=1, per_page=1)

    assert call_count["count"] == 3


def test_request_retries_on_timeout(monkeypatch):
    client = BreweryClient(max_retries=2, backoff_factor=0)
    call_count = {"count": 0}

    def fake_get(url, params, timeout):
        call_count["count"] += 1
        raise Timeout("request timed out")

    monkeypatch.setattr(client._session, "get", fake_get)

    with pytest.raises(BreweryRequestError):
        client.fetch_breweries_page(page=1, per_page=1)

    assert call_count["count"] == 3


def test_response_parse_error_on_invalid_json(monkeypatch):
    client = BreweryClient()

    def fake_get(url, params, timeout):
        response = DummyResponse(status_code=200)

        def invalid_json():
            raise ValueError("invalid json")

        response.json = invalid_json
        return response

    monkeypatch.setattr(client._session, "get", fake_get)

    with pytest.raises(BreweryResponseParseError):
        client.fetch_breweries_page(page=1, per_page=1)
