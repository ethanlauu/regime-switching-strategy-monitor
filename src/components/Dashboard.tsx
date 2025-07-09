import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { RegimeProbabilityChart } from "./RegimeProbabilityChart";
import { EquityCurveChart } from "./EquityCurveChart";
import { TradeSignal } from "./TradeSignal";
import { PerformanceMetrics } from "./PerformanceMetrics";
import { TrendingUp, Activity, Target, BarChart3 } from "lucide-react";

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Regime-Switching Strategy Monitor
          </h1>
          <p className="text-lg text-muted-foreground">
            Real-time HMM-driven trading strategy performance and regime analysis
          </p>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Live Regime Probabilities */}
          <Card className="shadow-elevated hover:shadow-glow transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
              <div className="flex items-center space-x-2">
                <Activity className="h-5 w-5 text-primary" />
                <CardTitle className="text-xl">Current Regime Probabilities</CardTitle>
              </div>
              <Badge variant="outline" className="ml-auto">
                Live
              </Badge>
            </CardHeader>
            <CardContent>
              <RegimeProbabilityChart />
            </CardContent>
          </Card>

          {/* Live Trade Signal */}
          <Card className="shadow-elevated hover:shadow-glow transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
              <div className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-primary" />
                <CardTitle className="text-xl">Latest Trade Signal</CardTitle>
              </div>
              <Badge variant="outline" className="ml-auto">
                Updated 2m ago
              </Badge>
            </CardHeader>
            <CardContent>
              <TradeSignal />
            </CardContent>
          </Card>

          {/* Back-test Performance */}
          <Card className="shadow-elevated hover:shadow-glow transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                <CardTitle className="text-xl">Back-test Performance (10 yr)</CardTitle>
              </div>
              <Badge variant="secondary" className="ml-auto">
                Historical
              </Badge>
            </CardHeader>
            <CardContent>
              <EquityCurveChart />
            </CardContent>
          </Card>

          {/* Key Metrics */}
          <Card className="shadow-elevated hover:shadow-glow transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                <CardTitle className="text-xl">Performance Metrics</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <PerformanceMetrics />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;