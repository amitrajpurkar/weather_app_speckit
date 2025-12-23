import React from 'react';
import { render, screen } from '@testing-library/react';

import MonthlyTrendView from '../../components/MonthlyTrendView';

jest.mock('../../lib/apiClient', () => ({
  fetchMonthlyTrend: jest.fn(),
}));

import { fetchMonthlyTrend } from '../../lib/apiClient';

describe('MonthlyTrendView', () => {
  it('shows prompt when no month selected', () => {
    render(<MonthlyTrendView month={null} />);
    expect(screen.getByText(/select a month/i)).toBeInTheDocument();
  });

  it('renders data after fetch', async () => {
    (fetchMonthlyTrend as jest.Mock).mockResolvedValue({
      year: 2024,
      month: 1,
      daily_aggregates: [{ day: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 2 }],
      most_common_condition: 'clear',
    });

    render(<MonthlyTrendView month={1} />);

    expect(await screen.findByText(/most common condition/i)).toBeInTheDocument();
    expect(await screen.findByText(/clear/i)).toBeInTheDocument();
    expect(await screen.findByText(/Year:\s*2024/i)).toBeInTheDocument();
  });

  it('shows error when fetch fails', async () => {
    (fetchMonthlyTrend as jest.Mock).mockRejectedValue(new Error('Backend down'));

    render(<MonthlyTrendView month={1} />);

    expect(await screen.findByText(/Error:/i)).toBeInTheDocument();
    expect(await screen.findByText(/Backend down/i)).toBeInTheDocument();
  });
});
