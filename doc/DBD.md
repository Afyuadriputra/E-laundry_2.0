
# DESIGN BRIEF DOCUMENTATION (DBD)

## WEB APP MANAJEMEN LAUNDRY UMKM

**Versi Dokumen:** 1.0
**Tanggal:** 3 November 2026
**Status:** Draft — Design Review
**Dokumen Acuan:** PRD v1.0, TRD v1.0, AFD v1.0
**Jenis Dokumen:** Product Design & UI/UX Brief
**Platform:** Responsive Web Application / Progressive Web App
**Target Pengguna:** Usaha Laundry Mikro, Kecil, dan Menengah
**Pendekatan:** Mobile-First, Simple, Accessible, Task-Oriented

---

# 1. PENDAHULUAN

## 1.1 Latar Belakang

Web App Manajemen Laundry UMKM dikembangkan untuk membantu pemilik usaha laundry melakukan digitalisasi operasional tanpa memerlukan perangkat tambahan seperti mesin kasir fisik, printer nota, scanner barcode, atau layanan payment gateway.

Aplikasi mengelola penerimaan pesanan, pelanggan, pencucian, pembayaran manual, nota digital, penjemputan, pengantaran, serta laporan operasional dalam satu sistem.

Keberhasilan aplikasi tidak hanya ditentukan oleh kelengkapan fitur, tetapi juga oleh kemudahan penggunaan bagi pemilik usaha dan karyawan yang belum tentu memiliki pengalaman menggunakan sistem manajemen bisnis.

Oleh karena itu, dibutuhkan rancangan antarmuka yang sederhana, jelas, cepat dipelajari, dan dapat dioperasikan melalui smartphone.

Design Brief Documentation ini menetapkan landasan desain agar seluruh antarmuka, komponen, interaksi, dan pengalaman pengguna memiliki standar yang konsisten.

## 1.2 Tujuan Dokumen

1. Mendefinisikan arah visual produk.
2. Menetapkan prinsip dan standar UI/UX.
3. Menentukan kebutuhan tampilan berdasarkan peran pengguna.
4. Menyusun information architecture dan navigasi.
5. Menentukan kebutuhan setiap halaman.
6. Mendefinisikan design system.
7. Menetapkan standar komponen dan interaksi.
8. Mendefinisikan desain mobile, tablet, dan desktop.
9. Menentukan tampilan status dan feedback sistem.
10. Menetapkan standar aksesibilitas.
11. Menentukan kriteria penerimaan desain.
12. Menjadi acuan pembuatan wireframe, high-fidelity design, dan prototype.

## 1.3 Hubungan dengan Dokumen Sebelumnya

| Dokumen  | Fungsi dalam Desain                                                                      |
| -------- | ---------------------------------------------------------------------------------------- |
| PRD v1.0 | Menentukan fitur, pengguna, prioritas, dan kebutuhan produk.                             |
| TRD v1.0 | Menentukan teknologi, autentikasi, API, dan batasan teknis.                              |
| AFD v1.0 | Menentukan perjalanan pengguna, transisi status, dan alur operasional.                   |
| DBD v1.0 | Menentukan visual, pengalaman pengguna, komponen, navigasi, dan standar implementasi UI. |

Dokumen DBD tidak boleh mengubah aturan bisnis, otorisasi, dan transaksi yang telah ditentukan dalam PRD, TRD, atau AFD tanpa proses perubahan yang terdokumentasi.

---

# 2. PRODUCT DESIGN VISION

## 2.1 Visi Desain

Menciptakan aplikasi manajemen laundry yang terasa sesederhana menggunakan aplikasi sehari-hari, tetapi memiliki kemampuan yang cukup untuk mengelola usaha secara profesional.

Aplikasi harus:

- Mudah dipahami oleh pengguna baru.
- Nyaman digunakan pada layar HP.
- Cepat dalam pencatatan pesanan.
- Menampilkan informasi dengan jelas.
- Memberikan kepercayaan kepada pelanggan.
- Meminimalkan kemungkinan kesalahan transaksi.
- Menjaga konsistensi tampilan pada seluruh modul.
- Mendukung operasional usaha kecil tanpa perangkat khusus.

## 2.2 Design Positioning

**Clean, Fresh & Trustworthy**

Makna:

**Clean:** Tampilan bersih, rapi, dan tidak berlebihan.

**Fresh:** Memberikan kesan usaha laundry yang modern, segar, dan aktif.

**Trustworthy:** Menekankan kejelasan transaksi, ketepatan status, dan rasa aman terhadap informasi pelanggan.

## 2.3 Design Personality

Karakter desain:

1. Modern.
2. Minimalis.
3. Profesional.
4. Ramah.
5. Praktis.
6. Terpercaya.
7. Mudah dipelajari.
8. Konsisten.
9. Tidak mengintimidasi pengguna awam.
10. Efisien untuk pekerjaan berulang.

## 2.4 Prinsip Pengalaman Utama

Pengguna harus mampu memahami:

- Di mana posisi mereka dalam aplikasi.
- Apa yang harus dilakukan selanjutnya.
- Apa konsekuensi dari suatu tindakan.
- Apakah data sudah berhasil disimpan.
- Apakah pembayaran sudah diverifikasi.
- Bagaimana perkembangan cucian.
- Apakah permintaan antar-jemput sudah dikonfirmasi.
- Apa yang harus dilakukan ketika terjadi kesalahan.

---

# 3. TARGET PENGGUNA DAN KEBUTUHAN DESAIN

## 3.1 Owner / Pemilik Laundry

**Tujuan utama:** Memantau operasional dan kondisi keuangan usaha.

Kebutuhan desain:

- Ringkasan bisnis pada dashboard.
- Akses mudah ke pesanan bermasalah.
- Informasi tagihan belum lunas.
- Pengaturan harga yang sederhana.
- Laporan yang mudah dipahami.
- Pengelolaan akun karyawan.
- Kemampuan menjalankan pekerjaan kasir jika dibutuhkan.

**Masalah yang harus dihindari:**

Dashboard terlalu kompleks, terlalu banyak grafik, atau penggunaan istilah akuntansi yang membingungkan.

## 3.2 Admin / Kasir

**Tujuan utama:** Membuat pesanan dan melayani pelanggan dengan cepat.

Kebutuhan desain:

- Tombol Buat Pesanan yang menonjol.
- Pencarian pelanggan.
- Input berat dan layanan.
- Perhitungan harga otomatis.
- Nota digital.
- Pembayaran manual.
- Tautan WhatsApp.

**Masalah yang harus dihindari:**

Terlalu banyak halaman untuk menyelesaikan satu transaksi.

## 3.3 Staf Laundry

**Tujuan utama:** Melihat pekerjaan dan memperbarui status cucian.

Kebutuhan desain:

- Daftar pekerjaan.
- Informasi layanan dan prioritas.
- Identitas pesanan yang jelas.
- Tombol perubahan status.
- Estimasi selesai.
- Peringatan keterlambatan.

**Masalah yang harus dihindari:**

Menampilkan informasi keuangan atau administrasi yang tidak diperlukan.

## 3.4 Kurir

**Tujuan utama:** Menjalankan penjemputan dan pengantaran.

Kebutuhan desain:

- Daftar tugas hari ini.
- Alamat pelanggan.
- Jadwal.
- Kontak WhatsApp.
- Status pekerjaan.
- Konfirmasi serah terima.

**Masalah yang harus dihindari:**

Terlalu banyak input ketika kurir sedang bekerja di lapangan.

## 3.5 Pelanggan

**Tujuan utama:** Mengetahui perkembangan cucian dan mengajukan penjemputan.

Kebutuhan desain:

- Tidak perlu login.
- Halaman ringan.
- Status mudah dimengerti.
- Informasi estimasi selesai.
- Informasi tagihan yang jelas.
- Tracking antar-jemput.
- Tombol WhatsApp.
- Formulir pickup yang singkat.

**Masalah yang harus dihindari:**

Meminta pelanggan membuat akun, menghafal password, atau membuka terlalu banyak halaman.

---

# 4. DESIGN SUCCESS CRITERIA

## 4.1 Tujuan Usability

| ID        | Target Desain            | Indikator                                                         |
| --------- | ------------------------ | ----------------------------------------------------------------- |
| UX-OBJ-01 | Mempermudah transaksi    | Pesanan standar ditargetkan dibuat dalam maksimal 2 menit.        |
| UX-OBJ-02 | Mempermudah pembelajaran | Pengguna baru memahami navigasi dasar setelah pengenalan singkat. |
| UX-OBJ-03 | Memperjelas status       | Pengguna dapat membedakan status cucian dan pembayaran.           |
| UX-OBJ-04 | Mengurangi kesalahan     | Input penting tervalidasi sebelum disimpan.                       |
| UX-OBJ-05 | Mempermudah tracking     | Pelanggan dapat membuka status melalui tautan tanpa login.        |
| UX-OBJ-06 | Mempermudah antar-jemput | Pelanggan dapat mengajukan pickup melalui formulir singkat.       |
| UX-OBJ-07 | Mendukung HP             | Seluruh alur P0 dapat digunakan pada layar smartphone.            |
| UX-OBJ-08 | Memberikan feedback      | Tindakan penting menampilkan hasil atau kesalahan yang jelas.     |

Target tersebut merupakan sasaran pengujian desain, bukan hasil yang sudah terbukti.

## 4.2 Ukuran Keberhasilan

Pengukuran dilakukan melalui:

- Task completion rate.
- Waktu penyelesaian transaksi.
- Jumlah kesalahan input.
- Jumlah langkah per alur.
- Keberhasilan pencarian pesanan.
- Keberhasilan pengajuan pickup.
- Keberhasilan membuka tracking.
- Hasil usability testing.
- Temuan aksesibilitas.
- Feedback pengguna.

---

# 5. DESIGN SCOPE DAN PRIORITAS

## 5.1 Cakupan MVP

Delapan modul desain:

| ID        | Modul           | Prioritas |
| --------- | --------------- | --------- |
| UI-MOD-01 | Dashboard       | P0        |
| UI-MOD-02 | Pesanan Laundry | P0        |
| UI-MOD-03 | Pelanggan       | P0        |
| UI-MOD-04 | Antar-Jemput    | P0        |
| UI-MOD-05 | Keuangan        | P0        |
| UI-MOD-06 | Nota Digital    | P0        |
| UI-MOD-07 | Tracking Publik | P0        |
| UI-MOD-08 | Pengaturan      | P0        |

Komponen pendukung:

- Login.
- Akses berdasarkan peran.
- Empty state.
- Loading state.
- Error state.
- Modal konfirmasi.
- Toast notification.
- Form validation.
- Responsive navigation.
- Aksesibilitas.

## 5.2 Prioritas Pengalaman

Urutan prioritas desain:

1. Pembuatan pesanan.
2. Pembaruan status cucian.
3. Pembayaran manual.
4. Tracking pelanggan.
5. Permintaan pickup.
6. Pengantaran.
7. Nota digital.
8. Dashboard.
9. Pelanggan.
10. Laporan dan pengaturan.

Urutan ini menunjukkan prioritas perancangan dan pengujian UX, bukan mengubah prioritas fitur dalam PRD.

---

# 6. VISUAL DESIGN DIRECTION

## 6.1 Konsep Visual

Aplikasi menggunakan pendekatan:

**Modern Minimalist Business Application**

Karakter visual:

- Latar dominan putih atau abu-abu sangat muda.
- Warna utama teal.
- Teks berwarna slate gelap.
- Ruang antar-elemen cukup.
- Card dengan border halus.
- Sudut komponen membulat secara moderat.
- Tipografi modern dan mudah dibaca.
- Ikon konsisten.
- Animasi singkat dan fungsional.
- Tidak menggunakan dekorasi berlebihan.

## 6.2 Color Palette

| Token          | Warna       | Hex     | Penggunaan                                    |
| -------------- | ----------- | ------- | --------------------------------------------- |
| Primary        | Deep Teal   | #0F766E | Tombol utama, navigasi aktif, link penting.   |
| Primary Hover  | Dark Teal   | #115E59 | Hover dan pressed state.                      |
| Accent         | Fresh Teal  | #14B8A6 | Ilustrasi, progres dekoratif, aksen terbatas. |
| Background     | Soft White  | #F8FAFC | Latar aplikasi.                               |
| Surface        | White       | #FFFFFF | Card, form, modal.                            |
| Text Primary   | Dark Slate  | #0F172A | Judul dan teks utama.                         |
| Text Secondary | Slate       | #475569 | Teks penjelasan.                              |
| Border         | Light Slate | #E2E8F0 | Pemisah dan border.                           |
| Success        | Dark Green  | #166534 | Status berhasil dan pembayaran lunas.         |
| Warning        | Dark Amber  | #92400E | Keterlambatan dan peringatan.                 |
| Danger         | Dark Red    | #B91C1C | Error dan aksi destruktif.                    |
| Info           | Dark Blue   | #1D4ED8 | Informasi dan progres tertentu.               |

## 6.3 Aturan Penggunaan Warna

1. Primary digunakan pada tindakan utama.
2. Accent tidak digunakan sebagai warna teks kecil di atas latar putih.
3. Success digunakan untuk keberhasilan yang telah terkonfirmasi.
4. Warning digunakan untuk kondisi yang memerlukan perhatian.
5. Danger digunakan untuk pembatalan, validasi gagal, atau tindakan berisiko.
6. Warna status harus selalu disertai label teks.
7. Kontras warna mengikuti target WCAG 2.2 AA.
8. Warna tidak boleh menjadi satu-satunya pembeda status.
9. Jumlah warna yang muncul bersamaan harus dibatasi.
10. Identitas visual mengikuti token agar mudah diubah melalui design system.

## 6.4 Typography

Rekomendasi:

**Font Utama:** Inter.

**Fallback:** System UI, Arial, sans-serif.

Alasan:

- Mudah dibaca pada layar kecil.
- Cocok untuk dashboard.
- Memiliki angka yang jelas.
- Tampil profesional.
- Mendukung antarmuka modern.

### Typography Scale

| Elemen     | Ukuran Awal | Berat    |
| ---------- | ----------: | -------- |
| Display    |       32 px | Bold     |
| Heading 1  |       28 px | Bold     |
| Heading 2  |       24 px | Semibold |
| Heading 3  |       20 px | Semibold |
| Heading 4  |       18 px | Semibold |
| Body       |       16 px | Regular  |
| Body Small |       14 px | Regular  |
| Caption    |       12 px | Regular  |
| Button     |   14–16 px | Semibold |

Ketentuan:

- Teks isi utama diutamakan 16 px.
- Caption tidak digunakan untuk informasi kritis yang memerlukan pembacaan cepat.
- Nominal uang memiliki penekanan visual.
- Angka pada dashboard dapat menggunakan tabular numerals.
- Line height harus mendukung keterbacaan.
- Pembesaran teks browser tidak boleh merusak alur utama.

---

# 7. DESIGN TOKENS

## 7.1 Spacing System

Menggunakan baseline 4 px.

| Token    | Nilai |
| -------- | ----: |
| space-1  |  4 px |
| space-2  |  8 px |
| space-3  | 12 px |
| space-4  | 16 px |
| space-5  | 20 px |
| space-6  | 24 px |
| space-8  | 32 px |
| space-10 | 40 px |
| space-12 | 48 px |
| space-16 | 64 px |

Penggunaan spacing harus konsisten antarhalaman.

## 7.2 Border Radius

| Token       |   Nilai | Penggunaan              |
| ----------- | ------: | ----------------------- |
| radius-sm   |    6 px | Badge, field kecil.     |
| radius-md   |   10 px | Input dan tombol.       |
| radius-lg   |   14 px | Card.                   |
| radius-xl   |   18 px | Modal atau panel utama. |
| radius-full | 9999 px | Pill dan avatar.        |

## 7.3 Shadow

Gunakan tiga tingkat:

**Shadow Small**

Untuk card dengan elevasi ringan.

**Shadow Medium**

Untuk popover dan dropdown.

**Shadow Large**

Untuk modal atau dialog penting.

Bayangan tidak boleh menjadi dekorasi berlebihan. Border halus menjadi pembeda utama antarkomponen.

## 7.4 Component Height

| Komponen                 | Ukuran Rekomendasi                        |
| ------------------------ | ----------------------------------------- |
| Input standar            | 44–48 px                                 |
| Button standar           | 44–48 px                                 |
| Button besar             | 48–52 px                                 |
| Icon button              | Minimal area sentuh 44 × 44 px           |
| Mobile bottom navigation | Sekitar 64–72 px, menyesuaikan safe area |
| Header mobile            | Sekitar 56–64 px                         |

## 7.5 Layout Grid

**Mobile**

- Satu kolom utama.
- Padding horizontal 16 px.
- Card penuh mengikuti lebar konten.
- Form menggunakan pola vertikal.

**Tablet**

- Grid dua kolom untuk konten yang sesuai.
- Navigasi adaptif.

**Desktop**

- Sidebar dan content area.
- Dashboard dapat menggunakan grid beberapa kolom.
- Tabel dapat tampil lebih lengkap.
- Maksimum lebar konten dapat dibatasi agar tidak terlalu melebar.

---

# 8. RESPONSIVE DESIGN STRATEGY

## 8.1 Target Viewport

Pengujian minimal:

| Viewport | Kategori              |
| -------- | --------------------- |
| 320 px   | Smartphone kecil      |
| 360 px   | Smartphone            |
| 375 px   | Smartphone            |
| 390 px   | Smartphone            |
| 430 px   | Smartphone besar      |
| 768 px   | Tablet                |
| 1024 px  | Laptop / tablet besar |
| 1440 px  | Desktop               |

## 8.2 Mobile Navigation

Navigasi utama harus:

- Mudah dijangkau.
- Memprioritaskan tugas sehari-hari.
- Tidak memiliki terlalu banyak menu.
- Memiliki indikator menu aktif.
- Menampilkan label ikon.

Rekomendasi navigasi mobile:

1. Beranda.
2. Pesanan.
3. Tambah Pesanan.
4. Antar-Jemput.
5. Menu.

Tombol Tambah Pesanan menjadi tindakan utama untuk Owner atau Kasir.

Untuk Staf dan Kurir, navigasi disesuaikan dengan tugas mereka.

## 8.3 Desktop Navigation

Gunakan sidebar dengan:

- Logo/nama usaha.
- Dashboard.
- Pesanan.
- Pelanggan.
- Antar-Jemput.
- Keuangan.
- Pengaturan.
- Profil pengguna.
- Logout.

Sidebar menampilkan menu berdasarkan permission.

## 8.4 Adaptasi Konten

**Desktop:** Daftar pesanan menggunakan tabel.

**Mobile:** Daftar pesanan menggunakan card atau tabel responsif yang tidak mengharuskan scroll horizontal pada alur utama.

Informasi penting yang tetap harus terlihat:

- Nomor pesanan.
- Nama pelanggan yang diizinkan.
- Jenis layanan.
- Status.
- Estimasi selesai.
- Tagihan.
- Tindakan detail.

---

# 9. INFORMATION ARCHITECTURE

## 9.1 Aplikasi Internal

Struktur navigasi:

**Login**

**Dashboard**

**Pesanan**

- Semua Pesanan
- Buat Pesanan
- Detail Pesanan
- Riwayat Status
- Nota
- Pembayaran

**Pelanggan**

- Daftar Pelanggan
- Tambah Pelanggan
- Detail Pelanggan
- Riwayat Pesanan

**Antar-Jemput**

- Permintaan Masuk
- Penjemputan
- Pengantaran
- Tugas Kurir
- Riwayat

**Keuangan**

- Ringkasan
- Pembayaran
- Tagihan Belum Lunas
- Pengeluaran
- Laporan

**Pengaturan**

- Profil Usaha
- Layanan dan Harga
- Pengguna
- Konfigurasi Operasional

## 9.2 Portal Pelanggan

Struktur:

**Halaman Tracking**

- Ringkasan Pesanan
- Status Cucian
- Status Penjemputan
- Status Pengantaran
- Pembayaran
- Nota Digital
- Hubungi Laundry

**Halaman Permintaan Pickup**

- Formulir Penjemputan
- Konfirmasi Pengajuan
- Tautan Tracking Permintaan

## 9.3 Aturan Information Architecture

1. Menu harus mengikuti peran pengguna.
2. Informasi prioritas ditempatkan paling atas.
3. Fitur utama dapat dijangkau dengan sedikit langkah.
4. Detail tambahan menggunakan progressive disclosure.
5. Menu publik terpisah dari menu internal.
6. Informasi keuangan sensitif tidak muncul pada halaman staf atau kurir tanpa izin.
7. Nomor pesanan menjadi identitas yang konsisten di berbagai modul.
8. Navigasi harus membantu pengguna kembali ke konteks sebelumnya.

---

# 10. SCREEN INVENTORY

Daftar layar yang harus dirancang.

| ID     | Halaman                        | Prioritas |
| ------ | ------------------------------ | --------- |
| SCR-01 | Login Petugas                  | P0        |
| SCR-02 | Dashboard Owner                | P0        |
| SCR-03 | Dashboard Kasir                | P0        |
| SCR-04 | Daftar Pesanan                 | P0        |
| SCR-05 | Buat Pesanan                   | P0        |
| SCR-06 | Detail Pesanan                 | P0        |
| SCR-07 | Ubah Status Cucian             | P0        |
| SCR-08 | Daftar Pelanggan               | P0        |
| SCR-09 | Form Pelanggan                 | P0        |
| SCR-10 | Detail Pelanggan               | P0        |
| SCR-11 | Permintaan Pickup Internal     | P0        |
| SCR-12 | Detail Pickup                  | P0        |
| SCR-13 | Tugas Kurir                    | P0        |
| SCR-14 | Detail Pengantaran             | P0        |
| SCR-15 | Pembayaran                     | P0        |
| SCR-16 | Riwayat Pembayaran             | P0        |
| SCR-17 | Keuangan                       | P0        |
| SCR-18 | Pengeluaran                    | P0        |
| SCR-19 | Laporan                        | P0        |
| SCR-20 | Nota Digital                   | P0        |
| SCR-21 | Pengaturan Profil              | P0        |
| SCR-22 | Pengaturan Layanan dan Harga   | P0        |
| SCR-23 | Manajemen Pengguna             | P0        |
| SCR-24 | Tracking Publik                | P0        |
| SCR-25 | Formulir Pickup Publik         | P0        |
| SCR-26 | Konfirmasi Pickup Publik       | P0        |
| SCR-27 | Halaman Akses Ditolak          | P0        |
| SCR-28 | Halaman Tracking Tidak Valid   | P0        |
| SCR-29 | Halaman Gangguan Layanan       | P0        |
| SCR-30 | Dialog Konfirmasi dan Feedback | P0        |

Screen inventory mencakup layar penuh, subhalaman, dan interaksi penting. Tidak semuanya harus menjadi route terpisah.

---

# 11. DETAIL DESAIN DASHBOARD

## 11.1 Dashboard Owner

**Tujuan:** Memberikan ringkasan kondisi usaha.

### Komponen

**Header**

- Nama laundry.
- Sapaan pengguna.
- Tanggal.
- Akses profil.

**Summary Cards**

- Jumlah pesanan.
- Nilai pesanan.
- Pembayaran diterima.
- Cucian diproses.
- Siap diambil.
- Tagihan belum lunas.

**Operational Overview**

- Distribusi status pesanan.
- Pesanan terlambat.
- Pesanan terbaru.

**Quick Actions**

- Buat Pesanan.
- Lihat Tagihan.
- Lihat Laporan.

### Hierarki Informasi

1. Kondisi usaha hari ini.
2. Masalah yang membutuhkan tindakan.
3. Pesanan aktif.
4. Informasi pendukung.

### UX Requirements

- Tidak memenuhi seluruh layar dengan grafik.
- Gunakan ringkasan sederhana.
- Pesanan terlambat harus mudah ditemukan.
- Nilai pesanan dibedakan dari pembayaran diterima.
- Card dapat membuka daftar terkait.
- Filter tanggal harus jelas.

## 11.2 Dashboard Kasir

Lebih berorientasi tindakan.

Prioritas:

1. Buat Pesanan.
2. Cari Pesanan.
3. Pesanan Siap Diambil.
4. Tagihan Belum Lunas.
5. Permintaan Pickup Masuk.

Informasi analitik tingkat Owner tidak perlu ditampilkan sepenuhnya.

---

# 12. DETAIL DESAIN PESANAN

## 12.1 Halaman Daftar Pesanan

### Komponen

- Judul halaman.
- Tombol Buat Pesanan.
- Search.
- Filter status.
- Filter tanggal.
- Filter pembayaran.
- Daftar/tabel pesanan.
- Pagination.
- Status badge.
- Aksi Detail.

### Desain Mobile

Setiap card memuat:

- Nomor pesanan.
- Nama pelanggan.
- Layanan utama.
- Status cucian.
- Status pembayaran.
- Estimasi selesai.
- Tombol Lihat Detail.

### Empty State

Teks:

"Belum ada pesanan."

Tindakan:

"Buat Pesanan Pertama."

### Error State

"Pesanan belum dapat dimuat. Coba lagi."

## 12.2 Halaman Buat Pesanan

**Halaman dengan prioritas UX tertinggi.**

### Struktur Formulir

**Bagian A — Pelanggan**

- Cari pelanggan.
- Tambah pelanggan baru.
- Nomor WhatsApp.

**Bagian B — Layanan**

- Pilih layanan.
- Berat atau jumlah.
- Harga satuan.
- Subtotal.
- Tambah layanan lainnya.

**Bagian C — Penyelesaian**

- Estimasi selesai.
- Metode pengambilan/pengantaran.
- Catatan.

**Bagian D — Ringkasan**

- Total layanan.
- Biaya tambahan.
- Biaya antar-jemput.
- Total tagihan.

**Bagian E — Aksi**

- Simpan Pesanan.
- Batal / Kembali.

### UX Requirements

1. Kasir tidak perlu membuka terlalu banyak halaman.
2. Pencarian pelanggan memiliki autocomplete.
3. Harga tampil segera setelah memilih layanan.
4. Kuantitas menerima format yang sesuai.
5. Total diperbarui ketika input berubah.
6. Informasi penting tidak disembunyikan.
7. Tombol simpan memiliki loading state.
8. Tidak boleh ada submit ganda.
9. Setelah sukses, pengguna diarahkan ke detail pesanan.
10. Jika harga server berbeda dari pratinjau, kasir diminta memeriksa ulang sebelum konfirmasi.

### Validasi

- Pelanggan wajib dipilih.
- Minimal satu layanan.
- Berat atau jumlah harus valid.
- Estimasi selesai harus masuk akal.
- Tarif harus aktif.
- Kesalahan ditampilkan pada field terkait.

## 12.3 Halaman Detail Pesanan

### Struktur

**Header**

- Nomor pesanan.
- Status utama.
- Tanggal pesanan.
- Tombol kembali.

**Identitas Pelanggan**

- Nama.
- Nomor WhatsApp.
- Aksi Hubungi.

**Rincian Layanan**

- Jenis layanan.
- Kuantitas.
- Tarif.
- Subtotal.

**Progress Cucian**

- Timeline.
- Status saat ini.
- Waktu pembaruan.
- Tombol perubahan status jika berizin.

**Pembayaran**

- Total.
- Dibayar.
- Sisa.
- Status pembayaran.

**Antar-Jemput**

- Metode penyerahan.
- Status tugas jika tersedia.

**Tindakan**

- Catat Pembayaran.
- Lihat Nota.
- Bagikan WhatsApp.
- Edit jika diizinkan.
- Batalkan jika diizinkan.

### UX Requirements

- Informasi utama muncul tanpa banyak scroll.
- Tindakan keuangan dibedakan dari operasional.
- Tindakan destruktif tidak ditempatkan berdekatan dengan aksi utama.
- Role pengguna menentukan tombol yang tampil.
- Timeline memiliki label dan urutan yang jelas.

## 12.4 Halaman Ubah Status Cucian

Gunakan kontrol yang sederhana.

Contoh:

Status saat ini: Sedang Dicuci.

Tindakan utama:

"Lanjut ke Pengeringan."

Jika terdapat beberapa transisi valid, sistem menampilkan pilihan yang relevan.

### Aturan UX

- Tidak menampilkan seluruh status secara bebas jika transisi tidak valid.
- Menampilkan konfirmasi untuk koreksi mundur.
- Menampilkan waktu pembaruan.
- Memberikan feedback setelah status disimpan.
- Menangani perubahan status oleh petugas lain.

---

# 13. DETAIL DESAIN PELANGGAN

## 13.1 Daftar Pelanggan

Komponen:

- Search berdasarkan nama atau nomor.
- Tombol Tambah Pelanggan.
- Daftar pelanggan.
- Informasi kontak.
- Jumlah pesanan bila diperlukan.
- Aksi Detail.

## 13.2 Formulir Pelanggan

Field:

- Nama.
- Nomor WhatsApp.
- Alamat opsional.
- Catatan opsional.

### UX Requirements

1. Gunakan format nomor telepon yang mudah diisi.
2. Tampilkan contoh nomor Indonesia.
3. Peringatkan kemungkinan data duplikat.
4. Tidak meminta data pribadi berlebihan.
5. Field alamat bersifat opsional untuk pelanggan yang tidak memakai antar-jemput.

## 13.3 Detail Pelanggan

Menampilkan:

- Identitas.
- Kontak.
- Alamat jika tersedia.
- Riwayat pesanan.
- Status pesanan aktif.
- Tombol Buat Pesanan Baru.

---

# 14. DETAIL DESAIN ANTAR-JEMPUT

## 14.1 Daftar Permintaan Pickup

Komponen:

- Jumlah permintaan baru.
- Filter status.
- Filter tanggal.
- Daftar permintaan.
- Informasi pelanggan.
- Lokasi singkat.
- Jadwal yang diminta.
- Tombol Detail.

### Status

- Menunggu Konfirmasi.
- Dikonfirmasi.
- Kurir Ditugaskan.
- Menuju Lokasi.
- Cucian Dijemput.
- Tiba di Laundry.
- Ditolak / Dibatalkan.

## 14.2 Detail Permintaan Pickup

Informasi:

- Nama pelanggan.
- Nomor WhatsApp.
- Alamat.
- Tanggal.
- Waktu.
- Catatan.
- Status.
- Kurir.

Aksi:

- Konfirmasi.
- Tolak.
- Jadwalkan ulang.
- Tugaskan Kurir.
- Hubungi Pelanggan.
- Buat Pesanan setelah cucian tiba.

## 14.3 Dashboard Kurir

Desain harus lebih sederhana daripada dashboard Owner.

### Komponen

**Header**

"Tugas Hari Ini"

**Ringkasan**

- Tugas Menunggu.
- Sedang Dikerjakan.
- Selesai.

**Task Card**

- Jenis tugas.
- Nama pelanggan.
- Alamat.
- Jadwal.
- Status.
- Tombol Hubungi.
- Tombol Ubah Status.

### UX Requirements

- Tombol berukuran besar.
- Informasi rute dan alamat mudah dibaca.
- Minim input manual.
- Tidak memerlukan GPS.
- Tidak menampilkan data keuangan yang tidak relevan.
- Konfirmasi serah terima harus jelas.

## 14.4 Detail Pengantaran

Menampilkan:

- Nomor pesanan.
- Nama penerima.
- Alamat.
- Kontak.
- Jadwal.
- Status pengantaran.
- Ringkasan instruksi khusus.

Tindakan:

- Mulai Pengantaran.
- Tandai Dalam Pengantaran.
- Konfirmasi Diterima.
- Tandai Gagal.
- Hubungi Pelanggan.

Jika pengantaran gagal, tampilkan field alasan dan opsi penjadwalan ulang oleh petugas yang berwenang.

---

# 15. DETAIL DESAIN KEUANGAN

## 15.1 Prinsip Desain Keuangan

Antarmuka keuangan harus mengutamakan kejelasan dan pencegahan kesalahan.

Jangan mencampurkan:

- Nilai pesanan.
- Pembayaran diterima.
- Sisa tagihan.
- Pengeluaran.
- Laba bersih.

## 15.2 Halaman Ringkasan

Komponen:

- Total pembayaran diterima.
- Total tagihan belum lunas.
- Total pengeluaran.
- Selisih kas sederhana.
- Filter tanggal.
- Riwayat transaksi.

Label "Laba Bersih" tidak digunakan pada MVP apabila komponen akuntansi belum lengkap.

## 15.3 Formulir Pembayaran Manual

Field:

- Nomor pesanan.
- Total tagihan.
- Sudah dibayar.
- Sisa tagihan.
- Metode pembayaran.
- Nominal pembayaran.
- Tanggal pembayaran.
- Catatan referensi opsional.

### Alur

1. Kasir membuka formulir.
2. Sistem menampilkan saldo terbaru.
3. Kasir memilih metode.
4. Kasir memasukkan nominal.
5. Kasir memeriksa bahwa dana sudah diterima.
6. Kasir menekan Konfirmasi Pembayaran.
7. Backend memvalidasi dan menyimpan.
8. Sistem menampilkan hasil.

### UX Requirements

- Nominal ditampilkan dalam format Rupiah.
- Sisa tagihan terlihat jelas.
- Tombol konfirmasi hanya aktif saat input valid.
- Ada pesan bahwa pembayaran harus diverifikasi manual.
- Loading state mencegah konfirmasi berulang.
- Jika pembayaran ditolak karena saldo berubah, tampilkan saldo terbaru.
- Jangan mengubah status lunas hanya berdasarkan upload bukti.

## 15.4 Halaman Riwayat Pembayaran

Informasi:

- Tanggal.
- Nominal.
- Metode.
- Petugas.
- Status verifikasi.
- Referensi.
- Riwayat koreksi jika ada.

## 15.5 Pengeluaran

Form:

- Kategori.
- Nominal.
- Tanggal.
- Keterangan.

Kategori menggunakan Bahasa Indonesia.

## 15.6 Laporan

Komponen:

- Filter periode.
- Ringkasan angka.
- Daftar transaksi.
- Ekspor CSV.
- Informasi definisi metrik.

Grafik hanya ditambahkan jika membantu pemilik memahami perubahan usaha.

---

# 16. DETAIL DESAIN NOTA DIGITAL

## 16.1 Tujuan

Memberikan bukti pesanan yang rapi dan dapat dibuka melalui HP tanpa printer.

## 16.2 Struktur Nota

**Bagian Header**

- Logo jika tersedia.
- Nama usaha.
- Kontak usaha.

**Informasi Pesanan**

- Nomor pesanan.
- Tanggal.
- Nama pelanggan.

**Rincian**

- Layanan.
- Kuantitas.
- Harga satuan.
- Subtotal.

**Pembayaran**

- Total.
- Dibayar.
- Sisa.
- Status pembayaran.

**Penyelesaian**

- Estimasi selesai.
- Status cucian.
- Informasi pengambilan.

**Footer**

- Catatan.
- Kontak.
- Tautan tracking.

## 16.3 Tindakan Nota

- Lihat.
- Simpan PDF.
- Bagikan melalui WhatsApp.
- Salin tautan.

## 16.4 Aturan

1. Nota harus mudah dibaca di HP.
2. Informasi biaya tidak boleh terpotong.
3. PDF memiliki layout yang konsisten.
4. PDF tidak membutuhkan printer.
5. Nota publik hanya dapat dibuka melalui akses tracking yang sah.
6. Pengiriman WhatsApp tetap manual.
7. Nota harus menampilkan status pembayaran yang benar saat dibuat atau dibuka.

---

# 17. DETAIL DESAIN PORTAL TRACKING PUBLIK

## 17.1 Tujuan

Memungkinkan pelanggan melihat perkembangan cucian tanpa akun.

## 17.2 Struktur Halaman

**Header**

- Nama laundry.
- Ikon atau logo.
- Informasi kontak.

**Order Summary**

- Nomor pesanan.
- Layanan.
- Berat atau jumlah.
- Estimasi selesai.

**Status Utama**

- Status cucian saat ini.
- Progress timeline.
- Waktu pembaruan terakhir.

**Antar-Jemput**

- Status penjemputan jika digunakan.
- Status pengantaran jika digunakan.

**Pembayaran**

- Total tagihan.
- Sudah dibayar.
- Sisa tagihan.
- Label status.

**Tindakan**

- Lihat Nota.
- Muat Ulang.
- Hubungi Laundry.

## 17.3 Aturan Visual Timeline

Tahapan yang sudah selesai:

- Ikon centang.
- Warna success.
- Label tetap terlihat.

Tahap aktif:

- Penekanan visual lebih kuat.
- Ikon proses.
- Label status saat ini.

Tahap belum dimulai:

- Warna netral.
- Label lebih redup tetapi tetap terbaca.

Jangan menggunakan progress percentage seolah-olah merupakan pengukuran waktu yang akurat. Jika progress ditampilkan, jelaskan sebagai tahapan pengerjaan.

## 17.4 Kondisi Tracking

**Pesanan aktif**

Tampilkan status saat ini dan estimasi selesai.

**Pesanan siap**

Tampilkan pesan "Cucian Anda sudah siap diambil" atau informasi pengantaran yang relevan.

**Pesanan selesai**

Tampilkan konfirmasi selesai dan informasi serah terima yang aman.

**Pesanan dibatalkan**

Tampilkan pesan pembatalan dan arahkan pelanggan menghubungi laundry.

**Token tidak valid**

Tampilkan:

"Tautan tracking tidak tersedia atau sudah tidak berlaku."

**Token dicabut atau kedaluwarsa**

Gunakan pesan umum yang tidak mengungkap informasi pesanan.

## 17.5 Perlindungan Privasi

Halaman tidak menampilkan:

- Nomor telepon lengkap pelanggan.
- Alamat lengkap.
- Data pelanggan lain.
- Catatan internal.
- Token autentikasi staf.
- Informasi keuangan internal.

Persyaratan teknis mengikuti TRD:

- HTTPS.
- Token acak.
- Token dapat dicabut.
- Noindex.
- No-store.
- Pembatasan data publik.
- Pengendalian akses dan rate limiting.
- Pencegahan kebocoran tautan melalui layanan pihak ketiga.

## 17.6 Penyegaran Status

MVP menyediakan:

- Pengambilan data saat halaman dibuka.
- Tombol Muat Ulang.
- Polling opsional ketika halaman aktif.
- Informasi waktu terakhir diperbarui.

Tidak memerlukan WebSocket atau GPS.

---

# 18. DETAIL DESAIN PERMINTAAN PICKUP PUBLIK

## 18.1 Tujuan

Memungkinkan pelanggan meminta penjemputan tanpa login atau menghubungi admin terlebih dahulu.

## 18.2 Struktur Formulir

Field utama:

1. Nama.
2. Nomor WhatsApp.
3. Alamat penjemputan.
4. Tanggal.
5. Rentang waktu.
6. Catatan opsional.

## 18.3 Prinsip Form

- Satu halaman sederhana.
- Tidak mewajibkan akun.
- Field tidak berlebihan.
- Validasi jelas.
- Tanggal mudah dipilih.
- Keyboard sesuai input.
- Tombol Ajukan Penjemputan terlihat jelas.
- Penjelasan bahwa jadwal perlu dikonfirmasi admin.

## 18.4 Halaman Berhasil

Setelah backend mengonfirmasi penyimpanan:

**Judul:**

"Permintaan penjemputan berhasil diajukan."

**Informasi:**

- Nomor permintaan.
- Status Menunggu Konfirmasi.
- Jadwal yang diajukan.
- Penjelasan bahwa admin akan mengonfirmasi secara manual.

**Tindakan:**

- Lihat Tracking.
- Salin Tautan.
- Hubungi Laundry.

Pelanggan perlu diberi tahu agar menyimpan tautan karena sistem tidak mengirim WhatsApp otomatis.

## 18.5 Kondisi Gagal

Jika pengajuan tidak dapat dipastikan berhasil karena koneksi terputus:

- Jangan langsung menampilkan status berhasil.
- Berikan pesan status belum terkonfirmasi.
- Gunakan mekanisme retry aman.
- Hindari duplikasi pengajuan.

---

# 19. DETAIL DESAIN PENGATURAN

## 19.1 Pengaturan Profil Usaha

Field:

- Nama laundry.
- Nomor WhatsApp.
- Alamat.
- Logo opsional.
- Zona waktu.
- Informasi usaha pada nota.

## 19.2 Pengaturan Layanan

Komponen:

- Daftar layanan.
- Tambah layanan.
- Edit harga.
- Tipe harga per kg/per satuan.
- Status aktif/nonaktif.
- Estimasi durasi.

### UX Requirements

- Perubahan harga meminta konfirmasi.
- Harga lama pada transaksi lama tidak ikut berubah.
- Perubahan tersimpan memiliki feedback.
- Tindakan hanya tersedia untuk Owner.

## 19.3 Pengaturan Pengguna

Komponen:

- Daftar akun.
- Nama.
- Role.
- Status aktif.
- Tambah pengguna.
- Ubah role.
- Nonaktifkan akun.

Penonaktifan akun harus menampilkan dialog konfirmasi.

## 19.4 Pengaturan Operasional

Dapat memuat:

- Estimasi durasi layanan.
- Biaya antar-jemput.
- Metode pembayaran yang diterima.
- Ketentuan umum usaha.

Fitur yang belum masuk MVP tidak perlu ditampilkan sebagai menu kosong.

---

# 20. COMPONENT LIBRARY

## 20.1 Navigation Components

- App Sidebar.
- Mobile Navigation.
- Page Header.
- Breadcrumb.
- Tabs.
- Back Button.
- User Menu.

## 20.2 Form Components

- Text Input.
- Number Input.
- Currency Input.
- Phone Input.
- Date Picker.
- Time Range Input.
- Select.
- Searchable Select.
- Textarea.
- Radio Group.
- Checkbox.
- Form Error.
- Form Section.
- Submit Button.

## 20.3 Data Components

- Summary Card.
- Order Card.
- Customer Card.
- Task Card.
- Data Table.
- Filter Bar.
- Search Bar.
- Pagination.
- Empty State.
- Status Badge.
- Transaction Summary.
- Detail List.

## 20.4 Feedback Components

- Loading Skeleton.
- Spinner.
- Toast.
- Inline Alert.
- Confirmation Dialog.
- Error State.
- Success State.
- Offline Warning.
- Conflict Notice.

## 20.5 Domain Components

- Laundry Status Timeline.
- Pickup Timeline.
- Delivery Timeline.
- Payment Summary.
- Invoice Preview.
- Order Price Calculator Preview.
- Courier Task Actions.
- WhatsApp Share Action.
- Tracking Link Action.
- Financial Metric Card.

## 20.6 Prinsip Penggunaan Komponen

1. Gunakan komponen yang sama untuk fungsi yang sama.
2. Semua komponen mendukung disabled state.
3. Komponen interaktif mendukung keyboard.
4. Komponen memiliki focus state.
5. Variasi ditentukan oleh kebutuhan, bukan dekorasi.
6. Status disampaikan melalui teks dan visual.
7. Tidak membuat komponen baru jika komponen yang ada sudah sesuai.
8. Komponen khusus domain harus dibangun di atas komponen dasar.

---

# 21. STATUS DESIGN SYSTEM

## 21.1 Status Cucian

| Status Sistem | Label UI                 | Visual  |
| ------------- | ------------------------ | ------- |
| RECEIVED      | Pesanan Diterima         | Netral  |
| QUEUED        | Dalam Antrean            | Netral  |
| WASHING       | Sedang Dicuci            | Info    |
| DRYING        | Dikeringkan              | Info    |
| IRONING       | Disetrika                | Info    |
| QC_PACKING    | Pemeriksaan & Pengemasan | Info    |
| READY         | Siap Diambil / Diantar   | Success |
| COMPLETED     | Selesai                  | Success |
| CANCELLED     | Dibatalkan               | Danger  |

## 21.2 Status Pembayaran

| Status         | Label          | Visual  |
| -------------- | -------------- | ------- |
| UNPAID         | Belum Bayar    | Warning |
| PARTIALLY_PAID | Bayar Sebagian | Warning |
| PAID           | Lunas          | Success |

## 21.3 Status Antar-Jemput

Gunakan label yang sesuai dengan terminologi pelanggan.

Contoh:

- Menunggu Konfirmasi.
- Dijadwalkan.
- Kurir Ditugaskan.
- Kurir Menuju Lokasi.
- Cucian Dijemput.
- Tiba di Laundry.
- Dalam Pengantaran.
- Diterima Pelanggan.
- Gagal Diantar.

Status internal yang lebih teknis boleh dipetakan ke label publik yang lebih sederhana.

## 21.4 Ketentuan

- Status pencucian dan pembayaran ditampilkan terpisah.
- Label status harus konsisten di seluruh halaman.
- Hindari mengganti warna status pada modul yang berbeda.
- Status penting memiliki teks yang dapat dibaca screen reader.
- Status gagal tidak boleh terlihat seperti berhasil.

---

# 22. MICRO-INTERACTIONS DAN ANIMASI

## 22.1 Tujuan

Animasi digunakan untuk memberikan feedback dan membantu pengguna memahami perubahan antarmuka.

Animasi tidak digunakan semata-mata sebagai dekorasi.

## 22.2 Animasi yang Direkomendasikan

**Button**

- Hover.
- Pressed.
- Loading.
- Disabled.

**Card**

- Hover ringan pada desktop.
- Feedback saat dipilih.

**Modal**

- Fade dan transisi singkat.

**Form**

- Fokus input.
- Pesan validasi.
- Konfirmasi penyimpanan.

**Status**

- Perubahan label setelah respons backend berhasil.
- Transisi progres yang halus.

**Toast**

- Muncul singkat.
- Dapat ditutup.
- Tidak menghalangi tindakan utama.

## 22.3 Animation Timing

Rekomendasi awal:

| Jenis             | Durasi                   |
| ----------------- | ------------------------ |
| Button feedback   | 100–150 ms              |
| Hover transition  | 150–200 ms              |
| Modal transition  | 180–250 ms              |
| Status transition | 150–250 ms              |
| Skeleton          | Sesuai kebutuhan loading |

## 22.4 Batasan

1. Tidak menggunakan animasi besar pada seluruh halaman.
2. Tidak menggunakan efek parallax yang mengganggu.
3. Animasi tidak boleh memperlambat input.
4. Mendukung prefers-reduced-motion.
5. Animasi keberhasilan hanya terjadi setelah konfirmasi backend.
6. Jangan menggunakan konfeti atau efek perayaan untuk setiap transaksi rutin.
7. Hindari animasi pada informasi keuangan yang bisa mengurangi kejelasan.

---

# 23. ACCESSIBILITY REQUIREMENTS

Target aksesibilitas menggunakan WCAG 2.2 Level AA sebagai acuan.

## 23.1 Visual Accessibility

1. Kontras teks normal memenuhi rasio minimal 4,5:1.
2. Teks besar memenuhi ketentuan kontras yang relevan.
3. Status tidak bergantung pada warna.
4. Focus indicator terlihat.
5. Teks dapat diperbesar tanpa kehilangan fungsi utama.
6. Informasi penting tidak menggunakan font terlalu kecil.

## 23.2 Keyboard Accessibility

1. Navigasi dapat menggunakan keyboard.
2. Focus order logis.
3. Modal mengelola fokus dengan benar.
4. Tombol dapat diaktifkan melalui keyboard.
5. Tidak ada keyboard trap.
6. Dropdown dapat dioperasikan tanpa mouse.

## 23.3 Form Accessibility

1. Semua input memiliki label.
2. Error terhubung ke field terkait.
3. Field wajib memiliki indikasi.
4. Instruksi ditampilkan sebelum pengguna gagal.
5. Perubahan status penting diumumkan secara semantik.
6. Konfirmasi pembayaran dapat dibaca dan dipahami.

## 23.4 Motion Accessibility

- Gunakan reduced motion.
- Hindari animasi berkedip.
- Hindari gerakan otomatis yang mengganggu konsentrasi.

---

# 24. UX WRITING DAN CONTENT DESIGN

## 24.1 Bahasa

Seluruh antarmuka menggunakan Bahasa Indonesia yang sederhana.

Hindari istilah teknis jika terdapat istilah sehari-hari yang lebih mudah dipahami.

## 24.2 Contoh Terminologi

| Hindari             | Gunakan                     |
| ------------------- | --------------------------- |
| Create Order        | Buat Pesanan                |
| Payment Outstanding | Sisa Tagihan                |
| Pending             | Menunggu Konfirmasi         |
| Fulfillment         | Penyerahan Cucian           |
| Dispatch            | Mulai Pengantaran           |
| Transaction Success | Pembayaran Berhasil Dicatat |
| Invalid Input       | Periksa Data yang Diisi     |
| Refresh Status      | Muat Ulang Status           |

## 24.3 Prinsip Penulisan Pesan

1. Singkat.
2. Jelas.
3. Tidak menyalahkan pengguna.
4. Memberi petunjuk tindakan.
5. Tidak mengklaim sesuatu yang belum terjadi.
6. Membedakan keberhasilan sistem dengan keberhasilan tindakan eksternal.

## 24.4 Contoh Feedback

**Berhasil Membuat Pesanan**

"Pesanan berhasil dibuat. Nota digital sudah tersedia."

**Berhasil Mencatat Pembayaran**

"Pembayaran Rp20.000 berhasil dicatat."

**Status Diperbarui**

"Status cucian berhasil diubah menjadi Sedang Dicuci."

**Token Tidak Berlaku**

"Tautan tracking tidak tersedia atau sudah tidak berlaku. Hubungi laundry untuk mendapatkan bantuan."

**WhatsApp**

"WhatsApp siap dibuka. Periksa pesan sebelum mengirim."

**Koneksi Terputus**

"Koneksi terputus. Status penyimpanan belum dapat dipastikan. Periksa kembali sebelum mengulang."

---

# 25. ERROR PREVENTION DAN CRITICAL UX

## 25.1 Pembuatan Pesanan

Risiko:

- Salah pelanggan.
- Salah berat.
- Salah layanan.
- Salah estimasi selesai.
- Harga tidak sesuai.

Mitigasi:

- Ringkasan sebelum penyimpanan.
- Perhitungan otomatis.
- Validasi.
- Peringatan perubahan tarif.
- Konfirmasi bila diperlukan.

## 25.2 Pembayaran

Risiko:

- Salah nominal.
- Pencatatan ganda.
- Transfer belum diterima.
- Pembayaran melebihi tagihan.

Mitigasi:

- Tampilkan sisa tagihan.
- Konfirmasi manual.
- Disable submit ketika memproses.
- Idempotency.
- Tampilkan hasil server.
- Peringatan konflik pembayaran.

## 25.3 Perubahan Status

Risiko:

- Salah status.
- Petugas mengubah data yang sudah berubah.
- Pesanan selesai tanpa serah terima.

Mitigasi:

- Hanya tampilkan transisi valid.
- Version check.
- Konfirmasi untuk koreksi.
- Konfirmasi serah terima.
- Audit perubahan.

## 25.4 Tracking

Risiko:

- Tautan bocor.
- Pelanggan melihat informasi orang lain.
- Pelanggan salah memahami status.

Mitigasi:

- Token aman.
- Informasi dibatasi.
- Label mudah dipahami.
- Waktu pembaruan terakhir.
- Kontak admin.
- Tidak menampilkan data pribadi lengkap.

---

# 26. PRIVACY DAN TRUST DESIGN

## 26.1 Prinsip

Antarmuka harus membangun kepercayaan tanpa mengorbankan privasi.

## 26.2 Praktik yang Wajib

1. Tidak meminta login pelanggan.
2. Tidak meminta data pribadi yang tidak diperlukan.
3. Tidak menampilkan informasi pelanggan lain.
4. Tidak menggunakan dark patterns.
5. Tidak menyembunyikan sisa tagihan.
6. Tidak mengklaim pembayaran otomatis.
7. Tidak mengklaim pengantaran memiliki GPS real-time.
8. Tidak mengklaim WhatsApp terkirim otomatis.
9. Tidak menggunakan ikon keamanan sebagai klaim tanpa dasar.
10. Memberikan akses ke informasi bantuan dan kebijakan privasi.

## 26.3 Data Publik

Portal pelanggan hanya memuat data yang diperlukan untuk tracking.

Informasi sensitif harus dibatasi di backend dan tidak cukup hanya disembunyikan menggunakan CSS.

---

# 27. DESIGN STATES DAN EDGE CASES

## 27.1 State yang Wajib Dirancang

Untuk setiap halaman utama, minimal tersedia:

1. Default.
2. Loading.
3. Empty.
4. Success.
5. Validation Error.
6. Server Error.
7. Unauthorized.
8. Offline / Network Error.
9. Conflict jika relevan.

## 27.2 Edge Case Pesanan

- Pelanggan belum terdaftar.
- Pelanggan sudah ada.
- Layanan belum tersedia.
- Berat nol.
- Harga berubah.
- Pesanan dibatalkan.
- Pesanan sudah selesai.
- Pembayaran sudah sebagian.
- Data berubah oleh petugas lain.

## 27.3 Edge Case Pickup

- Permintaan belum dikonfirmasi.
- Kurir belum tersedia.
- Jadwal berubah.
- Pickup gagal.
- Cucian sudah tiba.
- Permintaan sudah dikonversi menjadi pesanan.
- Request publik dikirim berulang.

## 27.4 Edge Case Pembayaran

- Nominal nol.
- Nominal negatif.
- Nominal melebihi sisa.
- Transaksi duplikat.
- Payment void.
- Koneksi terputus setelah submit.
- Pesanan berubah ketika pembayaran dilakukan.

## 27.5 Edge Case Tracking

- Token salah.
- Token kedaluwarsa.
- Token dicabut.
- Order dibatalkan.
- Status belum diperbarui.
- Pesanan belum memiliki pengantaran.
- Order selesai tetapi pembayaran belum lunas.
- Koneksi pelanggan lambat.

---

# 28. INTERACTIVE PROTOTYPE REQUIREMENTS

## 28.1 Tingkat Prototype

Desain dibuat dalam tiga tingkat.

**Low-Fidelity Wireframe**

Menentukan struktur informasi dan navigasi.

**High-Fidelity Design**

Menentukan warna, tipografi, ikon, spacing, dan komponen.

**Interactive Prototype**

Mensimulasikan perpindahan halaman dan interaksi utama.

## 28.2 Flow yang Wajib Diprototipekan

1. Login sampai dashboard.
2. Buat pesanan.
3. Pilih pelanggan lama.
4. Tambah pelanggan.
5. Tambah beberapa layanan.
6. Simpan pesanan.
7. Buka nota.
8. Buka WhatsApp manual.
9. Catat DP.
10. Catat pelunasan.
11. Ubah status cucian.
12. Ajukan pickup publik.
13. Konfirmasi pickup.
14. Tugaskan kurir.
15. Pickup menjadi pesanan.
16. Jadwalkan pengantaran.
17. Konfirmasi serah terima.
18. Buka tracking tanpa login.
19. Tangani token tidak valid.
20. Tangani error koneksi.

## 28.3 Prototipe Mobile dan Desktop

Minimal mencakup:

- Mobile 390 px.
- Mobile kecil 320 px untuk pemeriksaan kelayakan.
- Desktop 1440 px.

Ukuran lain diuji saat implementasi responsif.

## 28.4 Batasan Prototype

Prototype tidak dianggap sebagai sistem berfungsi.

Data dan interaksi prototype merupakan simulasi.

Keberhasilan prototype tidak menggantikan integration test, security test, atau acceptance test aplikasi sebenarnya.

---

# 29. USER TESTING PLAN

## 29.1 Tujuan

Mengukur apakah pengguna dapat memahami dan menyelesaikan tugas tanpa instruksi teknis yang panjang.

## 29.2 Peserta Uji

Rekomendasi awal:

- 2–3 pemilik atau pengelola laundry.
- 2–3 kasir atau staf.
- 2–3 calon pelanggan.

Jumlah peserta dapat disesuaikan dengan akses dan skala riset.

## 29.3 Skenario Uji

**Skenario 1 — Pesanan**

Peserta diminta mencatat cucian 3 kg menggunakan layanan cuci setrika.

**Skenario 2 — Pembayaran**

Peserta mencatat pembayaran sebagian dan menemukan sisa tagihan.

**Skenario 3 — Status Cucian**

Peserta mengubah status pesanan menjadi Sedang Dicuci.

**Skenario 4 — Pickup**

Pelanggan mengajukan penjemputan tanpa login.

**Skenario 5 — Tracking**

Pelanggan membuka tautan dan menjelaskan status cucian yang terlihat.

**Skenario 6 — Kurir**

Kurir menerima tugas dan mengonfirmasi serah terima.

## 29.4 Metrik

- Task success rate.
- Task completion time.
- Error count.
- Jumlah permintaan bantuan.
- Tingkat kesulitan yang dirasakan.
- Masalah navigasi.
- Masalah keterbacaan.
- Masalah aksesibilitas.

## 29.5 Target Awal

- Minimal 90% penyelesaian tugas inti pada pengujian desain.
- Pembuatan pesanan standar ditargetkan maksimal 2 menit.
- Tidak ada kesalahan kritis akibat antarmuka pada alur pembayaran.
- Pelanggan memahami status tracking tanpa penjelasan tambahan yang panjang.

Jika hasil tidak memenuhi target, desain diperbaiki dan diuji kembali.

---

# 30. DESIGN HANDOFF KE FRONTEND

## 30.1 Deliverables

Tim desain harus menghasilkan:

1. Design Brief Documentation.
2. Information Architecture.
3. Sitemap.
4. User Flow.
5. Low-Fidelity Wireframes.
6. High-Fidelity Screens.
7. Interactive Prototype.
8. Design Tokens.
9. Component Library.
10. Responsive Specifications.
11. State Specifications.
12. Accessibility Notes.
13. UI Copy.
14. Developer Handoff Notes.

## 30.2 Isi Handoff Setiap Halaman

Setiap halaman memiliki:

- Screen ID.
- Nama halaman.
- Pengguna.
- Tujuan.
- Route.
- Komponen.
- Data yang ditampilkan.
- Action.
- Permission.
- Loading state.
- Empty state.
- Error state.
- Responsive behavior.
- Acceptance criteria.

## 30.3 Koneksi ke Backend

Desain harus sesuai kontrak API.

Contoh:

**Halaman Detail Pesanan**

Menggunakan data dari `GET /api/v1/orders/{id}`.

**Pencatatan Pembayaran**

Menggunakan `POST /api/v1/orders/{id}/payments`.

**Tracking Publik**

Menggunakan `GET /api/v1/public/track/{token}`.

**Permintaan Pickup Publik**

Menggunakan `POST /api/v1/public/pickup-requests`.

Detail payload final mengikuti kontrak OpenAPI.

## 30.4 Desain Tidak Boleh Mengasumsikan

- WhatsApp otomatis.
- Pembayaran otomatis.
- GPS real-time.
- Pelanggan memiliki akun.
- Semua pegawai memiliki permission yang sama.
- Nilai harga dari frontend selalu benar.
- Penyimpanan berhasil sebelum server mengonfirmasi.

---

# 31. DESIGN QUALITY ASSURANCE

## 31.1 Visual QA

Pemeriksaan:

- Konsistensi tipografi.
- Konsistensi warna.
- Konsistensi spacing.
- Konsistensi border radius.
- Konsistensi ikon.
- Responsivitas.
- Hierarki visual.
- Tampilan angka.
- Penanganan teks panjang.
- Alignment.

## 31.2 Functional UI QA

Pemeriksaan:

- Tombol bekerja.
- Form validasi.
- Loading muncul.
- Error ditampilkan.
- Navigasi benar.
- Permission tercermin.
- Dialog konfirmasi bekerja.
- Status diperbarui.
- Nominal uang benar.
- Tidak ada submit ganda.

## 31.3 Responsive QA

Wajib memeriksa:

- Tidak ada horizontal overflow yang tidak diperlukan.
- Tombol dapat ditekan.
- Input tidak terpotong.
- Modal dapat dioperasikan.
- Tabel mobile dapat digunakan.
- Header tidak menutupi konten.
- Navigasi tidak menghalangi aksi.
- PDF/nota dapat dibuka dari HP.

## 31.4 Accessibility QA

Memeriksa:

- Kontras.
- Keyboard navigation.
- Focus.
- Label.
- Error announcement.
- Screen reader behavior.
- Reduced motion.
- Pembesaran teks.

---

# 32. DESIGN ACCEPTANCE MATRIX

| ID        | Kriteria                                               | Prioritas |
| --------- | ------------------------------------------------------ | --------- |
| DBD-AT-01 | Halaman login mudah digunakan                          | P0        |
| DBD-AT-02 | Dashboard sesuai peran                                 | P0        |
| DBD-AT-03 | Tombol Buat Pesanan mudah ditemukan                    | P0        |
| DBD-AT-04 | Pesanan dapat dibuat melalui HP                        | P0        |
| DBD-AT-05 | Form memiliki validasi yang jelas                      | P0        |
| DBD-AT-06 | Total biaya mudah dipahami                             | P0        |
| DBD-AT-07 | Status cucian ditampilkan konsisten                    | P0        |
| DBD-AT-08 | Status pembayaran dipisahkan                           | P0        |
| DBD-AT-09 | Pembayaran manual memiliki konfirmasi                  | P0        |
| DBD-AT-10 | WhatsApp tidak diklaim terkirim otomatis               | P0        |
| DBD-AT-11 | Nota dapat dibuka di HP                                | P0        |
| DBD-AT-12 | Tracking dapat dibuka tanpa login                      | P0        |
| DBD-AT-13 | Data sensitif tidak muncul di portal publik            | P0        |
| DBD-AT-14 | Form pickup mudah diisi                                | P0        |
| DBD-AT-15 | Jadwal pickup dibedakan dari konfirmasi                | P0        |
| DBD-AT-16 | Kurir dapat mengubah tugas dari HP                     | P0        |
| DBD-AT-17 | Pengantaran gagal memiliki penanganan                  | P0        |
| DBD-AT-18 | Halaman keuangan membedakan jenis metrik               | P0        |
| DBD-AT-19 | Konfirmasi tindakan destruktif tersedia                | P0        |
| DBD-AT-20 | Loading, empty, dan error state tersedia               | P0        |
| DBD-AT-21 | Permission diikuti dalam navigasi                      | P0        |
| DBD-AT-22 | Tidak ada overflow horizontal pada alur utama          | P0        |
| DBD-AT-23 | Keyboard navigation dapat digunakan                    | P0        |
| DBD-AT-24 | Design tokens digunakan konsisten                      | P0        |
| DBD-AT-25 | Prototype alur utama dapat diuji                       | P0        |
| DBD-AT-26 | Handoff sesuai API dan AFD                             | P0        |
| DBD-AT-27 | Komponen memiliki reduced-motion behavior              | P0        |
| DBD-AT-28 | Desain lulus review keterbacaan                        | P0        |
| DBD-AT-29 | Tidak ada klaim status sukses sebelum server merespons | P0        |
| DBD-AT-30 | User testing dilakukan dan temuan kritis diperbaiki    | P0        |

---

# 33. DESIGN IMPLEMENTATION ROADMAP

## D0 — Design Discovery

Deliverables:

- Review PRD.
- Review TRD.
- Review AFD.
- Daftar pengguna dan tugas utama.
- Design principles.
- Prioritas halaman.

## D1 — Information Architecture

Deliverables:

- Sitemap.
- Navigasi.
- Route map.
- Role-based menu.
- Hierarki konten.

## D2 — Low-Fidelity Wireframe

Deliverables:

- Login.
- Dashboard.
- Pesanan.
- Pembayaran.
- Tracking.
- Pickup.
- Kurir.
- Nota.
- Keuangan.
- Pengaturan.

## D3 — Design System

Deliverables:

- Colors.
- Typography.
- Spacing.
- Radius.
- Shadows.
- Icons.
- Base components.
- Status components.
- Feedback states.

## D4 — High-Fidelity Design

Deliverables:

- Seluruh layar P0.
- Desain mobile.
- Desain desktop.
- Responsive behavior.
- Empty, loading, dan error state.

## D5 — Interactive Prototype

Deliverables:

- Prototipe pembuatan pesanan.
- Prototipe pembayaran.
- Prototipe tracking.
- Prototipe pickup.
- Prototipe delivery.
- Prototipe koreksi dan error.

## D6 — Usability Testing

Deliverables:

- Test script.
- Catatan pengamatan.
- Daftar masalah.
- Prioritas perbaikan.
- Revisi desain.

## D7 — Developer Handoff

Deliverables:

- Design tokens.
- Component specifications.
- Screen specifications.
- Interaction notes.
- API mapping.
- Acceptance matrix.

## D8 — Design QA

Deliverables:

- Visual comparison.
- Responsive audit.
- Accessibility audit.
- Functional UI audit.
- Final design review.

Milestone desain dapat berjalan selaras dengan milestone M0–M8 implementasi teknis setelah spesifikasi disetujui.

---

# 34. DESIGN RISKS DAN MITIGASI

| Risiko                                  | Dampak                                    | Mitigasi                                            |
| --------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Terlalu banyak fitur di dashboard       | Pengguna bingung                          | Prioritaskan ringkasan dan tindakan utama.          |
| Form pesanan terlalu panjang            | Transaksi lambat                          | Progressive disclosure dan alur ringkas.            |
| Status tidak konsisten                  | Salah memahami progres                    | Design tokens dan status mapping terpusat.          |
| Pembayaran mudah salah input            | Selisih keuangan                          | Konfirmasi, validasi, dan ringkasan saldo.          |
| Tabel sulit digunakan di HP             | Operasional terganggu                     | Mobile card layout.                                 |
| Kurir kesulitan mengoperasikan HP       | Status terlambat diperbarui               | Tombol besar dan langkah minimal.                   |
| Tracking terlalu rumit                  | Pelanggan menghubungi admin terus-menerus | Timeline sederhana dan estimasi jelas.              |
| Data pribadi tampil di publik           | Risiko privasi                            | Public data minimization.                           |
| Animasi berlebihan                      | Performa dan usability menurun            | Animasi fungsional dan reduced motion.              |
| Desain berbeda dari implementasi        | Inkonistensi produk                       | Handoff, component reuse, dan visual QA.            |
| Terlalu banyak menu untuk usaha kecil   | Biaya belajar tinggi                      | Role-based navigation dan pengaturan fitur relevan. |
| Desain mengasumsikan integrasi otomatis | Ekspektasi salah                          | Label dan copy yang menjelaskan proses manual.      |

---

# 35. KEPUTUSAN DESAIN YANG MASIH TERBUKA

| ID         | Keputusan                    | Rekomendasi                             |
| ---------- | ---------------------------- | --------------------------------------- |
| DES-DEC-01 | Nama dan logo produk         | Belum ditentukan.                       |
| DES-DEC-02 | Warna utama                  | Deep Teal #0F766E.                      |
| DES-DEC-03 | Font                         | Inter + system fallback.                |
| DES-DEC-04 | Light/Dark Mode              | Light Mode pada MVP.                    |
| DES-DEC-05 | Navigasi Mobile              | Bottom navigation adaptif.              |
| DES-DEC-06 | Navigasi Desktop             | Sidebar.                                |
| DES-DEC-07 | Tipe tampilan daftar pesanan | Tabel desktop, card mobile.             |
| DES-DEC-08 | Flow pembuatan pesanan       | Form terstruktur dalam satu alur utama. |
| DES-DEC-09 | Model tracking publik        | Satu halaman ringkasan dan timeline.    |
| DES-DEC-10 | Model pickup publik          | Formulir singkat tanpa login.           |
| DES-DEC-11 | Model nota                   | Halaman web + PDF.                      |
| DES-DEC-12 | Bahasa antarmuka             | Bahasa Indonesia.                       |
| DES-DEC-13 | Gaya ikon                    | Lucide React.                           |
| DES-DEC-14 | Animasi                      | Ringan dan fungsional.                  |
| DES-DEC-15 | User testing                 | Wajib untuk alur P0.                    |
| DES-DEC-16 | Offline Mode                 | Tidak termasuk MVP.                     |

Seluruh rekomendasi desain perlu divalidasi melalui review sebelum ditetapkan sebagai baseline final.

---

# 36. TRACEABILITY PRD, TRD, AFD, DAN DBD

| Kebutuhan         | PRD      | TRD               | AFD       | DBD        |
| ----------------- | -------- | ----------------- | --------- | ---------- |
| Pembuatan pesanan | ORD      | Orders API        | FLOW-ORD  | SCR-05     |
| Detail pesanan    | ORD      | Orders API        | FLOW-ORD  | SCR-06     |
| Status cucian     | ORD      | State Machine     | FLOW-WRK  | SCR-07     |
| Pelanggan         | CUS      | Customers API     | FLOW-CUS  | SCR-08–10 |
| Pembayaran manual | FIN      | Payments API      | FLOW-PAY  | SCR-15–16 |
| Pengeluaran       | FIN      | Expenses API      | FLOW-FIN  | SCR-18     |
| Laporan           | FIN      | Reporting API     | FLOW-FIN  | SCR-19     |
| Pickup            | PUD      | Pickup API        | FLOW-PUP  | SCR-11–12 |
| Kurir             | PUD      | Delivery API      | FLOW-DLV  | SCR-13–14 |
| Nota              | INV      | Invoice API       | FLOW-INV  | SCR-20     |
| Tracking          | TRK      | Public API        | FLOW-TRK  | SCR-24     |
| Pickup Publik     | PUD      | Public Pickup API | FLOW-PUP  | SCR-25–26 |
| Pengaturan        | SET      | Settings API      | FLOW-SET  | SCR-21–23 |
| Authentication    | Security | Auth API          | FLOW-AUTH | SCR-01     |

Matriks ini digunakan untuk memastikan setiap kebutuhan memiliki rancangan antarmuka dan implementasi yang sesuai.

---

# 37. DEFINITION OF DONE — DESIGN

Sebuah desain dinyatakan selesai apabila:

1. Kebutuhannya sesuai PRD.
2. Alurnya sesuai AFD.
3. Batasan teknisnya sesuai TRD.
4. Hierarki konten jelas.
5. Komponen menggunakan design system.
6. Mobile layout tersedia.
7. Desktop layout tersedia.
8. Responsive behavior didefinisikan.
9. Loading state tersedia.
10. Empty state tersedia.
11. Error state tersedia.
12. Permission dipertimbangkan.
13. Form memiliki validasi.
14. Tindakan penting memiliki feedback.
15. Tindakan berisiko memiliki konfirmasi.
16. Privacy requirements terpenuhi.
17. Aksesibilitas diperiksa.
18. Prototype alur utama dapat digunakan.
19. Desain telah melalui usability review.
20. Developer handoff lengkap.

## 37.1 Status Desain

Status yang digunakan:

- NOT_STARTED.
- WIREFRAME.
- DESIGN_IN_PROGRESS.
- READY_FOR_REVIEW.
- REVISION_REQUIRED.
- APPROVED.
- IMPLEMENTED.
- VERIFIED.

Desain APPROVED tidak berarti sudah diimplementasikan.

Desain IMPLEMENTED tidak berarti sudah lulus visual QA dan usability test.

## 37.2 Design Approval Gate

DBD dapat disetujui apabila:

- Seluruh keputusan desain penting telah ditetapkan.
- Seluruh layar P0 memiliki spesifikasi.
- Prototipe alur utama selesai.
- Tidak ada konflik kritis terhadap PRD, TRD, dan AFD.
- Target aksesibilitas dan responsivitas diterapkan.
- Review Owner atau stakeholder produk telah dilakukan.

---

# 38. KESIMPULAN

Design Brief Documentation v1.0 menetapkan rancangan pengalaman pengguna dan arah visual untuk Web App Manajemen Laundry UMKM.

Desain menggunakan pendekatan **Clean, Fresh & Trustworthy**, dengan fokus pada tampilan modern, sederhana, mudah digunakan, dan sesuai dengan kebutuhan operasional laundry skala kecil.

Rancangan memprioritaskan:

1. Antarmuka mobile-first.
2. Pembuatan pesanan yang cepat.
3. Navigasi sederhana.
4. Perhitungan pembayaran yang jelas.
5. Nota digital tanpa printer.
6. Tracking pelanggan tanpa login.
7. Antar-jemput dengan status manual.
8. Hak akses berdasarkan peran.
9. Status dan feedback yang konsisten.
10. Aksesibilitas dan keamanan informasi.

Seluruh halaman harus menggunakan design system yang terpusat, komponen yang konsisten, serta interaksi yang mudah dipahami oleh pengguna nonteknis.

Dokumen ini menjadi dasar pembuatan wireframe, prototype interaktif, high-fidelity UI, design system, dan implementasi frontend.

**Status Akhir: DBD v1.0 — DRAFT FOR DESIGN REVIEW.**

Dokumen belum berarti bahwa desain Figma, prototype, atau implementasi frontend telah dibuat atau disetujui.

---

**AKHIR DOKUMEN — DESIGN BRIEF DOCUMENTATION v1.0**
