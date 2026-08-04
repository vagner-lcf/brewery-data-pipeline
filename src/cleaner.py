import pandas as pd
import logging


logger = logging.getLogger(__name__)


DEFAULT_MISSING_TEXT = "Not Informed"


class DataCleaner:
    """Clean and standardize brewery data from the Open Brewery DB API."""

    def __init__(self, raw_data: list[dict]) -> None:
        """Initialize the cleaner with raw API data.

        Args:
            raw_data: List of dictionaries returned by BreweryClient.
        """
        self.raw_data = raw_data

    def to_dataframe(self) -> pd.DataFrame:
        """Convert raw brewery records to a pandas DataFrame."""
        logger.info("Converting raw data to DataFrame with %d records", len(self.raw_data))
        return pd.DataFrame(self.raw_data)

    def select_output_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select only the columns that should appear in the final output."""
        columns_to_keep = [
            "id",
            "name",
            "brewery_type",
            "street",
            "city",
            "state",
            "postal_code",
            "country",
            "longitude",
            "latitude",
            "phone",
            "website_url",
        ]

        retained_columns = [column for column in columns_to_keep if column in df.columns]
        removed_columns = [column for column in df.columns if column not in columns_to_keep]

        if removed_columns:
            logger.info("Dropping unused columns: %s", removed_columns)

        return df[retained_columns]

    def clean_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values for common textual and geographic columns."""
        logger.debug("Cleaning missing values for columns: %s", df.columns.tolist())
        text_columns = [
            "name",
            "brewery_type",
            "street",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
            "website_url",
        ]

        for column in text_columns:
            if column in df.columns:
                df[column] = df[column].fillna(DEFAULT_MISSING_TEXT).astype(str)

        for column in ["latitude", "longitude"]:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0.0)

        logger.debug("Missing values cleaned; remaining missing values by column:\n%s", df.isna().sum())
        return df

    def standardize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize string columns to a consistent uppercase and trimmed form."""
        logger.debug("Standardizing text columns")
        upper_columns = [
            "country",
            "state",
            "city",
            "brewery_type",
            "name",
            "street",
            "postal_code",
        ]

        for column in upper_columns:
            if column in df.columns:
                df[column] = df[column].astype(str).str.strip().str.upper()

        if "website_url" in df.columns:
            df["website_url"] = df["website_url"].astype(str).str.strip()

        return df

    def sanitize_phone_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove non-digit characters from phone numbers and preserve missing markers."""
        if "phone" not in df.columns:
            logger.debug("No phone column found; skipping phone sanitization")
            return df

        logger.debug("Sanitizing phone numbers")
        phone_series = df["phone"].astype(str).str.strip()
        is_missing = phone_series == DEFAULT_MISSING_TEXT
        cleaned_phone = phone_series.str.replace(r"\D+", "", regex=True)
        df["phone"] = cleaned_phone.where(~is_missing, DEFAULT_MISSING_TEXT)

        return df

    def process(self) -> pd.DataFrame:
        """Run the full cleaning pipeline and return the cleaned DataFrame."""
        logger.info("Starting data cleaning pipeline")
        df = self.to_dataframe()
        df = self.clean_missing_values(df)
        df = self.standardize_text(df)
        df = self.sanitize_phone_numbers(df)
        df = self.select_output_columns(df)
        logger.info("Data cleaning pipeline finished with shape %s", df.shape)
        return df
