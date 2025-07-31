import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from app.data_loader import fetch_ohlcv, cache_data, load_cached_data, get_latest_df

class TestDataLoader:
    """Test cases for data_loader module."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_parquet_path = 'test_data_cache.parquet'
        self.sample_df = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [99, 100, 101],
            'Close': [103, 104, 105],
            'Volume': [1000, 1100, 1200]
        }, index=pd.date_range('2023-01-01', periods=3))
    
    def teardown_method(self):
        """Cleanup test environment."""
        if os.path.exists(self.test_parquet_path):
            os.remove(self.test_parquet_path)
    
    @patch('app.data_loader.yf.download')
    def test_fetch_ohlcv_success(self, mock_download):
        """Test successful OHLCV data fetch."""
        mock_download.return_value = self.sample_df
        result = fetch_ohlcv('SPY', '1y')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'Close' in result.columns
        mock_download.assert_called_once_with('SPY', period='1y', auto_adjust=True)
    
    @patch('app.data_loader.yf.download')
    def test_fetch_ohlcv_empty(self, mock_download):
        """Test fetch_ohlcv with empty data."""
        mock_download.return_value = pd.DataFrame()
        result = fetch_ohlcv('SPY', '1y')
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_cache_data(self):
        """Test data caching functionality."""
        cache_data(self.sample_df, self.test_parquet_path)
        assert os.path.exists(self.test_parquet_path)
    
    def test_load_cached_data_exists(self):
        """Test loading cached data when file exists."""
        cache_data(self.sample_df, self.test_parquet_path)
        result = load_cached_data(self.test_parquet_path)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'Close' in result.columns
    
    def test_load_cached_data_not_exists(self):
        """Test loading cached data when file doesn't exist."""
        result = load_cached_data('nonexistent.parquet')
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('app.data_loader.load_cached_data')
    @patch('app.data_loader.fetch_ohlcv')
    @patch('app.data_loader.cache_data')
    def test_get_latest_df_from_cache(self, mock_cache, mock_fetch, mock_load):
        """Test get_latest_df using cached data."""
        mock_load.return_value = self.sample_df
        result = get_latest_df(force_refresh=False)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        mock_load.assert_called_once()
        mock_fetch.assert_not_called()
    
    @patch('app.data_loader.load_cached_data')
    @patch('app.data_loader.fetch_ohlcv')
    @patch('app.data_loader.cache_data')
    def test_get_latest_df_force_refresh(self, mock_cache, mock_fetch, mock_load):
        """Test get_latest_df with force refresh."""
        mock_fetch.return_value = self.sample_df
        result = get_latest_df(force_refresh=True)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        mock_fetch.assert_called_once()
        mock_cache.assert_called_once()
    
    @patch('app.data_loader.load_cached_data')
    @patch('app.data_loader.fetch_ohlcv')
    @patch('app.data_loader.cache_data')
    def test_get_latest_df_empty_cache(self, mock_cache, mock_fetch, mock_load):
        """Test get_latest_df when cache is empty."""
        mock_load.return_value = pd.DataFrame()
        mock_fetch.return_value = self.sample_df
        result = get_latest_df(force_refresh=False)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        mock_fetch.assert_called_once()
        mock_cache.assert_called_once() 