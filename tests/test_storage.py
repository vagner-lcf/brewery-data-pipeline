import pandas as pd
from src.storage import LocalStorage


def test_storage_saves_csv_and_parquet(tmp_path):
    df = pd.DataFrame(
        [
            {
                "id": "1",
                "name": "Test Brewery",
                "city": "LISBON",
                "state": "PORTUGAL",
                "postal_code": "1000-000",
                "country": "PORTUGAL",
                "longitude": -9.142683,
                "latitude": 38.736946,
                "phone": "2112345678",
                "website_url": "http://example.com",
            }
        ]
    )

    storage = LocalStorage(output_dir=str(tmp_path))

    csv_path = storage.save_to_csv(df, "test_breweries.csv")
    parquet_path = storage.save_to_parquet(df, "test_breweries.parquet")

    assert csv_path.exists()
    assert parquet_path.exists()

    df_csv = pd.read_csv(csv_path)
    df_parquet = pd.read_parquet(parquet_path)

    assert df_csv.loc[0, "name"] == "Test Brewery"
    assert df_parquet.loc[0, "city"] == "LISBON"
