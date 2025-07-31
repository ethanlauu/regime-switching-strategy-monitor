from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

from .data_loader import get_latest_df
from .model import RegimeHMM
from .strategies import generate_signal
from .backtest import run_backtest

app = FastAPI(title="Regime-Switching Trading Engine", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8083"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
hmm_model: Optional[RegimeHMM] = None

class RegimeResponse(BaseModel):
    """Response model for regime probabilities."""
    bull_probability: float
    bear_probability: float
    sideways_probability: float
    timestamp: str

class SignalResponse(BaseModel):
    """Response model for trading signals."""
    action: str
    confidence: float
    regime_probs: list[float]
    weighted_signal: float
    timestamp: str

class BacktestResponse(BaseModel):
    """Response model for backtest results."""
    strategy_metrics: Dict[str, float]
    benchmark_metrics: Dict[str, float]
    strategy_cumulative: list[float]
    benchmark_cumulative: list[float]
    dates: list[str]

def get_or_create_model() -> RegimeHMM:
    """
    Get or create the HMM model instance.
    Returns:
        RegimeHMM: Fitted HMM model.
    """
    global hmm_model
    
    if hmm_model is None:
        # Load data and fit model
        df = get_latest_df()
        if df.empty:
            raise HTTPException(status_code=500, detail="No data available")
        
        hmm_model = RegimeHMM(n_states=3)
        try:
            hmm_model.fit(df)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model fitting failed: {str(e)}")
    
    return hmm_model

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    Returns:
        Dict[str, str]: Health status.
    """
    return {"status": "ok"}

@app.get("/regime/latest", response_model=RegimeResponse)
async def get_latest_regime() -> RegimeResponse:
    """
    Get latest regime probabilities.
    Returns:
        RegimeResponse: Current regime probabilities.
    """
    try:
        model = get_or_create_model()
        df = get_latest_df()
        
        if df.empty:
            raise HTTPException(status_code=500, detail="No data available")
        
        # Use last 30 days for prediction
        tail_df = df.tail(30)
        probs = model.predict_proba(tail_df)
        
        return RegimeResponse(
            bull_probability=float(probs[0]),
            bear_probability=float(probs[1]),
            sideways_probability=float(probs[2]),
            timestamp=str(df.index[-1])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signal/latest", response_model=SignalResponse)
async def get_latest_signal() -> SignalResponse:
    """
    Get latest trading signal.
    Returns:
        SignalResponse: Current trading signal.
    """
    try:
        model = get_or_create_model()
        df = get_latest_df()
        
        if df.empty:
            raise HTTPException(status_code=500, detail="No data available")
        
        # Use last 30 days for prediction
        tail_df = df.tail(30)
        probs = model.predict_proba(tail_df)
        
        # Generate signal using last 200 days for strategy calculation
        strategy_df = df.tail(200)
        signal_data = generate_signal(probs, strategy_df)
        
        return SignalResponse(
            action=signal_data["action"],
            confidence=signal_data["confidence"],
            regime_probs=signal_data["regime_probs"],
            weighted_signal=signal_data["weighted_signal"],
            timestamp=str(df.index[-1])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backtest", response_model=BacktestResponse)
async def get_backtest_results(years: int = 10) -> BacktestResponse:
    """
    Get backtest results.
    Args:
        years (int): Number of years to backtest.
    Returns:
        BacktestResponse: Backtest results.
    """
    try:
        results = run_backtest(years=years, lookback_years = 3)
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return BacktestResponse(
            strategy_metrics=results["strategy_metrics"],
            benchmark_metrics=results["benchmark_metrics"],
            strategy_cumulative=results["strategy_cumulative"],
            benchmark_cumulative=results["benchmark_cumulative"],
            dates=results["dates"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))