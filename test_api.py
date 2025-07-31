#!/usr/bin/env python3
"""
Test script for the Regime-Switching Trading Engine API.
"""

import requests
import time
import json

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("Testing Regime-Switching Trading Engine API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Wait a moment for data loading
    print("Waiting for data to load...")
    time.sleep(2)
    
    # Test regime endpoint
    try:
        response = requests.get(f"{base_url}/regime/latest")
        print(f"Regime check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Bull: {data.get('bull_probability', 'N/A'):.3f}")
            print(f"  Bear: {data.get('bear_probability', 'N/A'):.3f}")
            print(f"  Sideways: {data.get('sideways_probability', 'N/A'):.3f}")
    except Exception as e:
        print(f"Regime check failed: {e}")
    
    # Test signal endpoint
    try:
        response = requests.get(f"{base_url}/signal/latest")
        print(f"Signal check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Action: {data.get('action', 'N/A')}")
            print(f"  Confidence: {data.get('confidence', 'N/A'):.3f}")
    except Exception as e:
        print(f"Signal check failed: {e}")
    
    # Test backtest endpoint (with shorter period)
    try:
        response = requests.get(f"{base_url}/backtest?years=2")
        print(f"Backtest check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('strategy_metrics', {})
            print(f"  Annualized Return: {metrics.get('annualized_return', 'N/A'):.3f}")
            print(f"  Sharpe Ratio: {metrics.get('sharpe_ratio', 'N/A'):.3f}")
    except Exception as e:
        print(f"Backtest check failed: {e}")
    
    print("=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    test_api() 