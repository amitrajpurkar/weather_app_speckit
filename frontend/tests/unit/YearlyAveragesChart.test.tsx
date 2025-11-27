import React from 'react';
import { render, screen } from '@testing-library/react';
import YearlyAveragesChart from '../../components/YearlyAveragesChart';
import { YearlySummaryResponse } from '../../lib/apiClient';

const mockData: YearlySummaryResponse = {
  year: 2024,
  months: [
    { month: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 62 },
    { month: 2, avg_temperature: 6, avg_humidity: 65, observation_count: 57 },
    { month: 3, avg_temperature: 10, avg_humidity: 60, observation_count: 62 },
    { month: 4, avg_temperature: 14, avg_humidity: 55, observation_count: 60 },
    { month: 5, avg_temperature: 18, avg_humidity: 58, observation_count: 62 },
    { month: 6, avg_temperature: 22, avg_humidity: 62, observation_count: 60 },
    { month: 7, avg_temperature: 25, avg_humidity: 65, observation_count: 62 },
    { month: 8, avg_temperature: 24, avg_humidity: 68, observation_count: 62 },
    { month: 9, avg_temperature: 20, avg_humidity: 70, observation_count: 60 },
    { month: 10, avg_temperature: 15, avg_humidity: 72, observation_count: 62 },
    { month: 11, avg_temperature: 10, avg_humidity: 75, observation_count: 60 },
    { month: 12, avg_temperature: 6, avg_humidity: 78, observation_count: 62 },
  ],
};

describe('YearlyAveragesChart', () => {
  it('renders two chart containers', () => {
    render(<YearlyAveragesChart data={mockData} />);
    expect(screen.getByText(/Average Temperature by Month/i)).toBeInTheDocument();
    expect(screen.getByText(/Average Humidity by Month/i)).toBeInTheDocument();
  });

  it('displays the correct year in the title', () => {
    render(<YearlyAveragesChart data={mockData} />);
    expect(screen.getByText(/2024/i)).toBeInTheDocument();
  });

  it('renders without crashing when data is empty', () => {
    const emptyData: YearlySummaryResponse = { year: null, months: [] };
    render(<YearlyAveragesChart data={emptyData} />);
    expect(screen.getByText(/No data available/i)).toBeInTheDocument();
  });
});
