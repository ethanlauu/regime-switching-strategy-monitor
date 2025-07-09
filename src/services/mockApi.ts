// Mock API data for development
export interface RegimeData {
  regime: string;
  prob: number;
  color: string;
}

export interface TradeSignalData {
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  timestamp: string;
}

export interface EquityPoint {
  date: string;
  equity: number;
  benchmark: number;
}

export interface PerformanceMetrics {
  cagr: number;
  sharpe: number;
  max_dd: number;
  win_rate: number;
  total_trades: number;
}

// Simulate API delays
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const fetchRegimeData = async (): Promise<RegimeData[]> => {
  await delay(300);
  return [
    { regime: 'Bull Market', prob: 0.65, color: 'hsl(var(--chart-2))' },
    { regime: 'Bear Market', prob: 0.15, color: 'hsl(var(--chart-5))' },
    { regime: 'Sideways', prob: 0.20, color: 'hsl(var(--chart-3))' }
  ];
};

export const fetchTradeSignal = async (): Promise<TradeSignalData> => {
  await delay(200);
  return {
    action: 'BUY',
    confidence: 0.82,
    timestamp: new Date().toISOString()
  };
};

export const fetchEquityCurve = async (): Promise<EquityPoint[]> => {
  await delay(500);
  
  // Generate realistic equity curve data
  const data: EquityPoint[] = [];
  const startDate = new Date('2014-01-01');
  const endDate = new Date();
  
  let equity = 100000;
  let benchmark = 100000;
  
  for (let d = new Date(startDate); d <= endDate; d.setMonth(d.getMonth() + 1)) {
    // Simulate strategy outperformance with some volatility
    const strategyReturn = (Math.random() - 0.45) * 0.04 + 0.008; // Slight positive bias
    const benchmarkReturn = (Math.random() - 0.48) * 0.035 + 0.007; // Market return
    
    equity *= (1 + strategyReturn);
    benchmark *= (1 + benchmarkReturn);
    
    data.push({
      date: d.toISOString().split('T')[0],
      equity: Math.round(equity),
      benchmark: Math.round(benchmark)
    });
  }
  
  return data;
};

export const fetchPerformanceMetrics = async (): Promise<PerformanceMetrics> => {
  await delay(400);
  return {
    cagr: 0.124, // 12.4%
    sharpe: 1.85,
    max_dd: -0.089, // -8.9%
    win_rate: 0.67, // 67%
    total_trades: 342
  };
};