# Katalog Lengkap AI Agent Skills

Dokumen ini merangkum seluruh **19 Skills** yang terpasang pada repository **E-laundry 2.0** berdasarkan manifest `skills-lock.json` dan direktori `.agents/skills/`.

---

## Tabel Katalog Skills

| No | Nama Skill | Sumber & Tipe | Kategori | Fungsi Utama | Kapan Digunakan | Dependency Tambahan | Agent Compatibility | Cara Pemanggilan / Penggunaan |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `antislop` | `miqdadbadjuber/anti-slop`<br>(GitHub) | UI/UX dan Frontend | Filter inti anti-AI slop: menolak visual tanpa tujuan, memaksakan liveliness, WCAG AA, dan functional honesty. | Selalu aktif saat membuat atau mereview UI web/aplikasi. | Tidak ada (opsional settings mode di `%APPDATA%\antislop\settings.json`). | Antigravity, Claude Code, Codex, Cursor, OpenCode | Auto-loaded; pemilihan mode `during` (saat membuat) atau `after` (audit). |
| **2** | `antislop-code` | `miqdadbadjuber/anti-slop`<br>(GitHub) | UI/UX dan Frontend | Membersihkan komentar kode bergaya AI slop (banner dekoratif, restating obvious, narasi alur) tanpa mengubah kode eksekutabel. | Saat menulis atau mengedit komentar dalam kode sumber. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded bersama `antislop`. |
| **3** | `antislop-copywriting` | `miqdadbadjuber/anti-slop`<br>(GitHub) | UI/UX dan Frontend | Standar copywriting alami & manusiawi: eliminasi em dash (`—`), klaim fiktif, buzzwords kosong, dan signposting. | Saat menulis teks tombol (CTA), landing page, label antarmuka, atau panduan pengguna. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded saat penulisan teks UI / copy. |
| **4** | `antislop-layoutmobile` | `miqdadbadjuber/anti-slop`<br>(GitHub) | UI/UX dan Frontend | Standar tata letak responsif kontinu: reflow kolom, batas sentuh (min 44x44px), cegah horizontal overflow, safe-area insets. | Saat menyusun CSS, media query, grid, flexbox, dan tampilan layar ponsel hingga desktop. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded pada pekerjaan tata letak UI. |
| **5** | `antislop-ui` | `miqdadbadjuber/anti-slop`<br>(GitHub) | UI/UX dan Frontend | Aturan teknis antarmuka visual: batasan glassmorphism, glow, shadow, palet warna berhierarki, state dashboard (empty, loading, error). | Saat membuat komponen visual, dashboard admin, card, formulir, atau animasi. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded pada pekerjaan desain frontend. |
| **6** | `ui-taste` | `uizze.sh`<br>(Well-Known) | UI/UX dan Frontend | Playbook perancangan UI web & iOS berkualitas tinggi: visual hierarchy polish, image-to-UI workflow, dan native verification. | Desain antarmuka baru, visual redesign, polish detail, atau audit visual web. | Opsional Uizze MCP (berbayar) untuk referensi produk nyata. Fitur inti markdown gratis. | Antigravity, Claude Code, Codex, Cursor | Mengakses playbook terkait (`reference/polish.md`, `/overdrive`, dsb.). |
| **7** | `ios-design` | `uizze.sh`<br>(Well-Known) | UI/UX dan Frontend | Standar desain iOS native (SwiftUI, UIKit, React Native) sesuai Apple Human Interface Guidelines, Dynamic Type, dan safe areas. | Saat membangun aplikasi iOS, form mobile, gestur navigasi, atau audit antarmuka iOS. | Opsional Uizze MCP (berbayar). | Antigravity, Claude Code, Codex, Cursor | Auto-loaded saat menangani UI iOS / mobile framework. |
| **8** | `design-mobile-apps` | `designed-by-ai/skills`<br>(GitHub) | UI/UX dan Frontend | Menghasilkan desain antarmuka mobile melalui Sleek REST API dan mengonversinya ke React Native atau HTML. | Pembuatan prototipe cepat screen mobile berbasis spesifikasi brief. | **Memerlukan `SLEEK_API_KEY`** (atau device flow poll). | Antigravity, Claude Code, Codex | Mengirim request chat/render ke endpoint Sleek API (`https://sleek.design`). |
| **9** | `fastapi` | `fastapi/fastapi`<br>(GitHub) | Backend Engineering | Panduan dan best practices resmi FastAPI: penggunaan `Annotated`, Pydantic models, non-blocking async, SSE streaming, OpenTelemetry, dan router conventions. | Saat merancang arsitektur backend, API endpoint, routing, skema Pydantic, atau dependency injection. | Python, dependensi `fastapi`, `pydantic`. | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded saat menangani kode backend Python/FastAPI. |
| **10** | `improve-codebase-architecture` | `mattpocock/skills`<br>(GitHub) | Software Architecture dan Testing | Memindai arsitektur kode untuk menemukan "shallow modules", mengusulkan deepening boundaries (seams), dan menyajikan laporan visual HTML. | Evaluasi struktural arsitektur, refaktorisasi sistemik, atau pembagian modul besar. | Browser untuk membuka HTML report (CDN Tailwind & Mermaid). | Antigravity (manual/subagent), Claude Code, OpenCode | Dipanggil manual oleh user/sub-agent karena flag `disable-model-invocation: true`. |
| **11** | `tdd` | `mattpocock/skills`<br>(GitHub) | Software Architecture dan Testing | Test-Driven Development siklus Red $\rightarrow$ Green $\rightarrow$ Refactor, pengujian pada public seams, vertical slicing tanpa mock berlebihan. | Saat implementasi fitur baru atau perbaikan bug dengan pendekatan test-first. | Test runner proyek (pytest, vitest, dsb.). | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded saat instruksi mencakup pembuatan tes / TDD. |
| **12** | `security-audit` | `cloudflare/security-audit-skill`<br>(GitHub) | Security Engineering | Kerangka audit keamanan komprehensif: verifikasi batas kepercayaan (trust boundary), sandbox isolasi lokal, 6 fase audit, dan ledger temuan. | Saat audit keamanan menyeluruh, evaluasi kerentanan endpoint, atau review izin data sensitif. | Node.js (untuk menjalankan script validasi `validate-findings.cjs`). | Antigravity, Claude Code, Codex, OpenCode | Auto-loaded; Guidance mode (tanya jawab) atau Full audit mode (permintaan eksplisit). |
| **13** | `ponytail` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Filosofi lazy senior dev: solusi terkecil yang menyelesaikan masalah secara utuh (YAGNI, minimal diff, no bloat). | Mode utama pengerjaan kode umum, bugfix, refactoring, pemilihan dependensi. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Aktif secara default atau via `/ponytail [lite\|full\|ultra]`, `$ponytail:ponytail`. |
| **14** | `ponytail-audit` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Audit menyeluruh repository: deteksi bug, lubang keamanan, beban skala, tes yang hilang, bottleneck kecepatan, dan kode mati/bloat. | Audit kualitas repo satu kali tembak ("audit this codebase", "find bloat"). | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/ponytail-audit` atau `$ponytail:ponytail-audit`. |
| **15** | `ponytail-debt` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Mendata seluruh komentar penundaan `shortcut:` ke dalam buku besar technical debt (ceiling limit & upgrade trigger). | Pelacakan dan audit utang teknis ("what did ponytail defer", "list shortcuts"). | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/ponytail-debt` atau `$ponytail:ponytail-debt`. |
| **16** | `ponytail-gain` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Menampilkan papan skor benchmark penghematan baris kode, token output, biaya, dan waktu dari penggunaan Ponytail. | Melihat referensi efisiensi ponytail. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/ponytail-gain` atau `$ponytail:ponytail-gain`. |
| **17** | `ponytail-help` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Kartu referensi cepat untuk level ponytail, daftar perintah, dan opsi konfigurasi. | Bantuan penggunaan suite ponytail. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/ponytail-help` atau `$ponytail:ponytail-help`. |
| **18** | `ponytail-review` | `dietrichgebert/ponytail`<br>(GitHub) | Code Quality dan Maintenance | Review kualitas diff/commit: ketepatan logika, keamanan data, keandalan di bawah beban, tes yang relevan, dan efisiensi baris kode. | Review kode sebelum commit, pembuatan pull request, atau verifikasi perubahan. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/ponytail-review`, "review this", atau "review my PR". |
| **19** | `caveman` | `juliusbrussee/caveman`<br>(GitHub) | AI Communication | Gaya komunikasi super ringkas tanpa basa-basi (*all fluff dies, all facts stay*). Menghemat token dan waktu baca. | Hanya jika user secara eksplisit meminta penghematan token atau jawaban singkat. | Tidak ada | Antigravity, Claude Code, Codex, OpenCode | Dipanggil via `/caveman`, "caveman mode"; dimatikan via "stop caveman". |

---

## Pemetaan Penggunaan Berdasarkan Jenis Pekerjaan (Task Mapping)

Untuk menghindari kelebihan konteks atau benturan instruksi (*prompt clutter*), ikuti panduan pemilihan skill sesuai domain tugas:

```
[Jenis Pekerjaan]                     [Skill Utama yang Diaktifkan]
│
├── Frontend Development  ───────►  antislop, antislop-ui, antislop-layoutmobile, ui-taste
├── Copywriting & Labels  ───────►  antislop-copywriting, antislop-code
├── Mobile UI (iOS/React) ───────►  ios-design, antislop-layoutmobile (opsional: design-mobile-apps)
├── Backend Development   ───────►  fastapi
├── Database Engineering  ───────►  fastapi (SQLModel/Pydantic patterns), ponytail (lean schema)
├── Software Architecture ───────►  improve-codebase-architecture, ponytail
├── Testing & QA          ───────►  tdd, ponytail-review
├── Security Audit        ───────►  security-audit
├── Code Review & Clean   ───────►  ponytail-review, ponytail-audit, ponytail-debt
└── Terse Communication   ───────►  caveman (hanya atas permintaan user)
```

