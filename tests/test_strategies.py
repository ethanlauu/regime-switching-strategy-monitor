import pytest
import numpy as np
import pandas as pd
from app.strategies import (
    calculate_ma_crossover, calculate_rsi, bull_strategy, 
    bear_strategy, sideways_strategy, generate_signal
)

class TestStrategies:
    """Test cases for strategies module."""
    
    def setup_method(self):
        """Setup test environment."""
        # Create sample data with clear trends
        dates = pd.date_range('2023-01-01', periods=300)
        self.bull_df = pd.DataFrame({
            'Close': np.linspace(100, 200, 300)  # Upward trend
        }, index=dates)
        
        self.bear_df = pd.DataFrame({
            'Close': np.linspace(200, 100, 300)  # Downward trend
        }, index=dates)
        
        self.sideways_df = pd.DataFrame({
            'Close': 100 + 10 * np.sin(np.linspace(0, 4*np.pi, 300))  # Sideways with noise
        }, index=dates)
    
    def test_calculate_ma_crossover_bull(self):
        """Test MA crossover with bullish data."""
        signal = calculate_ma_crossover(self.bull_df, 50, 200)
        assert signal == 1.0  # Should be bullish
    
    def test_calculate_ma_crossover_bear(self):
        """Test MA crossover with bearish data."""
        signal = calculate_ma_crossover(self.bear_df, 50, 200)
        assert signal == -1.0  # Should be bearish
    
    def test_calculate_ma_crossover_insufficient_data(self):
        """Test MA crossover with insufficient data."""
        short_df = pd.DataFrame({
            'Close': [100, 101, 102]
        }, index=pd.date_range('2023-01-01', periods=3))
        
        signal = calculate_ma_crossover(short_df, 50, 200)
        assert signal == 0.0
    
    def test_calculate_rsi_normal(self):
        """Test RSI calculation with normal data."""
        rsi = calculate_rsi(self.sideways_df, 14)
        assert 0 <= rsi <= 100
        assert not np.isnan(rsi)
    
    def test_calculate_rsi_insufficient_data(self):
        """Test RSI calculation with insufficient data."""
        short_df = pd.DataFrame({
            'Close': [100, 101, 102]
        }, index=pd.date_range('2023-01-01', periods=3))
        
        rsi = calculate_rsi(short_df, 14)
        assert rsi == 50.0  # Default value
    
    def test_bull_strategy(self):
        """Test bull strategy."""
        signal = bull_strategy(self.bull_df)
        assert isinstance(signal, float)
        assert -1 <= signal <= 1
    
    def test_bear_strategy_oversold(self):
        """Test bear strategy with oversold conditions."""
        # Create oversold data (declining prices)
        oversold_df = pd.DataFrame({
            'Close': np.linspace(200, 150, 50)
        }, index=pd.date_range('2023-01-01', periods=50))
        
        signal = bear_strategy(oversold_df)
        assert isinstance(signal, float)
        assert -1 <= signal <= 1
    
    def test_sideways_strategy(self):
        """Test sideways strategy."""
        signal = sideways_strategy(self.sideways_df)
        assert signal == 0.0  # Always returns 0
    
    def test_generate_signal_buy(self):
        """Test signal generation with buy signal."""
        regime_probs = np.array([0.8, 0.1, 0.1])  # Strong bull regime
        signal_data = generate_signal(regime_probs, self.bull_df)
        
        assert signal_data["action"] in ["BUY", "SELL", "HOLD"]
        assert 0 <= signal_data["confidence"] <= 1
        assert len(signal_data["regime_probs"]) == 3
        assert isinstance(signal_data["weighted_signal"], float)
    
    def test_generate_signal_sell(self):
        """Test signal generation with sell signal."""
        regime_probs = np.array([0.1, 0.8, 0.1])  # Strong bear regime
        signal_data = generate_signal(regime_probs, self.bear_df)
        
        assert signal_data["action"] in ["BUY", "SELL", "HOLD"]
        assert 0 <= signal_data["confidence"] <= 1
        assert len(signal_data["regime_probs"]) == 3
    
    def test_generate_signal_hold(self):
        """Test signal generation with hold signal."""
        regime_probs = np.array([0.33, 0.33, 0.34])  # Balanced regimes
        signal_data = generate_signal(regime_probs, self.sideways_df)
        
        assert signal_data["action"] in ["BUY", "SELL", "HOLD"]
        assert 0 <= signal_data["confidence"] <= 1
    
    def test_generate_signal_invalid_probs(self):
        """Test signal generation with invalid probabilities."""
        regime_probs = np.array([0.5, 0.5])  # Only 2 probabilities
        
        with pytest.raises(ValueError, match="Expected 3 regime probabilities"):
            generate_signal(regime_probs, self.sideways_df)
    
    def test_generate_signal_edge_cases(self):
        """Test signal generation with edge case probabilities."""
        # All zeros
        regime_probs = np.array([0.0, 0.0, 0.0])
        signal_data = generate_signal(regime_probs, self.sideways_df)
        assert signal_data["action"] == "HOLD"
        
        # All ones (normalized)
        regime_probs = np.array([1.0, 0.0, 0.0])
        signal_data = generate_signal(regime_probs, self.bull_df)
        assert signal_data["action"] in ["BUY", "SELL", "HOLD"] 