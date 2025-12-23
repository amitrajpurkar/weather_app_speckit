import { test, expect } from '@playwright/test';

test.describe('Yearly Overview', () => {
  test('loads page and displays yearly averages charts', async ({ page }) => {
    await page.route('**/api/v1/yearly-summary', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          year: 2024,
          months: [
            { month: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 2 },
            { month: 2, avg_temperature: 6, avg_humidity: 65, observation_count: 2 },
          ],
          total_observation_count: 4,
          months_with_data: [1, 2],
        }),
      });
    });

    await page.goto('/');
    // Wait for the main dashboard to load
    await expect(page.getByText('Weather Trends Dashboard')).toBeVisible();
    // Verify both charts are rendered
    await expect(page.getByText('Average Temperature by Month')).toBeVisible();
    await expect(page.getByText('Average Humidity by Month')).toBeVisible();
    // Verify a year is displayed (e.g., 2024)
    await expect(page.getByRole('heading', { name: /Yearly Averages for\s+\d{4}/i })).toBeVisible();
  });

  test('shows no-data message when backend returns empty', async ({ page }: any) => {
    // Mock scenario: intercept /api/v1/yearly-summary to return empty
    await page.route('**/api/v1/yearly-summary', (route: any) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          year: null,
          months: [],
          total_observation_count: 0,
          months_with_data: [],
        }),
      });
    });
    await page.goto('/');
    await expect(page.getByText('No data available')).toBeVisible();
  });
});
