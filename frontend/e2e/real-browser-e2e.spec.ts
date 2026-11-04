import { test, expect } from '@playwright/test';

/**
 * True Browser-to-Database End-to-End Test Suite for E-Laundry 2.0 (M0 - M8)
 * 
 * Strict Acceptance Criteria:
 * - ZERO network mocks (no page.route / route.fulfill)
 * - Chromium -> React Frontend (Vite) -> FastAPI Backend -> PostgreSQL 17 Database
 * - Real JWT/session cookies, real database transactions, optimistic locks, invariants
 */

let sharedOrderNumber = '';
let sharedTrackingToken = '';
const uniqueSuffix = Date.now().toString().slice(-4);
const customerName = `Ibu E2E Test ${uniqueSuffix}`;
const customerPhone = `0812${Math.floor(10000000 + Math.random() * 90000000)}`;

test.describe.serial('True Browser-to-Database Real E2E Suite (Zero Mocks)', () => {

  test('Flow 1: Cashier Lifecycle - Customer CRUD, Order Creation, Workflow & Payments', async ({ page }) => {
    test.setTimeout(60000);

    // -------------------------------------------------------------
    // 1. Login as Cashier (kasir_budi)
    // -------------------------------------------------------------
    await page.goto('/');
    
    // Wait for login form to be visible (after session verification)
    const usernameInput = page.locator('input[autocomplete="username"]');
    await expect(usernameInput).toBeVisible({ timeout: 10000 });

    await usernameInput.fill('kasir_budi');
    await page.locator('input[autocomplete="current-password"]').fill('Kasir123!');
    await page.getByRole('button', { name: 'Masuk Sekarang' }).click();

    // Confirm session established
    await expect(page.getByText('Selamat datang, Budi Prasetyo')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Sesi Terotentikasi')).toBeVisible();

    // -------------------------------------------------------------
    // 2. Customer Directory CRUD
    // -------------------------------------------------------------
    await page.locator('aside nav button:has-text("Pelanggan")').click();
    await expect(page.getByRole('heading', { name: 'Direktori Pelanggan' })).toBeVisible();

    // Open Tambah Pelanggan modal
    await page.getByRole('button', { name: 'Tambah Pelanggan' }).click();
    await expect(page.getByRole('heading', { name: 'Tambah Pelanggan Baru' })).toBeVisible();

    // Fill customer form
    await page.locator('input[placeholder="Contoh: Ibu Ratna Sari"]').fill(customerName);
    await page.locator('input[placeholder="Contoh: 08123456789"]').fill(customerPhone);
    await page.locator('textarea[placeholder="Alamat untuk antar-jemput..."]').fill('Jl. Mawar Raya No. 88, Kebon Jeruk');
    await page.locator('input[placeholder="Preferensi pewangi, alergi sabun, dsb."]').fill('Pewangi lembut, pisahkan pakaian putih');

    // Submit to PostgreSQL
    await page.getByRole('button', { name: 'Simpan' }).click();

    // Verify customer appears in search
    const searchInput = page.locator('input[placeholder*="Cari berdasarkan nama"]');
    await searchInput.fill(customerName);
    await expect(page.getByText(customerName)).toBeVisible({ timeout: 5000 });

    // -------------------------------------------------------------
    // 3. Service Catalog & Order Creation with Auto-Pricing
    // -------------------------------------------------------------
    await page.locator('aside nav button:has-text("Pesanan")').click();
    await expect(page.getByRole('heading', { name: 'Manajemen Pesanan Laundry' })).toBeVisible();

    await page.getByRole('button', { name: 'Buat Pesanan Baru' }).click();
    await expect(page.getByRole('heading', { name: 'Penerimaan Pesanan Baru' })).toBeVisible();

    // Select the customer we just created
    const customerSelect = page.locator('select').first();
    const customerOption = customerSelect.locator(`option:has-text("${customerName}")`);
    await customerOption.waitFor({ state: 'attached', timeout: 5000 });
    const customerIdVal = await customerOption.getAttribute('value');
    await customerSelect.selectOption(customerIdVal || '');

    // Select Kiloan service (Cuci Komplit Reguler)
    const serviceSelect = page.locator('select').nth(1);
    const kiloanOption = serviceSelect.locator('option:has-text("Cuci Komplit Reguler")');
    await kiloanOption.waitFor({ state: 'attached', timeout: 5000 });
    const serviceVal = await kiloanOption.getAttribute('value');
    await serviceSelect.selectOption(serviceVal || '');

    // Set measured weight (3.5 kg kiloan)
    const qtyInput = page.locator('input[placeholder="Berat/Jml"]');
    await qtyInput.fill('3.5');

    // Set notes
    await page.locator('input[placeholder="Contoh: Pisahkan kelunturan, pewangi lavender"]').fill('Catatan E2E: Jangan disikat');

    // Verify backend pricing calculation is displayed
    await expect(page.getByText('Total Tagihan (Backend Calculated):')).toBeVisible();

    // Submit Order to backend
    await page.getByRole('button', { name: 'Simpan & Buat Nota' }).click();

    // Verify navigation to Order Detail view
    await expect(page.getByText('Alur Operasional Pengerjaan')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Diterima Kasir')).toBeVisible();

    // Capture generated order number
    const orderNumberEl = page.locator('h2.font-mono').first();
    await expect(orderNumberEl).toBeVisible();
    sharedOrderNumber = (await orderNumberEl.innerText()).trim();
    expect(sharedOrderNumber).toMatch(/^ORD-\d{8}-\d{4}$/);

    // -------------------------------------------------------------
    // 4. Sequential Operational Workflow Progression
    // -------------------------------------------------------------
    // Stage 1 -> Stage 2: QUEUED
    await page.getByRole('button', { name: '1. Masukkan ke Antrean (QUEUED)' }).click();
    await expect(page.getByText('Dalam Antrean')).toBeVisible({ timeout: 5000 });

    // Stage 2 -> Stage 3: WASHING
    await page.getByRole('button', { name: '2. Mulai Cuci (WASHING)' }).click();
    await expect(page.getByText('Sedang Dicuci')).toBeVisible({ timeout: 5000 });

    // Stage 3 -> Stage 4: DRYING
    await page.getByRole('button', { name: '3. Masukkan Pengering (DRYING)' }).click();
    await expect(page.getByText('Pengeringan')).toBeVisible({ timeout: 5000 });

    // Stage 4 -> Stage 5: IRONING or QC_PACKING
    const ironBtn = page.getByRole('button', { name: /4\. Mulai Setrika \(IRONING\)/ });
    const qcBtnDirect = page.getByRole('button', { name: /4\. QC & Packing \(Tanpa Setrika\)/ });
    if (await ironBtn.isVisible()) {
      await ironBtn.click();
      await expect(page.getByText('Penyetrikaan')).toBeVisible({ timeout: 5000 });
      await page.getByRole('button', { name: '5. Selesai Setrika & Packing (QC_PACKING)' }).click();
    } else if (await qcBtnDirect.isVisible()) {
      await qcBtnDirect.click();
    }

    // Stage 5 -> Stage 6: READY
    await expect(page.getByText('QC & Packing', { exact: true })).toBeVisible({ timeout: 5000 });
    await page.getByRole('button', { name: '6. Tandai Siap Serah Terima (READY)' }).click();
    await expect(page.getByText('Siap Ambil/Antar', { exact: true })).toBeVisible({ timeout: 5000 });

    // -------------------------------------------------------------
    // 5. Real Payment Intake & Balance Invariant
    // -------------------------------------------------------------
    await expect(page.getByText('BELUM LUNAS')).toBeVisible();

    await page.getByRole('button', { name: 'Catat Pembayaran' }).click();
    await expect(page.getByRole('heading', { name: 'Catat Pembayaran' })).toBeVisible();

    await page.getByRole('button', { name: 'Set Lunas Penuh' }).click();
    await page.getByRole('button', { name: 'Konfirmasi Pembayaran' }).click();

    // Verify status updates to LUNAS and balance is zero
    await expect(page.getByText('LUNAS', { exact: true })).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Sisa Tagihan')).toBeVisible();
    await expect(page.locator('text=Rp 0')).toBeVisible();

    // -------------------------------------------------------------
    // 6. Digital Invoice Modal & POS Thermal Receipt
    // -------------------------------------------------------------
    await page.getByRole('button', { name: 'Nota & WhatsApp' }).click();
    await expect(page.getByRole('heading', { name: 'Nota Digital & Cetak' })).toBeVisible();

    await expect(page.getByText('LUNAS', { exact: true })).toBeVisible();
    await expect(page.getByText(customerName)).toBeVisible();
    await expect(page.getByText(sharedOrderNumber)).toBeVisible();

    // Check POS Thermal 58mm preview
    await page.getByRole('button', { name: 'Pratinjau POS Thermal (58mm)' }).click();
    await expect(page.getByText('Terima kasih!')).toBeVisible();

    // Extract tracking link from backend via active session
    const invoiceLookup = await page.evaluate(async (ordNum) => {
      const ordRes = await fetch(`/api/v1/orders?search=${encodeURIComponent(ordNum)}`, { credentials: 'include' });
      const ordJson = await ordRes.json();
      const ordId = ordJson.data?.[0]?.id;
      if (!ordId) return null;

      const invRes = await fetch(`/api/v1/invoices/${ordId}`, { credentials: 'include' });
      const invJson = await invRes.json();
      return invJson.data?.tracking_url;
    }, sharedOrderNumber);

    expect(invoiceLookup).toBeTruthy();
    expect(invoiceLookup).toContain('/track/');
    sharedTrackingToken = invoiceLookup.split('/track/')[1];

    await page.locator('button[title="Tutup modal"]').click();
  });

  test('Flow 2: Unauthenticated Public Tracking (/track/:token)', async ({ browser }) => {
    expect(sharedTrackingToken).toBeTruthy();

    // Create a clean unauthenticated browser context with ZERO cookies or local storage
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto(`/track/${sharedTrackingToken}`);

    // Verify public tracking renders without auth
    await expect(page.getByText('Pelacakan Pesanan Resmi')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(sharedOrderNumber)).toBeVisible();
    await expect(page.getByText('Siap Diambil / Diantar', { exact: true })).toBeVisible();

    // Verify read-only enforcement (no management controls present)
    await expect(page.getByRole('button', { name: 'Catat Pembayaran' })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Batalkan Pesanan' })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Ubah Status' })).toHaveCount(0);

    await context.close();
  });

  test('Flow 3: Courier Role Authentication & Delivery Dashboard', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('/');
    const usernameInput = page.locator('input[autocomplete="username"]');
    await expect(usernameInput).toBeVisible({ timeout: 10000 });

    await usernameInput.fill('kurir_agus');
    await page.locator('input[autocomplete="current-password"]').fill('Kurir123!');
    await page.getByRole('button', { name: 'Masuk Sekarang' }).click();

    // Confirm Courier Dashboard
    await expect(page.getByText('Selamat datang, Agus Santoso')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Role aktif: COURIER')).toBeVisible();

    // Confirm RBAC restrictions (no access to Users or Settings)
    await expect(page.getByRole('button', { name: 'Pegawai' })).toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Pengaturan' })).toHaveCount(0);

    // Navigate to Antar-Jemput
    await page.locator('aside nav button:has-text("Antar-Jemput")').click();
    await expect(page.getByRole('heading', { name: 'Tugas Kurir Antar-Jemput' })).toBeVisible();

    await context.close();
  });

  test('Flow 4: Owner Role Authentication, Financial Dashboard & CSV Export', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('/');
    const usernameInput = page.locator('input[autocomplete="username"]');
    await expect(usernameInput).toBeVisible({ timeout: 10000 });

    await usernameInput.fill('owner');
    await page.locator('input[autocomplete="current-password"]').fill('Owner123!');
    await page.getByRole('button', { name: 'Masuk Sekarang' }).click();

    // Confirm Owner Dashboard & Metrics
    await expect(page.getByText('Selamat datang, Budi Setiawan')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Kinerja Finansial Hari Ini')).toBeVisible();
    await expect(page.getByText('Uang Masuk Diterima')).toBeVisible();

    // Navigate to Reports
    await page.locator('aside nav button:has-text("Laporan")').click();
    await expect(page.getByRole('heading', { name: 'Pusat Laporan & Rekonsiliasi' })).toBeVisible();

    // Verify Financial Report tab
    await expect(page.getByRole('button', { name: 'Ringkasan Finansial' })).toBeVisible();
    await expect(page.getByText('Uang Masuk Diterima').first()).toBeVisible();

    // Trigger CSV export for Payments
    await page.getByRole('button', { name: 'Unduh CSV Pembayaran' }).click();
    await expect(page.getByText('berhasil diunduh')).toBeVisible({ timeout: 10000 });

    await context.close();
  });

});
