import pandas as pd
import pytest
from cPOP.constants import Columns
from src.etl import read_data, calc_stats

@pytest.fixture
def sample_data():
    # Sample data for testing
    data = {
        Columns.TAG_GROUP: ['A', 'A', 'B', 'B'],
        Columns.COUNT: [10, 20, 15, 25],
        Columns.YEAR_COUNT: [100, 100, 200, 200]
    }
    return pd.DataFrame(data)

def test_read_data(sample_data):
    # Test read_data function
    expected_columns = [Columns.TAG_GROUP, Columns.COUNT, Columns.YEAR_COUNT, Columns.FRACTION]
    df = read_data(path=None)  # Assuming read_data will handle path=None correctly for testing
    assert isinstance(df, pd.DataFrame)
    assert all(column in df.columns for column in expected_columns)

def test_calc_stats(sample_data):
    # Test calc_stats function
    df = sample_data
    result_df = calc_stats(df)
    assert isinstance(result_df, pd.DataFrame)
    assert Columns.TAG_COUNT in result_df.columns
    assert Columns.FRACTION in result_df.columns
