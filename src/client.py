import requests
import time
import logging


logger = logging.getLogger(__name__)


class BreweryClientError(RuntimeError):
    """Base exception for BreweryClient failures."""


class BreweryRequestError(BreweryClientError):
    """Raised when an HTTP request to the brewery API fails."""


class BreweryResponseParseError(BreweryClientError):
    """Raised when the brewery API response cannot be parsed as JSON."""


class BreweryClient:
    """HTTP client for the Open Brewery DB API.

    This client handles request construction, status validation, pagination,
    and JSON parsing for brewery data.
    """

    def __init__(
        self,
        base_url: str = "https://api.openbrewerydb.org/v1",
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        """Initialize the client with API endpoint, timeout, and retry policy.

        Args:
            base_url: Base URL of the API.
            timeout: Request timeout in seconds.
            max_retries: Number of retry attempts for transient failures.
            backoff_factor: Base multiplier used to compute backoff delay.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._session = requests.Session()

    def __enter__(self) -> "BreweryClient":
        """Enter the context manager and return this client."""
        logger.debug("Entering BreweryClient context manager")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Exit the context manager and close the underlying session."""
        logger.debug("Exiting BreweryClient context manager")
        self.close()
        return False

    def close(self) -> None:
        """Close the underlying requests.Session."""
        self._session.close()
        logger.debug("Closed BreweryClient requests session")

    def fetch_breweries_page(self, page: int, per_page: int = 50) -> list[dict]:
        """Fetch a single page of breweries from the API.

        Args:
            page: Page number to request.
            per_page: Number of items per page.

        Returns:
            A list of brewery records as dictionaries.

        Raises:
            RuntimeError: If the request fails or the response is invalid.
        """
        params = {"page": page, "per_page": per_page}
        logger.info("Fetching brewery page %d with %d records per page", page, per_page)
        response = self._request("/breweries", params)
        logger.info("Received response with status %d for page %d", response.status_code, page)
        return self._parse_response(response)

    def fetch_all_breweries(self, max_pages: int = 3) -> list[dict]:
        """Fetch multiple brewery pages and return a consolidated list.

        Args:
            max_pages: Maximum number of pages to retrieve.

        Returns:
            A flattened list of brewery records.
        """
        breweries = []
        for page in range(1, max_pages + 1):
            page_data = self.fetch_breweries_page(page)
            if not page_data:
                break
            breweries.extend(page_data)
        return breweries

    def _request(self, path: str, params: dict) -> requests.Response:
        """Perform an HTTP GET request and validate the response.

        Args:
            path: API path to append to the base URL.
            params: Query parameters for the request.

        Returns:
            The raw HTTP response.

        Raises:
            BreweryRequestError: If the request fails or returns an error status.
        """
        url = f"{self.base_url}{path}"
        attempt = 0
        while True:
            attempt += 1
            try:
                logger.debug(
                    "Sending request to %s with params %s (attempt %d)",
                    url,
                    params,
                    attempt,
                )
                response = self._session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                logger.debug("Request succeeded with status %d", response.status_code)
                return response
            except requests.exceptions.RequestException as exc:
                status_code = None
                if isinstance(exc, requests.exceptions.HTTPError) and exc.response is not None:
                    status_code = exc.response.status_code

                should_retry = (
                    isinstance(exc, (requests.exceptions.ConnectionError, requests.exceptions.Timeout))
                    or (status_code is not None and 500 <= status_code < 600)
                )

                if not should_retry or attempt > self.max_retries:
                    logger.error(
                        "Request failed for %s after %d attempt(s): %s",
                        url,
                        attempt,
                        exc,
                    )
                    raise BreweryRequestError(f"Request error for {url}: {exc}") from exc

                delay = self.backoff_factor * (2 ** (attempt - 1))
                logger.warning(
                    "Transient failure detected for %s (status=%s); retrying in %.1f seconds (attempt %d of %d)",
                    url,
                    status_code,
                    delay,
                    attempt + 1,
                    self.max_retries + 1,
                )
                time.sleep(delay)

    def _parse_response(self, response: requests.Response) -> list[dict]:
        """Parse the HTTP response body as JSON.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed JSON data as a list of dictionaries.

        Raises:
            RuntimeError: If the response body is not valid JSON.
        """
        try:
            return response.json()
        except ValueError as exc:
            logger.error("Failed to parse JSON response: %s", exc)
            raise BreweryResponseParseError("Response body is not valid JSON") from exc
