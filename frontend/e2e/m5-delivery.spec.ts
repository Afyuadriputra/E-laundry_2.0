import { test, expect } from '@playwright/test';

test.describe('Milestone 5: Pickup & Delivery Logistics E2E', () => {
  test('Cashier manages pickup requests, confirms assignment, and converts to order (DEC-10)', async ({
    page,
  }) => {
    test.setTimeout(60000);
    // 1. Mock Authenticated Session as CASHIER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u-cashier-1',
            business_id: 'b-laundry-1',
            username: 'kasir_sari',
            full_name: 'Sari Kasir',
            role: 'CASHIER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
        }),
      });
    });

    // 2. Mock Couriers & Services list
    await page.route(/\/api\/v1\/users/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: [
            {
              id: 'u-courier-1',
              username: 'kurir_dodi',
              full_name: 'Dodi Kurir',
              role: 'COURIER',
              is_active: true,
            },
          ],
        }),
      });
    });

    await page.route(/\/api\/v1\/services/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: [
            {
              id: 's-kiloan-1',
              name: 'Cuci Lipat Reguler',
              pricing_type: 'PER_KG',
              unit: 'KG',
              unit_price: 7000,
              is_active: true,
            },
          ],
        }),
      });
    });

    // 3. Mock Pickup Requests State
    const pickupItem = {
      id: 'pck-req-1',
      business_id: 'b-laundry-1',
      request_number: 'PCK-20261103-0001',
      requester_name: 'Pak Ahmad Yani',
      phone_e164: '+6281299887766',
      pickup_address: 'Jl. Mawar No. 8, Bandung',
      requested_date: '2026-11-04',
      requested_time_start: '09:00:00',
      requested_time_end: '11:00:00',
      confirmed_start_at: null as string | null,
      confirmed_end_at: null as string | null,
      status: 'REQUESTED',
      notes: 'Tolong jemput di pos satpam',
      rejection_reason: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      tracking_token: 'tok-pck-1',
      tracking_url: '/track/tok-pck-1',
    };

    await page.route(/\/api\/v1\/pickup-delivery\/requests(\?.*)?$/, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: [pickupItem] }),
        });
      }
    });

    await page.route(/\/api\/v1\/pickup-delivery\/tasks(\?.*)?$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: [] }),
      });
    });

    // Confirm Endpoint
    await page.route(/\/api\/v1\/pickup-delivery\/requests\/pck-req-1\/confirm/, async (route) => {
      pickupItem.status = 'ASSIGNED';
      pickupItem.confirmed_start_at = '2026-11-04T09:00:00Z';
      pickupItem.confirmed_end_at = '2026-11-04T11:00:00Z';
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: pickupItem }),
      });
    });

    // Convert Endpoint (DEC-10)
    await page.route(/\/api\/v1\/pickup-delivery\/requests\/pck-req-1\/convert-order/, async (route) => {
      pickupItem.status = 'CONVERTED';
      await route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            order_id: 'ord-new-1',
            order_number: 'ORD-20261103-0999',
            total_amount: 36500,
          },
        }),
      });
    });

    // Navigate to App
    await page.goto('/');

    // Switch to Antar-Jemput tab
    await page.locator('button:has-text("Antar-Jemput")').first().click();

    // Verify Pickup Request is displayed
    await expect(page.locator('text=Pak Ahmad Yani')).toBeVisible();
    await expect(page.locator('span', { hasText: 'Menunggu Konfirmasi' })).toBeVisible();

    // Click "Konfirmasi & Kurir"
    const confirmBtn = page.locator('button', { hasText: 'Konfirmasi & Kurir' });
    await expect(confirmBtn).toBeVisible();
    await confirmBtn.click();

    // Modal opens, submit confirmation
    const submitConfirmBtn = page.locator('button', { hasText: 'Konfirmasi & Kirim Kurir' });
    await expect(submitConfirmBtn).toBeVisible();
    await submitConfirmBtn.click();

    // Verify success banner and status changed to ASSIGNED
    await expect(page.locator('text=Penjemputan dikonfirmasi dan kurir berhasil ditugaskan.')).toBeVisible();
    await expect(page.locator('span', { hasText: 'Kurir Ditugaskan' })).toBeVisible();

    // Simulate courier finishing pickup (status = PICKED_UP)
    pickupItem.status = 'PICKED_UP';
    await page.locator('button', { hasText: 'Segarkan' }).click();

    await expect(page.locator('span', { hasText: 'Sudah Dijemput' })).toBeVisible();
    const convertBtn = page.locator('button', { hasText: 'Konversi ke Pesanan (DEC-10)' });
    await expect(convertBtn).toBeVisible();
    await convertBtn.click();

    // Modal convert opens, set quantity and submit
    const qtyInput = page.locator('input[type="number"][step="0.1"]');
    await qtyInput.fill('4.5');
    const submitOrderBtn = page.locator('button', { hasText: 'Buat Pesanan Laundry' });
    await submitOrderBtn.click();

    // Verify order created successfully
    await expect(page.locator('text=Pesanan resmi berhasil dibuat: ORD-20261103-0999!')).toBeVisible();
    await expect(page.locator('span', { hasText: 'Sudah Menjadi Order' })).toBeVisible();
  });

  test('Courier mobile workflow: moves task from ASSIGNED -> EN_ROUTE -> ARRIVED -> COMPLETED', async ({
    page,
  }) => {
    // 1. Mock Authenticated Session as COURIER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u-courier-1',
            business_id: 'b-laundry-1',
            username: 'kurir_dodi',
            full_name: 'Dodi Kurir',
            role: 'COURIER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
        }),
      });
    });

    let currentTaskStatus = 'ASSIGNED';
    const courierTask = {
      id: 'dt-task-1',
      business_id: 'b-laundry-1',
      task_type: 'PICKUP',
      pickup_request_id: 'pck-1',
      order_id: null,
      order_number: null,
      courier_user_id: 'u-courier-1',
      courier_name: 'Dodi Kurir',
      status: currentTaskStatus,
      recipient_name: 'Ibu Ratna',
      destination_address: 'Jl. Merdeka No. 45, Bandung',
      destination_phone: '+6281299990000',
      proof_photo_path: null,
      completed_at: null,
      failure_reason: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    await page.route(/\/api\/v1\/pickup-delivery\/tasks\/my-tasks/, async (route) => {
      courierTask.status = currentTaskStatus;
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: [courierTask] }),
      });
    });

    await page.route(/\/api\/v1\/pickup-delivery\/tasks\/dt-task-1\/status/, async (route) => {
      const payload = JSON.parse(route.request().postData() || '{}');
      currentTaskStatus = payload.to_status;
      courierTask.status = currentTaskStatus;
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ data: courierTask }),
      });
    });

    await page.goto('/');

    // Switch to Antar-Jemput tab
    await page.locator('button:has-text("Antar-Jemput")').first().click();

    // Verify task card details
    await expect(page.locator('text=Ibu Ratna')).toBeVisible();
    await expect(page.locator('text=PENJEMPUTAN')).toBeVisible();
    await expect(page.locator('text=Ditugaskan')).toBeVisible();

    // Step 1: Click "Mulai Jalan (En Route)"
    const enRouteBtn = page.locator('button', { hasText: 'Mulai Jalan (En Route)' });
    await expect(enRouteBtn).toBeVisible();
    await enRouteBtn.click();

    // Step 2: Now status is Dalam Perjalanan, click "Tiba di Lokasi"
    await expect(page.locator('text=Dalam Perjalanan')).toBeVisible();
    const arrivedBtn = page.locator('button', { hasText: 'Tiba di Lokasi' });
    await expect(arrivedBtn).toBeVisible();
    await arrivedBtn.click();

    // Step 3: Now status is Tiba di Lokasi, click "Selesai Dijemput"
    await expect(page.locator('text=Tiba di Lokasi')).toBeVisible();
    const completeBtn = page.locator('button', { hasText: 'Selesai Dijemput' });
    await expect(completeBtn).toBeVisible();
    await completeBtn.click();

    // Verify success banner, switch to 'Selesai' tab, and verify completed card
    await expect(page.locator('text=Status tugas berhasil diubah ke: COMPLETED')).toBeVisible();
    await page.locator('button:has-text("Selesai")').click();
    await expect(page.locator('text=Tugas Selesai')).toBeVisible();
  });
});
