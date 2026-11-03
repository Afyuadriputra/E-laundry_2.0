
# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## WEB APP MANAJEMEN LAUNDRY UMKM

**Versi:** 1.0
**Tanggal:** 3 November 2026
**Status:** Draft untuk Review dan Persetujuan
**Jenis Produk:** Web Application — Mobile First
**Target Pengguna:** Usaha Laundry Mikro, Kecil, dan Menengah
**Tahap Produk:** Perencanaan dan Perancangan MVP

---

# 1. PENDAHULUAN

## 1.1 Latar Belakang

Usaha laundry berskala mikro, kecil, dan menengah umumnya menjalankan kegiatan operasional dengan pencatatan manual melalui buku, pesan WhatsApp, atau spreadsheet sederhana.

Pendekatan tersebut relatif mudah diterapkan, tetapi dapat menimbulkan beberapa permasalahan, antara lain:

1. Kesulitan menemukan informasi pesanan pelanggan.
2. Risiko kehilangan atau kesalahan pencatatan transaksi.
3. Tidak tersedianya informasi perkembangan cucian secara terpusat.
4. Pelanggan harus menghubungi admin untuk menanyakan status cucian.
5. Pencatatan pembayaran, uang muka, dan sisa tagihan kurang terorganisasi.
6. Penjadwalan penjemputan dan pengantaran sulit dipantau.
7. Pemilik usaha kesulitan mendapatkan laporan pendapatan dan pengeluaran.
8. Riwayat transaksi pelanggan tidak terdokumentasi secara konsisten.
9. Pemilik sulit memantau pekerjaan karyawan dan cucian yang terlambat.

Di sisi lain, sebagian usaha laundry belum memerlukan sistem kasir fisik, printer nota, scanner barcode, atau integrasi pembayaran otomatis yang menambah biaya operasional.

Oleh karena itu, diperlukan sebuah aplikasi manajemen laundry berbasis web yang sederhana, terjangkau, dan dapat dioperasikan menggunakan perangkat yang sudah dimiliki pelaku UMKM.

## 1.2 Deskripsi Produk

Web App Manajemen Laundry UMKM adalah aplikasi berbasis web yang digunakan untuk mengelola seluruh proses operasional laundry, mulai dari penerimaan pesanan, pengelolaan pelanggan, pencucian, pembayaran, hingga penjemputan dan pengantaran.

Aplikasi terdiri atas dua lingkungan utama:

**A. Dashboard Internal**

Digunakan oleh pemilik usaha, kasir, staf laundry, dan kurir untuk mengelola operasional sesuai hak akses.

**B. Portal Pelanggan Tanpa Login**

Digunakan pelanggan untuk memantau perkembangan cucian, memeriksa nota, melihat status antar-jemput, dan mengajukan permintaan penjemputan.

Seluruh transaksi pembayaran diverifikasi secara manual. WhatsApp digunakan melalui mekanisme tautan pesan siap kirim tanpa integrasi API berbayar.

## 1.3 Visi Produk

Menjadi solusi digitalisasi laundry UMKM yang mudah digunakan, hemat biaya, aman, dan mampu mengintegrasikan pengelolaan pesanan, pelanggan, keuangan, serta layanan antar-jemput melalui satu aplikasi.

## 1.4 Tujuan Produk

| ID     | Tujuan                               | Indikator Keberhasilan                                         |
| ------ | ------------------------------------ | -------------------------------------------------------------- |
| OBJ-01 | Mendigitalisasi pencatatan laundry   | Seluruh pesanan operasional dapat dicatat dalam sistem.        |
| OBJ-02 | Mempercepat penerimaan pesanan       | Pembuatan pesanan standar ditargetkan selesai dalam 2 menit.   |
| OBJ-03 | Memudahkan pelanggan memantau cucian | Status pesanan dapat diakses melalui tautan tanpa login.       |
| OBJ-04 | Meningkatkan keteraturan pembayaran  | Pembayaran dan sisa tagihan tercatat dengan jelas.             |
| OBJ-05 | Mendukung antar-jemput               | Admin dapat mengelola permintaan dan perkembangan tugas kurir. |
| OBJ-06 | Mengurangi biaya perangkat           | Seluruh fitur inti dapat dijalankan melalui HP atau laptop.    |
| OBJ-07 | Menyediakan informasi usaha          | Pemilik dapat melihat ringkasan operasional dan keuangan.      |
| OBJ-08 | Menjamin keamanan informasi          | Akses internal dibatasi berdasarkan peran pengguna.            |

Indikator tersebut merupakan target produk yang harus divalidasi melalui pengujian.

---

# 2. RUANG LINGKUP PRODUK

## 2.1 Target Implementasi MVP

MVP dirancang untuk satu usaha laundry dengan satu lokasi operasional utama.

Sistem mendukung:

1. Owner sebagai pengelola usaha.
2. Kasir atau admin untuk penerimaan pesanan.
3. Staf untuk proses cucian.
4. Kurir untuk antar-jemput.
5. Pelanggan tanpa login.

Pada usaha kecil yang belum memiliki banyak karyawan, satu orang dapat menjalankan beberapa tanggung jawab melalui akun Owner tanpa diwajibkan membuat akun pegawai tambahan.

## 2.2 Fitur Termasuk dalam MVP

| No. | Modul           | Cakupan                                                         |
| --- | --------------- | --------------------------------------------------------------- |
| 1   | Dashboard       | Ringkasan pesanan, pekerjaan, omzet, dan pembayaran.            |
| 2   | Pesanan Laundry | Pencatatan pesanan, tarif, status cucian, dan riwayat.          |
| 3   | Pelanggan       | Data pelanggan dan histori transaksi.                           |
| 4   | Antar-Jemput    | Permintaan, penjadwalan, penugasan, dan tracking status.        |
| 5   | Keuangan        | Pembayaran manual, DP, piutang, pengeluaran, dan laporan dasar. |
| 6   | Nota Digital    | Halaman nota, PDF, dan berbagi melalui WhatsApp.                |
| 7   | Tracking Publik | Tracking cucian dan antar-jemput tanpa login.                   |
| 8   | Pengaturan      | Profil usaha, harga, akun petugas, dan konfigurasi operasional. |

Fitur autentikasi, pengaturan peran, audit transaksi, dan backup menjadi kemampuan pendukung yang wajib tersedia.

## 2.3 Fitur di Luar MVP

Fitur berikut belum termasuk pengembangan awal:

1. Integrasi payment gateway.
2. Verifikasi transfer otomatis.
3. Integrasi mesin cuci dan timbangan digital.
4. Kewajiban penggunaan printer nota.
5. GPS tracking kurir secara real-time.
6. WhatsApp bot atau API pengiriman otomatis.
7. Sistem membership dan poin loyalitas.
8. Sistem stok bahan laundry yang kompleks.
9. Integrasi akuntansi eksternal.
10. Multi-cabang.
11. Multi-tenant SaaS.
12. Model AI untuk prediksi antrean atau estimasi cucian.
13. Aplikasi Android dan iOS native.
14. Mode operasional offline dengan sinkronisasi otomatis.

Fitur tersebut dapat dikembangkan pada fase berikutnya berdasarkan kebutuhan dan hasil penggunaan MVP.

---

# 3. PRINSIP PENGEMBANGAN PRODUK

## 3.1 Mobile-First

Aplikasi harus dirancang untuk penggunaan smartphone terlebih dahulu.

Antarmuka wajib:

- Nyaman digunakan dengan satu tangan.
- Memiliki tombol yang mudah ditekan.
- Menggunakan navigasi sederhana.
- Menampilkan informasi penting secara ringkas.
- Menghindari formulir yang terlalu panjang.
- Responsif pada tablet dan laptop.

## 3.2 Tanpa Perangkat Eksternal Wajib

Aplikasi tidak boleh mewajibkan pembelian:

- Mesin kasir.
- Printer thermal.
- Scanner barcode.
- Timbangan digital terintegrasi.
- Perangkat GPS khusus.
- Komputer server lokal.

Berat cucian dimasukkan secara manual berdasarkan hasil penimbangan yang dilakukan usaha dengan peralatan operasional yang sudah dimiliki.

## 3.3 Pembayaran Manual

Aplikasi tidak menangani perpindahan dana.

Sistem hanya mencatat informasi pembayaran yang telah diterima dan diverifikasi oleh petugas.

## 3.4 Pelanggan Tanpa Login

Pelanggan tidak diwajibkan:

- Membuat akun.
- Mengingat password.
- Melakukan OTP.
- Mengunduh aplikasi.

Akses tracking diberikan melalui tautan unik yang aman.

## 3.5 WhatsApp Manual

Aplikasi dapat menyiapkan teks pesan dan membuka WhatsApp, tetapi tindakan pengiriman dilakukan oleh petugas.

Sistem tidak boleh menganggap pesan berhasil terkirim hanya karena tautan WhatsApp dibuka.

## 3.6 Kesederhanaan Operasional

Setiap fitur harus memberikan manfaat nyata bagi kegiatan laundry sehari-hari.

Fitur yang menambah kompleksitas tanpa kebutuhan operasional yang jelas akan ditunda.

---

# 4. PENGGUNA DAN HAK AKSES

## 4.1 Jenis Pengguna

### A. Owner

Pemilik usaha yang bertanggung jawab terhadap operasional, keuangan, harga, karyawan, dan pengaturan sistem.

### B. Admin / Kasir

Petugas yang melayani pelanggan, membuat pesanan, mencatat pembayaran, serta mengelola nota digital.

### C. Staf Laundry

Petugas yang bertanggung jawab terhadap proses pencucian, pengeringan, penyetrikaan, pemeriksaan, dan pengemasan.

### D. Kurir

Petugas yang menangani penjemputan atau pengantaran cucian.

### E. Pelanggan

Pengguna eksternal yang mengakses halaman tracking dan permintaan penjemputan tanpa login.

## 4.2 Matriks Hak Akses

Keterangan:

- Penuh: dapat melihat dan mengelola.
- Terbatas: hanya tindakan yang berkaitan dengan tugas.
- Lihat: hanya membaca.
- Tidak: tidak memiliki akses.

| Fitur                     | Owner | Kasir    | Staf     | Kurir    | Pelanggan         |
| ------------------------- | ----- | -------- | -------- | -------- | ----------------- |
| Dashboard usaha           | Penuh | Terbatas | Tidak    | Tidak    | Tidak             |
| Membuat pesanan           | Penuh | Penuh    | Tidak    | Tidak    | Tidak             |
| Mengubah data pesanan     | Penuh | Terbatas | Tidak    | Tidak    | Tidak             |
| Melihat daftar pesanan    | Penuh | Penuh    | Terbatas | Terbatas | Tidak             |
| Mengubah status cucian    | Penuh | Penuh    | Penuh    | Tidak    | Tidak             |
| Mengatur harga            | Penuh | Tidak    | Tidak    | Tidak    | Tidak             |
| Mengelola pelanggan       | Penuh | Penuh    | Tidak    | Tidak    | Tidak             |
| Mencatat pembayaran       | Penuh | Penuh    | Tidak    | Tidak    | Tidak             |
| Melihat laporan keuangan  | Penuh | Terbatas | Tidak    | Tidak    | Tidak             |
| Mencatat pengeluaran      | Penuh | Terbatas | Tidak    | Tidak    | Tidak             |
| Menjadwalkan antar-jemput | Penuh | Penuh    | Tidak    | Terbatas | Tidak             |
| Memperbarui tugas kurir   | Penuh | Penuh    | Tidak    | Penuh    | Tidak             |
| Mengelola akun pegawai    | Penuh | Tidak    | Tidak    | Tidak    | Tidak             |
| Melihat tracking sendiri  | Ya    | Ya       | Ya       | Ya       | Ya, dengan tautan |
| Mengajukan penjemputan    | Ya    | Ya       | Ya       | Ya       | Ya, tanpa login   |

Setiap permintaan API harus memverifikasi izin pada backend, bukan hanya menyembunyikan tombol pada frontend.

---

# 5. KEBUTUHAN FUNGSIONAL

Prioritas menggunakan klasifikasi:

- **P0:** Wajib tersedia pada MVP.
- **P1:** Penting untuk penyempurnaan berikutnya.
- **P2:** Pengembangan lanjutan.

## 5.1 Modul Dashboard

**Tujuan:** Memberikan gambaran kondisi usaha secara cepat kepada pemilik dan kasir.

| ID      | Fitur                             | Prioritas |
| ------- | --------------------------------- | --------- |
| DASH-01 | Ringkasan jumlah pesanan hari ini | P0        |
| DASH-02 | Ringkasan total nilai pesanan     | P0        |
| DASH-03 | Ringkasan pembayaran diterima     | P0        |
| DASH-04 | Jumlah pesanan sedang diproses    | P0        |
| DASH-05 | Jumlah pesanan siap diambil       | P0        |
| DASH-06 | Jumlah pesanan terlambat          | P0        |
| DASH-07 | Jumlah tagihan belum lunas        | P0        |
| DASH-08 | Daftar pesanan terbaru            | P0        |
| DASH-09 | Grafik tren pendapatan            | P1        |
| DASH-10 | Perbandingan kinerja bulanan      | P1        |

### Persyaratan

1. Dashboard menampilkan data sesuai tanggal dan hak akses.
2. Nilai pesanan dan jumlah pembayaran diterima ditampilkan secara terpisah.
3. Pesanan dibatalkan tidak dihitung sebagai pesanan aktif.
4. Pesanan yang melewati estimasi selesai dan belum siap harus ditandai terlambat.
5. Setiap ringkasan dapat mengarahkan pengguna menuju daftar data terkait.
6. Dashboard harus memiliki tampilan kosong ketika belum terdapat transaksi.

### Acceptance Criteria

- Setelah pesanan baru dibuat, jumlah pesanan bertambah.
- Setelah pembayaran diverifikasi, nilai pembayaran diterima diperbarui.
- Setelah pesanan dibatalkan, ringkasan pesanan aktif menyesuaikan.
- Data dashboard sesuai dengan transaksi tersimpan.
- Pengguna tanpa izin tidak dapat membaca data keuangan.

## 5.2 Modul Manajemen Pesanan

**Tujuan:** Mendigitalisasi seluruh proses penerimaan dan penyelesaian cucian.

| ID     | Fitur                                         | Prioritas |
| ------ | --------------------------------------------- | --------- |
| ORD-01 | Membuat pesanan baru                          | P0        |
| ORD-02 | Menghasilkan nomor pesanan unik               | P0        |
| ORD-03 | Memilih pelanggan                             | P0        |
| ORD-04 | Menambahkan pelanggan baru saat transaksi     | P0        |
| ORD-05 | Memilih jenis layanan                         | P0        |
| ORD-06 | Menginput berat atau jumlah cucian            | P0        |
| ORD-07 | Menghitung total biaya otomatis               | P0        |
| ORD-08 | Menentukan estimasi selesai                   | P0        |
| ORD-09 | Mengubah status pengerjaan                    | P0        |
| ORD-10 | Mencari dan memfilter pesanan                 | P0        |
| ORD-11 | Melihat detail dan riwayat pesanan            | P0        |
| ORD-12 | Mengubah pesanan dengan aturan izin           | P0        |
| ORD-13 | Membatalkan pesanan dengan alasan             | P0        |
| ORD-14 | Mendukung beberapa layanan dalam satu pesanan | P0        |
| ORD-15 | Mencatat catatan khusus pelanggan             | P0        |
| ORD-16 | Mencatat riwayat perubahan status             | P0        |
| ORD-17 | Melampirkan foto kondisi cucian               | P1        |
| ORD-18 | Label prioritas express                       | P1        |

### Data Pesanan

Setiap pesanan minimal menyimpan:

- ID internal.
- Nomor pesanan.
- Pelanggan.
- Tanggal dan waktu penerimaan.
- Jenis dan rincian layanan.
- Berat atau jumlah setiap layanan.
- Harga satuan saat transaksi.
- Subtotal dan biaya tambahan.
- Total tagihan.
- Estimasi selesai.
- Status pengerjaan.
- Status pembayaran.
- Metode serah terima.
- Catatan pelanggan.
- Petugas pembuat.
- Riwayat perubahan.

### Aturan Bisnis

1. Nomor pesanan harus unik dan dihasilkan otomatis.
2. Harga layanan diambil dari konfigurasi aktif.
3. Harga transaksi harus disimpan sebagai snapshot sehingga perubahan tarif baru tidak mengubah transaksi lama.
4. Berat dan jumlah tidak boleh negatif.
5. Pesanan yang disimpan sebagai pesanan aktif harus memiliki minimal satu layanan yang valid.
6. Perubahan total setelah menerima pembayaran harus memicu perhitungan ulang sisa tagihan.
7. Pengubahan nilai pesanan setelah pembayaran memerlukan alasan yang tercatat.
8. Pembatalan pesanan harus memiliki alasan.
9. Pesanan yang sudah dibatalkan tidak boleh diproses kembali tanpa prosedur pemulihan yang diizinkan.
10. Data pesanan tidak boleh dihapus permanen melalui antarmuka operasional biasa.

### Contoh Kasus

Pelanggan Budi membawa 3 kg cucian.

- Layanan: Cuci Setrika.
- Tarif: Rp7.000/kg.
- Berat: 3 kg.
- Total: Rp21.000.
- Pembayaran awal: Rp0.
- Sisa tagihan: Rp21.000.
- Status: Dalam Antrean.

Tarif di atas hanya contoh, bukan harga tetap sistem.

### Acceptance Criteria

- Kasir dapat membuat pesanan lengkap.
- Total biaya dihitung sesuai tarif tersimpan.
- Nomor pesanan tidak duplikat.
- Pesanan tersimpan dan dapat dicari.
- Perubahan status muncul pada portal tracking.
- Perubahan harga layanan tidak memengaruhi pesanan lama.
- Pembatalan dan koreksi pesanan tercatat dalam audit log.

## 5.3 Modul Manajemen Pelanggan

**Tujuan:** Menyimpan informasi pelanggan untuk mempermudah pelayanan dan transaksi berikutnya.

| ID     | Fitur                                       | Prioritas |
| ------ | ------------------------------------------- | --------- |
| CUS-01 | Menambahkan pelanggan                       | P0        |
| CUS-02 | Mengubah data pelanggan                     | P0        |
| CUS-03 | Mencari pelanggan                           | P0        |
| CUS-04 | Melihat riwayat pesanan                     | P0        |
| CUS-05 | Menyimpan nomor WhatsApp                    | P0        |
| CUS-06 | Menyimpan alamat untuk layanan antar-jemput | P0        |
| CUS-07 | Peringatan kemungkinan pelanggan duplikat   | P0        |
| CUS-08 | Menampilkan frekuensi transaksi             | P1        |
| CUS-09 | Segmentasi pelanggan langganan              | P1        |

### Data Pelanggan

- ID pelanggan.
- Nama pelanggan.
- Nomor WhatsApp.
- Alamat opsional.
- Catatan pelayanan opsional.
- Tanggal pendaftaran.
- Riwayat pesanan.

### Aturan

1. Nama dan nomor WhatsApp diperlukan untuk pelayanan standar.
2. Nomor WhatsApp harus divalidasi dan dinormalisasi.
3. Sistem memberi peringatan jika nomor yang sama sudah terdaftar.
4. Pelanggan lama dapat dipilih tanpa input ulang.
5. Riwayat pesanan tidak boleh hilang ketika data profil diperbarui.
6. Penghapusan data pelanggan harus mengikuti kebijakan retensi dan perlindungan data.
7. Pelanggan tidak memiliki akun login internal.

### Acceptance Criteria

- Kasir dapat menemukan pelanggan berdasarkan nama atau nomor telepon.
- Sistem mengurangi risiko duplikasi pelanggan.
- Riwayat pesanan tampil sesuai pelanggan.
- Staf yang tidak berwenang tidak dapat mengakses seluruh data pribadi pelanggan.

## 5.4 Modul Antar-Jemput

**Tujuan:** Mempermudah penjadwalan dan pemantauan penjemputan serta pengantaran cucian.

| ID     | Fitur                                           | Prioritas |
| ------ | ----------------------------------------------- | --------- |
| PUD-01 | Formulir penjemputan publik                     | P0        |
| PUD-02 | Mencatat permintaan penjemputan                 | P0        |
| PUD-03 | Mengonfirmasi atau menolak permintaan           | P0        |
| PUD-04 | Menjadwalkan penjemputan                        | P0        |
| PUD-05 | Menugaskan kurir                                | P0        |
| PUD-06 | Mengubah status penjemputan                     | P0        |
| PUD-07 | Mengubah status pengantaran                     | P0        |
| PUD-08 | Menampilkan daftar tugas kurir                  | P0        |
| PUD-09 | Mencatat biaya antar-jemput manual              | P0        |
| PUD-10 | Mencatat konfirmasi serah terima                | P0        |
| PUD-11 | Menghubungkan permintaan dengan pesanan laundry | P0        |
| PUD-12 | Reschedule dan pembatalan tugas                 | P0        |
| PUD-13 | Optimasi rute perjalanan                        | P2        |
| PUD-14 | GPS tracking real-time                          | P2        |

### Formulir Penjemputan Pelanggan

Pelanggan mengisi:

1. Nama.
2. Nomor WhatsApp.
3. Alamat penjemputan.
4. Tanggal yang diinginkan.
5. Rentang waktu yang diinginkan.
6. Catatan tambahan jika diperlukan.

Pelanggan tidak perlu login.

### Alur Penjemputan

1. Pelanggan mengirim permintaan.
2. Sistem mencatat permintaan sebagai menunggu konfirmasi.
3. Admin memeriksa ketersediaan.
4. Admin mengonfirmasi jadwal.
5. Admin memilih kurir.
6. Kurir menuju lokasi.
7. Kurir mengambil cucian.
8. Cucian tiba di laundry.
9. Admin menimbang dan membuat pesanan laundry.

**Ketentuan penting:** Permintaan penjemputan bukan otomatis menjadi transaksi laundry final. Berat dan total harga baru ditetapkan setelah cucian diterima dan diperiksa.

### Alur Pengantaran

1. Cucian dinyatakan siap diantar.
2. Admin menentukan jadwal.
3. Admin menugaskan kurir.
4. Kurir menerima tugas.
5. Kurir melakukan pengantaran.
6. Kurir mencatat nama penerima atau konfirmasi sederhana.
7. Status berubah menjadi diterima pelanggan.

### Ketentuan Tracking

- Status diperbarui secara manual oleh petugas.
- Tidak ada pelacakan lokasi GPS.
- Perkiraan waktu bersifat informatif, bukan jaminan kedatangan.
- Detail alamat lengkap tidak ditampilkan pada halaman tracking publik.
- Jadwal yang diajukan pelanggan harus dikonfirmasi terlebih dahulu.

### Acceptance Criteria

- Pelanggan dapat mengajukan penjemputan tanpa akun.
- Admin menerima permintaan dalam dashboard.
- Admin dapat mengonfirmasi, menjadwalkan, dan menugaskan kurir.
- Kurir dapat memperbarui tugas dari HP.
- Tracking pelanggan menampilkan status terakhir.
- Permintaan dapat dikonversi menjadi pesanan laundry tanpa kehilangan hubungan riwayatnya.
- Status penjemputan dan pengantaran disimpan terpisah.

## 5.5 Modul Keuangan dan Pembayaran

**Tujuan:** Mengelola pembayaran manual dan informasi keuangan sederhana.

| ID     | Fitur                                | Prioritas |
| ------ | ------------------------------------ | --------- |
| FIN-01 | Pencatatan pembayaran tunai          | P0        |
| FIN-02 | Pencatatan transfer manual           | P0        |
| FIN-03 | Pencatatan QRIS manual               | P0        |
| FIN-04 | Pembayaran uang muka / DP            | P0        |
| FIN-05 | Pembayaran bertahap                  | P0        |
| FIN-06 | Perhitungan sisa tagihan otomatis    | P0        |
| FIN-07 | Riwayat pembayaran pesanan           | P0        |
| FIN-08 | Daftar tagihan belum lunas           | P0        |
| FIN-09 | Pencatatan pengeluaran sederhana     | P0        |
| FIN-10 | Ringkasan pemasukan dan pengeluaran  | P0        |
| FIN-11 | Filter transaksi berdasarkan tanggal | P0        |
| FIN-12 | Koreksi pembayaran dengan audit      | P0        |
| FIN-13 | Ekspor laporan CSV                   | P0        |
| FIN-14 | Laporan laba rugi lebih lengkap      | P1        |
| FIN-15 | Rekonsiliasi bank otomatis           | P2        |

### Metode Pembayaran

**Tunai**

Kasir menerima uang dan mencatat jumlah pembayaran.

**Transfer Bank**

Pelanggan melakukan transfer, kemudian kasir memeriksa penerimaan dana melalui rekening usaha.

**QRIS Manual**

Pelanggan membayar menggunakan QRIS yang telah dimiliki usaha. Kasir memeriksa pembayaran sebelum mengonfirmasi.

**DP / Pembayaran Sebagian**

Pelanggan dapat membayar sebagian tagihan, kemudian melunasinya pada transaksi berikutnya.

### Perhitungan

Total tagihan:

Total = Jumlah seluruh biaya layanan + Biaya tambahan + Biaya antar-jemput.

Sisa tagihan:

Sisa = Total tagihan - Total pembayaran yang sah.

Status pembayaran dihitung menjadi:

| Status        | Kondisi                                                        |
| ------------- | -------------------------------------------------------------- |
| Belum Bayar   | Tidak ada pembayaran yang sah.                                 |
| Sebagian / DP | Pembayaran lebih dari nol tetapi belum mencapai total tagihan. |
| Lunas         | Total pembayaran sah telah mencapai total tagihan.             |

Status harus diturunkan dari data pembayaran, bukan ditentukan secara bebas tanpa transaksi pendukung.

### Aturan Pembayaran

1. Pembayaran harus dikonfirmasi oleh petugas berwenang.
2. Bukti transfer tidak otomatis berarti lunas.
3. Setiap pembayaran memiliki waktu, nominal, metode, dan petugas pencatat.
4. Pembayaran tidak boleh bernilai negatif atau nol.
5. Sistem harus mencegah pencatatan pembayaran melebihi sisa tagihan tanpa alur koreksi khusus.
6. Koreksi dan pembatalan pembayaran wajib memiliki alasan dan jejak audit.
7. Pembayaran yang telah tercatat tidak boleh dihapus tanpa histori.
8. Pembayaran dan status pengerjaan laundry bersifat independen.
9. Jika cucian diserahkan ketika belum lunas, sistem harus menampilkan peringatan dan tetap mencatat piutang.
10. Biaya merchant dari bank atau penyelenggara QRIS, jika ada, berada di luar mekanisme transaksi aplikasi dan dapat dicatat sebagai pengeluaran.

### Pencatatan Pengeluaran

Contoh pengeluaran:

- Deterjen.
- Pewangi.
- Plastik laundry.
- Listrik.
- Air.
- Transportasi kurir.
- Perawatan mesin.
- Pengeluaran operasional lainnya.

Laporan MVP membedakan:

- **Nilai pesanan:** total nilai transaksi laundry.
- **Uang diterima:** pembayaran yang benar-benar tercatat.
- **Tagihan belum dibayar:** nilai piutang pelanggan.
- **Pengeluaran:** biaya operasional yang dicatat.
- **Selisih kas operasional sederhana:** pembayaran masuk dikurangi pengeluaran tercatat.

Selisih kas tidak boleh diberi label laba bersih resmi karena belum mencakup seluruh konsep akuntansi seperti penyusutan, kewajiban, dan penyesuaian akrual.

### Acceptance Criteria

- Pembayaran tunai, transfer, dan QRIS dapat dicatat manual.
- Satu pesanan dapat memiliki lebih dari satu pembayaran.
- Sisa tagihan dihitung dengan benar.
- Transaksi yang belum lunas tetap terlihat dalam daftar piutang.
- Pembayaran hanya dapat dikoreksi oleh pengguna berwenang.
- Laporan keuangan konsisten dengan data pembayaran dan pengeluaran.
- Tidak ada integrasi payment gateway pada MVP.

## 5.6 Modul Nota Digital

**Tujuan:** Menggantikan kebutuhan nota fisik dengan bukti pesanan digital.

| ID     | Fitur                     | Prioritas |
| ------ | ------------------------- | --------- |
| INV-01 | Nomor nota otomatis       | P0        |
| INV-02 | Halaman nota digital      | P0        |
| INV-03 | Rincian layanan dan biaya | P0        |
| INV-04 | Informasi pembayaran      | P0        |
| INV-05 | Tautan tracking pesanan   | P0        |
| INV-06 | Unduh atau simpan PDF     | P0        |
| INV-07 | Tombol bagikan WhatsApp   | P0        |
| INV-08 | Nama dan identitas usaha  | P0        |
| INV-09 | Riwayat nota              | P0        |
| INV-10 | Penyesuaian desain nota   | P1        |

### Informasi Nota

Nota minimal memuat:

1. Nama laundry.
2. Kontak usaha.
3. Nomor pesanan.
4. Tanggal pesanan.
5. Nama pelanggan.
6. Rincian layanan.
7. Berat atau jumlah.
8. Tarif dan subtotal.
9. Biaya tambahan jika ada.
10. Total tagihan.
11. Nominal dibayar.
12. Sisa tagihan.
13. Estimasi selesai.
14. Tautan tracking.
15. Catatan atau ketentuan layanan.

### Mekanisme WhatsApp

1. Kasir membuat pesanan.
2. Sistem membuat nota dan tautan tracking.
3. Kasir menekan tombol Kirim Nota.
4. Sistem membuka WhatsApp dengan nomor tujuan dan pesan siap kirim.
5. Kasir meninjau dan mengirim pesan secara manual.

Aplikasi dapat mencatat bahwa tindakan membuka WhatsApp dilakukan, tetapi tidak boleh mengklaim pesan terkirim atau diterima tanpa bukti yang memadai.

### Acceptance Criteria

- Nota dibuat dari data pesanan.
- Informasi total dan sisa tagihan benar.
- Nota dapat dibuka dari HP.
- File PDF dapat disimpan tanpa printer.
- Tautan WhatsApp mengarah ke nomor yang benar.
- Pelanggan tidak membutuhkan login untuk membuka nota yang diotorisasi melalui tautan.

## 5.7 Modul Tracking Pelanggan Tanpa Login

**Tujuan:** Memberikan transparansi status cucian melalui tautan publik yang aman.

| ID     | Fitur                              | Prioritas |
| ------ | ---------------------------------- | --------- |
| TRK-01 | Token tracking unik                | P0        |
| TRK-02 | Halaman tracking tanpa login       | P0        |
| TRK-03 | Informasi ringkas pesanan          | P0        |
| TRK-04 | Timeline pengerjaan cucian         | P0        |
| TRK-05 | Tracking penjemputan               | P0        |
| TRK-06 | Tracking pengantaran               | P0        |
| TRK-07 | Estimasi waktu selesai             | P0        |
| TRK-08 | Status pembayaran ringkas          | P0        |
| TRK-09 | Tombol WhatsApp admin              | P0        |
| TRK-10 | Pencabutan atau penggantian token  | P0        |
| TRK-11 | Indikator waktu pembaruan terakhir | P0        |
| TRK-12 | Notifikasi otomatis                | P2        |

### Contoh Tautan

`https://domain-laundry.id/track/{token-acak}`

Token merupakan kredensial akses terbatas dan tidak boleh berupa nomor pesanan yang mudah ditebak.

### Informasi yang Dapat Dilihat Pelanggan

- Nomor pesanan.
- Jenis layanan.
- Berat atau jumlah cucian.
- Status pengerjaan.
- Estimasi selesai.
- Status antar-jemput jika digunakan.
- Total dan sisa tagihan.
- Waktu terakhir diperbarui.
- Kontak WhatsApp laundry.

### Informasi yang Tidak Ditampilkan

- Nomor telepon lengkap pelanggan.
- Alamat lengkap.
- Informasi internal pegawai.
- Catatan rahasia operasional.
- Data pembayaran sensitif.
- Pesanan pelanggan lain.
- Data laporan internal.

### Ketentuan Keamanan

1. Token dihasilkan secara kriptografis dengan entropi minimal 128 bit.
2. Token tidak boleh mudah diprediksi.
3. Setiap token hanya memberikan akses ke informasi yang diotorisasi.
4. Token dapat dicabut dan diganti.
5. Halaman tracking tidak boleh diindeks mesin pencari.
6. Endpoint publik menerapkan pembatasan permintaan.
7. Data pribadi yang ditampilkan harus diminimalkan.
8. Akses dengan token tidak valid menampilkan pesan umum tanpa mengungkapkan data pesanan.
9. Pelanggan tidak bisa mengubah status pesanan melalui halaman tracking.
10. Untuk permintaan penjemputan, tautan tracking awal dapat tetap digunakan setelah permintaan dikonversi menjadi pesanan laundry.

### Acceptance Criteria

- Pelanggan dapat mengakses pesanan melalui token valid tanpa login.
- Token tidak valid atau dicabut tidak memberikan data.
- Token satu pelanggan tidak dapat digunakan untuk melihat pesanan lain.
- Perubahan status petugas terlihat pada halaman tracking setelah data diperbarui.
- Halaman tracking berfungsi dengan baik melalui browser HP.

## 5.8 Modul Pengaturan

**Tujuan:** Memungkinkan usaha laundry menyesuaikan aplikasi dengan kondisi operasionalnya.

| ID     | Fitur                              | Prioritas |
| ------ | ---------------------------------- | --------- |
| SET-01 | Profil usaha laundry               | P0        |
| SET-02 | Nomor WhatsApp usaha               | P0        |
| SET-03 | Alamat usaha                       | P0        |
| SET-04 | Logo usaha opsional                | P0        |
| SET-05 | Manajemen jenis layanan            | P0        |
| SET-06 | Pengaturan harga                   | P0        |
| SET-07 | Pengaturan biaya antar-jemput      | P0        |
| SET-08 | Manajemen akun pengguna            | P0        |
| SET-09 | Pengaturan peran pengguna          | P0        |
| SET-10 | Pengaturan estimasi durasi layanan | P0        |
| SET-11 | Jam operasional                    | P1        |
| SET-12 | Template pesan WhatsApp            | P1        |
| SET-13 | Pengaturan diskon dan promosi      | P1        |

### Ketentuan

1. Hanya Owner yang dapat mengubah harga resmi.
2. Perubahan harga harus dicatat dalam audit log.
3. Perubahan tarif tidak berlaku surut pada transaksi lama.
4. Akun petugas dapat dinonaktifkan tanpa menghapus histori pekerjaannya.
5. Profil usaha digunakan pada nota dan halaman publik.
6. Harga dan estimasi layanan dapat disesuaikan tanpa perubahan kode aplikasi.

---

# 6. ALUR BISNIS UTAMA

## 6.1 Skenario A — Pelanggan Datang Langsung

1. Pelanggan datang membawa cucian.
2. Kasir membuka aplikasi.
3. Kasir mencari atau menambah pelanggan.
4. Kasir memilih layanan.
5. Kasir memasukkan berat atau jumlah.
6. Sistem menghitung total biaya.
7. Kasir menentukan estimasi selesai.
8. Kasir menyimpan pesanan.
9. Sistem membuat nomor pesanan dan nota.
10. Kasir membagikan nota melalui WhatsApp secara manual.
11. Staf memproses cucian.
12. Staf memperbarui status.
13. Pelanggan memantau progres melalui tautan.
14. Cucian dinyatakan siap.
15. Pelanggan mengambil cucian.
16. Kasir melakukan verifikasi serah terima dan pembayaran.
17. Pesanan dinyatakan selesai secara operasional.

Jika pembayaran belum lunas, kewajiban pelanggan tetap tercatat.

## 6.2 Skenario B — Pelanggan Meminta Penjemputan

1. Pelanggan membuka halaman permintaan penjemputan.
2. Pelanggan mengisi formulir tanpa login.
3. Sistem mencatat permintaan.
4. Pelanggan mendapatkan nomor permintaan dan tautan tracking.
5. Admin memeriksa permintaan.
6. Admin mengonfirmasi jadwal melalui WhatsApp manual.
7. Admin menugaskan kurir.
8. Kurir menuju lokasi.
9. Kurir mengambil cucian.
10. Kurir menyerahkan cucian kepada laundry.
11. Kasir memeriksa serta menimbang cucian.
12. Kasir menetapkan layanan dan biaya final.
13. Sistem menghubungkan permintaan penjemputan dengan pesanan laundry.
14. Proses pencucian dimulai.
15. Pelanggan dapat melanjutkan tracking melalui tautan terkait.

## 6.3 Skenario C — Pembayaran DP

1. Pesanan memiliki total Rp50.000.
2. Pelanggan membayar Rp20.000.
3. Kasir memilih metode pembayaran.
4. Kasir mencatat pembayaran Rp20.000.
5. Status pembayaran menjadi Sebagian / DP.
6. Sistem menampilkan sisa Rp30.000.
7. Pelanggan membayar Rp30.000 pada transaksi berikutnya.
8. Kasir mengonfirmasi pembayaran.
9. Sistem mengubah status menjadi Lunas.

Tidak diperlukan perubahan manual pada status Lunas di luar pencatatan transaksi pembayaran.

## 6.4 Skenario D — Pengantaran Cucian

1. Cucian selesai diperiksa dan dikemas.
2. Admin menentukan metode pengantaran.
3. Admin menjadwalkan pengantaran.
4. Admin menugaskan kurir.
5. Kurir menuju lokasi.
6. Kurir menyerahkan cucian.
7. Kurir mencatat konfirmasi penerimaan.
8. Status pengantaran menjadi Diterima.
9. Status operasional pesanan menjadi Selesai.
10. Jika tagihan belum lunas, sistem tetap mempertahankan data piutang.

---

# 7. STATUS DAN STATE TRANSITION

## 7.1 Status Pengerjaan Cucian

| No. | Status                   | Deskripsi                                  |
| --- | ------------------------ | ------------------------------------------ |
| 1   | Pesanan Diterima         | Pesanan baru berhasil dibuat.              |
| 2   | Dalam Antrean            | Menunggu proses laundry.                   |
| 3   | Sedang Dicuci            | Proses pencucian berlangsung.              |
| 4   | Dikeringkan              | Pakaian dalam tahap pengeringan.           |
| 5   | Disetrika                | Pakaian sedang disetrika.                  |
| 6   | Pemeriksaan & Pengemasan | Pemeriksaan akhir dan pengemasan.          |
| 7   | Siap Diambil / Diantar   | Pakaian telah siap diserahkan.             |
| 8   | Selesai                  | Pakaian telah diserahkan kepada pelanggan. |

Status tambahan: **Dibatalkan**.

### Aturan Perubahan

- Perubahan dilakukan oleh petugas berwenang.
- Setiap perubahan memiliki waktu dan identitas petugas.
- Tahap yang tidak relevan boleh dilewati sesuai jenis layanan.
- Sistem tidak boleh mewajibkan penyetrikaan pada layanan cuci kering.
- Perubahan mundur atau koreksi status harus memiliki alasan.
- Status Selesai mensyaratkan adanya konfirmasi serah terima.
- Status Dibatalkan menghentikan proses normal.
- Riwayat perubahan harus tetap tersimpan.

## 7.2 Status Penjemputan

| Status                     | Keterangan                        |
| -------------------------- | --------------------------------- |
| Menunggu Konfirmasi        | Permintaan baru dibuat pelanggan. |
| Dikonfirmasi / Dijadwalkan | Jadwal telah disetujui admin.     |
| Kurir Menuju Lokasi        | Kurir sedang menuju pelanggan.    |
| Cucian Dijemput            | Cucian diterima kurir.            |
| Tiba di Laundry            | Cucian diserahkan kepada laundry. |
| Dibatalkan                 | Permintaan atau tugas dibatalkan. |

Permintaan juga dapat berstatus Ditolak jika usaha tidak dapat melayani.

## 7.3 Status Pengantaran

| Status              | Keterangan                    |
| ------------------- | ----------------------------- |
| Belum Dijadwalkan   | Pengantaran belum ditentukan. |
| Dijadwalkan         | Jadwal dan kurir ditentukan.  |
| Kurir Menuju Lokasi | Kurir memulai perjalanan.     |
| Dalam Pengantaran   | Cucian sedang dikirim.        |
| Diterima Pelanggan  | Serah terima berhasil.        |
| Gagal Diantar       | Pengiriman tidak berhasil.    |
| Dibatalkan          | Tugas pengantaran dibatalkan. |

Pengantaran gagal dapat dijadwalkan ulang dengan tetap mempertahankan riwayat sebelumnya.

## 7.4 Status Pembayaran

Status pembayaran terpisah dari semua status operasional.

- Belum Bayar.
- Sebagian / DP.
- Lunas.

Pembatalan dan pengembalian dana dicatat sebagai aktivitas keuangan tersendiri sesuai kewenangan.

---

# 8. ATURAN BISNIS DAN VALIDASI

## 8.1 Perhitungan Harga

Sistem mendukung dua tipe harga utama:

**A. Harga per Kilogram**

Subtotal = Berat × Tarif per kilogram.

**B. Harga per Satuan**

Subtotal = Jumlah item × Tarif per item.

Total pesanan merupakan penjumlahan seluruh subtotal layanan dan biaya tambahan yang berlaku.

Ketentuan:

1. Mata uang menggunakan Rupiah.
2. Nilai uang disimpan tanpa kesalahan pembulatan floating-point.
3. Berat dapat menerima angka desimal sesuai presisi yang ditentukan usaha.
4. Aturan berat minimum dan pembulatan harus dapat dikonfigurasi jika digunakan.
5. Harga total harus ditampilkan sebelum pesanan dikonfirmasi.
6. Tarif yang digunakan pada transaksi disimpan permanen sebagai snapshot.

## 8.2 Keterlambatan

Pesanan dinyatakan terlambat apabila:

- Waktu saat ini sudah melewati estimasi selesai; dan
- Status cucian belum mencapai Siap Diambil / Diantar atau status akhir yang setara.

Pesanan terlambat ditandai pada dashboard.

## 8.3 Koreksi Transaksi

Perubahan berikut harus masuk audit log:

- Harga pesanan.
- Total tagihan.
- Status pembayaran.
- Koreksi pembayaran.
- Pembatalan pesanan.
- Perubahan layanan.
- Perubahan status yang tidak mengikuti alur normal.

## 8.4 Penanganan Kesalahan

Sistem harus menangani:

1. Data wajib belum diisi.
2. Berat tidak valid.
3. Nomor WhatsApp tidak valid.
4. Layanan tidak aktif.
5. Tarif tidak ditemukan.
6. Token tracking tidak valid.
7. Permintaan antar-jemput duplikat.
8. Pembayaran melebihi tagihan.
9. Pesanan sudah dibatalkan.
10. Dua petugas mengubah pesanan bersamaan.
11. Koneksi internet terputus.
12. Permintaan API gagal.
13. Pengguna tidak memiliki izin.
14. Sesi petugas kedaluwarsa.

Sistem harus memberikan pesan kesalahan yang mudah dipahami dan menghindari penyimpanan data ganda akibat pengiriman ulang permintaan.

---

# 9. RANCANGAN ANTARMUKA DAN PENGALAMAN PENGGUNA

## 9.1 Struktur Navigasi Internal

Menu utama:

1. Dashboard.
2. Pesanan.
3. Pelanggan.
4. Antar-Jemput.
5. Keuangan.
6. Nota Digital.
7. Pengaturan.

Tracking pelanggan disediakan pada portal publik terpisah.

Pada tampilan mobile, fitur Nota Digital dapat menjadi bagian dari detail pesanan sehingga navigasi lebih ringkas.

## 9.2 Daftar Halaman MVP

| ID    | Halaman                      | Pengguna                    |
| ----- | ---------------------------- | --------------------------- |
| UI-01 | Login                        | Pengguna internal           |
| UI-02 | Dashboard Owner              | Owner                       |
| UI-03 | Dashboard Kasir              | Kasir                       |
| UI-04 | Daftar Pesanan               | Owner, Kasir, Staf terbatas |
| UI-05 | Buat Pesanan                 | Owner, Kasir                |
| UI-06 | Detail Pesanan               | Pengguna berwenang          |
| UI-07 | Ubah Status Cucian           | Owner, Kasir, Staf          |
| UI-08 | Daftar Pelanggan             | Owner, Kasir                |
| UI-09 | Detail Pelanggan             | Owner, Kasir                |
| UI-10 | Daftar Antar-Jemput          | Owner, Kasir                |
| UI-11 | Detail Tugas Kurir           | Owner, Kasir, Kurir         |
| UI-12 | Pembayaran                   | Owner, Kasir                |
| UI-13 | Laporan Keuangan             | Owner, Kasir terbatas       |
| UI-14 | Nota Digital                 | Pengguna berwenang          |
| UI-15 | Pengaturan Usaha             | Owner                       |
| UI-16 | Pengaturan Layanan           | Owner                       |
| UI-17 | Pengaturan Pengguna          | Owner                       |
| UI-18 | Tracking Publik              | Pelanggan                   |
| UI-19 | Permintaan Penjemputan       | Pelanggan                   |
| UI-20 | Konfirmasi Permintaan Publik | Pelanggan                   |

## 9.3 Prinsip UI/UX

1. Gunakan antarmuka bersih dan modern.
2. Hindari kepadatan informasi berlebihan.
3. Prioritaskan tombol Buat Pesanan.
4. Gunakan label status dalam Bahasa Indonesia.
5. Gunakan warna status secara konsisten.
6. Status tidak boleh dibedakan berdasarkan warna saja.
7. Tampilkan informasi utama sebelum detail tambahan.
8. Sediakan pencarian pada daftar yang panjang.
9. Gunakan konfirmasi pada tindakan sensitif.
10. Tampilkan feedback setelah setiap tindakan.
11. Gunakan loading, empty state, dan error state.
12. Pastikan formulir mudah digunakan pada layar sentuh.
13. Pertahankan struktur navigasi yang konsisten.
14. Hindari modal yang terlalu kompleks pada layar kecil.
15. Gunakan ikon yang memiliki makna jelas.
16. Sediakan tampilan responsif untuk HP, tablet, dan laptop.

## 9.4 Rekomendasi Komponen

- Card ringkasan.
- Data table responsif.
- Bottom navigation atau navigasi mobile yang ringkas.
- Form input.
- Select layanan.
- Status badge.
- Timeline tracking.
- Dialog konfirmasi.
- Toast notification.
- Filter tanggal.
- Pencarian pelanggan.
- Empty state.
- Loading skeleton.
- Ringkasan pembayaran.

## 9.5 Keadaan Antarmuka yang Wajib Ditangani

Setiap halaman utama harus mempunyai penanganan untuk:

- Loading.
- Berhasil.
- Tidak ada data.
- Validasi gagal.
- Error server.
- Tidak memiliki akses.
- Koneksi terputus.
- Data sudah berubah oleh pengguna lain.

---

# 10. RANCANGAN DATA KONSEPTUAL

Bagian ini merupakan kebutuhan data awal untuk menjadi dasar penyusunan Database Design Document.

## 10.1 Entitas Utama

| Entitas                 | Fungsi                             |
| ----------------------- | ---------------------------------- |
| businesses              | Profil usaha laundry.              |
| users                   | Akun pengguna internal.            |
| roles / permissions     | Peran dan kewenangan pengguna.     |
| customers               | Data pelanggan.                    |
| services                | Katalog layanan dan tarif aktif.   |
| orders                  | Informasi utama pesanan laundry.   |
| order_items             | Rincian layanan dalam pesanan.     |
| order_status_history    | Riwayat perubahan proses cucian.   |
| payments                | Riwayat pembayaran.                |
| expenses                | Pengeluaran operasional.           |
| pickup_requests         | Permintaan penjemputan pelanggan.  |
| delivery_tasks          | Tugas penjemputan dan pengantaran. |
| delivery_status_history | Riwayat status tugas kurir.        |
| tracking_tokens         | Token akses tracking publik.       |
| audit_logs              | Riwayat tindakan penting pengguna. |
| business_settings       | Konfigurasi operasional usaha.     |

Entitas ini merupakan rancangan konseptual dan dapat disesuaikan ketika desain database terperinci dibuat.

## 10.2 Data Pesanan

Struktur minimum `orders`:

- id
- order_number
- customer_id
- created_by
- order_date
- estimated_completion_at
- operational_status
- subtotal_amount
- extra_charge_amount
- delivery_fee_amount
- total_amount
- payment_status turunan atau hasil kalkulasi
- fulfillment_method
- customer_notes
- internal_notes
- created_at
- updated_at
- cancelled_at
- cancellation_reason

## 10.3 Data Rincian Pesanan

Struktur minimum `order_items`:

- id
- order_id
- service_id
- service_name_snapshot
- pricing_type
- quantity
- unit
- unit_price_snapshot
- subtotal

## 10.4 Data Pembayaran

Struktur minimum `payments`:

- id
- order_id
- amount
- payment_method
- verification_status
- payment_time
- verified_by
- reference_note
- correction_reason
- created_at

Catatan: status pembayaran pesanan harus dihitung berdasarkan transaksi yang sah, bukan hanya sebuah nilai bebas yang dapat diubah tanpa dasar.

## 10.5 Data Tracking

Struktur minimum `tracking_tokens`:

- id
- related_resource_type
- related_resource_id
- token_hash
- created_at
- expires_at
- revoked_at

Token mentah harus diperlakukan sebagai kredensial rahasia, tidak dicatat dalam log, dan tidak disimpan dalam bentuk yang mudah diakses ketika tidak diperlukan.

## 10.6 Relasi Data Utama

1. Satu pelanggan dapat memiliki banyak pesanan.
2. Satu pesanan dapat memiliki banyak item layanan.
3. Satu pesanan dapat memiliki banyak pembayaran.
4. Satu pesanan memiliki riwayat perubahan status.
5. Satu permintaan penjemputan dapat dihubungkan dengan satu pesanan yang terbentuk setelah cucian diterima.
6. Satu pesanan dapat memiliki tugas penjemputan dan pengantaran.
7. Satu tugas antar-jemput mempunyai riwayat status.
8. Satu pengguna internal dapat membuat atau memperbarui banyak transaksi.
9. Token tracking memberikan akses terbatas pada resource yang diotorisasi.

---

# 11. ARSITEKTUR TEKNOLOGI

## 11.1 Rekomendasi Technology Stack

| Lapisan        | Teknologi                                |
| -------------- | ---------------------------------------- |
| Frontend       | React + TypeScript                       |
| Build Tool     | Vite                                     |
| Styling        | Tailwind CSS                             |
| UI Components  | shadcn/ui                                |
| Icons          | Lucide React                             |
| Backend        | FastAPI                                  |
| Database       | PostgreSQL                               |
| ORM            | SQLAlchemy                               |
| Migration      | Alembic                                  |
| API            | REST + OpenAPI                           |
| Authentication | Secure Cookie-Based Session              |
| Authorization  | Role-Based Access Control                |
| PDF            | Generator PDF dari template nota         |
| Deployment     | Docker atau platform hosting terkelola   |
| Monitoring     | Application logging dan error monitoring |

Pemilihan teknologi merupakan rekomendasi awal dan harus dikonfirmasi dalam Technical Requirements Document.

## 11.2 Arsitektur Logis

Alur komponen:

**Frontend Internal dan Portal Publik**
→ **Backend REST API**
→ **Business Logic / Service Layer**
→ **Database PostgreSQL**

Layanan pendukung:

- Authentication dan Authorization.
- PDF Generation.
- Tracking Token Service.
- Audit Logging.
- Backup.
- Monitoring.

WhatsApp dibuka melalui tautan yang telah disiapkan frontend, bukan melalui pengiriman otomatis dari backend.

## 11.3 Ketentuan Infrastruktur

1. Aplikasi harus dapat diakses melalui HTTPS.
2. Database tidak boleh dapat diakses langsung dari internet publik tanpa pembatasan yang tepat.
3. Kredensial disimpan dalam environment/secret management.
4. Backup database dijalankan secara rutin.
5. Frontend dan backend harus memiliki konfigurasi environment terpisah.
6. Endpoint publik dan internal harus memiliki kebijakan keamanan berbeda.
7. Hosting dipilih dengan mempertimbangkan biaya operasional UMKM.

## 11.4 Ketergantungan Eksternal

MVP hanya memerlukan:

- Perangkat HP atau laptop.
- Koneksi internet.
- Hosting aplikasi dan database.
- Domain atau alamat aplikasi.
- WhatsApp pada perangkat petugas untuk berbagi pesan.
- Rekening atau QRIS usaha jika metode tersebut digunakan.

Tidak diperlukan payment gateway ataupun perangkat POS khusus.

---

# 12. NON-FUNCTIONAL REQUIREMENTS

## 12.1 Keamanan

| ID         | Kebutuhan                                                                     |
| ---------- | ----------------------------------------------------------------------------- |
| NFR-SEC-01 | Seluruh komunikasi menggunakan HTTPS.                                         |
| NFR-SEC-02 | Password internal disimpan menggunakan password hashing yang aman.            |
| NFR-SEC-03 | Semua endpoint internal memverifikasi autentikasi.                            |
| NFR-SEC-04 | Semua tindakan sensitif memverifikasi kewenangan.                             |
| NFR-SEC-05 | Session cookie dilindungi menggunakan konfigurasi keamanan sesuai lingkungan. |
| NFR-SEC-06 | Sistem memiliki proteksi CSRF pada operasi yang relevan.                      |
| NFR-SEC-07 | Semua input pengguna divalidasi di backend.                                   |
| NFR-SEC-08 | Endpoint publik memiliki rate limiting.                                       |
| NFR-SEC-09 | Token tracking tidak dapat diprediksi dan dapat dicabut.                      |
| NFR-SEC-10 | Audit log mencatat tindakan penting.                                          |
| NFR-SEC-11 | Data sensitif tidak dimasukkan ke log aplikasi.                               |
| NFR-SEC-12 | Halaman publik tidak boleh mengekspos data pelanggan lain.                    |

## 12.2 Kinerja

Target awal yang diuji:

| ID          | Target                                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------- |
| NFR-PERF-01 | Halaman utama dan daftar inti ditargetkan responsif dalam 3 detik pada kondisi pengujian jaringan representatif. |
| NFR-PERF-02 | Aksi pembuatan pesanan memberikan respons atau indikator progres yang jelas.                                     |
| NFR-PERF-03 | Pencarian pelanggan dan pesanan tetap responsif pada volume data uji yang disepakati.                            |
| NFR-PERF-04 | Aplikasi tidak menyebabkan pengiriman transaksi ganda saat pengguna menekan tombol berulang kali.                |
| NFR-PERF-05 | Perubahan status muncul setelah halaman melakukan refresh atau pengambilan data terbaru.                         |

Angka performa merupakan target awal dan bukan jaminan pada semua perangkat atau jaringan.

## 12.3 Usability

1. Mendukung tampilan mobile minimal lebar 320 px.
2. Tidak terdapat overflow horizontal pada halaman utama.
3. Pengguna dapat menyelesaikan transaksi standar dengan langkah minimal.
4. Bahasa antarmuka menggunakan Bahasa Indonesia.
5. Pesan kesalahan mudah dipahami.
6. Navigasi tidak bergantung pada hover.
7. Tombol penting memiliki area sentuh yang memadai.
8. Warna dan tipografi memperhatikan keterbacaan.
9. Indikator status dilengkapi teks.
10. Formulir memiliki label dan validasi yang jelas.

## 12.4 Reliability dan Backup

1. Aplikasi harus menjaga konsistensi transaksi database.
2. Kegagalan penyimpanan tidak boleh menghasilkan transaksi setengah selesai.
3. Pengiriman permintaan ulang harus ditangani agar tidak menimbulkan duplikasi.
4. Backup otomatis ditargetkan minimal harian.
5. Backup disimpan terpisah dari database utama sesuai kemampuan hosting.
6. Prosedur pemulihan data harus terdokumentasi.
7. Restore backup wajib diuji sebelum produksi.
8. Kesalahan server tidak boleh mengekspos stack trace kepada pengguna akhir.

## 12.5 Privacy

1. Data pelanggan digunakan untuk pelayanan laundry.
2. Akses data dibatasi berdasarkan kebutuhan tugas.
3. Halaman publik hanya menampilkan informasi yang diperlukan.
4. Data pribadi tidak digunakan untuk tujuan lain tanpa dasar yang sesuai.
5. Kebijakan privasi dan retensi harus disusun sebelum peluncuran publik.
6. Aplikasi harus mendukung penanganan permintaan koreksi atau penghapusan data sesuai kewajiban yang berlaku.

## 12.6 Maintainability

1. Backend menggunakan struktur modular.
2. Business logic dipisahkan dari route/controller.
3. Frontend menggunakan komponen yang dapat digunakan ulang.
4. API terdokumentasi melalui OpenAPI.
5. Database menggunakan migration terkontrol.
6. Perubahan fitur penting memiliki pengujian.
7. Konfigurasi pengembangan dan produksi dipisahkan.
8. Riwayat perubahan kode disimpan melalui version control.

---

# 13. LAPORAN DAN INDIKATOR KINERJA

## 13.1 Laporan MVP

Laporan yang wajib tersedia:

1. Jumlah pesanan per hari.
2. Total nilai pesanan.
3. Total uang diterima.
4. Total tagihan belum lunas.
5. Total pengeluaran.
6. Pesanan berdasarkan status.
7. Pesanan terlambat.
8. Riwayat transaksi pelanggan.
9. Laporan berdasarkan rentang tanggal.

## 13.2 KPI Produk

| KPI                       | Definisi                                                     |
| ------------------------- | ------------------------------------------------------------ |
| Waktu Input Pesanan       | Durasi yang diperlukan kasir membuat pesanan.                |
| Pesanan Tercatat          | Persentase transaksi operasional yang masuk sistem.          |
| Ketepatan Penyelesaian    | Persentase pesanan siap sebelum atau saat estimasi.          |
| Pesanan Terlambat         | Jumlah pesanan melewati estimasi selesai.                    |
| Nilai Piutang             | Total tagihan belum dilunasi.                                |
| Penyelesaian Antar-Jemput | Perbandingan tugas selesai terhadap tugas yang dikonfirmasi. |
| Keberhasilan Tracking     | Persentase akses tracking yang berhasil saat pengujian.      |
| Keberhasilan Transaksi    | Persentase pembuatan pesanan dan pembayaran tanpa error.     |

## 13.3 Sasaran Uji Awal

- Pembuatan pesanan standar ditargetkan kurang dari 2 menit.
- Seluruh kasus uji kritis pembayaran harus lulus.
- Seluruh kasus uji kritis keamanan tracking harus lulus.
- Seluruh kasus uji kritis hak akses harus lulus.
- Seluruh proses utama dapat diselesaikan melalui HP.

Target produksi yang lebih rinci ditentukan setelah pengujian dengan perangkat dan koneksi yang representatif.

---

# 14. USER STORIES

## 14.1 Owner

**US-001**

Sebagai Owner, saya ingin melihat jumlah pesanan dan pendapatan hari ini agar dapat memantau kondisi usaha tanpa memeriksa buku transaksi.

**US-002**

Sebagai Owner, saya ingin mengubah harga layanan agar dapat menyesuaikan tarif dengan biaya operasional.

**US-003**

Sebagai Owner, saya ingin melihat pesanan yang terlambat agar dapat mengambil tindakan dengan cepat.

**US-004**

Sebagai Owner, saya ingin mengatur akun pegawai agar setiap karyawan hanya dapat mengakses fitur sesuai tanggung jawabnya.

## 14.2 Kasir

**US-005**

Sebagai Kasir, saya ingin membuat pesanan hanya melalui HP agar tidak memerlukan mesin kasir tambahan.

**US-006**

Sebagai Kasir, saya ingin sistem menghitung biaya otomatis agar mengurangi kesalahan perhitungan.

**US-007**

Sebagai Kasir, saya ingin membagikan nota melalui WhatsApp agar pelanggan mendapatkan bukti pesanan tanpa nota cetak.

**US-008**

Sebagai Kasir, saya ingin mencatat pembayaran sebagian agar sisa tagihan pelanggan dapat dipantau.

## 14.3 Staf Laundry

**US-009**

Sebagai Staf, saya ingin melihat antrean pekerjaan agar mengetahui cucian mana yang harus dikerjakan.

**US-010**

Sebagai Staf, saya ingin memperbarui status cucian agar pelanggan dan kasir mengetahui perkembangannya.

## 14.4 Kurir

**US-011**

Sebagai Kurir, saya ingin melihat daftar tugas penjemputan agar dapat mengetahui alamat dan jadwal yang ditugaskan.

**US-012**

Sebagai Kurir, saya ingin memperbarui status pengiriman agar pelanggan mengetahui progres antar-jemputnya.

## 14.5 Pelanggan

**US-013**

Sebagai Pelanggan, saya ingin memantau status cucian tanpa login agar tidak perlu membuat akun.

**US-014**

Sebagai Pelanggan, saya ingin melihat nota digital agar dapat mengetahui rincian tagihan.

**US-015**

Sebagai Pelanggan, saya ingin mengajukan permintaan penjemputan dari HP agar tidak perlu datang langsung ke laundry.

**US-016**

Sebagai Pelanggan, saya ingin mengetahui status pengantaran agar dapat memperkirakan kapan cucian akan diterima.

**US-017**

Sebagai Pelanggan, saya ingin menghubungi laundry melalui WhatsApp agar mudah meminta bantuan.

---

# 15. PENGUJIAN DAN ACCEPTANCE TEST

## 15.1 Kategori Pengujian

Pengujian dibagi menjadi:

1. Unit Test.
2. API / Integration Test.
3. Database Test.
4. Authorization Test.
5. Functional End-to-End Test.
6. Responsive UI Test.
7. Security Test.
8. User Acceptance Test.
9. Backup and Recovery Test.

## 15.2 Skenario Pengujian MVP

| ID    | Skenario                               | Hasil yang Diharapkan                                  |
| ----- | -------------------------------------- | ------------------------------------------------------ |
| AT-01 | Owner login dengan akun valid          | Login berhasil.                                        |
| AT-02 | Pengguna memakai password salah        | Login ditolak.                                         |
| AT-03 | Kasir membuat pesanan baru             | Pesanan tersimpan dan nomor dibuat.                    |
| AT-04 | Pesanan menggunakan harga per kg       | Total dihitung benar.                                  |
| AT-05 | Pesanan memiliki beberapa layanan      | Total adalah jumlah seluruh item dan biaya tambahan.   |
| AT-06 | Harga layanan diubah                   | Pesanan lama tidak berubah.                            |
| AT-07 | Kasir membuat nota                     | Nota sesuai transaksi.                                 |
| AT-08 | Kasir membuka WhatsApp                 | Pesan siap kirim dengan informasi benar.               |
| AT-09 | Staf mengubah status                   | Riwayat status tersimpan.                              |
| AT-10 | Pelanggan membuka tracking valid       | Status pesanan terlihat.                               |
| AT-11 | Pelanggan memakai token salah          | Akses ditolak.                                         |
| AT-12 | Token tracking dicabut                 | Token lama tidak dapat digunakan.                      |
| AT-13 | Pelanggan mencoba melihat pesanan lain | Data tidak dapat diakses.                              |
| AT-14 | Pelanggan mengajukan pickup            | Permintaan masuk dashboard.                            |
| AT-15 | Admin mengonfirmasi pickup             | Status berubah sesuai.                                 |
| AT-16 | Kurir menyelesaikan penjemputan        | Riwayat tugas tercatat.                                |
| AT-17 | Pickup dikonversi menjadi order        | Hubungan data tidak hilang.                            |
| AT-18 | Kasir mencatat DP                      | Sisa tagihan benar.                                    |
| AT-19 | Kasir mencatat pelunasan               | Status pembayaran menjadi Lunas.                       |
| AT-20 | Input pembayaran melebihi tagihan      | Ditolak atau memerlukan alur koreksi yang sah.         |
| AT-21 | Kasir mencatat pengeluaran             | Laporan diperbarui.                                    |
| AT-22 | Staf mencoba mengubah harga            | Ditolak backend.                                       |
| AT-23 | Kurir mencoba membuka laporan keuangan | Akses ditolak.                                         |
| AT-24 | Pesanan dibatalkan                     | Status dan histori konsisten.                          |
| AT-25 | Dua petugas mengubah pesanan bersamaan | Sistem mencegah kehilangan pembaruan.                  |
| AT-26 | Tombol simpan diklik berulang          | Tidak muncul transaksi ganda.                          |
| AT-27 | Koneksi terputus saat menyimpan        | Pengguna memperoleh feedback dan data tetap konsisten. |
| AT-28 | Pengantaran gagal                      | Tugas dapat dijadwalkan ulang.                         |
| AT-29 | Pesanan melewati estimasi              | Ditandai terlambat.                                    |
| AT-30 | Backup dipulihkan pada lingkungan uji  | Data penting kembali konsisten.                        |

## 15.3 Syarat Kelulusan MVP

MVP hanya dinyatakan siap digunakan apabila:

1. Seluruh fitur P0 sudah diimplementasikan.
2. Seluruh acceptance test kritis lulus.
3. Tidak terdapat bug kritis pada pembayaran.
4. Tidak terdapat kebocoran data antar-pelanggan.
5. Tidak terdapat bypass hak akses yang diketahui.
6. Perubahan status dan pembayaran konsisten.
7. Pembuatan serta penyimpanan pesanan tidak menghasilkan duplikasi.
8. Antarmuka mobile telah diuji.
9. Backup dan proses restore berhasil diuji.
10. Owner atau perwakilan pengguna menyetujui hasil UAT.
11. Dokumentasi penggunaan dasar tersedia.

---

# 16. RISIKO DAN MITIGASI

| Risiko                               | Dampak                                     | Mitigasi                                                 |
| ------------------------------------ | ------------------------------------------ | -------------------------------------------------------- |
| Koneksi internet tidak stabil        | Transaksi tidak dapat disimpan sementara   | Feedback jaringan, retry aman, dan pencegahan duplikasi. |
| Kasir salah input berat              | Tagihan keliru                             | Validasi dan konfirmasi rincian.                         |
| Pembayaran tidak diverifikasi        | Status keuangan tidak sesuai               | Konfirmasi manual dan audit.                             |
| Tautan tracking tersebar             | Informasi pesanan dapat dilihat pihak lain | Token acak, pembatasan data, dan pencabutan token.       |
| Pesanan duplikat                     | Operasional dan laporan tidak akurat       | Idempotency dan kontrol transaksi.                       |
| Karyawan mengakses fitur terlarang   | Risiko perubahan data                      | RBAC pada backend.                                       |
| Data terhapus atau rusak             | Gangguan usaha                             | Backup dan restore berkala.                              |
| Kurir terlambat memperbarui status   | Pelanggan menerima informasi usang         | Tampilkan waktu pembaruan terakhir.                      |
| Terlalu banyak fitur pada versi awal | Pengembangan lambat                        | Prioritas P0 dan milestone bertahap.                     |
| Biaya hosting meningkat              | Beban operasional UMKM                     | Infrastruktur sederhana dan monitoring penggunaan.       |

---

# 17. ROADMAP PENGEMBANGAN

## Milestone M0 — Persiapan dan Analisis

Lingkup:

- Finalisasi PRD.
- Penyusunan Technical Requirements Document.
- Penyusunan Database Design Document.
- Perancangan arsitektur sistem.
- Perancangan user flow.
- Pembuatan wireframe dan UI design system.
- Penetapan standar coding dan testing.

**Exit Criteria:**

Seluruh dokumen dasar konsisten dan lingkup MVP disetujui.

## Milestone M1 — Fondasi Sistem

Lingkup:

- Setup frontend.
- Setup backend.
- Setup database.
- Migration.
- Authentication.
- Authorization.
- Profil usaha.
- Manajemen pengguna.
- Struktur layout aplikasi.

**Exit Criteria:**

Pengguna internal dapat login dan mengakses halaman sesuai perannya.

## Milestone M2 — Pesanan dan Pelanggan

Lingkup:

- Katalog layanan.
- Pengaturan harga.
- Manajemen pelanggan.
- Pembuatan pesanan.
- Rincian layanan.
- Perhitungan tagihan.
- Daftar dan detail pesanan.
- Riwayat status.
- Validasi bisnis.

**Exit Criteria:**

Pesanan laundry dapat dibuat, diproses, dan ditelusuri secara internal.

## Milestone M3 — Pembayaran dan Nota

Lingkup:

- Pembayaran manual.
- Pembayaran DP.
- Pelunasan.
- Piutang.
- Pengeluaran sederhana.
- Nota digital.
- PDF.
- Tautan WhatsApp.

**Exit Criteria:**

Proses transaksi dari pembuatan pesanan hingga pencatatan pembayaran dan penerbitan nota berjalan benar.

## Milestone M4 — Tracking Publik

Lingkup:

- Token tracking.
- Halaman pelanggan tanpa login.
- Timeline cucian.
- Estimasi selesai.
- Informasi tagihan.
- Pembatasan data publik.
- Keamanan token.

**Exit Criteria:**

Pelanggan dapat melihat status pesanannya secara aman tanpa akun.

## Milestone M5 — Antar-Jemput

Lingkup:

- Permintaan pickup publik.
- Konfirmasi jadwal.
- Penugasan kurir.
- Status penjemputan.
- Status pengantaran.
- Konfirmasi serah terima.
- Integrasi dengan tracking pesanan.

**Exit Criteria:**

Proses pickup sampai pengantaran dapat diselesaikan dengan pembaruan status manual.

## Milestone M6 — Dashboard dan Laporan

Lingkup:

- Ringkasan operasional.
- Ringkasan pembayaran.
- Data pengeluaran.
- Pesanan terlambat.
- Laporan berdasarkan tanggal.
- Ekspor CSV.

**Exit Criteria:**

Data dashboard dan laporan konsisten dengan transaksi tersimpan.

## Milestone M7 — Hardening dan UAT

Lingkup:

- Unit test.
- Integration test.
- E2E test.
- Security testing.
- Responsive testing.
- Performance baseline.
- Backup and restore.
- Perbaikan bug.
- Pengujian bersama pengguna.

**Exit Criteria:**

Seluruh kriteria kelulusan MVP terpenuhi.

## Milestone M8 — Deployment Produksi

Lingkup:

- Konfigurasi hosting.
- Konfigurasi HTTPS.
- Konfigurasi database produksi.
- Backup produksi.
- Logging dan monitoring.
- Dokumentasi pengguna.
- Pelatihan penggunaan dasar.
- Go-live checklist.

**Exit Criteria:**

Aplikasi dapat digunakan pada operasional laundry nyata dengan persetujuan Owner.

---

# 18. DEFINITION OF DONE

Sebuah fitur dinyatakan selesai apabila:

1. Memenuhi spesifikasi fungsional.
2. Mengikuti hak akses yang ditentukan.
3. Memiliki validasi backend.
4. Memiliki penanganan kesalahan.
5. Memiliki antarmuka responsif.
6. Memiliki state loading, success, dan error yang relevan.
7. Tidak merusak fungsi lain.
8. Memiliki pengujian sesuai tingkat risiko.
9. Dokumentasi API atau penggunaan diperbarui bila diperlukan.
10. Lulus code review.
11. Lulus pengujian integrasi.
12. Lulus acceptance criteria fitur.

Status pengembangan dibedakan menjadi:

- NOT_STARTED.
- IN_PROGRESS.
- IMPLEMENTED.
- TESTED.
- PASS.
- BLOCKED.

Fitur tidak boleh dinyatakan PASS hanya karena antarmukanya sudah dibuat.

---

# 19. ASUMSI DAN KEPUTUSAN YANG PERLU DIKONFIRMASI

## 19.1 Keputusan yang Telah Ditetapkan

1. Produk berbentuk web application.
2. Mendukung HP dan laptop.
3. Tidak mewajibkan alat kasir.
4. Tidak mewajibkan printer nota.
5. Pembayaran manual.
6. Tanpa payment gateway.
7. WhatsApp manual.
8. Pelanggan tidak wajib login.
9. Tracking cucian menggunakan tautan unik.
10. Tracking kurir berdasarkan pembaruan status manual.
11. Fitur dikembangkan secara bertahap berdasarkan prioritas MVP.

## 19.2 Asumsi Desain Awal

Asumsi berikut digunakan untuk menyusun PRD dan harus diverifikasi sebelum implementasi:

1. MVP digunakan untuk satu lokasi laundry.
2. Bahasa antarmuka adalah Bahasa Indonesia.
3. Mata uang utama adalah Rupiah.
4. Zona waktu operasional mengikuti zona waktu usaha yang dikonfigurasi.
5. Satu pesanan dapat berisi beberapa layanan.
6. Pelanggan dapat mengajukan pickup melalui formulir publik.
7. Owner dapat menangani fungsi kasir atau kurir jika belum memiliki pegawai.
8. Aplikasi membutuhkan koneksi internet selama operasional MVP.
9. Tarif dan durasi layanan ditentukan oleh pemilik usaha.
10. Hosting dan database dipilih berdasarkan kebutuhan serta anggaran.

## 19.3 Keputusan Terbuka

Hal yang perlu disepakati:

| ID     | Pertanyaan                                                    | Opsi Awal                                                           |
| ------ | ------------------------------------------------------------- | ------------------------------------------------------------------- |
| DEC-01 | Apakah layanan antar-jemput selalu tersedia?                  | Opsional dan dapat dinonaktifkan.                                   |
| DEC-02 | Apakah biaya antar-jemput tetap atau berdasarkan zona?        | Biaya tetap/manual untuk MVP.                                       |
| DEC-03 | Apakah pembayaran saat pengantaran diperbolehkan?             | Boleh, dicatat manual.                                              |
| DEC-04 | Apakah pesanan boleh diserahkan sebelum lunas?                | Boleh dengan peringatan dan pencatatan piutang.                     |
| DEC-05 | Berapa presisi berat cucian yang digunakan?                   | Dikonfigurasi sesuai praktik usaha.                                 |
| DEC-06 | Apakah diskon diperlukan sejak MVP?                           | Ditunda ke P1.                                                      |
| DEC-07 | Berapa lama data pesanan dan token disimpan?                  | Ditentukan melalui kebijakan retensi.                               |
| DEC-08 | Bagaimana prosedur refund atau pembatalan setelah pembayaran? | Perlu aturan operasional yang disetujui Owner.                      |
| DEC-09 | Apakah kurir memerlukan akun tersendiri?                      | Ya bila ada petugas khusus; Owner/Admin dapat menangani jika tidak. |
| DEC-10 | Apakah akan dikembangkan menjadi SaaS?                        | Tidak termasuk MVP; dipertimbangkan kemudian.                       |

Keputusan terbuka tidak boleh dianggap sebagai persetujuan final.

---

# 20. DOKUMEN TURUNAN

Setelah PRD disetujui, pengembangan dilanjutkan dengan dokumen berikut.

| Dokumen                                | Tujuan                                                                       |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| TRD — Technical Requirements Document | Menjabarkan kebutuhan teknis, stack, API, dan batasan implementasi.          |
| AFD — Architecture & Flow Design      | Mendefinisikan arsitektur, alur pengguna, dan komunikasi komponen.           |
| DBD — Database Design Document        | Mendefinisikan struktur tabel, relasi, indeks, migrasi, dan integritas data. |
| UI/UX Design Specification             | Mendefinisikan halaman, komponen, interaksi, status, dan responsivitas.      |
| API Contract                           | Menentukan endpoint, request, response, validasi, dan kode kesalahan.        |
| Test Plan & Acceptance Matrix          | Memetakan kebutuhan ke pengujian dan kriteria kelulusan.                     |
| Deployment & Operations Guide          | Menjelaskan konfigurasi produksi, backup, monitoring, dan pemulihan.         |

Setiap dokumen turunan harus konsisten dengan persyaratan dan keputusan yang telah disetujui dalam PRD.

---

# 21. KESIMPULAN

Web App Manajemen Laundry UMKM merupakan solusi digitalisasi operasional laundry yang dirancang dengan pendekatan sederhana, hemat biaya, dan berorientasi pada kebutuhan usaha kecil.

Sistem mencakup delapan modul utama:

1. Dashboard.
2. Manajemen Pesanan.
3. Manajemen Pelanggan.
4. Antar-Jemput.
5. Keuangan.
6. Nota Digital.
7. Tracking Cucian.
8. Pengaturan.

Keunggulan produk adalah kemampuan mengelola proses usaha menggunakan perangkat HP atau laptop yang telah dimiliki, tanpa mengharuskan pembelian perangkat POS, printer nota, atau integrasi payment gateway.

Pelanggan dapat memantau cucian dan antar-jemput melalui tautan tracking tanpa membuat akun, sementara seluruh perubahan operasional dan pembayaran dikelola oleh petugas yang memiliki kewenangan.

Pengembangan dilaksanakan melalui milestone terukur, mulai dari fondasi sistem, transaksi, tracking, antar-jemput, hingga pengujian dan deployment produksi.

**PRD v1.0 ini merupakan baseline kebutuhan produk untuk proses review. Setelah keputusan terbuka diselesaikan dan disetujui, dokumen dapat ditetapkan sebagai PRD v1.0 Approved dan digunakan sebagai acuan implementasi frontend, backend, database, serta pengujian.**

---

**AKHIR DOKUMEN — PRODUCT REQUIREMENTS DOCUMENT v1.0**
