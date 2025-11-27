import { test, expect } from '@playwright/test';

test.describe('Yearly Overview', () => {
  test('loads page and displays yearly averages charts', async ({ page }) => {
    await page.goto('/');
    // Wait for the main dashboard to load
    await expect(page.getByText('Weather Trends Dashboard')).toBeVisible();
    // Verify both charts are rendered
    await expect(page.getByText('Average Temperature by Month')).toBeVisible();
    await expect(page.getByText('Average Humidity by Month')).toBeVisible();
    // Verify a year is displayed (e.g., 2024)
    await expect(page.locator('h2')).toContainText(/\d{4}/);
  });

  test('shows no-data message when backend returns empty', async ({ page }: any) => {
    // Mock scenario: intercept /api/v1/yearly-summary to return empty
    await page.route('**/api/v1/yearly-summary', (route: any) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ year: null, months: [] }),
      });
    });
    await page.goto('/');
    await expect(page.getByText('No data available')).toBeVisible();
  });
});
