import { useQuery } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { fetchTradeSignal } from "@/services/api";
import { Loader2, TrendingUp, TrendingDown, Minus } from "lucide-react";

export const TradeSignal = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['trade-signal'],
    queryFn: fetchTradeSignal,
    refetchInterval: 60000, // Refetch every minute for live signals
  });

  if (isLoading) {
    return (
      <div className="h-32 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-32 flex items-center justify-center text-destructive">
        Failed to load signal data
      </div>
    );
  }

  const getSignalColor = (action: string) => {
    switch (action) {
      case 'BUY':
        return 'profit';
      case 'SELL':
        return 'loss';
      default:
        return 'muted';
    }
  };

  const getSignalIcon = (action: string) => {
    switch (action) {
      case 'BUY':
        return <TrendingUp className="h-6 w-6" />;
      case 'SELL':
        return <TrendingDown className="h-6 w-6" />;
      default:
        return <Minus className="h-6 w-6" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-profit';
    if (confidence >= 0.6) return 'text-warning';
    return 'text-muted-foreground';
  };

  return (
    <div className="space-y-4">
      {/* Signal Action */}
      <Card className={`border-l-4 ${
        data?.action === 'BUY' ? 'border-l-profit' : 
        data?.action === 'SELL' ? 'border-l-loss' : 'border-l-muted'
      }`}>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`text-${getSignalColor(data?.action || 'HOLD')}`}>
                {getSignalIcon(data?.action || 'HOLD')}
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Current Signal</p>
                <p className="text-2xl font-bold">{data?.action}</p>
              </div>
            </div>
            <Badge 
              variant={data?.action === 'BUY' ? 'default' : data?.action === 'SELL' ? 'destructive' : 'secondary'}
              className="text-lg px-3 py-1"
            >
              {data?.action}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Confidence Level */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Signal Confidence</p>
              <p className={`text-2xl font-bold ${getConfidenceColor(data?.confidence || 0)}`}>
                {((data?.confidence || 0) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="w-16 h-16 relative">
              <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="hsl(var(--border))"
                  strokeWidth="2"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="hsl(var(--primary))"
                  strokeWidth="2"
                  strokeDasharray={`${(data?.confidence || 0) * 100}, 100`}
                />
              </svg>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Timestamp */}
      <p className="text-xs text-muted-foreground text-center">
        Last updated: {data?.timestamp ? new Date(data.timestamp).toLocaleTimeString() : 'N/A'}
      </p>
    </div>
  );
};