'use client';

import React, { useEffect, useMemo, useState } from 'react';

import { fetchMonthlyTrend, MonthlyTrendResponse } from '../lib/apiClient';

interface Props {
  month: number | null;
}

export default function MonthlyTrendView({ month }: Props) {
  const [data, setData] = useState<MonthlyTrendResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!month) {
      setData(null);
      setError(null);
      return;
    }

    setLoading(true);
    fetchMonthlyTrend(month)
      .then((d: MonthlyTrendResponse) => {
        setData(d);
        setError(null);
      })
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error';
        setError(message);
        setData(null);
      })
      .finally(() => setLoading(false));
  }, [month]);

  const title = useMemo(() => {
    if (!month) return 'Monthly trend';
    return `Monthly trend for month ${month}`;
  }, [month]);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-2">{title}</h2>

      {!month && <div className="text-gray-600">Select a month to view trends.</div>}

      {loading && <div>Loading...</div>}

      {error && <div className="text-red-500">Error: {error}</div>}

      {data && (
        <div>
          <div className="mb-4">
            <div className="text-sm text-gray-700">Year: {data.year}</div>
            <div className="text-sm text-gray-700">
              Most common condition: {data.most_common_condition ?? 'N/A'}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-200 bg-white">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left p-2 border-b">Day</th>
                  <th className="text-left p-2 border-b">Avg Temp</th>
                  <th className="text-left p-2 border-b">Avg Humidity</th>
                  <th className="text-left p-2 border-b">Obs</th>
                </tr>
              </thead>
              <tbody>
                {data.daily_aggregates.map((d) => (
                  <tr key={d.day}>
                    <td className="p-2 border-b">{d.day}</td>
                    <td className="p-2 border-b">{d.avg_temperature ?? 'N/A'}</td>
                    <td className="p-2 border-b">{d.avg_humidity ?? 'N/A'}</td>
                    <td className="p-2 border-b">{d.observation_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
