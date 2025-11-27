'use client';

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

import { YearlySummaryResponse } from '../src/lib/apiClient';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  data: YearlySummaryResponse;
}

const monthLabels = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
];

export default function YearlyAveragesChart({ data }: Props) {
  if (!data.year || data.months.length === 0) {
    return <div>No data available</div>;
  }

  const temperatureData = {
    labels: monthLabels,
    datasets: [
      {
        label: 'Avg Temperature (°C)',
        data: data.months.map(m => m.avg_temperature ?? null),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        tension: 0.1,
      },
    ],
  };

  const humidityData = {
    labels: monthLabels,
    datasets: [
      {
        label: 'Avg Humidity (%)',
        data: data.months.map((m: any) => m.avg_humidity ?? null),
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Yearly Averages for {data.year}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="text-lg font-semibold mb-2">Average Temperature by Month</h3>
          <Line data={temperatureData} options={chartOptions} />
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2">Average Humidity by Month</h3>
          <Line data={humidityData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}
