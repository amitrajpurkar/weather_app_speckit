import { fetchMonthlyTrend, fetchYearlySummary } from '../../lib/apiClient';

describe('apiClient', () => {
  const originalEnv = process.env;
  const originalFetch = global.fetch;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
    global.fetch = jest.fn();
  });

  afterEach(() => {
    process.env = originalEnv;
    global.fetch = originalFetch;
  });

  it('fetchYearlySummary uses relative URL when NEXT_PUBLIC_API_BASE_URL is not set', async () => {
    delete process.env.NEXT_PUBLIC_API_BASE_URL;

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        year: 2024,
        months: [],
        total_observation_count: 0,
        months_with_data: [],
      }),
    });

    await fetchYearlySummary();
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/yearly-summary');
  });

  it('fetchYearlySummary uses NEXT_PUBLIC_API_BASE_URL when set', async () => {
    process.env.NEXT_PUBLIC_API_BASE_URL = 'http://localhost:8000';

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        year: 2024,
        months: [],
        total_observation_count: 0,
        months_with_data: [],
      }),
    });

    await fetchYearlySummary();
    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/yearly-summary');
  });

  it('fetchYearlySummary throws descriptive error on non-200', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      text: async () => 'boom',
    });

    await expect(fetchYearlySummary()).rejects.toThrow(
      'Failed to fetch yearly summary: 500 Internal Server Error - boom'
    );
  });

  it('fetchMonthlyTrend calls the correct URL and returns JSON', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        year: 2024,
        month: 1,
        daily_aggregates: [],
        most_common_condition: null,
      }),
    });

    await fetchMonthlyTrend(1);
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/monthly-trend?month=1');
  });

  it('fetchMonthlyTrend throws descriptive error on non-200', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 404,
      statusText: 'Not Found',
      text: async () => '',
    });

    await expect(fetchMonthlyTrend(12)).rejects.toThrow(
      'Failed to fetch monthly trend: 404 Not Found'
    );
  });
});
