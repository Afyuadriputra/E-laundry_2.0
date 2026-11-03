import { test, expect } from '@playwright/test';

test.describe('Milestone 6: Dashboard & Reporting E2E', () => {
  test('Owner dashboard displays live operational & financial KPIs with overdue alert', async ({
    page,
  }) => {
    // 1. Mock Authenticated Session as OWNER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u-owner-1',
            business_id: 'b-laundry-1',
            username: 'owner_hendra',
            full_name: 'Hendra Pemilik',
            role: 'OWNER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
        }),
      });
    });

    // 2. Mock Reports Dashboard API
    await page.route(/\/api\/v1\/reports\/dashboard(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            orders_count_today: 12,
            active_orders_count: 5,
            ready_orders_count: 3,
            completed_orders_today: 4,
            overdue_orders_count: 2,
            order_value_period: 600000,
            cash_received_period: 450000,
            expenses_period: 120000,
            simple_cash_difference: 330000,
            outstanding_receivables: 150000,
            start_date: '2026-11-03',
            end_date: '2026-11-03',
          },
        }),
      });
    });

    // 3. Mock Overdue Orders API
    await page.route(/\/api\/v1\/reports\/overdue/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: [
            {
              order_id: 'ord-ov-1',
              order_number: 'ORD-20261103-0888',
              customer_name: 'Pak Bambang',
              customer_phone: '+6281299887766',
              operational_status: 'WASHING',
              estimated_completion_at: '2026-11-02T10:00:00Z',
              hours_overdue: 24.5,
              total_amount: 50000,
              remaining_amount: 20000,
            },
          ],
        }),
      });
    });

    // Visit Dashboard
    await page.goto('/');

    // Verify Welcome Greeting
    await expect(page.locator('text=Selamat datang, Hendra Pemilik')).toBeVisible();

    // Verify Overdue Alert
    await expect(page.locator('text=Peringatan: 1 Pesanan Terlambat!')).toBeVisible();

    // Verify Financial KPIs
    await expect(page.locator('text=Rp 450.000')).toBeVisible(); // Uang Masuk Diterima
    await expect(page.locator('text=Rp 600.000')).toBeVisible(); // Nilai Pesanan Baru
    await expect(page.locator('text=Rp 120.000')).toBeVisible(); // Pengeluaran
    await expect(page.locator('text=Rp 330.000')).toBeVisible(); // Selisih Kas Bersih

    // Verify Operational KPIs
    await expect(page.getByText('12', { exact: true })).toBeVisible(); // Pesanan Baru
    await expect(page.getByText('5', { exact: true })).toBeVisible();  // Sedang Diproses
    await expect(page.getByText('3', { exact: true })).toBeVisible();  // Siap Diambil
  });

  test('Owner accesses Reports center, inspects finances, orders, and downloads CSV', async ({
    page,
  }) => {
    // Mock Session as OWNER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u-owner-1',
            business_id: 'b-laundry-1',
            username: 'owner_hendra',
            full_name: 'Hendra Pemilik',
            role: 'OWNER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
        }),
      });
    });

    await page.route(/\/api\/v1\/reports\/dashboard(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: { orders_count_today: 1 } }),
      });
    });

    await page.route(/\/api\/v1\/reports\/overdue/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: [] }),
      });
    });

    // Mock Finances Report
    await page.route(/\/api\/v1\/reports\/finances(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            start_date: '2026-11-03',
            end_date: '2026-11-03',
            total_cash_received: 350000,
            cash_by_method: { CASH: 200000, QRIS: 150000 },
            total_expenses: 80000,
            expenses_by_category: { DETERGENT: 50000, PACKAGING: 30000 },
            simple_cash_difference: 270000,
            outstanding_receivables: 60000,
          },
        }),
      });
    });

    // Mock Orders Report
    await page.route(/\/api\/v1\/reports\/orders(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            total_orders: 1,
            total_amount: 50000,
            total_paid: 30000,
            total_outstanding: 20000,
            items: [
              {
                order_id: 'ord-rep-1',
                order_number: 'ORD-20261103-0555',
                created_at: new Date().toISOString(),
                customer_name: 'Ibu Fatimah',
                customer_phone: '+6281233445566',
                operational_status: 'WASHING',
                payment_status: 'PARTIALLY_PAID',
                total_amount: 50000,
                paid_amount: 30000,
                remaining_amount: 20000,
                items_summary: 'Cuci Setrika (5 KG)',
              },
            ],
          },
        }),
      });
    });

    // Mock Outstanding Report
    await page.route(/\/api\/v1\/reports\/outstanding/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: [
            {
              order_id: 'ord-rep-1',
              order_number: 'ORD-20261103-0555',
              created_at: new Date().toISOString(),
              customer_name: 'Ibu Fatimah',
              customer_phone: '+6281233445566',
              total_amount: 50000,
              paid_amount: 30000,
              remaining_amount: 20000,
              payment_status: 'PARTIALLY_PAID',
              operational_status: 'WASHING',
            },
          ],
        }),
      });
    });

    // Mock CSV endpoints
    await page.route(/\/api\/v1\/reports\/export\/payments\.csv(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'text/csv',
        body: 'ID Pembayaran,Waktu,Metode,Jumlah\np-1,2026-11-03,CASH,200000\n',
      });
    });

    await page.goto('/');

    // Click "Laporan" tab
    await page.locator('button:has-text("Laporan")').first().click();

    // Verify Financial Overview
    await expect(page.locator('text=Rp 350.000')).toBeVisible(); // Total Uang Masuk
    await expect(page.locator('text=Rp 80.000')).toBeVisible();  // Total Pengeluaran
    await expect(page.locator('text=Rp 270.000')).toBeVisible(); // Selisih Kas Bersih
    await expect(page.locator('text=DETERGENT')).toBeVisible();

    // Trigger CSV Download
    const downloadPaymentsBtn = page.locator('button', { hasText: 'Unduh CSV Pembayaran' });
    await expect(downloadPaymentsBtn).toBeVisible();
    await downloadPaymentsBtn.click();
    await expect(page.locator('text=berhasil diunduh')).toBeVisible();

    // Switch to Orders Report Tab
    await page.locator('button:has-text("Laporan Pesanan")').click();
    await expect(page.locator('text=ORD-20261103-0555')).toBeVisible();
    await expect(page.locator('text=Ibu Fatimah')).toBeVisible();
    await expect(page.locator('span', { hasText: 'PARTIALLY_PAID' })).toBeVisible();

    // Switch to Outstanding Balances Tab
    await page.locator('button:has-text("Tagihan Belum Lunas (Piutang)")').click();
    await expect(page.locator('text=Sisa Rp 20.000')).toBeVisible();
    await expect(page.locator('text=Ingatkan via WA')).toBeVisible();
  });

  test('Cashier has role-gated operational dashboard without financial KPIs', async ({
    page,
  }) => {
    // Mock Session as CASHIER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u-cashier-1',
            business_id: 'b-laundry-1',
            username: 'kasir_maya',
            full_name: 'Maya Kasir',
            role: 'CASHIER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
        }),
      });
    });

    // Mock Dashboard for Cashier (financial KPIs are null)
    await page.route(/\/api\/v1\/reports\/dashboard(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            orders_count_today: 7,
            active_orders_count: 4,
            ready_orders_count: 2,
            completed_orders_today: 1,
            overdue_orders_count: 0,
            order_value_period: null,
            cash_received_period: null,
            expenses_period: null,
            simple_cash_difference: null,
            outstanding_receivables: null,
            start_date: '2026-11-03',
            end_date: '2026-11-03',
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

    // Cashier sees operational counts
    await expect(page.getByText('7', { exact: true })).toBeVisible();
    await expect(page.getByText('4', { exact: true })).toBeVisible();
    await expect(page.getByText('2', { exact: true })).toBeVisible();

    // Financial KPIs section is NOT visible to Cashier
    await expect(page.locator('text=Kinerja Finansial Hari Ini')).not.toBeVisible();
    await expect(page.locator('text=Uang Masuk Diterima')).not.toBeVisible();
  });
});
