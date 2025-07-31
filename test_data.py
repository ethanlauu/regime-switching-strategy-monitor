#!/usr/bin/env python3
"""
Test script to debug data loading and model fitting issues.
"""

import sys
import traceback

def test_data_loading():
    """Test data loading functionality."""
    print("Testing data loading...")
    try:
        from app.data_loader import get_latest_df
        df = get_latest_df()
        print(f"Data loaded successfully: {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print(f"Date range: {df.index[0]} to {df.index[-1]}")
        return df
    except Exception as e:
        print(f"Data loading failed: {e}")
        traceback.print_exc()
        return None

def test_model_fitting(df):
    """Test model fitting functionality."""
    print("\nTesting model fitting...")
    try:
        from app.model import RegimeHMM
        hmm = RegimeHMM(n_states=3)
        hmm.fit(df)
        print("Model fitted successfully!")
        
        # Test prediction
        tail_df = df.tail(30)
        probs = hmm.predict_proba(tail_df)
        print(f"Prediction successful: {probs}")
        return hmm
    except Exception as e:
        print(f"Model fitting failed: {e}")
        traceback.print_exc()
        return None

def test_strategies(df):
    """Test strategy functionality."""
    print("\nTesting strategies...")
    try:
        from app.strategies import generate_signal
        import numpy as np
        
        # Create dummy regime probabilities
        regime_probs = np.array([0.4, 0.3, 0.3])
        signal = generate_signal(regime_probs, df.tail(200))
        print(f"Signal generated: {signal}")
        return True
    except Exception as e:
        print(f"Strategy test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Regime-Switching Trading Engine Components")
    print("=" * 50)
    
    # Test data loading
    df = test_data_loading()
    if df is None:
        print("Cannot proceed without data")
        sys.exit(1)
    
    # Test model fitting
    model = test_model_fitting(df)
    if model is None:
        print("Cannot proceed without model")
        sys.exit(1)
    
    # Test strategies
    strategies_ok = test_strategies(df)
    
    print("\n" + "=" * 50)
    if strategies_ok:
        print("All tests passed! The backend should work now.")
    else:
        print("Some tests failed. Check the errors above.")
    print("=" * 50) 