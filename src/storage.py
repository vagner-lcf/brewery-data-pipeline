from pathlib import Path
import pandas as pd
import logging


logger = logging.getLogger(__name__)



class LocalStorage:
    """Persist pandas DataFrames to disk in CSV and Parquet formats.

    Responsibilities:
    - Ensure the output directory exists.
    - Provide simple save methods that return the written file Path.

    Args:
        output_dir: Directory where files will be written (default: 'data/processed').
    """

    def __init__(self, output_dir: str = "data/processed") -> None:
        """Create a LocalStorage bound to `output_dir`.

        The constructor ensures the directory exists so callers can write files
        immediately after instantiation.
        """
        self.output_dir = Path(output_dir)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Create the output directory if it does not exist.

        This method is idempotent and safe to call repeatedly.
        """
        logger.info("Ensuring output directory exists at %s", self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> Path:
        """Save a DataFrame as CSV (UTF-8-sig) and return the file path.

        Args:
            df: DataFrame to persist.
            filename: Target filename, for example 'breweries_clean.csv'.

        Returns:
            Path pointing to the saved CSV file.
        """
        target = self.output_dir / filename
        df.to_csv(target, index=False, encoding="utf-8-sig")
        logger.info("Saved CSV to %s", target)
        return target

    def save_to_parquet(self, df: pd.DataFrame, filename: str) -> Path:
        """Save a DataFrame as Parquet using the PyArrow engine and return the file path.

        Args:
            df: DataFrame to persist.
            filename: Target filename, for example 'breweries_clean.parquet'.

        Returns:
            Path pointing to the saved Parquet file.
        """
        target = self.output_dir / filename
        df.to_parquet(target, engine="pyarrow", index=False)
        logger.info("Saved Parquet to %s", target)
        return target

