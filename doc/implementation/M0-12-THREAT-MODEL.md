# M0-12: Initial Security Threat Model (STRIDE) — E-Laundry 2.0

Dokumen ini memetakan evaluasi ancaman keamanan awal (*threat modeling*) menggunakan metodologi **STRIDE** untuk melindungi batas kepercayaan (*trust boundaries*) sistem E-Laundry 2.0.

---

## 1. Trust Boundaries & Data Flow

```
[ Publik / Pelanggan ]           [ Staff / Kasir / Kurir / Owner ]
         │                                       │
         ▼ (Public Tracking / Pickup)            ▼ (Staff Portal)
════════════════════════════════════════════════════════════════════════════ Trust Boundary 1
[ Frontend Client (React 19 / Browser) ]
         │
         ▼ (REST API / HTTPS / Secure Cookie / CSRF)
════════════════════════════════════════════════════════════════════════════ Trust Boundary 2
[ Reverse Proxy / Security Headers / RequestId Middleware / CORS ]
         │
         ▼ (ASGI Dispatch)
[ FastAPI Backend (Modular Monolith) ]
         │
         ▼ (Sync Connection Pool / Parameterized SQL)
════════════════════════════════════════════════════════════════════════════ Trust Boundary 3
[ PostgreSQL Database 17 ]
```

---

## 2. STRIDE Threat Assessment & Mitigasi

| Kategori Ancaman | Deskripsi Skenario Risiko | Mitigasi yang Diterapkan di M0 & M1 | Status Mitigasi |
| :--- | :--- | :--- | :---: |
| **Spoofing (Pemalsuan Identitas)** | Penyerang memalsukan identitas staf atau mencuri cookie sesi. | Autentikasi menggunakan server-side session token yang di-hash dengan SHA-256 (`session_token_hash`). Cookie menggunakan flag `HttpOnly`, `SameSite=Lax/Strict`, dan `Secure`. Password di-hash menggunakan Argon2id. | **CONFIGURED & READY FOR M1** |
| **Tampering (Manipulasi Data)** | Penyerang memanipulasi payload harga, berat pesanan, atau parameter transaksi. | Validasi skema ketat menggunakan Pydantic v2. Seluruh perhitungan harga dilakukan di backend (DEC-01, DEC-02). Data mutasi uang menggunakan tipe `Decimal`, bukan `float`. | **CONFIGURED (M0 Foundation)** |
| **Repudiation (Penyangkalan Tindakan)** | Pengguna menyangkal telah mengubah status cucian atau membatalkan pembayaran. | Tabel `order_status_history` dan penandaan `is_void` pada pembayaran mencatat `user_id`, `timestamp`, dan `reason`. Setiap log request mencatat `request_id`. | **FOUNDATION READY** |
| **Information Disclosure (Kebocoran Data)** | Stack trace SQL mentah terekspos ke client atau nomor HP pelanggan bocor via tracking link. | Exception handler global menyaring `SQLAlchemyError` dan error internal agar tidak membocorkan detail database. Public tracking (M4) menggunakan restricted schema tanpa nomor telepon lengkap atau alamat sensitif. | **VERIFIED (M0 Error Handlers)** |
| **Denial of Service (Penyalahgunaan Sumber Daya)** | Serangan brute-force pada login atau spam request tracking tanpa batas. | Implementasi security headers (`nosniff`, `DENY`), connection pool limits (10 connections, max overflow 20), dan persiapan middleware rate limiter (`RATE_LIMITED` 429). | **VERIFIED (M0 Middlewares)** |
| **Elevation of Privilege (Eskalasi Hak Akses)** | Kurir atau Kasir mengakses menu laporan omset atau konfigurasi bisnis milik Owner. | Penegakan Role-Based Access Control (RBAC) pada setiap endpoint backend (Router $\rightarrow$ Permission Dependency), tidak mengandalkan penyembunyian tombol di frontend semata. | **PLANNED FOR M1** |

---

## 3. Kebijakan Kemanan Baseline (M0)
1. **Zero Secret in VCS:** File `.env` diabaikan oleh `.gitignore`.
2. **Security Headers:** Header `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, dan `Referrer-Policy: strict-origin-when-cross-origin` otomatis dipasang pada setiap response HTTP.
3. **Traceability:** Header `X-Request-ID` dihasilkan secara unik (UUID v4) atau dipropagasi untuk setiap request masuk.

**Kesimpulan Evaluasi:** **PASS — PONDASI KEAMANAN TERVERIFIKASI**.

