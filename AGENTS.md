# AI AGENT DIRECTIVES & GUIDELINES

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->

## 1. Project Context & Philosophy
- **Project:** E-Laundry 2.0 — Web Application Manajemen Laundry UMKM (Mobile First).
- **Core Strategy:** Lean, reliable, and user-centric architecture for micro, small, and medium laundry operations.
- **Documentation First:** Always consult domain and technical specifications in `doc/` (`PRD.md`, `AFD.md`, `BSD.md`, `DBD.md`, `TRD.md`, `IPD.md`) before proposing or modifying architecture.

## 2. Engineering Standards & Anti-Overengineering
- **Minimal Complete Solutions (YAGNI):** The best code is code never written. Solve problems with the minimum necessary new code without unnecessary wrappers, speculative abstractions, or unused configuration.
- **Preserve Documentation & Formatting:** Maintain existing comments, type hints, and docstrings unless explicitly tasked to update them.
- **Consistency:** Align with the conventions and frameworks already adopted in the codebase.
- **Scope Discipline:** Only touch files and logic strictly necessary for the current task. Never modify unrelated files or libraries.

## 3. Skills Mapping & Usage Matrix
Use specialized skills located in `.agents/skills/` based on the task domain:

| Domain | Recommended Skills | Key Principles |
| :--- | :--- | :--- |
| **Frontend & Mobile UI** | `antislop`, `antislop-ui`, `antislop-layoutmobile`, `ui-taste`, `ios-design`, `design-mobile-apps` | Reject generic AI slop, ensure mobile-first responsiveness (44px tap targets, no overflow), WCAG AA contrast, and real component states (empty, loading, error). |
| **Copywriting & Comments** | `antislop-copywriting`, `antislop-code` | Human, natural copy; eliminate em dashes (`—`), generic buzzwords, and redundant AI comment fluff. |
| **Backend & API** | `fastapi` | Modern FastAPI standards: `Annotated[...]`, explicit Pydantic return types, non-blocking async, clean router prefixes. |
| **Architecture & Quality** | `improve-codebase-architecture`, `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` | Favor deep modules with simple seams; track deliberate shortcuts with `shortcut: <ceiling>, <upgrade-path>`. |
| **Testing** | `tdd` | Test at public seams, red-green-refactor loop, vertical slices, no implementation-coupled mocks. |
| **Security** | `security-audit` | Verify trust boundaries, sandboxed execution, least privilege, zero tolerance for hardcoded secrets. |
| **Communication** | `caveman` | Use terse, fluff-free communication ONLY when explicitly prompted (`/caveman`). |

## 4. Testing & Verification Rules
- **Behavior over Implementation:** Tests must verify behavior through public seams, not private internal methods.
- **Mandatory Self-Check:** Non-trivial logic (auth, financial calculations, state transitions, parsers) must include automated tests or verifiable assertions before delivery.
- **Pre-Delivery Verification:** Run and verify test suites, linters, or typecheckers before finalizing tasks.

## 5. Security & Git Discipline
- **Zero Secrets in VCS:** Never commit `.env`, credentials, private keys, or API tokens. Ensure `.gitignore` remains respected.
- **Safe Git Operations:**
  - DO NOT run destructive commands (`git reset --hard`, `git clean -fd`, force push).
  - DO NOT perform automatic commits or pushes without explicit user confirmation.
- **Environment Isolation:** Never execute untrusted scripts or modify system hosts outside isolated workspaces.
