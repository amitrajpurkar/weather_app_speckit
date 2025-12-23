import { test, expect } from '@playwright/test';

test.describe('Monthly Trend', () => {
  test('selecting a month shows monthly trend view', async ({ page }) => {
    await page.route('**/api/v1/yearly-summary', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          year: 2024,
          months: [
            { month: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 2 },
            { month: 2, avg_temperature: null, avg_humidity: null, observation_count: 0 },
          ],
        }),
      });
    });

    await page.route('**/api/v1/monthly-trend?month=1', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          year: 2024,
          month: 1,
          daily_aggregates: [{ day: 1, avg_temperature: 5, avg_humidity: 70, observation_count: 2 }],
          most_common_condition: 'clear',
        }),
      });
    });

    await page.goto('/');

    await expect(page.getByText('Weather Trends Dashboard')).toBeVisible();

    await page.selectOption('#month-select', '1');

    await expect(page.getByText(/Most common condition/i)).toBeVisible();
    await expect(page.getByText('clear')).toBeVisible();
  });
});
