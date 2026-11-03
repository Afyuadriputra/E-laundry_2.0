
# TASK: AI AGENT ENVIRONMENT SETUP & CODEGRAPH INTEGRATION

Bertindaklah sebagai Senior AI Engineering Infrastructure Engineer dan Software Architect.

Saya ingin kamu memahami dan menyiapkan lingkungan AI Coding Agent pada repository ini sebelum pengembangan frontend dan backend dimulai.

**Root project:**
`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

## 1. TUJUAN UTAMA

Lakukan audit dan konfigurasi terhadap:

1. AI Agent Skills.
2. Skills Management dan skills-lock.json.
3. CodeGraph Knowledge Graph.
4. Model Context Protocol (MCP).
5. Integrasi Antigravity.
6. Integrasi Codex dan agent lainnya.
7. Instruksi global dan project-level AI Agent.

Targetnya adalah membuat lingkungan pengembangan yang konsisten sehingga Antigravity, Codex, Claude Code, Gemini CLI, dan OpenCode dapat menggunakan konfigurasi dan skills proyek yang relevan.

Jangan membangun aplikasi frontend atau backend terlebih dahulu.

## 2. AUDIT STRUKTUR PROJECT

Periksa seluruh struktur repository, khususnya:

- `.agents/`
- `.agents/skills/`
- `.claude/`
- `.codex/`
- `.gemini/`
- `.vscode/`
- `.codegraph/`
- `backend/`
- `frontend/`
- `doc/`
- `.mcp.json`
- `opencode.jsonc`
- `AGENTS.md`
- `GEMINI.md`
- `skills-lock.json`
- `.gitignore`

Identifikasi fungsi setiap konfigurasi dan hubungan antaragent.

Periksa juga apakah ada konfigurasi duplikat, konflik, instruksi yang bertentangan, atau konfigurasi yang belum lengkap.

Jangan menghapus atau mengganti konfigurasi yang sudah berjalan tanpa alasan teknis yang jelas.

## 3. AUDIT DAN SETUP SELURUH SKILLS

Baca dan pahami `skills-lock.json`.

Ada 19 skills yang harus diperiksa:

### A. UI/UX dan Frontend

- antislop
- antislop-code
- antislop-copywriting
- antislop-layoutmobile
- antislop-ui
- ui-taste
- ios-design
- design-mobile-apps

### B. Backend Engineering

- fastapi

### C. Software Architecture dan Testing

- improve-codebase-architecture
- tdd

### D. Security Engineering

- security-audit

### E. Code Quality dan Maintenance

- ponytail
- ponytail-audit
- ponytail-debt
- ponytail-gain
- ponytail-help
- ponytail-review

### F. AI Communication

- caveman

Untuk setiap skill:

1. Baca file `SKILL.md` secara lengkap.
2. Periksa file referensi pendukung.
3. Pahami tujuan dan kondisi kapan skill digunakan.
4. Identifikasi dependency eksternal, API key, atau konfigurasi tambahan.
5. Periksa apakah skill memiliki script yang perlu dijalankan.
6. Identifikasi potensi konflik dengan skill lainnya.
7. Pastikan skill ditemukan melalui mekanisme discovery yang didukung Antigravity.
8. Jangan mengubah isi skill pihak ketiga tanpa kebutuhan yang jelas.

Gunakan `skills-lock.json` sebagai manifest sumber dan versi skill.

Jangan mengunduh ulang atau menggandakan skills yang sudah tersedia.

Jangan menjalankan script dari skill pihak ketiga secara otomatis sebelum memahami fungsinya dan risikonya.

### Tujuan integrasi Skills

Pastikan setiap agent dapat mengetahui skills yang tersedia dan menggunakan skill yang relevan ketika mengerjakan tugas.

Pahami bahwa tidak semua skills harus dijalankan bersamaan.

Buat pemetaan penggunaan skills berdasarkan jenis pekerjaan:

- Frontend development.
- Backend development.
- Database engineering.
- UI/UX design.
- Software architecture.
- Testing.
- Security audit.
- Code review.
- Refactoring.
- Maintenance.

Jangan mengklaim skill aktif hanya karena file SKILL.md tersedia. Verifikasi bahwa Antigravity benar-benar dapat menemukannya dan mengikuti instruksinya.

## 4. SETUP CODEGRAPH

CodeGraph sudah diinstal menggunakan CLI versi 1.6.2.

Periksa terlebih dahulu:

```powershell
codegraph version
codegraph status
```

Pelajari konfigurasi yang tersedia dan dokumentasi resmi CodeGraph:

https://github.com/colbymchenry/codegraph

Lakukan pemeriksaan terhadap:

- Instalasi CLI.
- Konfigurasi MCP.
- Database Knowledge Graph.
- Konfigurasi project-local.
- Sinkronisasi perubahan file.
- Integrasi dengan Antigravity.

Jika indeks proyek belum dibuat atau belum aktif, lakukan inisialisasi menggunakan perintah resmi yang sesuai:

```powershell
codegraph init
```

Jangan membuat database baru jika database yang benar sudah tersedia.

Periksa hasilnya menggunakan:

```powershell
codegraph status
```

### Integrasi Antigravity

Antigravity sebelumnya terdeteksi oleh installer CodeGraph sebagai:

`Antigravity IDE (detected) — global only`

Antigravity menggunakan konfigurasi global, sedangkan CodeGraph Knowledge Graph tetap berada pada root project.

Pastikan:

1. Integrasi MCP CodeGraph untuk Antigravity sudah aktif.
2. Konfigurasi global Antigravity tidak merusak MCP server lain.
3. MCP dapat mengakses proyek yang sedang dibuka.
4. Antigravity dapat menggunakan tool `codegraph_explore` jika tersedia.
5. Tidak ada konfigurasi MCP ganda atau konflik.
6. Konfigurasi Codex dan agent lain yang sudah terpasang tetap dipertahankan.

Jika integrasi Antigravity belum terpasang, gunakan mekanisme instalasi resmi CodeGraph dan hanya konfigurasi Antigravity. Jangan menginstal ulang seluruh agent.

## 5. VERIFIKASI CODEGRAPH

Setelah integrasi aktif, lakukan pengujian nyata.

Uji apakah CodeGraph dapat:

1. Mengakses Knowledge Graph proyek.
2. Menemukan file dan simbol.
3. Menelusuri relasi fungsi.
4. Menelusuri dependency.
5. Melakukan eksplorasi struktur proyek.
6. Memberikan hasil query yang relevan.

Gunakan `codegraph_explore` melalui MCP jika tersedia.

Jika frontend dan backend belum berisi kode, jangan mengarang hasil analisis. Verifikasi saja bahwa indeks dan integrasinya siap digunakan.

## 6. KELOLA INSTRUKSI AI AGENT

Audit `AGENTS.md`, `GEMINI.md`, `.claude/CLAUDE.md`, dan konfigurasi agent lainnya.

Pastikan instruksinya:

- Tidak saling bertentangan.
- Memiliki aturan keamanan.
- Memiliki aturan coding.
- Memiliki aturan testing.
- Memiliki standar arsitektur.
- Memiliki panduan penggunaan Skills.
- Memiliki panduan penggunaan CodeGraph.
- Tidak mengandung konfigurasi rahasia.

Jadikan `AGENTS.md` sebagai instruksi utama proyek yang dapat digunakan oleh agent yang mendukung format tersebut.

Instruksi harus mengarahkan AI untuk:

- Memahami arsitektur sebelum mengubah kode.
- Menggunakan CodeGraph ketika melakukan eksplorasi struktur dan relasi kode.
- Memilih skills sesuai kebutuhan.
- Tidak melakukan overengineering.
- Mempertahankan konsistensi coding style.
- Melakukan testing setelah perubahan.
- Melakukan security review untuk perubahan sensitif.
- Tidak mengubah bagian yang tidak relevan dengan tugas.

Jangan mengganti instruksi yang sudah baik hanya untuk membuat format baru.

## 7. KEAMANAN DAN GIT

Periksa `.gitignore`.

Pastikan:

- `.codegraph/` tidak masuk Git.
- `.env` tidak masuk Git.
- API key dan credentials tidak masuk Git.
- Cache dan dependency tidak masuk Git.
- File skills dan dokumentasi yang memang dibagikan tetap dapat di-commit.
- Konfigurasi agent yang aman dapat digunakan bersama oleh tim.

Jangan melakukan:

- `git reset --hard`.
- `git clean -fd`.
- Penghapusan file konfigurasi.
- Force push.
- Commit otomatis.
- Push otomatis.

Jangan mengubah remote repository atau branch.

## 8. BATASAN PEKERJAAN

PENTING:

Frontend dan backend belum disiapkan.

Untuk tahap ini:

- Jangan membuat aplikasi frontend.
- Jangan membuat aplikasi backend.
- Jangan menginstal dependency aplikasi.
- Jangan membuat database PostgreSQL.
- Jangan membuat tabel atau migration.
- Jangan membuat API.
- Jangan membuat komponen UI.
- Jangan mengubah requirement produk.

Fokus hanya pada infrastruktur AI Agent, Skills, MCP, CodeGraph, dan dokumentasi konfigurasi.

Jika ada konfigurasi yang tidak dapat diselesaikan karena keterbatasan akses, jelaskan secara transparan.

## 9. DOKUMENTASI HASIL

Buat dokumentasi di dalam folder `doc/`.

Dokumen yang perlu dibuat:

### A. `doc/AI-AGENT-SETUP.md`

Berisi:

- Arsitektur AI Agent.
- Daftar agent yang terintegrasi.
- Lokasi konfigurasi.
- Mekanisme penggunaan skills.
- Aturan instruksi agent.
- Cara menambahkan agent baru.

### B. `doc/CODEGRAPH-GUIDE.md`

Berisi:

- Arsitektur CodeGraph.
- Cara kerja Knowledge Graph.
- Instalasi dan inisialisasi.
- Integrasi MCP.
- Cara menggunakan CodeGraph melalui Antigravity dan Codex.
- Perintah CLI.
- Cara verifikasi dan troubleshooting.
- Ketentuan indeks lokal dan Git.

### C. `doc/SKILLS-CATALOG.md`

Berisi tabel:

- Nama skill.
- Sumber.
- Fungsi.
- Kategori.
- Kapan digunakan.
- Dependency tambahan.
- Agent compatibility.
- Cara pemanggilan atau penggunaannya.

Pastikan dokumentasi berdasarkan konfigurasi aktual, bukan asumsi.

## 10. LAPORAN AKHIR

Setelah pekerjaan selesai, berikan laporan:

1. Kondisi awal repository.
2. Skills yang berhasil diverifikasi.
3. Skills yang belum kompatibel atau membutuhkan konfigurasi tambahan.
4. Status CodeGraph.
5. Status MCP Antigravity.
6. Status integrasi agent lainnya.
7. File konfigurasi yang dibuat atau diperbarui.
8. Dokumentasi yang dihasilkan.
9. Masalah yang ditemukan.
10. Rekomendasi langkah berikutnya sebelum mulai membangun frontend dan backend.

Gunakan status:

- VERIFIED: berhasil diuji.
- CONFIGURED: konfigurasi sudah dibuat tetapi belum diuji.
- NEEDS ATTENTION: membutuhkan tindakan.
- NOT AVAILABLE: belum didukung atau tidak tersedia.

**PRINSIP UTAMA:**

Jangan sekadar mengatakan semua sudah terpasang. Lakukan pemeriksaan nyata, validasi konfigurasi, dan pengujian integrasi.

Utamakan kestabilan konfigurasi, keamanan, kompatibilitas antaragent, dan kemudahan pemeliharaan.

Mulai dengan audit repository terlebih dahulu, kemudian lanjutkan konfigurasi dan verifikasi secara bertahap.
