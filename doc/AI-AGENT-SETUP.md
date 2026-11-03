# Panduan Setup & Arsitektur AI Agent

Dokumen ini mendefinisikan arsitektur, konfigurasi terpadu, mekanisme manajemen skills, dan protokol interoperabilitas antar AI Coding Agent pada repository **E-laundry 2.0**.

---

## 1. Arsitektur AI Agent Lingkungan Pengembangan

Arsitektur agent dirancang dengan model **Multi-Agent Decoupled Infrastructure**, di mana berbagai agent (Antigravity, Codex, Claude Code, Gemini CLI, dan OpenCode) berbagi fondasi instruksi, skills, dan context knowledge graph yang sama tanpa saling mengunci (*vendor lock-in*).

```
                      +---------------------------------------+
                      |               DEVELOPER               |
                      +---------------------------------------+
                                          |
          +-------------------------------+-------------------------------+
          |                               |                               |
          v                               v                               v
+-------------------+           +-------------------+           +-------------------+
|    Antigravity    |           |    Claude Code    |           |       Codex       |
| (Google DeepMind) |           |    (Anthropic)    |           |     (OpenAI)      |
+-------------------+           +-------------------+           +-------------------+
          |                               |                               |
          +-------------------------------+-------------------------------+
                                          |
          +-------------------------------+-------------------------------+
          |                               |                               |
          v                               v                               v
+-------------------+           +-------------------+           +-------------------+
|    Gemini CLI     |           |     OpenCode      |           |     VS Code       |
|    (Google AI)    |           |   (Open Source)   |           |    (MCP Client)   |
+-------------------+           +-------------------+           +-------------------+
          |                               |                               |
          +-------------------------------+-------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           SHARED AGENT INFRASTRUCTURE                             |
|                                                                                   |
|  1. Master Directives & Rules        : AGENTS.md, GEMINI.md, .claude/CLAUDE.md     |
|  2. Agent Skills Catalog & Lock      : .agents/skills/ & skills-lock.json         |
|  3. Knowledge Graph Engine (MCP/CLI) : CodeGraph (SQLite WAL, codegraph_explore)  |
|  4. MCP Configuration Matrix         : .mcp.json, opencode.jsonc, .vscode/mcp.json|
|  5. Domain & Technical Blueprint     : doc/ (PRD, AFD, BSD, DBD, TRD, IPD)       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Daftar Agent yang Terintegrasi & Lokasi Konfigurasi

Setiap agent memiliki mekanisme konfigurasi spesifik yang disinkronkan ke root project:

| Agent | Peran Utama | Lokasi File Konfigurasi | Status Integrasi |
| :--- | :--- | :--- | :--- |
| **Antigravity (AGY)** | Pair-programming agent utama, visual artifacts, multi-agent orchestration | Global: `%APPDATA%\antigravity\mcp\codegraph\`<br>Project: `.mcp.json`, `AGENTS.md` | **VERIFIED** |
| **Claude Code** | Terminal-based agent untuk task focused, code editing, git workflow | `.claude/settings.json`<br>`.claude/CLAUDE.md` | **VERIFIED** |
| **Codex** | Code review, command execution, and code generation | `.codex/config.toml`<br>`AGENTS.md` | **VERIFIED** |
| **Gemini CLI** | Workspace exploration and Google AI model interactions | `.gemini/settings.json`<br>`GEMINI.md` | **VERIFIED** |
| **OpenCode** | Open-source agent runner with terminal and local MCP | `opencode.jsonc`<br>`AGENTS.md` | **VERIFIED** |
| **VS Code (MCP)** | IDE workspace client with stdio transport | `.vscode/mcp.json` | **VERIFIED** |

### Rincian Konfigurasi Konkret:

1. **Root `.mcp.json` (Universal MCP Standard):**
   ```json
   {
     "mcpServers": {
       "codegraph": {
         "type": "stdio",
         "command": "codegraph",
         "args": ["serve", "--mcp"],
         "alwaysLoad": true
       }
     }
   }
   ```

2. **`.vscode/mcp.json`:**
   ```json
   {
     "servers": {
       "codegraph": {
         "type": "stdio",
         "command": "codegraph",
         "args": ["serve", "--mcp", "--path", "D:\\Kuliah\\joki\\Kerja Praktek Aqil\\kawan aqil\\projek"]
       }
     }
   }
   ```

3. **`opencode.jsonc`:**
   ```jsonc
   {
     "$schema": "https://opencode.ai/config.json",
     "mcp": {
       "servers": {
         "codegraph": {
           "type": "local",
           "command": ["codegraph", "serve", "--mcp"],
           "disabled": false,
           "codemode": false
         }
       }
     }
   }
   ```

4. **`.codex/config.toml`:**
   ```toml
   [mcp_servers.codegraph]
   command = "codegraph"
   args = ["serve", "--mcp"]
   ```

5. **`.claude/settings.json`:**
   ```json
   {
     "permissions": {
       "allow": ["mcp__codegraph__*"]
     },
     "hooks": {
       "UserPromptSubmit": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "codegraph.cmd prompt-hook"
             }
           ]
         }
       ]
     }
   }
   ```

6. **`.gemini/settings.json`:**
   ```json
   {
     "mcpServers": {
       "codegraph": {
         "type": "stdio",
         "command": "codegraph",
         "args": ["serve", "--mcp"]
       }
     }
   }
   ```

---

## 3. Mekanisme Penggunaan Skills

Repository ini menggunakan arsitektur **Skills Ecosystem** yang berstandar terbuka (`agentskills.io` / `skills-lock.json`).

### Struktur Direktori:
```
.agents/
  └── skills/
      ├── antislop/
      ├── antislop-code/
      ├── antislop-copywriting/
      ├── antislop-layoutmobile/
      ├── antislop-ui/
      ├── caveman/
      ├── design-mobile-apps/
      ├── fastapi/
      ├── improve-codebase-architecture/
      ├── ios-design/
      ├── ponytail/
      ├── ponytail-audit/
      ├── ponytail-debt/
      ├── ponytail-gain/
      ├── ponytail-help/
      ├── ponytail-review/
      ├── security-audit/
      ├── tdd/
      └── ui-taste/
```

### Manifest Kunci (`skills-lock.json`):
- Berisi sha256 `computedHash`, URL sumber GitHub/Well-known, dan path relatif setiap skill.
- Menjamin integritas dan versi skill yang terpasang agar tidak berubah tanpa audit.
- **Prinsip Utama:** Tidak mengunduh ulang atau menggandakan skill yang telah terpasang.

### Mekanisme Discovery pada Berbagai Agent:
- **Antigravity:** Secara otomatis memindai `.agents/skills/*/SKILL.md`. Frontmatter YAML menentukan nama, deskripsi, dan parameter pemanggilan. Jika skill memiliki `disable-model-invocation: true` (seperti `improve-codebase-architecture`), skill tersebut hanya aktif jika dipanggil langsung oleh user atau sub-agent yang didelegasikan.
- **Claude Code & OpenCode:** Membaca skill dari `.agents/skills/` dan mendukung pemanggilan melalui slash command seperti `/ponytail`, `/caveman`, `/tdd`.
- **Codex:** Mendukung pemanggilan skill menggunakan namespace `$skill-name:skill-name`.

---

## 4. Aturan Instruksi Agent (Directives Alignment)

Instruksi agent berpusat pada **`AGENTS.md`** sebagai sumber kebenaran tunggal (*single source of truth*), sementara `GEMINI.md` dan `.claude/CLAUDE.md` bertindak sebagai *bridge/pointer* yang konsisten.

### Prinsip Operasional Wajib:
1. **Consult Architecture First:** Selalu pelajari dokumentasi spesifikasi di `doc/` sebelum membuat kesimpulan arsitektural.
2. **CodeGraph First for Code Discovery:** Wajib menggunakan MCP `codegraph_explore` atau CLI `codegraph explore` sebelum melakukan grep atau pembacaan file manual.
3. **YAGNI & Lean Engineering (Ponytail Philosophy):** Solusi terkecil yang menyelesaikan tugas secara utuh selalu lebih diutamakan dibandingkan menambahkan layer, abstraksi, atau dependensi baru.
4. **Anti-Slop Craftsmanship:** Antarmuka harus memenuhi standar WCAG AA, bebas dari template generic AI (seperti em dash `—`, bento box tanpa kebutuhan, tombol tidak berfungsi, atau angka fiktif).
5. **Deterministic Testing:** TDD loop (Red $\rightarrow$ Green $\rightarrow$ Refactor) diuji pada *public seams*, bukan implementasi internal.
6. **Security Hygiene:** Nol toleransi terhadap hardcoded secrets, verifikasi boundary input, dan tidak menjalankan script tanpa memahami risikonya.
7. **Git Safety:** Dilarang keras melakukan `git reset --hard`, `git clean -fd`, atau force push.

---

## 5. Prosedur Menambahkan AI Agent Baru

Jika di masa mendatang tim ingin mengintegrasikan agent baru (misalnya Cursor, Windsurf, Roo Code, dsb.):

1. **Verifikasi Dukungan MCP:**
   Tambahkan konfigurasi MCP stdio ke client baru mengarah ke command `codegraph serve --mcp`.
2. **Sambungkan Instruksi Utama:**
   Arahkan file aturan agent baru (misal `.cursorrules`, `.windsurfrules`) untuk merujuk ke `AGENTS.md`.
3. **Konfigurasi Path Skills:**
   Pastikan agent baru memiliki akses baca ke folder `.agents/skills/`.
4. **Verifikasi Tool Execution:**
   Uji apakah agent dapat menjalankan tool `codegraph_explore` atau CLI `codegraph explore`.
5. **Perbarui Dokumentasi:**
   Catat agent baru pada dokumen `doc/AI-AGENT-SETUP.md`.

