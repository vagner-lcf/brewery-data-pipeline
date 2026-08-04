"""Entry point for the brewery data ingestion pipeline.

This module orchestrates extraction from the Open Brewery DB API, cleaning
with pandas, and persistence to local CSV and Parquet files.
"""

from src.client import BreweryClient, BreweryClientError
from src.cleaner import DataCleaner
from src.storage import LocalStorage
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Run the brewery ETL pipeline and return a status code.

    Returns:
        0 when the pipeline completes successfully.
        1 when an extraction error occurs.
        2 when an unexpected internal error occurs.
    """
    try:
        with BreweryClient() as client:
            raw_data = client.fetch_breweries_page(page=1, per_page=5)

            cleaner = DataCleaner(raw_data)
            cleaned_df = cleaner.process()

            storage = LocalStorage()
            storage.save_to_csv(cleaned_df, "breweries_clean.csv")
            storage.save_to_parquet(cleaned_df, "breweries_clean.parquet")

            logger.info("Loaded %d raw records", len(raw_data))
            logger.info("Cleaned DataFrame shape: %s", cleaned_df.shape)
            logger.debug("Cleaned DataFrame head:\n%s", cleaned_df.head(5))
            logger.debug("Cleaned DataFrame dtypes:\n%s", cleaned_df.dtypes)
            logger.debug("Missing values by column:\n%s", cleaned_df.isna().sum())

            logger.info("Pipeline completed successfully")
            return 0

    except BreweryClientError as exc:
        logger.error("Data extraction failed: %s", exc)
        return 1

    except Exception:
        logger.exception("Unexpected error in pipeline")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())