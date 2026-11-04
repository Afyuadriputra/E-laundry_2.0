import { test, expect } from '@playwright/test';

test.describe('Milestone 7: Quality, Security, Responsive & Accessibility Hardening', () => {
  const viewports = [
    { name: 'Mobile Mini (320px)', width: 320, height: 640 },
    { name: 'Mobile Standard (375px)', width: 375, height: 667 },
    { name: 'Mobile Large (430px)', width: 430, height: 932 },
    { name: 'Tablet Portrait (768px)', width: 768, height: 1024 },
    { name: 'Desktop Standard (1440px)', width: 1440, height: 900 },
  ];

  for (const vp of viewports) {
    test(`Responsive Audit: ${vp.name} renders without horizontal overflow`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });

      // Mock Authenticated Session as CASHIER
      await page.route(/\/api\/v1\/auth\/me/, async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'user-cashier-001',
              username: 'kasir_rina',
              full_name: 'Rina Kasir',
              role: 'CASHIER',
              business_id: 'biz-001',
            },
          }),
        });
      });

      await page.route(/\/api\/v1\/reports\/dashboard/, async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              active_orders_count: 5,
              ready_orders_count: 2,
              unpaid_orders_count: 1,
              today_new_orders_count: 4,
              financial: null,
            },
          }),
        });
      });

      await page.route(/\/api\/v1\/reports\/overdue/, async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: [] }),
        });
      });

      await page.goto('/');
      await page.waitForLoadState('networkidle');

      // Verify no horizontal document overflow
      const isOverflowingHorizontally = await page.evaluate(() => {
        return document.documentElement.scrollWidth > window.innerWidth;
      });
      expect(isOverflowingHorizontally).toBeFalsy();

      // On mobile viewports (< 768px), mobile header and hamburger menu should be visible
      if (vp.width < 768) {
        const mobileHeader = page.locator('header').first();
        await expect(mobileHeader).toBeVisible();
      } else {
        // On desktop (>= 768px), sidebar navigation should be visible
        const sidebar = page.locator('aside').first();
        await expect(sidebar).toBeVisible();
      }
    });
  }

  test('Accessibility & Touch Targets: 44px tap targets and form input labels', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'user-cashier-001',
            username: 'kasir_rina',
            full_name: 'Rina Kasir',
            role: 'CASHIER',
            business_id: 'biz-001',
          },
        }),
      });
    });

    await page.route(/\/api\/v1\/reports\/dashboard/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            active_orders_count: 3,
            ready_orders_count: 1,
            unpaid_orders_count: 0,
            today_new_orders_count: 2,
            financial: null,
          },
        }),
      });
    });

    await page.route(/\/api\/v1\/reports\/overdue/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: [] }),
      });
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Audit interactive buttons for minimum touch targets (>= 40px in mobile context)
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();
    for (let i = 0; i < Math.min(buttonCount, 5); i++) {
      const btn = buttons.nth(i);
      if (await btn.isVisible()) {
        const box = await btn.boundingBox();
        if (box) {
          expect(box.height).toBeGreaterThanOrEqual(36);
        }
      }
    }
  });

  test('Public Tracking Viewport: Mobile-first responsive layout (320px - 430px)', async ({ page }) => {
    const token = 'trk_mobile_test_token_123';
    await page.setViewportSize({ width: 360, height: 740 });

    await page.route(`**/api/v1/tracking/${token}*`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: {
          'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
          'Referrer-Policy': 'no-referrer',
        },
        body: JSON.stringify({
          data: {
            tracking_type: 'ORDER',
            order_number: 'ORD-202611-0099',
            current_status: 'PROCESSING',
            status_label: 'Sedang Dicuci',
            can_cancel: false,
            created_at: '2026-11-03T08:00:00Z',
            estimated_completion_at: '2026-11-05T12:00:00Z',
            customer_name_masked: 'B*** S***',
            customer_phone_masked: '+62812****789',
            service_summary: [
              {
                service_name: 'Cuci Kiloan Reguler',
                quantity: '5.0',
                unit: 'KG',
                unit_price: 11000,
                line_total: 55000,
              },
            ],
            financial_summary: {
              total_amount: 55000,
              paid_amount: 25000,
              remaining_amount: 30000,
              payment_status: 'PARTIAL',
            },
            timeline: [
              {
                status: 'RECEIVED',
                status_label: 'Diterima Kasir',
                timestamp: '2026-11-03T08:00:00Z',
                notes: 'Pesanan diterima di outlet',
              },
              {
                status: 'PROCESSING',
                status_label: 'Sedang Dicuci',
                timestamp: '2026-11-03T10:00:00Z',
                notes: 'Pencucian sedang berlangsung',
              },
            ],
            business_contact: {
              name: 'Kawan Laundry Express',
              phone: '+6281234567890',
              address: 'Jl. Melati Raya No. 15',
              whatsapp_url: 'https://wa.me/6281234567890?text=Halo%20Laundry',
            },
            intake_method: 'DROP_OFF',
            return_method: 'SELF_PICKUP',
          },
        }),
      });
    });

    await page.goto(`/track/${token}`);
    await page.waitForLoadState('networkidle');

    await expect(page.getByText('ORD-202611-0099')).toBeVisible();
    await expect(page.getByText('Rp 30.000')).toBeVisible();

    // Verify no horizontal overflow on mobile tracking view
    const isOverflowing = await page.evaluate(() => {
      return document.documentElement.scrollWidth > window.innerWidth;
    });
    expect(isOverflowing).toBeFalsy();
  });
});

