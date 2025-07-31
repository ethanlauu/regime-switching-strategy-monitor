# Regime-Switching Trading Engine with Hidden-Markov-Model (HMM)

A Python-based backend trading engine that uses Gaussian Hidden Markov Models to detect market regimes and generate trading signals, with a React frontend for visualization.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   AWS Services  │
│                 │    │                 │    │                 │
│ • Dashboard     │◄──►│ • Data Layer    │◄──►│ • Lambda        │
│ • Charts        │    │ • Model Layer   │    │ • API Gateway   │
│ • Signals       │    │ • Strategy Layer│    │ • DynamoDB      │
│ • Backtesting   │    │ • Backtest Layer│    │ • CloudWatch    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Market Data    │
                       │                 │
                       │ • yfinance API  │
                       │ • OHLCV Data    │
                       │ • Local Cache   │
                       └─────────────────┘
```

## Backend Components

### Data Layer (`app/data_loader.py`)
- Fetches OHLCV data from yfinance API
- Caches data locally in parquet format
- Provides `get_latest_df()` for fresh data access

### Model Layer (`app/model.py`)
- `RegimeHMM` class with Gaussian HMM implementation
- Fits 3-regime model (bull, bear, sideways)
- Saves/loads model parameters to `/tmp/model.pkl`

### Strategy Layer (`app/strategies.py`)
- **Bull Strategy**: 50/200-day MA crossover trend-following
- **Bear Strategy**: RSI < 30 mean-reversion long
- **Sideways Strategy**: Option selling placeholder
- `generate_signal()` combines regime probabilities with strategies

### Backtest Layer (`app/backtest.py`)
- Rolling window HMM fitting
- Daily regime inference and strategy application
- Performance metrics calculation (Sharpe, drawdown, etc.)

### API Layer (`app/api.py`)
- FastAPI endpoints:
  - `GET /health` - Health check
  - `GET /regime/latest` - Current regime probabilities
  - `GET /signal/latest` - Latest trading signal
  - `GET /backtest?years=10` - Backtest results

## Local Development

### Prerequisites
- Python 3.11+
- Node.js & npm (for frontend)

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov=app --cov-report=html

# Start development server
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables
```bash
export SYMBOL=SPY  # Default trading symbol
export DYNAMODB_TABLE=trading-data-cache  # For AWS deployment
```

## AWS Deployment

### Prerequisites
- AWS CLI configured
- AWS SAM CLI installed
- Appropriate AWS permissions

### Deploy to AWS
```bash
# Build the application
sam build

# Deploy to AWS
sam deploy --guided

# Or deploy with existing configuration
sam deploy
```

### AWS Services Used
- **Lambda**: Python 3.11 runtime, 1024MB memory, 300s timeout
- **API Gateway**: REST API with CORS enabled
- **DynamoDB**: Data caching table with TTL
- **CloudWatch**: Logging and monitoring

### Environment Variables (AWS)
- `SYMBOL`: Trading symbol (default: SPY)
- `DYNAMODB_TABLE`: DynamoDB table name
- `PYTHONPATH`: Set to `/var/task` for Lambda

## API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "ok"}
```

### Latest Regime Probabilities
```bash
GET /regime/latest
Response: {
  "bull_probability": 0.6,
  "bear_probability": 0.2,
  "sideways_probability": 0.2,
  "timestamp": "2023-12-01 15:30:00"
}
```

### Latest Trading Signal
```bash
GET /signal/latest
Response: {
  "action": "BUY",
  "confidence": 0.75,
  "regime_probs": [0.6, 0.2, 0.2],
  "weighted_signal": 0.8,
  "timestamp": "2023-12-01 15:30:00"
}
```

### Backtest Results
```bash
GET /backtest?years=10
Response: {
  "strategy_metrics": {
    "annualized_return": 0.12,
    "sharpe_ratio": 1.2,
    "max_drawdown": -0.15,
    "volatility": 0.18
  },
  "benchmark_metrics": {...},
  "strategy_cumulative": [1.0, 1.05, ...],
  "benchmark_cumulative": [1.0, 1.03, ...],
  "dates": ["2023-01-01", ...]
}
```

## Testing

### Run All Tests
```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

### Test Coverage
- **Target**: >80% coverage
- **Coverage Report**: Generated in `htmlcov/` directory
- **Test Files**:
  - `tests/test_data_loader.py`
  - `tests/test_model.py`
  - `tests/test_strategies.py`

## Project Structure

```
regime-switching-strategy-monitor/
├── app/                          # Backend Python application
│   ├── data_loader.py           # Market data fetching and caching
│   ├── model.py                 # HMM regime detection
│   ├── strategies.py            # Trading strategies
│   ├── backtest.py              # Backtesting engine
│   ├── api.py                   # FastAPI endpoints
│   └── lambda_handler.py        # AWS Lambda handler
├── tests/                       # Test suite
│   ├── test_data_loader.py
│   ├── test_model.py
│   └── test_strategies.py
├── src/                         # React frontend
│   ├── components/
│   ├── pages/
│   └── services/
├── template.yaml                # AWS SAM template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure test coverage >80%
6. Submit a pull request

## License

This project is licensed under the MIT License.

---

