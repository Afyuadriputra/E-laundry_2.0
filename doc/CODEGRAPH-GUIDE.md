# Panduan Lengkap CodeGraph Knowledge Graph

Dokumen ini menjelaskan arsitektur, cara kerja, integrasi MCP, perintah CLI, serta tata kelola Git untuk **CodeGraph** pada proyek **E-laundry 2.0**.

---

## 1. Arsitektur CodeGraph

**CodeGraph** adalah semantic code knowledge graph engine berkecepatan tinggi yang memetakan relasi kode, simbol, pemanggilan fungsi, dependensi, dan hirarki file ke dalam database relasional graf berbasis SQLite.

```
+-------------------------------------------------------------------------------+
|                             SOURCE CODEBASE REPO                              |
|   (Python, JavaScript, TypeScript, HTML, CSS, YAML, Markdown, JSON, etc.)     |
+-------------------------------------------------------------------------------+
                                        |
                                        v  [Tree-Sitter AST & Semantic Parsers]
+-------------------------------------------------------------------------------+
|                            CODEGRAPH ENGINE (v1.6.2)                          |
|                                                                               |
|  - Ingestion: Ekstraksi AST, nodes (functions, classes, constants, imports)  |
|  - Edges    : Resolusi pemanggilan (calls), relasi dependensi, type links     |
|  - Storage  : SQLite Embedded Engine (.codegraph/codegraph.db)                |
|  - Mode     : WAL (Write-Ahead Logging) & Full WAL Synchronization            |
+-------------------------------------------------------------------------------+
                                        |
                 +----------------------+----------------------+
                 |                                             |
                 v [STDIO MCP Protocol]                        v [Terminal CLI]
+----------------------------------+          +----------------------------------+
|           MCP SERVERS            |          |           COMMAND LINE           |
|                                  |          |                                  |
| - codegraph serve --mcp          |          | - codegraph status               |
| - Tool: codegraph_explore        |          | - codegraph explore "<query>"    |
| - Clients: Antigravity, Claude,  |          | - codegraph sync                 |
|   Codex, Gemini, VS Code         |          | - codegraph search "<term>"      |
+----------------------------------+          +----------------------------------+
```

### Karakteristik Utama:
- **Index Storage:** Tersimpan secara lokal di folder `.codegraph/`.
- **Database Engine:** `node:sqlite` built-in dengan journal mode `wal` (Write-Ahead Logging).
- **Blast Radius Analysis:** Mampu menelusuri dampak perubahan kode (*call paths*) yang tidak dapat dilacak oleh pencarian berbasis teks biasa (`grep`).
- **Verbatim Source Snippets:** Tool MCP mengembalikan source code berbaris aktual langsung dari disk tanpa perlu membuka file berulang kali.

---

## 2. Status Indeks Saat Ini

Hasil verifikasi aktual pada repository:

```text
CodeGraph Status

Project: D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek

Index Statistics:
  Files:     10
  Nodes:     175
  Edges:     927
  DB Size:   1.45 MB
  WAL Size:  0.01 MB
  Backend:   node:sqlite - built-in (full WAL)
  Journal:   wal

Nodes by Kind:
  function        98
  constant        59
  import          8
  file            6
  class           4

Files by Language:
  javascript      6
  yaml            4

[OK] Index is up to date
```

---

## 3. Instalasi dan Inisialisasi

CodeGraph telah terpasang secara global pada environment sistem dengan versi `1.6.2`.

### Memeriksa Versi:
```powershell
codegraph version
# Output: 1.6.2
```

### Inisialisasi Project Baru (Jika Belum Terindeks):
```powershell
codegraph init
```
*Catatan:* Karena database `.codegraph/codegraph.db` sudah aktif dan terverifikasi pada repository ini, inisialisasi ulang **tidak diperlukan**.

### Melakukan Sinkronisasi Perubahan Kode:
Setiap kali ada file baru yang ditambahkan atau diubah secara signifikan, perbarui indeks dengan:
```powershell
codegraph sync
```

---

## 4. Integrasi Model Context Protocol (MCP)

CodeGraph mendukung protokol MCP melalui transportasi `stdio`.

### 1. Integrasi Antigravity
Antigravity mendeteksi CodeGraph secara global pada:
- Direktori schema: `%APPDATA%\antigravity\mcp\codegraph\`
- Tool schema: `codegraph_explore.json`
- Tool instructions: `instructions.md`

Parameter pemanggilan tool `codegraph_explore`:
- `query` *(string, required)*: Simbol, fungsi, atau pertanyaan arsitektural (contoh: `"validate-findings"`).
- `projectPath` *(string, required)*: Path absolut repository (`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`).
- `maxFiles` *(number, optional)*: Maksimum file yang dimuat dalam satu pemanggilan (default: 12).

### 2. Integrasi Codex, Claude Code, Gemini CLI, OpenCode, dan VS Code
Konfigurasi file client:
- **VS Code:** `.vscode/mcp.json`
- **Claude Code:** `.claude/settings.json` (termasuk permission `mcp__codegraph__*` dan hook `codegraph.cmd prompt-hook`)
- **Codex:** `.codex/config.toml`
- **Gemini CLI:** `.gemini/settings.json`
- **OpenCode:** `opencode.jsonc`

---

## 5. Cara Penggunaan CodeGraph

### A. Melalui Antigravity (MCP Tool)
AI Agent memanggil lazy tool `codegraph_explore` menggunakan MCP:
```json
{
  "ServerName": "codegraph",
  "ToolName": "codegraph_explore",
  "Arguments": {
    "query": "validate-findings",
    "projectPath": "D:\\Kuliah\\joki\\Kerja Praktek Aqil\\kawan aqil\\projek"
  }
}
```
Hasil pemanggilan mengembalikan line-numbered verbatim source code dan rantai pemanggilan fungsi (call path) yang relevan dalam satu kali round-trip.

### B. Melalui Codex dan Agent Lainnya
Pada terminal agent Codex atau Claude Code:
```bash
codegraph explore "<simbol atau pertanyaan>"
```

### C. Melalui Terminal / CLI
1. **Eksplorasi Simbol & Relasi:**
   ```powershell
   codegraph explore "createErrorList"
   ```
2. **Pencarian Cepat Simbol:**
   ```powershell
   codegraph search "validate"
   ```
3. **Cek Status Database Indeks:**
   ```powershell
   codegraph status
   ```
4. **Sinkronisasi Indeks Setelah Perubahan Kode:**
   ```powershell
   codegraph sync
   ```

---

## 6. Verifikasi & Troubleshooting

| Gejala Masalah | Penyebab | Solusi |
| :--- | :--- | :--- |
| `Pending Changes: Added X files` | Ada file baru belum dimasukkan ke Knowledge Graph | Jalankan `codegraph sync` |
| MCP tool error: `required: projectPath` | Parameter `projectPath` tidak disertakan pada tool call Antigravity | Sertakan `projectPath` absolut workspace pada argumen tool call |
| Index terkunci (*database locked*) | Proses daemon background lain sedang menulis ke WAL | Hentikan proses zombie dengan PowerShell atau tunggu proses selesai |
| Indeks korup atau tidak valid | Penghentian paksa saat penulisan database | Jalankan `codegraph init` ulang secara terkontrol |

---

## 7. Ketentuan Indeks Lokal dan Git

### Keamanan Git:
- Folder `.codegraph/` berisi file binary database lokal (`codegraph.db`, `codegraph.db-wal`, `codegraph.db-shm`) yang unik untuk setiap mesin developer.
- **Wajib diabaikan dari Git:**
  1. Pada `.gitignore` root telah didefinisikan:
     ```gitignore
     .codegraph/
     *.db-wal
     *.db-shm
     ```
  2. Di dalam direktori `.codegraph/` terdapat file `.codegraph/.gitignore`:
     ```gitignore
     *
     !.gitignore
     ```
- Hal ini menjamin bahwa database lokal tidak akan ter-commit ke remote repository, menjaga repo tetap bersih dan ringan.

