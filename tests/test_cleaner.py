import pandas as pd
from pandas.testing import assert_frame_equal
from src.cleaner import DataCleaner


def test_cleaner_drops_unused_address_columns():
    raw_data = [
        {
            "id": "1",
            "name": "Test Brewery",
            "brewery_type": "micro",
            "street": "Example Street 10",
            "address_2": "unused",
            "address_3": "unused",
            "city": "Lisbon",
            "state": "Lisbon",
            "postal_code": "1000-000",
            "country": "Portugal",
            "longitude": "-9.142683",
            "latitude": "38.736946",
            "phone": "(21) 1234-5678",
            "website_url": "http://example.com",
        }
    ]

    cleaner = DataCleaner(raw_data)
    result = cleaner.process()

    assert "address_2" not in result.columns
    assert "address_3" not in result.columns
    assert result.loc[0, "city"] == "LISBON"
    assert result.loc[0, "street"] == "EXAMPLE STREET 10"
    assert result.loc[0, "phone"] == "2112345678"
    assert result.loc[0, "website_url"] == "http://example.com"

    expected = pd.DataFrame(
        [
            {
                "id": "1",
                "name": "TEST BREWERY",
                "brewery_type": "MICRO",
                "street": "EXAMPLE STREET 10",
                "city": "LISBON",
                "state": "LISBON",
                "postal_code": "1000-000",
                "country": "PORTUGAL",
                "longitude": -9.142683,
                "latitude": 38.736946,
                "phone": "2112345678",
                "website_url": "http://example.com",
            }
        ]
    )

    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
