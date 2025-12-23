'use client';

import React from 'react';

import { YearlySummaryResponse } from '../lib/apiClient';

interface Props {
  data: YearlySummaryResponse;
}

export default function DataAssumptions({ data }: Props) {
  const yearLabel = data.year ?? 'N/A';
  const monthsWithDataLabel = data.months_with_data.length
    ? data.months_with_data.join(', ')
    : 'None';

  return (
    <section className="p-4" aria-label="Data assumptions">
      <h2 className="text-2xl font-bold mb-2">Data assumptions</h2>
      <div className="text-sm text-gray-700 space-y-2">
        <p>
          Data source: Weather observations are loaded from a local CSV file
          (<code>src/main/resources/WeatherData.csv</code>).
        </p>
        <p>
          Selected year: <strong>{yearLabel}</strong>
        </p>
        <p>
          Coverage: <strong>{data.total_observation_count}</strong> total observations across
          months with data ({monthsWithDataLabel}).
        </p>
        <p>
          Averages: Monthly averages are computed from all valid observations in each month.
          Months with no observations are shown with empty values.
        </p>
        <p>
          Monthly trends: Daily aggregates are computed for the selected month, and the most
          common condition is derived from the month's observations.
        </p>
      </div>
    </section>
  );
}
