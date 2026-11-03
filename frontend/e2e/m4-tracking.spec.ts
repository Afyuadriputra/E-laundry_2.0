import { test, expect } from '@playwright/test';

test.describe('Milestone 4: Public Customer Tracking E2E', () => {
  const sampleToken = 'trk_test_token_cryptographic_entropy_256bit_12345';

  test.beforeEach(async ({ page }) => {
    let currentStatus = 'RECEIVED';
    let currentStatusLabel = 'Diterima Kasir';
    let canCancel = true;

    // Mock Public Tracking API
    await page.route(/\/api\/v1\/tracking\/trk_test_token_cryptographic_entropy_256bit_12345$/, async (route) => {
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
            order_number: 'ORD-20261103-0888',
            current_status: currentStatus,
            status_label: currentStatusLabel,
            can_cancel: canCancel,
            created_at: '2026-11-03T09:00:00Z',
            estimated_completion_at: '2026-11-04T09:00:00Z',
            customer_name_masked: 'I** R****',
            customer_phone_masked: '+62812****7899',
            service_summary: [
              {
                service_name: 'Cuci Setrika Reguler',
                quantity: '4.0',
                unit: 'KG',
                unit_price: 10000,
                line_total: 40000,
              },
            ],
            financial_summary: {
              total_amount: 40000,
              paid_amount: 0,
              remaining_amount: 40000,
              payment_status: 'UNPAID',
            },
            timeline: [
              {
                status: 'RECEIVED',
                status_label: 'Diterima Kasir',
                timestamp: '2026-11-03T09:00:00Z',
                note: 'Pesanan diterima di outlet',
              },
            ],
            business_contact: {
              name: 'Laundry Bersih Cemerlang',
              phone: '+6281234567890',
              address: 'Jl. Melati Raya No. 15, Jakarta Selatan',
              whatsapp_url: 'https://wa.me/6281234567890?text=Halo%20Laundry',
            },
            intake_method: 'DROP_OFF',
            return_method: 'SELF_PICKUP',
          },
          request_id: 'req-trk-sample',
        }),
      });
    });

    // Mock Public Cancellation API
    await page.route(/\/api\/v1\/tracking\/trk_test_token_cryptographic_entropy_256bit_12345\/cancel/, async (route) => {
      currentStatus = 'CANCELLED';
      currentStatusLabel = 'Pesanan Dibatalkan';
      canCancel = false;

      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            success: true,
            order_number: 'ORD-20261103-0888',
            new_status: 'CANCELLED',
            message: 'Pesanan Anda berhasil dibatalkan.',
            cancelled_at: new Date().toISOString(),
          },
          request_id: 'req-trk-cancel',
        }),
      });
    });
  });

  test('E2E: Unauthenticated Customer Tracking View, PII Masking, Progress Stepper & Read-Only Assistance (PRD §5.7 #9)', async ({ page }) => {
    // 1. Visit Public Tracking URL directly without auth cookies
    await page.goto(`/track/${sampleToken}`);

    // 2. Verify Outlet header and WhatsApp action
    await expect(page.locator('h1:has-text("Laundry Bersih Cemerlang")')).toBeVisible();
    await expect(page.locator('text=Pelacakan Pesanan Resmi')).toBeVisible();
    await expect(page.locator('a:has-text("Tanya Kasir")')).toBeVisible();

    // 3. Verify Order Number and Masked PII
    await expect(page.locator('h2:has-text("ORD-20261103-0888")')).toBeVisible();
    await expect(page.locator('text=Diterima Kasir').first()).toBeVisible();
    await expect(page.locator('text=I** R****')).toBeVisible();
    await expect(page.locator('text=+62812****7899')).toBeVisible();

    // 4. Verify Progress Stepper stages
    await expect(page.locator('text=Progres Pengerjaan')).toBeVisible();
    await expect(page.locator('text=Diterima').first()).toBeVisible();
    await expect(page.locator('text=Antrean').first()).toBeVisible();
    await expect(page.locator('text=Cuci').first()).toBeVisible();
    await expect(page.locator('text=Kering').first()).toBeVisible();
    await expect(page.locator('text=Setrika').first()).toBeVisible();
    await expect(page.locator('text=QC & Packing').first()).toBeVisible();
    await expect(page.locator('text=Siap Ambil').first()).toBeVisible();

    // 5. Verify Item Summary & Financial status
    await expect(page.locator('text=Cuci Setrika Reguler')).toBeVisible();
    await expect(page.locator('text=Rp 40.000').first()).toBeVisible();
    await expect(page.locator('text=BELUM LUNAS')).toBeVisible();

    // 6. Verify Read-Only Tracking Enforcement (PRD §5.7 #9: no customer state mutation)
    await expect(page.locator('button:has-text("Batalkan Pesanan Ini")')).not.toBeVisible();
    const contactBtn = page.locator('[data-testid="contact-cashier-btn"]');
    await expect(contactBtn).toBeVisible();
    await expect(contactBtn).toHaveAttribute('href', /wa\.me/);
    await expect(page.locator('text=Halaman pelacakan publik bersifat baca-saja')).toBeVisible();
  });
});

