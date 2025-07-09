import { useQuery } from "@tanstack/react-query";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { fetchRegimeData } from "@/services/mockApi";
import { Loader2 } from "lucide-react";

export const RegimeProbabilityChart = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['regime-probabilities'],
    queryFn: fetchRegimeData,
    refetchInterval: 30000, // Refetch every 30 seconds for live data
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
        Failed to load regime data
      </div>
    );
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
          <p className="font-medium">{data.regime}</p>
          <p className="text-primary">
            Probability: {(data.prob * 100).toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ regime, prob }) => `${regime}: ${(prob * 100).toFixed(1)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="prob"
          >
            {data?.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};