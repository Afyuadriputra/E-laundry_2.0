# APPLICATION FLOW DOCUMENTATION (AFD)

## WEB APP MANAJEMEN LAUNDRY UMKM

**Versi Dokumen:** 1.0
**Tanggal:** 3 November 2026
**Status:** Draft — Architecture & Flow Review
**Dokumen Induk:** PRD v1.0 dan TRD v1.0
**Arsitektur:** Modular Monolith — Client-Server REST API
**Target Implementasi:** MVP, Satu Usaha Laundry
**Platform:** Mobile Web, Desktop Web, dan PWA

---

# 1. PENDAHULUAN

## 1.1 Tujuan Dokumen

Application Flow Documentation (AFD) merupakan dokumen teknis yang menjelaskan alur penggunaan aplikasi, perpindahan halaman, proses bisnis, komunikasi komponen, perubahan status, dan mekanisme penanganan kondisi khusus.

Dokumen ini menjadi penghubung antara:

1. Product Requirements Document (PRD).
2. Technical Requirements Document (TRD).
3. UI/UX Design Specification.
4. Database Design Document (DBD).
5. API Contract.
6. Test Plan dan User Acceptance Test.

AFD digunakan oleh frontend developer, backend developer, UI/UX designer, database engineer, dan QA engineer untuk memastikan seluruh sistem dibangun dengan alur yang konsisten.

## 1.2 Tujuan Perancangan Alur

1. Mendefinisikan perjalanan pengguna secara menyeluruh.
2. Menentukan halaman yang dapat diakses setiap peran.
3. Menentukan interaksi frontend dan backend.
4. Mendefinisikan status dan aturan perpindahannya.
5. Memastikan pencatatan keuangan terpisah dari proses pencucian.
6. Menentukan mekanisme tracking pelanggan tanpa login.
7. Menentukan hubungan penjemputan dengan pesanan laundry.
8. Mencegah alur yang membingungkan atau saling bertentangan.
9. Mendefinisikan penanganan kesalahan dan pemulihan.
10. Menjadi acuan penyusunan API, database, dan pengujian.

## 1.3 Ruang Lingkup

AFD mencakup delapan modul:

| ID     | Modul               |
| ------ | ------------------- |
| MOD-01 | Dashboard           |
| MOD-02 | Manajemen Pesanan   |
| MOD-03 | Manajemen Pelanggan |
| MOD-04 | Antar-Jemput        |
| MOD-05 | Keuangan            |
| MOD-06 | Nota Digital        |
| MOD-07 | Tracking Pelanggan  |
| MOD-08 | Pengaturan          |

Kemampuan pendukung:

- Authentication.
- Role-Based Access Control.
- Pricing Engine.
- State Machine.
- Audit Logging.
- Reporting.
- Session Management.
- Tracking Token Management.
- Error Handling.

## 1.4 Batasan Sistem

MVP tidak mengimplementasikan:

- Payment gateway.
- WhatsApp API otomatis.
- GPS real-time.
- Printer nota wajib.
- Scanner barcode wajib.
- Mesin kasir fisik.
- Integrasi mesin cuci.
- Multi-cabang.
- Multi-tenant SaaS.
- Offline synchronization.
- AI prediction.

Sistem dirancang agar dapat dijalankan melalui perangkat yang sudah dimiliki usaha.

---

# 2. AKTOR DAN LINGKUNGAN APLIKASI

## 2.1 Daftar Aktor

| Aktor         | Peran                                                                      |
| ------------- | -------------------------------------------------------------------------- |
| Owner         | Mengelola usaha secara keseluruhan.                                        |
| Admin / Kasir | Menerima pesanan, mencatat pembayaran, dan melayani pelanggan.             |
| Staf Laundry  | Memproses dan memperbarui status cucian.                                   |
| Kurir         | Mengelola penjemputan dan pengantaran.                                     |
| Pelanggan     | Memantau cucian dan meminta penjemputan tanpa login.                       |
| Sistem        | Menjalankan perhitungan, validasi, perubahan data, dan pencatatan riwayat. |

## 2.2 Lingkungan Internal

Digunakan oleh petugas yang memiliki akun.

Rute utama:

- `/login`
- `/app/dashboard`
- `/app/orders`
- `/app/customers`
- `/app/pickup-delivery`
- `/app/finance`
- `/app/settings`

Hanya pengguna yang telah terautentikasi dan memiliki izin yang dapat membuka halaman internal.

## 2.3 Lingkungan Publik

Digunakan pelanggan tanpa akun.

Rute utama:

- `/pickup`
- `/track/{token}`
- `/track/{token}/invoice`

Halaman publik tidak boleh memberikan akses terhadap menu administrasi, data pelanggan lain, ataupun laporan usaha.

## 2.4 Prinsip Perjalanan Pengguna

**Pengguna internal:**

Login → Dashboard sesuai peran → Pilih pekerjaan → Jalankan tindakan → Simpan → Lihat hasil.

**Pelanggan:**

Buka tautan → Lihat status atau isi formulir → Dapatkan informasi → Hubungi laundry jika diperlukan.

Pelanggan tidak diarahkan ke login internal.

---

# 3. ARSITEKTUR ALUR APLIKASI

## 3.1 Komponen Utama

Aplikasi terdiri atas:

**Frontend React**

Bertanggung jawab terhadap tampilan, navigasi, input, validasi pengalaman pengguna, pengelolaan state, dan komunikasi API.

**Backend FastAPI**

Bertanggung jawab terhadap autentikasi, otorisasi, validasi data, proses bisnis, transaksi, pembuatan nota, serta response API.

**Application Service**

Mengorkestrasi use case seperti membuat pesanan, menerima pembayaran, mengonversi pickup menjadi order, dan menyelesaikan pengantaran.

**Domain Logic**

Menentukan perhitungan harga, aturan pembayaran, validitas perubahan status, dan business invariants.

**Repository**

Menjalankan operasi penyimpanan dan pembacaan database.

**PostgreSQL**

Menyimpan seluruh data operasional, transaksi, histori, sesi, dan audit.

## 3.2 Diagram Alur Arsitektur

Alur logis:

Pengguna Internal / Pelanggan
↓
Browser HP atau Laptop
↓
React Web Application
↓ HTTPS
REST API FastAPI
↓
Authentication / Authorization / Public Token Validation
↓
Application Service
↓
Domain Business Logic
↓
Repository
↓
PostgreSQL

Komponen pendukung backend:

- Invoice Generator.
- Tracking Token Service.
- Audit Logging.
- Reporting Queries.
- Health Monitoring.

## 3.3 Alur Request Internal

1. Pengguna menjalankan tindakan.
2. Frontend melakukan validasi dasar.
3. Frontend mengirim request ke API.
4. Backend memeriksa sesi.
5. Backend memeriksa permission.
6. Backend memvalidasi payload.
7. Application Service menjalankan aturan bisnis.
8. Repository mengakses database.
9. Transaksi database di-commit apabila berhasil.
10. Backend mengembalikan response.
11. Frontend memperbarui tampilan.
12. Pengguna menerima feedback.

Jika gagal, perubahan tidak boleh dinyatakan berhasil.

## 3.4 Alur Request Publik

1. Pelanggan membuka halaman publik.
2. Frontend melakukan request ke public API.
3. Backend memeriksa rate limit.
4. Backend memvalidasi token jika endpoint memerlukannya.
5. Backend mengambil data yang diotorisasi.
6. Backend membentuk response dengan field terbatas.
7. Frontend menampilkan informasi.
8. Pelanggan tidak diberikan kemampuan mengubah data internal.

---

# 4. INFORMATION ARCHITECTURE DAN NAVIGASI

## 4.1 Struktur Aplikasi Internal

**Login**

→ Dashboard

→ Pesanan

- Daftar Pesanan
- Buat Pesanan
- Detail Pesanan
- Perubahan Status
- Pembayaran Pesanan
- Nota Digital
- Riwayat Perubahan

→ Pelanggan

- Daftar Pelanggan
- Tambah Pelanggan
- Detail Pelanggan
- Riwayat Pesanan

→ Antar-Jemput

- Permintaan Masuk
- Penjadwalan
- Penugasan Kurir
- Status Penjemputan
- Status Pengantaran
- Riwayat Tugas

→ Keuangan

- Ringkasan Pembayaran
- Riwayat Pembayaran
- Tagihan Belum Lunas
- Pengeluaran
- Laporan
- Ekspor CSV

→ Pengaturan

- Profil Usaha
- Daftar Layanan
- Harga
- Akun Pengguna
- Pengaturan Operasional

## 4.2 Struktur Portal Publik

**Halaman Publik**

→ Permintaan Penjemputan

- Formulir Permintaan
- Konfirmasi Pengajuan
- Tautan Tracking

→ Tracking

- Informasi Pesanan
- Status Cucian
- Status Penjemputan
- Status Pengantaran
- Ringkasan Tagihan
- Nota Digital
- Hubungi Laundry

Portal publik tidak menampilkan sidebar dashboard internal.

## 4.3 Navigasi Berdasarkan Peran

### Owner

Login → Dashboard Owner → Seluruh Modul Sesuai Permission.

### Kasir

Login → Dashboard Kasir → Pesanan / Pelanggan / Pembayaran / Antar-Jemput.

### Staf Laundry

Login → Daftar Pekerjaan → Detail Pesanan → Ubah Status.

### Kurir

Login → Daftar Tugas → Detail Penjemputan/Pengantaran → Perbarui Status.

### Pelanggan

Buka tautan → Tracking atau Formulir Pickup → Informasi Pelayanan.

## 4.4 Aturan Navigasi

1. Pengguna tanpa sesi yang membuka halaman internal diarahkan ke login.
2. Pengguna yang sudah login tidak perlu mengulang login selama sesinya valid.
3. Pengguna dengan peran terbatas hanya melihat menu yang diizinkan.
4. Akses langsung ke URL terlarang tetap harus ditolak backend.
5. Pelanggan tidak diarahkan ke halaman login ketika membuka tracking.
6. Token tracking yang tidak valid menghasilkan halaman kesalahan yang aman.
7. Halaman login tidak menampilkan informasi operasional.
8. Setelah logout, halaman internal tidak boleh lagi mengungkapkan data melalui sesi yang telah dicabut.

---

# 5. FLOW AUTHENTICATION DAN SESSION

## 5.1 FLOW-AUTH-001 — Login Petugas

**Aktor:** Owner, Kasir, Staf, Kurir.

**Trigger:** Pengguna membuka halaman login.

**Precondition:** Akun aktif dan belum memiliki sesi yang digunakan pada browser tersebut.

### Main Flow

1. Frontend menampilkan formulir username dan password.
2. Pengguna memasukkan kredensial.
3. Frontend melakukan validasi field wajib.
4. Frontend mengirim request login beserta perlindungan CSRF yang sesuai.
5. Backend memeriksa rate limit.
6. Backend memverifikasi kredensial.
7. Backend memeriksa status akun.
8. Backend membuat sesi server.
9. Backend mengirim cookie sesi aman.
10. Frontend meminta informasi akun melalui `/auth/me`.
11. Backend mengembalikan peran dan permission.
12. Frontend memilih halaman awal sesuai peran.
13. Pengguna masuk ke aplikasi internal.

### Alternate Flow

**Username atau password salah**

- Backend menolak autentikasi.
- Frontend menampilkan pesan umum.
- Sesi tidak dibuat.

**Akun tidak aktif**

- Login ditolak.
- Pengguna tidak diberikan akses ke dashboard.

**Percobaan login berlebihan**

- Backend menerapkan throttling.
- Frontend menampilkan informasi percobaan dibatasi.

**Server tidak tersedia**

- Form tetap tersedia.
- Pengguna mendapat pesan gangguan layanan.
- Tidak ada klaim bahwa login berhasil.

### Postcondition

Sesi aktif tersimpan secara aman dan permission tersedia bagi frontend.

### Acceptance Criteria

- Login valid berhasil.
- Login tidak valid ditolak.
- Akun nonaktif tidak dapat login.
- Session cookie terlindungi.
- Role menentukan halaman awal.
- Permission ditegakkan pada backend.

## 5.2 FLOW-AUTH-002 — Pemeriksaan Sesi

**Trigger:** Pengguna melakukan refresh atau membuka ulang aplikasi.

### Main Flow

1. Frontend memulai aplikasi.
2. Frontend memanggil `/auth/me`.
3. Browser menyertakan cookie sesi.
4. Backend memvalidasi sesi.
5. Backend memeriksa masa berlaku dan status akun.
6. Backend mengembalikan profil pengguna.
7. Frontend memuat menu dan halaman yang sesuai.

### Alternate Flow

Jika sesi telah berakhir:

- Backend mengembalikan 401.
- Frontend menghapus state autentikasi lokal.
- Pengguna diarahkan ke login.
- Tidak ada operasi mutasi yang dilanjutkan tanpa autentikasi baru.

## 5.3 FLOW-AUTH-003 — Logout

1. Pengguna menekan Logout.
2. Frontend mengirim request logout.
3. Backend mencabut sesi.
4. Cookie sesi dihapus.
5. Frontend menghapus cache data privat.
6. Pengguna diarahkan ke login.

Jika terjadi gangguan koneksi saat logout, frontend harus menjelaskan bahwa pencabutan sesi server belum dapat dikonfirmasi. Menutup tampilan lokal saja tidak boleh dianggap sebagai logout server yang berhasil.

---

# 6. FLOW DASHBOARD

## 6.1 FLOW-DASH-001 — Memuat Dashboard

**Aktor:** Owner atau Kasir sesuai permission.

### Main Flow

1. Pengguna membuka dashboard.
2. Frontend menampilkan skeleton.
3. Frontend meminta ringkasan data.
4. Backend memvalidasi sesi dan hak akses.
5. Dashboard Service menjalankan query agregasi.
6. Backend mengembalikan nilai pesanan, pembayaran, piutang, dan status operasional.
7. Frontend menampilkan ringkasan.
8. Pengguna dapat membuka daftar detail.

### Informasi Dashboard

- Pesanan hari ini.
- Nilai pesanan.
- Uang diterima.
- Dalam proses.
- Siap diambil.
- Terlambat.
- Belum lunas.
- Pesanan terbaru.

### Ketentuan

Nilai pesanan tidak boleh disamakan dengan uang yang sudah diterima.

Contoh:

Nilai pesanan hari ini: Rp500.000.
Pembayaran diterima hari ini: Rp300.000.

Kedua nilai tersebut dapat berbeda.

## 6.2 FLOW-DASH-002 — Navigasi dari Ringkasan

Contoh:

Pengguna memilih kartu "Pesanan Terlambat".

Sistem membuka daftar pesanan dengan filter keterlambatan aktif.

Filter harus tercermin pada data yang diambil melalui API, bukan hanya menyembunyikan sebagian data yang sudah dimuat.

---

# 7. FLOW MANAJEMEN PELANGGAN

## 7.1 FLOW-CUS-001 — Menambahkan Pelanggan

**Aktor:** Owner atau Kasir.

### Main Flow

1. Pengguna membuka menu Pelanggan.
2. Pengguna memilih Tambah Pelanggan.
3. Sistem menampilkan formulir.
4. Pengguna memasukkan nama dan nomor WhatsApp.
5. Pengguna dapat menambahkan alamat.
6. Frontend memvalidasi input.
7. Backend menormalisasi nomor telepon.
8. Backend memeriksa kemungkinan duplikasi.
9. Jika valid, data disimpan.
10. Frontend menampilkan konfirmasi berhasil.

### Alternate Flow

**Nomor sudah terdaftar**

Sistem menampilkan pelanggan yang sudah ada dan memberikan pilihan menggunakan data tersebut, bukan langsung membuat duplikasi.

**Nomor tidak valid**

Sistem meminta pengguna memperbaiki input.

**Koneksi terputus**

Sistem mempertahankan data formulir selama halaman masih tersedia dan menawarkan percobaan ulang yang aman.

## 7.2 FLOW-CUS-002 — Menggunakan Pelanggan Lama

1. Kasir membuka formulir pesanan.
2. Kasir mencari nama atau nomor WhatsApp.
3. Sistem menampilkan hasil pencarian.
4. Kasir memilih pelanggan.
5. Data dasar diisi otomatis.
6. Kasir melanjutkan pembuatan pesanan.

## 7.3 FLOW-CUS-003 — Melihat Riwayat Pelanggan

1. Pengguna membuka detail pelanggan.
2. Frontend meminta daftar pesanan pelanggan.
3. Backend memeriksa permission.
4. Backend mengembalikan riwayat yang relevan.
5. Frontend menampilkan tanggal, nomor pesanan, layanan, dan status.

Data pelanggan lain tidak boleh ikut ditampilkan.

---

# 8. FLOW PEMBUATAN PESANAN

## 8.1 FLOW-ORD-001 — Pembuatan Pesanan Langsung

**Aktor:** Owner atau Kasir.

**Trigger:** Pelanggan datang membawa cucian.

**Precondition:**

- Petugas telah login.
- Layanan laundry tersedia.
- Tarif layanan telah dikonfigurasi.

### Main Flow

1. Kasir memilih Buat Pesanan.
2. Frontend membuka formulir pesanan.
3. Kasir mencari atau membuat pelanggan.
4. Kasir memilih layanan.
5. Kasir memasukkan berat atau jumlah.
6. Sistem menampilkan pratinjau harga.
7. Kasir dapat menambahkan layanan lain.
8. Kasir mengisi estimasi selesai.
9. Kasir memilih cara penyerahan cucian.
10. Kasir memasukkan catatan bila diperlukan.
11. Frontend memvalidasi input.
12. Kasir menekan Simpan Pesanan.
13. Frontend mengirim request dengan idempotency key.
14. Backend memverifikasi sesi dan permission.
15. Backend memvalidasi pelanggan serta layanan.
16. Backend mengambil harga aktif dari database.
17. Backend menghitung ulang total.
18. Backend memulai transaksi database.
19. Backend membuat nomor pesanan unik.
20. Backend menyimpan order dan order items.
21. Backend menyimpan status awal.
22. Backend menyiapkan atau menghasilkan token tracking.
23. Backend menyimpan riwayat pembuatan.
24. Transaksi di-commit.
25. Backend mengembalikan hasil.
26. Frontend membuka detail pesanan.
27. Kasir dapat membuka nota digital.

### Postcondition

- Pesanan tersimpan.
- Nomor pesanan unik tersedia.
- Rincian layanan tersimpan sebagai snapshot.
- Status awal tercatat.
- Sisa tagihan dihitung.
- Tautan tracking dapat dibuat atau diakses melalui mekanisme yang aman.

### Alternate Flow

**Belum memilih pelanggan**

Form menampilkan validasi.

**Belum memilih layanan**

Pesanan tidak dapat disimpan.

**Berat tidak valid**

Backend menolak request.

**Tarif berubah saat formulir terbuka**

Backend menggunakan tarif aktif yang sah dan mengembalikan konflik/konfirmasi harga jika pratinjau tidak lagi cocok.

**Tombol Simpan ditekan berulang**

Idempotency mencegah duplikasi.

**Database gagal menyimpan**

Transaksi di-rollback dan tidak ada pesanan parsial yang dianggap berhasil.

### Acceptance Criteria

- Kasir dapat membuat pesanan dari HP.
- Harga benar.
- Nomor unik.
- Tidak ada order ganda.
- Item dan header pesanan konsisten.
- Pesanan dapat dibuka kembali.

## 8.2 FLOW-ORD-002 — Pesanan Multi-Layanan

Contoh:

Pelanggan membawa:

- Cuci Setrika 3 kg.
- Bed Cover 1 pcs.

### Main Flow

1. Kasir memilih layanan pertama.
2. Kasir memasukkan kuantitas.
3. Sistem menghitung subtotal.
4. Kasir memilih Tambah Layanan.
5. Kasir memilih layanan kedua.
6. Kasir memasukkan jumlah.
7. Sistem menghitung subtotal kedua.
8. Sistem menjumlahkan seluruh item.
9. Kasir memeriksa total.
10. Backend menghitung ulang total saat penyimpanan.

### Aturan

- Setiap item memiliki tipe satuan.
- Harga satuan disimpan sebagai snapshot.
- Perhitungan dilakukan di backend.
- Item dengan kuantitas tidak valid ditolak.
- Tahapan pencucian dapat disesuaikan dengan jenis layanan.

## 8.3 FLOW-ORD-003 — Mengubah Pesanan

### Main Flow

1. Pengguna membuka detail pesanan.
2. Pengguna memilih Edit jika memiliki izin.
3. Sistem menampilkan data dan versi pesanan saat ini.
4. Pengguna melakukan perubahan.
5. Frontend mengirim versi yang dibaca.
6. Backend memeriksa permission.
7. Backend memeriksa status pesanan.
8. Backend memeriksa versi.
9. Backend memvalidasi perubahan.
10. Backend menghitung ulang total bila perlu.
11. Backend menyimpan perubahan dan audit log.
12. Frontend memperbarui tampilan.

### Aturan Khusus

Jika pesanan sudah memiliki pembayaran:

- Perubahan nilai total wajib dihitung ulang.
- Sisa tagihan harus konsisten.
- Pengurangan total di bawah jumlah yang telah dibayar tidak boleh diproses tanpa alur koreksi/refund yang disetujui.
- Alasan koreksi wajib dicatat.

### Alternate Flow

Jika versi pesanan tidak lagi sama, backend mengembalikan konflik.

Frontend meminta pengguna memuat ulang data.

## 8.4 FLOW-ORD-004 — Membatalkan Pesanan

1. Pengguna membuka detail.
2. Pengguna memilih Batalkan.
3. Sistem meminta alasan.
4. Backend memeriksa permission.
5. Backend memeriksa status operasional.
6. Backend memeriksa pembayaran dan tugas pengiriman terkait.
7. Jika terdapat pembayaran, sistem menerapkan prosedur pembatalan keuangan yang disetujui.
8. Jika ada tugas aktif, pembatalan atau penyelesaiannya harus dipastikan.
9. Backend menyimpan status CANCELLED dan audit.
10. Frontend menampilkan status dibatalkan.

### Ketentuan

- Pesanan yang selesai tidak dapat sekadar diubah menjadi dibatalkan.
- Pengembalian dana tidak terjadi otomatis.
- Pembayaran yang sudah tercatat tidak boleh dihapus untuk menyesuaikan pembatalan.
- Pembatalan dengan kewajiban keuangan belum diselesaikan harus ditangani melalui SOP yang ditetapkan sebelum produksi.

---

# 9. FLOW PROSES PENCUCIAN

## 9.1 FLOW-WRK-001 — Daftar Pekerjaan Staf

**Aktor:** Staf Laundry.

### Main Flow

1. Staf login.
2. Staf membuka Daftar Pekerjaan.
3. Frontend meminta pesanan aktif.
4. Backend memeriksa permission.
5. Backend mengembalikan pesanan yang boleh dikerjakan.
6. Staf melihat antrean.
7. Staf memilih pesanan.
8. Sistem menampilkan detail operasional yang relevan.

Data keuangan sensitif tidak perlu ditampilkan kepada staf.

## 9.2 FLOW-WRK-002 — Perubahan Status Cucian

### Main Flow

1. Staf membuka detail pesanan.
2. Staf melihat status saat ini.
3. Staf memilih status berikutnya yang diperbolehkan.
4. Frontend mengirim status tujuan dan versi data.
5. Backend memeriksa sesi dan permission.
6. Backend memvalidasi state transition.
7. Backend memeriksa konflik pembaruan.
8. Backend memperbarui status.
9. Backend menyimpan riwayat perubahan.
10. Transaksi di-commit.
11. Frontend menampilkan status terbaru.
12. Portal tracking menampilkan status setelah mengambil data terbaru.

### Contoh

QUEUED → WASHING → DRYING → IRONING → QC_PACKING → READY.

### Aturan

- Tidak semua layanan membutuhkan IRONING.
- Transisi yang dilewati harus sesuai jenis layanan.
- Perubahan mundur wajib disertai alasan.
- Staf tidak dapat mengubah status pembayaran.
- Riwayat status tidak boleh dihapus.

## 9.3 FLOW-WRK-003 — Pemeriksaan Kualitas

1. Staf menyelesaikan tahap produksi.
2. Sistem mengarahkan ke QC_PACKING.
3. Staf melakukan pemeriksaan.
4. Staf mencatat catatan jika diperlukan.
5. Jika lolos, status menjadi READY.
6. Jika tidak lolos, pekerjaan dikembalikan ke tahap yang relevan melalui transisi koreksi beralasan.

Kegagalan pemeriksaan tidak boleh otomatis menghasilkan status READY.

---

# 10. FLOW PEMBAYARAN MANUAL

## 10.1 FLOW-PAY-001 — Pembayaran Penuh

**Aktor:** Owner atau Kasir.

### Main Flow

1. Kasir membuka detail pesanan.
2. Sistem menampilkan total dan sisa tagihan.
3. Kasir memilih Catat Pembayaran.
4. Kasir memilih metode pembayaran.
5. Kasir memasukkan nominal.
6. Kasir memeriksa penerimaan uang.
7. Kasir mengonfirmasi pencatatan.
8. Frontend mengirim request dengan idempotency key.
9. Backend memeriksa permission.
10. Backend memulai transaksi.
11. Backend mengunci data pesanan yang relevan.
12. Backend menghitung saldo pembayaran terbaru.
13. Backend memvalidasi nominal.
14. Backend menyimpan transaksi pembayaran terverifikasi.
15. Backend menyimpan identitas petugas.
16. Backend memperbarui hasil perhitungan status pembayaran.
17. Backend menyimpan audit.
18. Transaksi di-commit.
19. Frontend menampilkan status PAID.

### Postcondition

- Pembayaran tercatat.
- Sisa tagihan nol.
- Status pembayaran lunas.
- Riwayat transaksi tersedia.

## 10.2 FLOW-PAY-002 — Pembayaran DP

### Contoh

Total tagihan Rp50.000.

DP Rp20.000.

### Main Flow

1. Kasir membuka pesanan.
2. Kasir memilih Catat Pembayaran.
3. Kasir memasukkan Rp20.000.
4. Kasir memilih metode.
5. Kasir memverifikasi uang diterima.
6. Backend menyimpan pembayaran.
7. Backend menghitung total pembayaran Rp20.000.
8. Backend menghitung sisa Rp30.000.
9. Status menjadi PARTIALLY_PAID.
10. Nota diperbarui berdasarkan data terbaru.

Pembayaran berikutnya menggunakan alur pembayaran yang sama.

## 10.3 FLOW-PAY-003 — Verifikasi Transfer atau QRIS Manual

1. Pelanggan melakukan pembayaran di luar aplikasi.
2. Pelanggan dapat memberitahukan pembayaran kepada kasir.
3. Kasir memeriksa mutasi rekening atau dashboard QRIS milik usaha.
4. Jika dana sudah diterima, kasir mencatat pembayaran.
5. Backend menyimpan metode dan informasi referensi.
6. Status dihitung ulang.

### Ketentuan

- Bukti transfer tidak otomatis menandakan pembayaran berhasil.
- Sistem tidak memanggil payment gateway.
- Sistem tidak melakukan settlement.
- Kasir bertanggung jawab atas konfirmasi penerimaan.

## 10.4 FLOW-PAY-004 — Pembayaran Ganda

### Skenario

Dua kasir mencoba mencatat pelunasan pesanan yang sama.

### Penanganan

1. Kasir A dan B melihat sisa tagihan.
2. Kasir A mengirim pembayaran.
3. Backend mengunci record yang relevan.
4. Pembayaran A diproses.
5. Kasir B mengirim pembayaran.
6. Backend membaca ulang sisa tagihan setelah lock tersedia.
7. Jika tagihan sudah lunas, pembayaran B ditolak.
8. Tidak terbentuk pembayaran melebihi tagihan.

## 10.5 FLOW-PAY-005 — Koreksi atau Void Pembayaran

1. Petugas berwenang membuka riwayat pembayaran.
2. Petugas memilih transaksi.
3. Petugas mengajukan Void.
4. Sistem meminta alasan.
5. Backend memeriksa permission khusus.
6. Backend memeriksa apakah transaksi sudah pernah dibatalkan.
7. Backend menjalankan prosedur void.
8. Backend mencatat siapa yang melakukan koreksi.
9. Backend menghitung ulang total pembayaran sah.
10. Status pembayaran dan piutang diperbarui.

### Aturan

- Pembayaran asli tetap memiliki jejak histori.
- Koreksi harus dapat diaudit.
- Void tidak sama dengan transfer pengembalian dana.
- Prosedur refund uang harus mengikuti SOP bisnis tersendiri.

---

# 11. FLOW NOTA DIGITAL

## 11.1 FLOW-INV-001 — Membuka Nota

1. Kasir membuka pesanan.
2. Kasir memilih Lihat Nota.
3. Frontend meminta data nota.
4. Backend memeriksa permission.
5. Backend mengambil snapshot layanan dan pembayaran sah.
6. Backend membentuk data nota.
7. Frontend menampilkan rincian.

## 11.2 FLOW-INV-002 — Unduh PDF

1. Pengguna memilih Unduh PDF.
2. Frontend memanggil endpoint PDF.
3. Backend memvalidasi akses.
4. Backend membentuk dokumen.
5. Backend mengembalikan file PDF.
6. Browser membuka atau menyimpan file.

Proses pembuatan PDF tidak boleh mengubah status pesanan atau pembayaran.

## 11.3 FLOW-INV-003 — Berbagi WhatsApp

1. Kasir memilih Kirim Nota.
2. Sistem membentuk pesan.
3. Sistem mengambil nomor WhatsApp pelanggan.
4. Sistem menambahkan tautan tracking.
5. Frontend membuat tautan WhatsApp.
6. Browser membuka WhatsApp.
7. Kasir meninjau dan mengirim pesan secara manual.

### Batasan

Sistem hanya mengetahui bahwa tindakan membuka WhatsApp dilakukan.

Sistem tidak boleh menganggap pesan terkirim atau telah dibaca tanpa integrasi yang menyediakan bukti tersebut.

---

# 12. FLOW PERMINTAAN PENJEMPUTAN PUBLIK

## 12.1 FLOW-PUP-001 — Pelanggan Mengajukan Pickup

**Aktor:** Pelanggan tanpa login.

**Trigger:** Pelanggan membuka halaman `/pickup`.

### Main Flow

1. Pelanggan membuka halaman permintaan penjemputan.
2. Sistem menampilkan formulir.
3. Pelanggan mengisi nama.
4. Pelanggan mengisi nomor WhatsApp.
5. Pelanggan mengisi alamat.
6. Pelanggan menentukan tanggal.
7. Pelanggan menentukan rentang waktu.
8. Pelanggan mengisi catatan opsional.
9. Frontend melakukan validasi.
10. Pelanggan menekan Ajukan Penjemputan.
11. Frontend mengirim request publik.
12. Backend menerapkan rate limiting dan perlindungan abuse.
13. Backend memvalidasi data.
14. Backend memeriksa kemungkinan pengajuan berulang.
15. Backend menyimpan pickup request.
16. Backend membuat token tracking.
17. Backend mengembalikan nomor permintaan dan tautan tracking melalui respons pembuatan yang aman.
18. Frontend menampilkan halaman berhasil.
19. Pelanggan dapat menyalin tautan tracking.

### Postcondition

Permintaan berstatus REQUESTED.

### Ketentuan

- Pengajuan bukan konfirmasi penjemputan.
- Jadwal final ditentukan setelah admin mengonfirmasi.
- Harga laundry belum final.
- Pelanggan tidak perlu akun.
- Formulir tidak boleh menciptakan pesanan berbayar secara otomatis.

### Alternate Flow

**Jadwal tidak tersedia**

Jika validasi jadwal diterapkan, sistem meminta pelanggan memilih jadwal lain atau tetap mencatat sebagai permintaan yang menunggu konfirmasi sesuai kebijakan.

**Data tidak valid**

Backend menolak pengajuan dan frontend menampilkan kesalahan input.

**Spam atau penyalahgunaan**

Backend dapat menolak sementara permintaan.

**Request berulang**

Sistem menggunakan mekanisme pengurangan duplikasi dan kontrol idempotency yang sesuai.

## 12.2 FLOW-PUP-002 — Admin Meninjau Permintaan

1. Admin membuka Antar-Jemput.
2. Sistem menampilkan permintaan REQUESTED.
3. Admin membuka detail.
4. Admin memeriksa alamat dan jadwal.
5. Admin memilih Konfirmasi atau Tolak.
6. Jika dikonfirmasi, status berubah menjadi CONFIRMED.
7. Jika ditolak, alasan dicatat.
8. Admin dapat menghubungi pelanggan melalui WhatsApp manual.

## 12.3 FLOW-PUP-003 — Penugasan Kurir

1. Admin membuka permintaan yang dikonfirmasi.
2. Admin memilih petugas kurir aktif.
3. Admin menentukan jadwal tugas.
4. Backend memvalidasi pengguna dan status pickup.
5. Backend membuat tugas kurir.
6. Status menjadi ASSIGNED.
7. Tugas muncul pada halaman kurir.

## 12.4 FLOW-PUP-004 — Penjemputan

1. Kurir login.
2. Kurir membuka tugas.
3. Kurir memeriksa alamat dan jadwal.
4. Kurir mulai menuju lokasi.
5. Status menjadi EN_ROUTE.
6. Kurir mengambil cucian.
7. Status menjadi PICKED_UP.
8. Kurir membawa cucian ke laundry.
9. Kurir menyerahkan cucian ke kasir.
10. Status menjadi AT_LAUNDRY.

Tidak diperlukan GPS atau pembacaan lokasi real-time.

## 12.5 FLOW-PUP-005 — Konversi Pickup ke Pesanan Laundry

**Precondition:** Cucian telah tiba di laundry.

### Main Flow

1. Kasir membuka pickup request.
2. Kasir memilih Buat Pesanan.
3. Data pelanggan diisi dari permintaan yang ada.
4. Kasir memeriksa cucian.
5. Kasir memasukkan berat dan layanan.
6. Kasir menetapkan estimasi selesai.
7. Sistem menampilkan perhitungan total.
8. Kasir mengonfirmasi.
9. Backend memvalidasi request belum dikonversi.
10. Backend menjalankan transaksi database.
11. Backend membuat order dan order items.
12. Backend menghubungkan order dengan pickup request.
13. Backend mencatat status awal cucian.
14. Backend mempertahankan cakupan tracking yang sah.
15. Transaksi di-commit.
16. Frontend membuka detail pesanan baru.

### Aturan Penting

1. Pickup request bukan otomatis order final.
2. Berat dan harga ditentukan setelah cucian diperiksa.
3. Satu pickup request tidak boleh dikonversi dua kali menjadi order aktif.
4. Relasi pickup dan order harus dapat ditelusuri.
5. Tautan tracking pelanggan dapat tetap digunakan untuk melihat perkembangan pesanan terkait.
6. Token tidak boleh memberikan akses ke seluruh pesanan pelanggan.

---

# 13. FLOW PENGANTARAN CUCIAN

## 13.1 FLOW-DLV-001 — Menjadwalkan Pengantaran

**Precondition:** Cucian memiliki status READY.

### Main Flow

1. Admin membuka detail pesanan.
2. Admin memilih Jadwalkan Pengantaran.
3. Sistem menampilkan pilihan jadwal dan kurir.
4. Admin menentukan petugas.
5. Admin menentukan waktu.
6. Admin mengonfirmasi.
7. Backend memvalidasi status cucian.
8. Backend membuat delivery task.
9. Status tugas menjadi SCHEDULED.
10. Tugas muncul di dashboard kurir.

## 13.2 FLOW-DLV-002 — Kurir Mengantarkan Cucian

1. Kurir membuka tugas.
2. Kurir memeriksa rincian.
3. Kurir memulai perjalanan.
4. Status berubah menjadi EN_ROUTE.
5. Kurir memperbarui status IN_DELIVERY sesuai prosedur.
6. Kurir tiba di pelanggan.
7. Kurir menyerahkan cucian.
8. Kurir mencatat konfirmasi penerima.
9. Backend mengubah status menjadi DELIVERED.
10. Backend memeriksa persyaratan penyelesaian order.
11. Jika terpenuhi, status order menjadi COMPLETED.

### Ketentuan Pembayaran

Jika pembayaran belum lunas:

- Sistem menampilkan peringatan.
- Petugas mengikuti aturan usaha untuk serah terima.
- Jika serah terima diperbolehkan, order dapat COMPLETED.
- Sisa tagihan tetap tercatat sebagai piutang.

## 13.3 FLOW-DLV-003 — Pengantaran Gagal

Contoh:

Pelanggan tidak berada di lokasi.

### Main Flow

1. Kurir membuka tugas.
2. Kurir memilih Gagal Diantar.
3. Kurir memasukkan alasan.
4. Backend memvalidasi status.
5. Status menjadi FAILED.
6. Sistem menyimpan riwayat kegagalan.
7. Admin mendapatkan informasi tugas gagal melalui dashboard.
8. Admin dapat menjadwalkan ulang.
9. Riwayat tugas sebelumnya tetap tersimpan.

Order tidak boleh menjadi COMPLETED jika pakaian belum diserahkan.

---

# 14. FLOW TRACKING PELANGGAN TANPA LOGIN

## 14.1 FLOW-TRK-001 — Membuka Tracking

**Aktor:** Pelanggan.

### Main Flow

1. Pelanggan membuka tautan tracking.
2. Browser memuat halaman publik.
3. Frontend membaca token dari route.
4. Frontend mengirim token ke public API.
5. Backend memeriksa rate limit.
6. Backend melakukan hash token.
7. Backend mencari token tersimpan.
8. Backend memeriksa status aktif dan kedaluwarsa.
9. Backend menentukan resource yang boleh ditampilkan.
10. Backend mengambil data status.
11. Backend mengembalikan response publik yang telah dibatasi.
12. Frontend menampilkan status cucian dan antar-jemput.
13. Frontend menampilkan waktu pembaruan terakhir.

### Data yang Boleh Ditampilkan

- Nomor pesanan.
- Jenis layanan.
- Berat atau jumlah.
- Status cucian.
- Estimasi selesai.
- Status penjemputan.
- Status pengantaran.
- Total dan sisa tagihan.
- Waktu pembaruan terakhir.
- Kontak usaha.

### Data yang Tidak Boleh Ditampilkan

- Alamat pelanggan lengkap.
- Nomor telepon lengkap.
- Data pelanggan lain.
- Audit internal.
- Catatan rahasia petugas.
- Informasi autentikasi.
- Detail keuangan internal.

## 14.2 FLOW-TRK-002 — Memperbarui Tampilan Tracking

1. Pelanggan membuka tracking.
2. Frontend menampilkan data terbaru.
3. Staf melakukan perubahan status melalui dashboard.
4. Backend menyimpan status baru.
5. Ketika pelanggan menekan Muat Ulang atau polling berjalan, frontend meminta data terbaru.
6. Backend mengembalikan status yang telah diperbarui.
7. Frontend menampilkan progres terbaru.

Rekomendasi polling otomatis: 60 detik ketika halaman aktif.

MVP tidak menggunakan WebSocket.

## 14.3 FLOW-TRK-003 — Token Tidak Valid

Jika token salah, kedaluwarsa, atau dicabut:

1. Backend menolak akses.
2. Backend tidak mengungkapkan apakah nomor pesanan tertentu ada.
3. Frontend menampilkan pesan umum.
4. Pelanggan dapat menghubungi admin untuk meminta bantuan.
5. Data privat tidak ditampilkan.

## 14.4 FLOW-TRK-004 — Rotasi Token

1. Admin membuka pengaturan tracking pesanan.
2. Admin memilih Ganti Tautan.
3. Backend memeriksa permission.
4. Backend mencabut token lama.
5. Backend menghasilkan token baru.
6. Backend menyimpan hash token baru.
7. Admin menerima tautan baru.
8. Admin dapat membagikan tautan secara manual.

Token lama tidak dapat digunakan lagi.

---

# 15. FLOW KEUANGAN DAN LAPORAN

## 15.1 FLOW-FIN-001 — Mencatat Pengeluaran

1. Owner atau Kasir yang berizin membuka Keuangan.
2. Pengguna memilih Tambah Pengeluaran.
3. Pengguna memasukkan kategori.
4. Pengguna memasukkan nominal.
5. Pengguna menentukan tanggal.
6. Pengguna memasukkan keterangan.
7. Backend memvalidasi data.
8. Backend menyimpan pengeluaran.
9. Audit dicatat jika diperlukan.
10. Dashboard keuangan diperbarui.

## 15.2 FLOW-FIN-002 — Melihat Laporan

1. Owner membuka laporan.
2. Owner memilih rentang tanggal.
3. Frontend mengirim filter.
4. Backend menjalankan query agregasi.
5. Backend mengembalikan ringkasan.
6. Frontend menampilkan hasil.

Laporan wajib membedakan:

- Nilai pesanan.
- Pembayaran diterima.
- Sisa tagihan.
- Pengeluaran.
- Selisih kas sederhana.

Selisih kas tidak boleh dinyatakan sebagai laba bersih akuntansi.

## 15.3 FLOW-FIN-003 — Ekspor CSV

1. Pengguna membuka laporan.
2. Pengguna menentukan filter.
3. Pengguna memilih Ekspor CSV.
4. Backend memeriksa permission.
5. Backend menjalankan query.
6. Backend menghasilkan file.
7. Browser mengunduh file.

Data yang diekspor mengikuti hak akses pengguna.

---

# 16. FLOW PENGATURAN USAHA

## 16.1 FLOW-SET-001 — Memperbarui Profil

1. Owner membuka Pengaturan.
2. Owner memperbarui nama, alamat, kontak, atau profil usaha.
3. Frontend memvalidasi.
4. Backend memeriksa permission.
5. Backend menyimpan perubahan.
6. Nota dan informasi publik berikutnya menggunakan profil terbaru.

## 16.2 FLOW-SET-002 — Mengubah Harga

1. Owner membuka daftar layanan.
2. Owner memilih layanan.
3. Owner mengubah tarif.
4. Sistem menampilkan konfirmasi.
5. Backend memvalidasi tarif.
6. Backend menyimpan harga aktif.
7. Backend menyimpan audit.
8. Harga baru digunakan oleh pesanan berikutnya.

Pesanan lama tidak boleh dihitung ulang secara otomatis hanya karena perubahan tarif katalog.

## 16.3 FLOW-SET-003 — Membuat Akun Pegawai

1. Owner membuka Pengguna.
2. Owner memilih Tambah Pengguna.
3. Owner memasukkan data akun.
4. Owner memilih role.
5. Backend memvalidasi input.
6. Backend membuat akun.
7. Password diproses menggunakan hashing yang aman.
8. Akun tersedia untuk login.

## 16.4 FLOW-SET-004 — Menonaktifkan Pegawai

1. Owner membuka akun.
2. Owner memilih Nonaktifkan.
3. Backend memeriksa permission.
4. Backend menonaktifkan akun.
5. Backend mencabut sesi aktif.
6. Riwayat pekerjaan pegawai tetap tersimpan.

---

# 17. STATE MACHINE SISTEM

## 17.1 Prinsip Umum

Sistem mempunyai empat kelompok status independen:

1. Laundry Status.
2. Pickup Status.
3. Delivery Status.
4. Payment Status.

Status tidak boleh digabungkan menjadi satu field umum.

## 17.2 Laundry State Machine

Alur standar:

RECEIVED
→ QUEUED
→ WASHING
→ DRYING
→ IRONING
→ QC_PACKING
→ READY
→ COMPLETED

Untuk layanan tanpa setrika:

DRYING → QC_PACKING.

### Aturan Transisi

| Dari       | Ke         | Kondisi                             |
| ---------- | ---------- | ----------------------------------- |
| RECEIVED   | QUEUED     | Pesanan diterima secara valid.      |
| QUEUED     | WASHING    | Pekerjaan dimulai.                  |
| WASHING    | DRYING     | Tahap cuci selesai.                 |
| DRYING     | IRONING    | Layanan membutuhkan setrika.        |
| DRYING     | QC_PACKING | Layanan tidak memerlukan setrika.   |
| IRONING    | QC_PACKING | Penyetrikaan selesai.               |
| QC_PACKING | READY      | Pemeriksaan dan pengemasan selesai. |
| READY      | COMPLETED  | Serah terima terkonfirmasi.         |

Transisi koreksi dapat dibuat berdasarkan permission dan alasan.

Status CANCELLED hanya dapat digunakan melalui prosedur pembatalan yang sah.

## 17.3 Pickup State Machine

Alur standar:

REQUESTED
→ CONFIRMED
→ ASSIGNED
→ EN_ROUTE
→ PICKED_UP
→ AT_LAUNDRY

Cabang:

- REQUESTED → REJECTED.
- Status aktif → CANCELLED sesuai izin.
- Status perjalanan → FAILED jika penjemputan tidak berhasil.

## 17.4 Delivery State Machine

Alur standar:

PENDING
→ SCHEDULED
→ EN_ROUTE
→ IN_DELIVERY
→ DELIVERED

Cabang:

- Status aktif → FAILED.
- FAILED → Penjadwalan ulang melalui alur yang terdokumentasi.
- Status yang masih dapat dibatalkan → CANCELLED.

## 17.5 Payment State

Status pembayaran diturunkan dari transaksi sah.

**UNPAID**

Jumlah pembayaran sah = 0.

**PARTIALLY_PAID**

Jumlah pembayaran sah lebih dari 0 dan lebih kecil dari total tagihan.

**PAID**

Jumlah pembayaran sah sama dengan total tagihan.

Jika pembayaran dibatalkan, status dihitung ulang.

---

# 18. ATURAN KONSISTENSI ANTARMODUL

## 18.1 Aturan Pesanan dan Pembayaran

- Order dapat aktif meski belum dibayar.
- Order dapat READY meski belum lunas.
- Order dapat COMPLETED meski belum lunas jika serah terima diizinkan.
- Sisa tagihan tetap menjadi piutang.
- Pembayaran tidak otomatis mengubah status pencucian.

## 18.2 Aturan Pesanan dan Pickup

- Pickup request dibuat sebelum order jika pelanggan menggunakan penjemputan.
- Order final dibuat setelah pemeriksaan dan penimbangan.
- Konversi pickup harus atomik.
- Satu pickup request tidak boleh membuat dua order akibat retry.
- Histori pickup harus tetap dapat dilacak.

## 18.3 Aturan Pesanan dan Delivery

- Pengantaran normal memerlukan order READY.
- Delivery DELIVERED menunjukkan serah terima berhasil.
- Order COMPLETED hanya boleh terjadi setelah syarat serah terima terpenuhi.
- Jika delivery FAILED, order tidak boleh otomatis COMPLETED.

## 18.4 Aturan Tracking dan Database

- Tracking merupakan representasi data yang tersimpan.
- Tracking tidak memiliki salinan status bisnis yang dikelola terpisah.
- Perubahan status terjadi melalui endpoint internal yang berwenang.
- Public API membaca informasi terbaru dari sistem.
- Token tracking tidak memberikan izin mutasi.

## 18.5 Aturan Laporan

- Nilai order berasal dari pesanan sah.
- Uang masuk berasal dari pembayaran sah.
- Piutang berasal dari sisa tagihan.
- Pengeluaran berasal dari transaksi pengeluaran.
- Refund atau void memengaruhi perhitungan sesuai aturan keuangan.
- Dashboard dan laporan menggunakan definisi metrik yang sama.

---

# 19. SEQUENCE FLOW ANTARKOMPONEN

## 19.1 SQ-001 — Membuat Pesanan

Kasir
→ React Form
→ Orders API
→ Authentication Middleware
→ Authorization
→ Order Service
→ Pricing Engine
→ Orders Repository
→ PostgreSQL
→ Audit / Tracking Service
→ API Response
→ React Detail Pesanan

### Transaction Boundary

Pembuatan order, item layanan, status awal, dan relasi tracking yang wajib tersedia harus konsisten dalam satu operasi bisnis.

## 19.2 SQ-002 — Mencatat Pembayaran

Kasir
→ React Payment Form
→ Payments API
→ Authentication & Permission
→ Payment Service
→ Lock Order
→ Validate Remaining Balance
→ Save Payment
→ Update Derived Payment Summary
→ Commit Transaction
→ API Response
→ React Payment Result

## 19.3 SQ-003 — Tracking Publik

Pelanggan
→ React Public Tracking
→ Public Tracking API
→ Rate Limiter
→ Token Validator
→ Tracking Service
→ Repository
→ PostgreSQL
→ Public Response Mapper
→ React Timeline

Tidak ada middleware login petugas pada jalur publik ini.

## 19.4 SQ-004 — Pickup ke Order

Kasir
→ Pickup Detail
→ Convert to Order
→ Pickup API
→ Authentication & Authorization
→ Pickup Service
→ Validate Pickup Status
→ Lock Pickup Resource
→ Order Creation Service
→ Save Linked Order
→ Update Pickup Conversion Reference
→ Commit
→ API Response

## 19.5 SQ-005 — Update Status Cucian

Staf
→ Status Control
→ Orders API
→ Authorization
→ State Machine
→ Version Check
→ Update Order
→ Insert Status History
→ Commit
→ API Response

Tracking pelanggan membaca hasil setelah perubahan disimpan.

---

# 20. ERROR, EXCEPTION, DAN RECOVERY FLOW

## 20.1 Error Matrix

| Kondisi                 | Respons Sistem                       | Tindakan Pengguna                                  |
| ----------------------- | ------------------------------------ | -------------------------------------------------- |
| Session expired         | 401 dan arahkan login                | Login kembali.                                     |
| Tidak memiliki izin     | 403 dan halaman akses ditolak        | Hubungi Owner jika perlu.                          |
| Data tidak ditemukan    | 404 aman                             | Kembali ke daftar.                                 |
| Input tidak valid       | 422 dan pesan per field              | Perbaiki input.                                    |
| Data sudah berubah      | 409 Conflict                         | Muat ulang data.                                   |
| Pembayaran berlebih     | Error domain                         | Periksa saldo terbaru.                             |
| Permintaan duplikat     | Hasil idempoten atau konflik terarah | Jangan buat transaksi baru.                        |
| Token tracking salah    | Pesan tracking tidak tersedia        | Hubungi admin.                                     |
| Token kedaluwarsa       | Akses tracking ditolak               | Minta tautan baru.                                 |
| Rate limit tercapai     | 429                                  | Coba lagi sesuai arahan.                           |
| Server gagal            | 500 aman                             | Coba lagi; cek status transaksi sebelum mengulang. |
| Database tidak tersedia | 503                                  | Tampilkan gangguan.                                |
| PDF gagal dibuat        | Error unduhan                        | Coba lagi tanpa mengubah pesanan.                  |
| WhatsApp tidak terbuka  | Tampilkan alternatif salin pesan     | Kirim manual.                                      |
| Pengantaran gagal       | Status FAILED                        | Jadwalkan ulang.                                   |
| Koneksi terputus        | Informasi belum terkonfirmasi        | Periksa hasil sebelum retry.                       |

## 20.2 FLOW-ERR-001 — Koneksi Putus Saat Membuat Pesanan

1. Kasir menekan Simpan.
2. Request dikirim.
3. Koneksi terputus sebelum respons diterima.
4. Frontend tidak mengetahui apakah transaksi berhasil.
5. Frontend menampilkan status belum terkonfirmasi.
6. Pengguna dapat melakukan retry dengan idempotency key yang sama.
7. Backend mengembalikan hasil operasi sebelumnya jika sudah berhasil.
8. Tidak terjadi pesanan ganda.

## 20.3 FLOW-ERR-002 — Konflik Status

1. Dua staf membuka pesanan versi sama.
2. Staf pertama mengubah status.
3. Backend menyimpan versi baru.
4. Staf kedua mengirim perubahan berdasarkan versi lama.
5. Backend mengembalikan 409.
6. Frontend meminta pemuatan ulang.
7. Staf meninjau status terbaru.

## 20.4 FLOW-ERR-003 — Layanan PDF Tidak Tersedia

1. Pengguna memilih unduh nota.
2. PDF generator gagal.
3. Backend mengembalikan error terstruktur.
4. Frontend menampilkan pesan.
5. Pengguna tetap dapat melihat informasi pesanan.
6. Data pesanan dan pembayaran tidak berubah.

## 20.5 FLOW-ERR-004 — Token Tracking Dicabut

1. Pelanggan membuka tautan lama.
2. Backend memeriksa token.
3. Token berstatus revoked.
4. Backend menolak akses.
5. Frontend menampilkan informasi umum.
6. Pelanggan dapat meminta tautan baru melalui admin.

---

# 21. UI STATE DAN FEEDBACK

## 21.1 Loading State

Ditampilkan ketika:

- Login diproses.
- Daftar pesanan dimuat.
- Detail pesanan dibuka.
- Pembayaran diproses.
- Status diperbarui.
- Tracking dimuat.
- Laporan dihitung.

## 21.2 Success State

Ditampilkan hanya setelah backend mengonfirmasi keberhasilan.

Contoh:

- Pesanan berhasil dibuat.
- Pembayaran berhasil dicatat.
- Status berhasil diperbarui.
- Jadwal berhasil dikonfirmasi.

Membuka WhatsApp tidak boleh menghasilkan pesan "WhatsApp berhasil terkirim".

## 21.3 Empty State

Contoh:

- Belum ada pesanan hari ini.
- Belum ada pelanggan.
- Tidak ada tugas kurir.
- Belum ada pengeluaran.
- Tidak ada pesanan terlambat.

Setiap empty state sebaiknya menyediakan tindakan berikutnya yang relevan.

## 21.4 Error State

Pesan harus:

1. Singkat.
2. Mudah dipahami.
3. Menjelaskan hal yang dapat dilakukan pengguna.
4. Tidak menampilkan stack trace.
5. Tidak mengungkapkan data sensitif.

## 21.5 Confirmation State

Konfirmasi wajib pada:

- Pembatalan pesanan.
- Void pembayaran.
- Perubahan harga yang signifikan.
- Penonaktifan akun.
- Pencabutan token tracking.
- Tindakan yang dapat berdampak pada transaksi yang sudah berjalan.

---

# 22. SECURITY FLOW

## 22.1 Security Boundary

Sistem memisahkan:

- Jalur pengguna internal.
- Jalur publik pelanggan.
- Resource data keuangan.
- Resource data pribadi.
- Operasi administratif.

## 22.2 Authorization Flow

1. Backend menerima request.
2. Backend memvalidasi sesi atau token.
3. Backend mengidentifikasi subjek akses.
4. Backend memeriksa permission.
5. Backend memeriksa cakupan resource.
6. Backend mengizinkan atau menolak.
7. Hanya data yang sesuai izin dikembalikan.

## 22.3 Public Tracking Security

Ketentuan:

- Token tidak mudah ditebak.
- Token disimpan sebagai hash.
- Token dapat dicabut.
- Tidak ada indeks mesin pencari.
- Tidak ada cache publik data sensitif.
- Tidak ada analytics pihak ketiga yang membocorkan URL.
- Token mentah tidak dicatat di log.
- Informasi pribadi diminimalkan.
- Akses dibatasi berdasarkan resource.

## 22.4 Payment Security

- Hanya petugas berizin dapat mencatat pembayaran.
- Backend menghitung saldo.
- Perubahan pembayaran memiliki audit.
- Tidak ada verifikasi otomatis palsu.
- Tidak ada pembayaran negatif.
- Tidak ada pembayaran melebihi tagihan tanpa alur khusus.
- Retry tidak boleh menciptakan pembayaran kedua.

---

# 23. DATA FLOW DAN EVENT MATRIX

## 23.1 Event Utama

| Event                      | Trigger                        | Data yang Dipengaruhi            |
| -------------------------- | ------------------------------ | -------------------------------- |
| `ORDER_CREATED`          | Kasir membuat order            | Orders, Items, History, Tracking |
| `ORDER_UPDATED`          | Kasir mengubah order           | Orders, Items, Audit             |
| `ORDER_STATUS_CHANGED`   | Staf mengubah status           | Orders, Status History           |
| `ORDER_CANCELLED`        | Pembatalan disetujui           | Orders, Audit, relasi terkait    |
| `PAYMENT_RECORDED`       | Kasir memverifikasi pembayaran | Payments, Ringkasan tagihan      |
| `PAYMENT_VOIDED`         | Koreksi pembayaran disetujui   | Payments, Void, Audit            |
| `PICKUP_REQUESTED`       | Pelanggan mengajukan pickup    | Pickup Requests, Tracking        |
| `PICKUP_CONFIRMED`       | Admin mengonfirmasi            | Pickup Requests                  |
| `PICKUP_ASSIGNED`        | Admin menugaskan kurir         | Delivery Tasks                   |
| `PICKUP_COMPLETED`       | Cucian tiba di laundry         | Pickup Status History            |
| `PICKUP_CONVERTED`       | Kasir membuat order            | Pickup Requests, Orders          |
| `DELIVERY_SCHEDULED`     | Admin membuat tugas            | Delivery Tasks                   |
| `DELIVERY_DELIVERED`     | Serah terima berhasil          | Delivery History, Orders         |
| `DELIVERY_FAILED`        | Pengantaran gagal              | Delivery History                 |
| `SERVICE_PRICE_UPDATED`  | Owner mengubah tarif           | Services, Audit                  |
| `TRACKING_TOKEN_ROTATED` | Admin mengganti token          | Tracking Tokens, Audit           |

Event di atas merupakan peristiwa logis dalam aplikasi, bukan kewajiban menggunakan message broker atau event bus eksternal.

## 23.2 Konsistensi Event

1. Event logis hanya dianggap berhasil setelah transaksi utama berhasil.
2. Audit harus konsisten dengan perubahan yang dicatat.
3. Event tidak boleh menggandakan transaksi keuangan.
4. Jika kelak terdapat notifikasi otomatis, pengiriman eksternal harus dipisahkan dari transaksi database menggunakan mekanisme andal seperti outbox.
5. MVP tidak memerlukan queue untuk komunikasi WhatsApp manual.

---

# 24. ALUR RESPONSIVE DAN PWA

## 24.1 Penggunaan Melalui HP

Alur kasir harus mendukung:

1. Membuka dashboard.
2. Menekan Buat Pesanan.
3. Mencari pelanggan.
4. Memilih layanan.
5. Memasukkan berat.
6. Meninjau total.
7. Menyimpan.
8. Membuka nota.
9. Membagikan melalui WhatsApp.

Pengguna tidak perlu berpindah ke laptop.

## 24.2 Penggunaan Melalui Laptop

Fungsi yang sama dapat menggunakan ruang layar lebih besar.

Contoh:

- Sidebar.
- Tabel pesanan.
- Filter.
- Detail panel.
- Grafik laporan.

## 24.3 Kondisi PWA

Aplikasi dapat dipasang ke home screen pada browser yang mendukung.

Tetapi:

- MVP tetap membutuhkan koneksi internet.
- Transaksi tidak disimpan sebagai transaksi sukses ketika offline.
- Data privat tidak boleh tersimpan dalam cache publik.
- Kegagalan jaringan harus ditangani secara eksplisit.

---

# 25. END-TO-END USER JOURNEY

## 25.1 Journey A — Laundry Langsung

Pelanggan datang
→ Kasir mencari pelanggan
→ Kasir membuat pesanan
→ Backend menghitung total
→ Pesanan tersimpan
→ Nota dibuat
→ Kasir membagikan tautan secara manual
→ Staf memproses cucian
→ Staf memperbarui status
→ Pelanggan melihat tracking
→ Cucian siap
→ Pelanggan mengambil
→ Kasir memverifikasi serah terima
→ Pesanan selesai secara operasional
→ Pembayaran tetap dipantau sampai lunas

## 25.2 Journey B — Pickup dan Delivery

Pelanggan mengajukan pickup
→ Admin meninjau
→ Admin mengonfirmasi
→ Kurir ditugaskan
→ Kurir menjemput
→ Cucian tiba di laundry
→ Kasir menimbang dan membuat order
→ Pesanan diproses
→ Cucian siap
→ Admin menjadwalkan delivery
→ Kurir mengantar
→ Pelanggan menerima
→ Serah terima dikonfirmasi
→ Order selesai secara operasional

## 25.3 Journey C — Pembayaran Bertahap

Pesanan dibuat
→ Total dihitung
→ Pelanggan membayar DP
→ Kasir mencatat pembayaran
→ Sistem menghitung sisa
→ Pelanggan membayar pelunasan
→ Kasir memverifikasi
→ Sistem menghitung total pembayaran sah
→ Status menjadi PAID

## 25.4 Journey D — Pelanggan Memantau Tanpa Login

Pelanggan menerima tautan
→ Membuka browser
→ Token diverifikasi
→ Status ditampilkan
→ Staf memperbarui proses
→ Pelanggan memuat ulang
→ Status terbaru terlihat

Tidak memerlukan login, OTP, atau instalasi aplikasi.

---

# 26. FLOW VALIDATION DAN ACCEPTANCE MATRIX

| ID        | Flow               | Acceptance Criteria                                |
| --------- | ------------------ | -------------------------------------------------- |
| AFD-AT-01 | Login              | Akun valid masuk sesuai peran.                     |
| AFD-AT-02 | Session            | Sesi kedaluwarsa tidak dapat digunakan.            |
| AFD-AT-03 | Customer           | Data pelanggan dapat dibuat dan dicari.            |
| AFD-AT-04 | Order              | Pesanan dibuat tanpa duplikasi.                    |
| AFD-AT-05 | Pricing            | Backend menghitung total yang benar.               |
| AFD-AT-06 | Multi-Service      | Beberapa item dihitung konsisten.                  |
| AFD-AT-07 | Update Order       | Konflik versi ditangani.                           |
| AFD-AT-08 | Cancellation       | Alasan dan audit tersimpan.                        |
| AFD-AT-09 | Laundry Status     | Transisi valid berhasil, invalid ditolak.          |
| AFD-AT-10 | QC                 | Cucian tidak otomatis READY saat gagal QC.         |
| AFD-AT-11 | Full Payment       | Tagihan menjadi lunas.                             |
| AFD-AT-12 | DP                 | Sisa tagihan dihitung benar.                       |
| AFD-AT-13 | Concurrent Payment | Tidak terjadi pembayaran berlebih.                 |
| AFD-AT-14 | Payment Void       | Riwayat dan saldo konsisten.                       |
| AFD-AT-15 | Invoice            | Nota sesuai data backend.                          |
| AFD-AT-16 | WhatsApp           | Pesan siap kirim, tidak diklaim terkirim otomatis. |
| AFD-AT-17 | Pickup Public      | Pelanggan dapat mengajukan tanpa login.            |
| AFD-AT-18 | Pickup Confirm     | Admin dapat mengonfirmasi.                         |
| AFD-AT-19 | Courier Assignment | Tugas terlihat oleh kurir yang tepat.              |
| AFD-AT-20 | Pickup Conversion  | Satu pickup hanya menjadi satu order.              |
| AFD-AT-21 | Delivery           | Status berubah sesuai tindakan kurir.              |
| AFD-AT-22 | Failed Delivery    | Order tidak otomatis selesai.                      |
| AFD-AT-23 | Tracking           | Token valid membuka data yang tepat.               |
| AFD-AT-24 | Tracking Security  | Token lain tidak membuka pesanan berbeda.          |
| AFD-AT-25 | Token Rotation     | Token lama tidak berlaku.                          |
| AFD-AT-26 | Expenses           | Pengeluaran masuk laporan.                         |
| AFD-AT-27 | Reports            | Metrik konsisten dengan transaksi.                 |
| AFD-AT-28 | Price Changes      | Harga lama pada order tidak berubah.               |
| AFD-AT-29 | RBAC               | Tindakan tanpa izin ditolak backend.               |
| AFD-AT-30 | Network Failure    | Retry tidak menghasilkan transaksi duplikat.       |
| AFD-AT-31 | Mobile UX          | Seluruh alur utama dapat dijalankan pada HP.       |
| AFD-AT-32 | Audit              | Perubahan penting memiliki jejak audit.            |

---

# 27. TRACEABILITY TERHADAP PRD DAN TRD

| Modul PRD      | Komponen TRD                      | Flow AFD  |
| -------------- | --------------------------------- | --------- |
| Dashboard      | Dashboard API dan Reporting       | FLOW-DASH |
| Pesanan        | Orders Service dan Pricing Engine | FLOW-ORD  |
| Pelanggan      | Customers Service                 | FLOW-CUS  |
| Pencucian      | Order State Machine               | FLOW-WRK  |
| Pembayaran     | Payments Service                  | FLOW-PAY  |
| Nota           | Invoice Service                   | FLOW-INV  |
| Pickup         | Pickup Service                    | FLOW-PUP  |
| Delivery       | Delivery Service                  | FLOW-DLV  |
| Tracking       | Token Service dan Public API      | FLOW-TRK  |
| Pengaturan     | Settings dan User Management      | FLOW-SET  |
| Autentikasi    | Session dan RBAC                  | FLOW-AUTH |
| Error Handling | Exception Handler dan Idempotency | FLOW-ERR  |

AFD menjadi sumber alur yang harus diikuti oleh desain frontend, service backend, kontrak API, dan pengujian.

---

# 28. KEPUTUSAN TERBUKA

Beberapa keputusan tetap memerlukan persetujuan sebelum implementasi final.

| ID         | Keputusan                           | Rekomendasi                                                  |
| ---------- | ----------------------------------- | ------------------------------------------------------------ |
| AFD-DEC-01 | Aturan pembulatan berat             | Mengikuti pengaturan usaha.                                  |
| AFD-DEC-02 | Pickup di luar jam operasional      | Memerlukan konfirmasi manual.                                |
| AFD-DEC-03 | Biaya antar-jemput                  | Tetap/manual untuk MVP.                                      |
| AFD-DEC-04 | Serah terima ketika belum lunas     | Diizinkan dengan peringatan bila disetujui Owner.            |
| AFD-DEC-05 | Pembatalan order yang telah dibayar | Memerlukan SOP refund.                                       |
| AFD-DEC-06 | Masa berlaku tracking               | Usulan 90 hari setelah penyelesaian.                         |
| AFD-DEC-07 | Status layanan khusus               | Menggunakan jalur tahap yang relevan.                        |
| AFD-DEC-08 | Karyawan merangkap tugas            | Owner dapat menjalankan semua fungsi yang berizin.           |
| AFD-DEC-09 | Pengantaran gagal                   | Dapat dijadwalkan ulang tanpa menghapus histori.             |
| AFD-DEC-10 | Pemulihan akun tanpa email          | Prosedur reset oleh Owner atau administrator yang berwenang. |
| AFD-DEC-11 | Pengembalian dana                   | Proses manual dan catatan keuangan terpisah.                 |
| AFD-DEC-12 | Penyimpanan formulir pickup         | Mengikuti kebijakan privasi dan retensi data.                |

Keputusan tersebut belum otomatis menjadi persetujuan final.

---

# 29. DEFINITION OF DONE AFD

AFD dianggap lengkap secara desain apabila:

1. Setiap fitur P0 memiliki alur utama.
2. Setiap alur memiliki aktor dan kondisi awal yang jelas.
3. Perubahan data dapat ditelusuri ke modul yang bertanggung jawab.
4. Status sistem telah didefinisikan.
5. Transisi tidak valid dapat diidentifikasi.
6. Penanganan error utama tersedia.
7. Alur pembayaran tidak menciptakan inkonsistensi.
8. Tracking tanpa login memiliki batas keamanan yang jelas.
9. Alur pickup dan order dapat dihubungkan.
10. Tugas kurir memiliki riwayat.
11. Aturan serah terima terdokumentasi.
12. Navigasi mengikuti permission.
13. Alur dapat diterjemahkan ke UI dan API.
14. Acceptance criteria dapat diuji.
15. Tidak terdapat konflik yang belum dijelaskan antara PRD, TRD, dan AFD.

Persetujuan akhir memerlukan review lintas dokumen.

---

# 30. KESIMPULAN

Application Flow Documentation v1.0 mendefinisikan alur teknis dan operasional Web App Manajemen Laundry UMKM berdasarkan PRD v1.0 dan TRD v1.0.

Sistem terdiri atas dua lingkungan utama:

**Dashboard Internal**

Digunakan Owner, Kasir, Staf Laundry, dan Kurir untuk mengelola operasional, pelanggan, pembayaran, dan antar-jemput.

**Portal Publik**

Digunakan pelanggan untuk mengajukan penjemputan, memantau status cucian, melihat nota, dan memeriksa pengantaran tanpa login.

AFD memisahkan empat status penting, yaitu status cucian, penjemputan, pengantaran, dan pembayaran, sehingga pengelolaan proses tetap konsisten.

Perubahan bisnis dilakukan melalui backend yang memvalidasi permission, aturan domain, dan transaksi database.

Aplikasi mempertahankan prinsip sederhana dan hemat biaya, tanpa ketergantungan pada mesin kasir, printer nota, payment gateway, WhatsApp API, atau pelacakan GPS.

Dokumen ini menjadi dasar bagi penyusunan Database Design Document, API Contract, UI/UX Specification, serta implementasi frontend dan backend.

**Status: AFD v1.0 — DRAFT FOR ARCHITECTURE & FLOW REVIEW.**

---

**AKHIR DOKUMEN — APPLICATION FLOW DOCUMENTATION v1.0**
