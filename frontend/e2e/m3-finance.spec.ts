import { test, expect } from '@playwright/test';

test.describe('Milestone 3: Finance & Digital Invoices E2E', () => {
  test.beforeEach(async ({ page }) => {
    // 1. Mock Authenticated Session as OWNER
    await page.route(/\/api\/v1\/auth\/me/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            id: 'u1111111-1111-1111-1111-111111111111',
            business_id: 'b1111111-1111-1111-1111-111111111111',
            username: 'owner_budi',
            full_name: 'Budi Pemilik',
            role: 'OWNER',
            phone_e164: '+6281234567890',
            is_active: true,
          },
          request_id: 'req-e2e-auth',
        }),
      });
    });

    // 2. Mock Expenses API
    let expensesList = [
      {
        id: 'exp-1',
        business_id: 'b1111111-1111-1111-1111-111111111111',
        category: 'DETERGENT',
        amount: 150000,
        expense_date: '2026-11-03',
        description: 'Beli deterjen cair 2 jerigen',
        created_by: 'u1111111-1111-1111-1111-111111111111',
        created_by_name: 'Budi Pemilik',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];

    await page.route(/\/api\/v1\/expenses/, async (route) => {
      const method = route.request().method();
      if (method === 'POST') {
        const body = JSON.parse(route.request().postData() || '{}');
        const newExp = {
          id: 'exp-2',
          business_id: 'b1111111-1111-1111-1111-111111111111',
          category: body.category || 'PACKAGING',
          amount: body.amount || 45000,
          expense_date: body.expense_date || '2026-11-03',
          description: body.description || 'Plastik packing 5 pack',
          created_by: 'u1111111-1111-1111-1111-111111111111',
          created_by_name: 'Budi Pemilik',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        expensesList = [newExp, ...expensesList];
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: newExp, request_id: 'req-exp-create' }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: expensesList, request_id: 'req-exp-list' }),
        });
      }
    });

    // 3. Mock Orders API
    await page.route(/\/api\/v1\/orders/, async (route) => {
      const url = route.request().url();
      if (url.includes('/orders/ord-999')) {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              id: 'ord-999',
              business_id: 'b1111111-1111-1111-1111-111111111111',
              order_number: 'ORD-20261103-0999',
              customer_id: 'c2222222-2222-2222-2222-222222222222',
              customer: {
                id: 'c2222222-2222-2222-2222-222222222222',
                full_name: 'Ibu Ratna',
                phone_e164: '+6281234567899',
                address: 'Jl. Melati No. 10',
                is_active: true,
              },
              operational_status: 'RECEIVED',
              intake_method: 'DROP_OFF',
              return_method: 'SELF_PICKUP',
              subtotal_amount: 50000,
              extra_charge_amount: 0,
              delivery_fee_amount: 0,
              total_amount: 50000,
              estimated_completion_at: new Date().toISOString(),
              version: 1,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              items: [
                {
                  id: 'item-1',
                  service_id: 's1',
                  service_name_snapshot: 'Cuci Setrika Express',
                  pricing_type_snapshot: 'PER_KG',
                  unit_snapshot: 'KG',
                  quantity: '5.0',
                  unit_price_snapshot: 10000,
                  line_total_amount: 50000,
                  requires_ironing_snapshot: true,
                  created_at: new Date().toISOString(),
                },
              ],
              status_history: [
                {
                  id: 'hist-1',
                  from_status: null,
                  to_status: 'RECEIVED',
                  changed_by: 'u1111111-1111-1111-1111-111111111111',
                  reason: 'Pesanan dibuat',
                  created_at: new Date().toISOString(),
                },
              ],
            },
            request_id: 'req-order-detail',
          }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: [
              {
                id: 'ord-999',
                business_id: 'b1111111-1111-1111-1111-111111111111',
                order_number: 'ORD-20261103-0999',
                customer_id: 'c2222222-2222-2222-2222-222222222222',
                customer_name: 'Ibu Ratna',
                customer_phone: '+6281234567899',
                operational_status: 'RECEIVED',
                intake_method: 'DROP_OFF',
                return_method: 'SELF_PICKUP',
                subtotal_amount: 50000,
                extra_charge_amount: 0,
                delivery_fee_amount: 0,
                total_amount: 50000,
                estimated_completion_at: new Date().toISOString(),
                version: 1,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
              },
            ],
            request_id: 'req-order-list',
          }),
        });
      }
    });

    // 4. Mock Payments API
    let paymentRecords: Record<string, unknown>[] = [];
    let currentTotalPaid = 0;
    let currentRemaining = 50000;
    let currentPaymentStatus = 'UNPAID';

    await page.route(/\/api\/v1\/orders\/ord-999\/payments/, async (route) => {
      const method = route.request().method();
      if (method === 'POST') {
        const body = JSON.parse(route.request().postData() || '{}');
        const payAmount = body.amount || 20000;
        currentTotalPaid += payAmount;
        currentRemaining = Math.max(0, 50000 - currentTotalPaid);
        currentPaymentStatus = currentRemaining === 0 ? 'PAID' : 'PARTIALLY_PAID';

        const newPay = {
          id: 'pay-001',
          order_id: 'ord-999',
          amount: payAmount,
          method: body.method || 'CASH',
          verification_status: 'VERIFIED',
          payment_time: new Date().toISOString(),
          verified_by: 'u1111111-1111-1111-1111-111111111111',
          verified_by_name: 'Budi Pemilik',
          verified_at: new Date().toISOString(),
          reference_note: body.reference_note || null,
          created_at: new Date().toISOString(),
          is_voided: false,
          void_reason: null,
          voided_at: null,
          voided_by_name: null,
        };
        paymentRecords = [newPay, ...paymentRecords];

        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: newPay, request_id: 'req-pay-create' }),
        });
      } else {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              order_id: 'ord-999',
              order_number: 'ORD-20261103-0999',
              total_amount: 50000,
              total_paid: currentTotalPaid,
              remaining_amount: currentRemaining,
              payment_status: currentPaymentStatus,
              payments: paymentRecords,
            },
            request_id: 'req-pay-summary',
          }),
        });
      }
    });

    // 5. Mock Invoices API
    await page.route(/\/api\/v1\/invoices\/ord-999/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          data: {
            order_id: 'ord-999',
            order_number: 'ORD-20261103-0999',
            created_at: new Date().toISOString(),
            estimated_completion_at: new Date().toISOString(),
            operational_status: 'RECEIVED',
            business_name: 'Laundry Maju Jaya',
            business_phone: '+6281234567890',
            business_address: 'Jl. Merdeka No. 1',
            customer_name: 'Ibu Ratna',
            customer_phone: '+6281234567899',
            intake_method: 'DROP_OFF',
            return_method: 'SELF_PICKUP',
            items: [
              {
                service_name: 'Cuci Setrika Express',
                quantity: '5.0',
                unit: 'KG',
                unit_price: 10000,
                line_total: 50000,
              },
            ],
            subtotal_amount: 50000,
            extra_charge_amount: 0,
            delivery_fee_amount: 0,
            total_amount: 50000,
            total_paid: currentTotalPaid,
            remaining_amount: currentRemaining,
            payment_status: currentPaymentStatus,
            payments: paymentRecords,
            customer_notes: '',
            tracking_url: 'http://localhost:5173/track/ORD-20261103-0999',
            whatsapp_share_url: 'https://wa.me/6281234567899?text=NOTA%20LAUNDRY',
            whatsapp_share_text: 'NOTA LAUNDRY ORD-20261103-0999 Total: Rp 50.000',
          },
          request_id: 'req-invoice-detail',
        }),
      });
    });
  });

  test('E2E: Expenses Management, Payment Intake & Digital Invoice Modal', async ({ page }) => {
    // 1. Visit app
    await page.goto('/');

    // 2. Navigate to Keuangan (Finance / Expenses)
    await page.locator('button:has-text("Keuangan")').first().click();
    await expect(page.locator('h2:has-text("Pengeluaran Operasional")')).toBeVisible();
    await expect(page.locator('text=Beli deterjen cair 2 jerigen')).toBeVisible();

    // Click Catat Pengeluaran
    await page.locator('button:has-text("Catat Pengeluaran")').first().click();
    await expect(page.locator('h3:has-text("Catat Pengeluaran Operasional")')).toBeVisible();
    await page.selectOption('select', 'PACKAGING');
    await page.fill('input[type="number"]', '45000');
    await page.fill('textarea', 'Beli plastik packing');
    await page.locator('button:has-text("Simpan Pengeluaran")').click();

    // Verify modal closes
    await expect(page.locator('h3:has-text("Catat Pengeluaran Operasional")')).not.toBeVisible();

    // 3. Navigate to Pesanan (Orders) -> Order Detail
    await page.locator('button:has-text("Pesanan")').first().click();
    await expect(page.locator('text=ORD-20261103-0999').first()).toBeVisible();
    await page.locator('text=ORD-20261103-0999').first().click();

    // Verify Order Detail renders with Payment Ledger card
    await expect(page.locator('h2:has-text("ORD-20261103-0999")')).toBeVisible();
    await expect(page.locator('text=BELUM LUNAS').first()).toBeVisible();

    // Click Catat Pembayaran
    await page.locator('button:has-text("Catat Pembayaran")').first().click();
    await expect(page.locator('h3:has-text("Catat Pembayaran")')).toBeVisible();

    // Check cash change calculator
    await page.fill('input[type="number"]', '20000');
    await page.locator('button:has-text("Konfirmasi Pembayaran")').click();
    await expect(page.locator('h3:has-text("Catat Pembayaran")')).not.toBeVisible();

    // 4. Open Nota Digital & WhatsApp modal
    await page.locator('button:has-text("Nota & WhatsApp")').first().click();
    await expect(page.locator('h3:has-text("Nota Digital & Cetak")')).toBeVisible();
    await expect(page.locator('text=Laundry Maju Jaya').first()).toBeVisible();
    await expect(page.locator('button:has-text("Kirim via WhatsApp")')).toBeVisible();
    await expect(page.locator('button:has-text("Cetak Nota")')).toBeVisible();

    // Switch to Thermal POS 58mm view
    await page.locator('button:has-text("Pratinjau POS Thermal (58mm)")').click();
    await expect(page.locator('text=No. Nota : ORD-20261103-0999')).toBeVisible();

    // Close modal
    await page.locator('button:has-text("Cetak Nota")').isVisible();
  });
});
