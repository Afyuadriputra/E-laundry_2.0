import { test, expect } from '@playwright/test';

test.describe('Milestone 2: Core Laundry Operations E2E', () => {
  test.beforeEach(async ({ page }) => {
    // 1. Mock Authenticated Session as CASHIER
    await page.route('**/api/v1/auth/me', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'c1111111-1111-1111-1111-111111111111',
            business_id: 'b1111111-1111-1111-1111-111111111111',
            username: 'kasir_budi',
            full_name: 'Budi Kasir',
            role: 'CASHIER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
          request_id: 'req-e2e-auth',
        }),
      });
    });

    // 2. Mock Services Catalog
    await page.route(/\/api\/v1\/services/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: [
            {
              id: 's1111111-1111-1111-1111-111111111111',
              business_id: 'b1111111-1111-1111-1111-111111111111',
              name: 'Cuci Setrika Reguler',
              pricing_type: 'PER_KG',
              unit: 'KG',
              unit_price: 10000,
              estimated_hours: 24,
              requires_ironing: true,
              is_active: true,
              version: 1,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            },
          ],
          request_id: 'req-e2e-services',
        }),
      });
    });

    // 3. Mock Customers List
    await page.route(/\/api\/v1\/customers/, async (route) => {
      if (route.request().method() === 'POST') {
        const body = JSON.parse(route.request().postData() || '{}');
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'cust-new-id',
              business_id: 'b1111111-1111-1111-1111-111111111111',
              full_name: body.full_name || 'Pelanggan Baru',
              phone_e164: '+6281234567899',
              address: body.address || 'Jl. Melati',
              notes: body.notes || '',
              is_active: true,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              total_orders: 0,
            },
            request_id: 'req-e2e-cust-create',
          }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: [
              {
                id: 'c2222222-2222-2222-2222-222222222222',
                business_id: 'b1111111-1111-1111-1111-111111111111',
                full_name: 'Ibu Ratna',
                phone_e164: '+6281234567899',
                address: 'Jl. Melati No. 10',
                is_active: true,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
                total_orders: 2,
              },
            ],
            request_id: 'req-e2e-cust-list',
          }),
        });
      }
    });

    // 4. Mock Orders API
    let currentOrderStatus = 'RECEIVED';
    let currentOrderVersion = 1;

    await page.route(/\/api\/v1\/orders/, async (route) => {
      const url = route.request().url();
      const method = route.request().method();

      if (url.includes('/transition') && method === 'POST') {
        const body = JSON.parse(route.request().postData() || '{}');
        currentOrderStatus = body.to_status;
        currentOrderVersion += 1;

        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'ord-123',
              business_id: 'b1111111-1111-1111-1111-111111111111',
              order_number: 'ORD-20261103-0001',
              customer_id: 'c2222222-2222-2222-2222-222222222222',
              customer: {
                id: 'c2222222-2222-2222-2222-222222222222',
                full_name: 'Ibu Ratna',
                phone_e164: '+6281234567899',
                address: 'Jl. Melati No. 10',
                is_active: true,
              },
              operational_status: currentOrderStatus,
              intake_method: 'DROP_OFF',
              return_method: 'SELF_PICKUP',
              subtotal_amount: 30000,
              extra_charge_amount: 0,
              delivery_fee_amount: 0,
              total_amount: 30000,
              estimated_completion_at: new Date().toISOString(),
              version: currentOrderVersion,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              items: [
                {
                  id: 'item-1',
                  service_id: 's1111111-1111-1111-1111-111111111111',
                  service_name_snapshot: 'Cuci Setrika Reguler',
                  pricing_type_snapshot: 'PER_KG',
                  unit_snapshot: 'KG',
                  quantity: '2.5',
                  unit_price_snapshot: 10000,
                  line_total_amount: 30000,
                  requires_ironing_snapshot: true,
                  created_at: new Date().toISOString(),
                },
              ],
              status_history: [
                {
                  id: 'hist-1',
                  from_status: null,
                  to_status: 'RECEIVED',
                  changed_by: 'c1111111-1111-1111-1111-111111111111',
                  reason: 'Pesanan dibuat',
                  created_at: new Date().toISOString(),
                },
                {
                  id: 'hist-2',
                  from_status: 'RECEIVED',
                  to_status: currentOrderStatus,
                  changed_by: 'c1111111-1111-1111-1111-111111111111',
                  reason: 'Transisi status',
                  created_at: new Date().toISOString(),
                },
              ],
            },
            request_id: 'req-e2e-order-transition',
          }),
        });
      } else if (url.includes('/orders/ord-123') && method === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'ord-123',
              business_id: 'b1111111-1111-1111-1111-111111111111',
              order_number: 'ORD-20261103-0001',
              customer_id: 'c2222222-2222-2222-2222-222222222222',
              customer: {
                id: 'c2222222-2222-2222-2222-222222222222',
                full_name: 'Ibu Ratna',
                phone_e164: '+6281234567899',
                address: 'Jl. Melati No. 10',
                is_active: true,
              },
              operational_status: currentOrderStatus,
              intake_method: 'DROP_OFF',
              return_method: 'SELF_PICKUP',
              subtotal_amount: 30000,
              extra_charge_amount: 0,
              delivery_fee_amount: 0,
              total_amount: 30000,
              estimated_completion_at: new Date().toISOString(),
              version: currentOrderVersion,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              items: [
                {
                  id: 'item-1',
                  service_id: 's1111111-1111-1111-1111-111111111111',
                  service_name_snapshot: 'Cuci Setrika Reguler',
                  pricing_type_snapshot: 'PER_KG',
                  unit_snapshot: 'KG',
                  quantity: '2.5',
                  unit_price_snapshot: 10000,
                  line_total_amount: 30000,
                  requires_ironing_snapshot: true,
                  created_at: new Date().toISOString(),
                },
              ],
              status_history: [
                {
                  id: 'hist-1',
                  from_status: null,
                  to_status: 'RECEIVED',
                  changed_by: 'c1111111-1111-1111-1111-111111111111',
                  reason: 'Pesanan dibuat',
                  created_at: new Date().toISOString(),
                },
              ],
            },
            request_id: 'req-e2e-order-detail',
          }),
        });
      } else if (method === 'POST') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'ord-123',
            },
            request_id: 'req-e2e-order-create',
          }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: [
              {
                id: 'ord-123',
                business_id: 'b1111111-1111-1111-1111-111111111111',
                order_number: 'ORD-20261103-0001',
                customer_id: 'c2222222-2222-2222-2222-222222222222',
                customer_name: 'Ibu Ratna',
                customer_phone: '+6281234567899',
                operational_status: currentOrderStatus,
                intake_method: 'DROP_OFF',
                return_method: 'SELF_PICKUP',
                subtotal_amount: 30000,
                extra_charge_amount: 0,
                delivery_fee_amount: 0,
                total_amount: 30000,
                estimated_completion_at: new Date().toISOString(),
                version: currentOrderVersion,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
              },
            ],
            request_id: 'req-e2e-order-list',
          }),
        });
      }
    });
  });

  test('E2E: Navigation, Customers, Services, Order Intake & Status Progression', async ({ page }) => {
    // 1. Visit app
    await page.goto('/');

    // Verify authenticated AppShell renders
    await expect(page.getByRole('heading', { name: 'Selamat datang, Budi Kasir' })).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=Role aktif: CASHIER')).toBeVisible();

    // 2. Navigate to Pelanggan (Customers)
    await page.locator('button:has-text("Pelanggan")').first().click();
    await expect(page.locator('h2:has-text("Direktori Pelanggan")')).toBeVisible();
    await expect(page.locator('text=Ibu Ratna').first()).toBeVisible();

    // Open Tambah Pelanggan modal
    await page.locator('button:has-text("Tambah Pelanggan")').first().click();
    await expect(page.locator('h3:has-text("Tambah Pelanggan Baru")')).toBeVisible();
    await page.fill('input[placeholder*="Ibu Ratna"]', 'Pak Joko Widodo');
    await page.fill('input[type="tel"]', '081234567800');
    await page.locator('button:has-text("Simpan")').first().click();

    // 3. Navigate to Layanan (Services)
    await page.locator('button:has-text("Layanan")').first().click();
    await expect(page.locator('h2:has-text("Katalog Layanan & Tarif")')).toBeVisible();
    await expect(page.locator('text=Cuci Setrika Reguler').first()).toBeVisible();

    // 4. Navigate to Pesanan (Orders)
    await page.locator('button:has-text("Pesanan")').first().click();
    await expect(page.locator('h2:has-text("Manajemen Pesanan Laundry")')).toBeVisible();
    await expect(page.locator('text=ORD-20261103-0001').first()).toBeVisible();

    // Click Buat Pesanan Baru
    await page.locator('button:has-text("Buat Pesanan Baru")').first().click();
    await expect(page.locator('h2:has-text("Penerimaan Pesanan Baru")')).toBeVisible();

    // Verify DEC-02 floor warning/note renders when weight is under 3.0 kg
    await page.selectOption('select', { index: 1 }); // select Ibu Ratna
    await page.fill('input[placeholder="Berat/Jml"]', '2.4');
    await expect(page.locator('text=Dikenakan minimum 3.0 kg per nota kiloan')).toBeVisible();

    // Submit order
    await page.locator('button:has-text("Simpan & Buat Nota")').click();

    // 5. Verify transitions to Order Detail view
    await expect(page.locator('text=ORD-20261103-0001').first()).toBeVisible();
    await expect(page.locator('text=Diterima Kasir').first()).toBeVisible();

    // Transition: 1. Masukkan ke Antrean (QUEUED)
    await page.locator('button:has-text("1. Masukkan ke Antrean (QUEUED)")').click();
    await expect(page.locator('text=Dalam Antrean').first()).toBeVisible();

    // Transition: 2. Mulai Cuci (WASHING)
    await page.locator('button:has-text("2. Mulai Cuci (WASHING)")').click();
    await expect(page.locator('text=Sedang Dicuci').first()).toBeVisible();
  });
});
