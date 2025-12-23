import React from 'react';
import { render, screen } from '@testing-library/react';

import DataAssumptions from '../../components/DataAssumptions';
import { YearlySummaryResponse } from '../../lib/apiClient';

describe('DataAssumptions', () => {
  it('renders data source, year, and coverage metadata', () => {
    const data: YearlySummaryResponse = {
      year: 2024,
      months: [
        { month: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 2 },
        { month: 2, avg_temperature: null, avg_humidity: null, observation_count: 0 },
      ],
      total_observation_count: 2,
      months_with_data: [1],
    };

    render(<DataAssumptions data={data} />);

    expect(screen.getByRole('heading', { name: /data assumptions/i })).toBeInTheDocument();
    expect(screen.getByText(/WeatherData\.csv/i)).toBeInTheDocument();
    expect(screen.getByText(/Selected year:/i)).toBeInTheDocument();
    expect(screen.getByText(/2024/i)).toBeInTheDocument();
    expect(screen.getByText(/total observations/i)).toBeInTheDocument();
    expect(screen.getByText(/^2$/)).toBeInTheDocument();
    expect(screen.getByText(/\(1\)/)).toBeInTheDocument();
  });

  it('shows None when there are no months_with_data', () => {
    const data: YearlySummaryResponse = {
      year: 2024,
      months: [],
      total_observation_count: 0,
      months_with_data: [],
    };

    render(<DataAssumptions data={data} />);

    expect(screen.getByText(/months with data \(None\)/i)).toBeInTheDocument();
  });
});
