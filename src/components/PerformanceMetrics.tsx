import { useQuery } from "@tanstack/react-query";
import { Card, CardContent } from "@/components/ui/card";
import { fetchPerformanceMetrics } from "@/services/mockApi";
import { Loader2, TrendingUp, Activity, Target, BarChart3 } from "lucide-react";

export const PerformanceMetrics = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['performance-metrics'],
    queryFn: fetchPerformanceMetrics,
    refetchInterval: 300000, // Refetch every 5 minutes
  });

  if (isLoading) {
    return (
      <div className="h-64 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-64 flex items-center justify-center text-destructive">
        Failed to load performance metrics
      </div>
    );
  }

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const getValueColor = (value: number, isPositiveGood = true) => {
    if (isPositiveGood) {
      return value > 0 ? 'text-profit' : 'text-loss';
    } else {
      return value < 0 ? 'text-profit' : 'text-loss';
    }
  };

  const metrics = [
    {
      icon: <TrendingUp className="h-5 w-5" />,
      label: "Annual Return (CAGR)",
      value: formatPercentage(data?.cagr || 0),
      color: getValueColor(data?.cagr || 0),
      description: "Compound Annual Growth Rate"
    },
    {
      icon: <Activity className="h-5 w-5" />,
      label: "Sharpe Ratio",
      value: (data?.sharpe || 0).toFixed(2),
      color: (data?.sharpe || 0) > 1 ? 'text-profit' : 'text-warning',
      description: "Risk-adjusted returns"
    },
    {
      icon: <Target className="h-5 w-5" />,
      label: "Max Drawdown",
      value: formatPercentage(data?.max_dd || 0),
      color: getValueColor(data?.max_dd || 0, false),
      description: "Largest peak-to-trough decline"
    },
    {
      icon: <BarChart3 className="h-5 w-5" />,
      label: "Win Rate",
      value: formatPercentage(data?.win_rate || 0),
      color: (data?.win_rate || 0) > 0.6 ? 'text-profit' : 'text-warning',
      description: "Percentage of profitable trades"
    }
  ];

  return (
    <div className="space-y-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="text-primary">
                  {metric.icon}
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">{metric.label}</p>
                  <p className="text-xs text-muted-foreground">{metric.description}</p>
                </div>
              </div>
              <div className="text-right">
                <p className={`text-xl font-bold ${metric.color}`}>
                  {metric.value}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}

      {/* Additional Stats */}
      <Card className="border-dashed">
        <CardContent className="p-4">
          <div className="text-center">
            <p className="text-sm text-muted-foreground">Total Trades Executed</p>
            <p className="text-2xl font-bold text-primary">
              {data?.total_trades?.toLocaleString() || 0}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};