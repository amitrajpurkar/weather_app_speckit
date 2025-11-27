'use client';

import React, { useEffect, useState } from 'react';
import YearlyAveragesChart from '../components/YearlyAveragesChart';
import { fetchYearlySummary, YearlySummaryResponse } from '../src/lib/apiClient';

export default function HomePage() {
  const [data, setData] = useState<YearlySummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchYearlySummary()
      .then(setData)
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error';
        setError(message);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold text-gray-900">Weather Trends Dashboard</h1>
        </div>
      </header>
      <section>
        {data ? <YearlyAveragesChart data={data} /> : <div className="p-4">No data available</div>}
      </section>
    </main>
  );
}
