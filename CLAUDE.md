# CLAUDE.md — UX Figma Workflow

## Overview

Working directory สำหรับ end-to-end UX pipeline: TOR/Brief → BA Analysis (NLM) → Internal Research (NLM) + External Research (Perplexity) → Synthesis → Site Map → React Prototype → Audit → (optional) Figma push → Design System deliverable

Pipeline ขับด้วย slash commands ใน `.claude/commands/` และส่งงานต่อกันระหว่าง 5 agents ใน `.claude/agents/`:

| Agent | หน้าที่ |
|-------|--------|
| **UX Researcher** | Stage 1–4 (BA → NLM+Perplexity Q/A → Synthesis → Site Map) |
| **UX/UI Producer** | Stage 5–6 (React Shell → Feature Loop) |
| **UX/UI Auditor** | Stage 6B (7-point audit ก่อน deliver) |
| **Figma Publisher** | Stage 7 (optional — push tokens/screens เข้า Figma) |
| **Design System Publisher** | Stage 8–9 (DS deliverable + token 2-way sync) |

---

## Tech Stack

### Tooling
| Layer | Tool |
|-------|------|
| Internal research | notebooklm-py CLI (Python venv) — TOR / client docs |
| External research | Perplexity MCP (`mcp__perplexity__*`) — competitors / regulation / web |
| Design extraction/write | Figma MCP (`mcp__claude_ai_Figma__*` — official: use_figma, get_variable_defs, get_design_context, etc.; `mcp__Figma__get_figma_data` — Framelink read-only) |
| Browser automation | Playwright MCP (`mcp__playwright__*`) |

**Perplexity setup (one-time, paid):**
```bash
export PERPLEXITY_API_KEY="pplx-..."   # ใส่ใน ~/.zshrc หรือ shell init
```
MCP server config อยู่ใน `.claude/settings.local.json` (`@chatmcp/server-perplexity-ask` ผ่าน npx)

ราคาประมาณ:
- รัน batch research 1 ครั้ง ≈ $0.30–0.80
- รัน competitive scan ≈ $1–2
- ครบ pipeline 1 project ≈ $3–5
- ต้อง add credit ขั้นต่ำ $5 และใส่บัตร: https://www.perplexity.ai/account/api/keys

**Fallback แบบฟรี (ถ้ายังไม่อยาก setup API):**

`plx-*` skills ทุกตัวมีไว้แล้ว แต่ถ้าไม่มี API key ใช้ทางเลือกเหล่านี้แทนได้:

| ทางเลือก | วิธีใช้ | Trade-off |
|----------|---------|-----------|
| **Claude WebSearch** (built-in) | ขอ Claude ค้น web ตรงๆ ใช้ tool `WebSearch` | ไม่มี recency filter, ไม่มี deep research mode |
| **Perplexity web UI** | เปิด perplexity.ai → copy คำถามจาก `plx-questions-[name].md` ไปถามทีละข้อ → paste กลับ | ช้ากว่า ไม่ auto |
| **ข้าม Perplexity** | ใช้แค่ NLM + ใส่ competitor/regulation docs ลง NotebookLM sources | ไม่ได้ external real-time data |

ทุกทางเลือกใช้ workflow ฝั่ง synthesis ตัวเดียวกัน — แค่เปลี่ยน source ของ external research

### Prototype Stack (เลือกต่อ project)

**Web (default):**
- React 19 + TypeScript 5 (strict) + Vite 6
- React Router v7
- Tailwind v4 (default) / HeroUI / shadcn/ui
- Lucide React + Motion

**Mobile:**
- Expo + React Native + TypeScript 5
- React Navigation v7
- Nativewind v4 / React Native Paper
- Lucide React Native + Reanimated

**Core invariant (ทุก project):**
- TypeScript strict mode
- ภาษาไทยทั้งระบบ — ไม่มี English text ใน UI
- Design tokens ใช้เสมอ — ห้าม hardcode สี/spacing/font

### Single-File Export
หลัง audit ผ่าน รัน `/skills:export-prototype [project]` → ได้ไฟล์ HTML เดียวที่เปิดด้วย `file://` ได้ (Vite + `vite-plugin-singlefile` + `createHashRouter`)

---

## Project Structure

```
UX Figma Workflow/
├── CLAUDE.md                        ← ไฟล์นี้
├── README.md                        ← คู่มือภาษาไทย
│
├── .claude/
│   ├── agents/
│   │   ├── ux-researcher.md         ← Stage 1–4
│   │   ├── ux-producer.md           ← Stage 5–6
│   │   ├── ux-auditor.md            ← Stage 6B
│   │   ├── figma-publisher.md       ← Stage 7 (optional)
│   │   └── ds-publisher.md          ← Stage 8–9 (Design System)
│   ├── commands/
│   │   ├── ux-figma-pipeline.md     ← Pipeline หลัก (Stage 1–7)
│   │   ├── figma-pipeline.md        ← Figma push (thin wrapper เรียก figma-publisher agent)
│   │   ├── design-system-pipeline.md ← Stage 8–9 (DS deliverable + token sync)
│   │   └── skills/                  ← Slash skills (เรียกด้วย /skills:[name])
│   │       ├── nlm-ask.md           ← Internal (NLM)
│   │       ├── nlm-batch-research.md
│   │       ├── plx-ask.md           ← External (Perplexity)
│   │       ├── plx-batch-research.md
│   │       ├── plx-competitive.md
│   │       ├── plx-regulation.md
│   │       ├── ds-extract.md        ← Design System
│   │       ├── ds-cards.md
│   │       ├── ds-overview.md
│   │       ├── ds-handoff.md
│   │       ├── ds-push-figma.md
│   │       ├── ds-pull-tokens.md
│   │       ├── ds-push-tokens.md
│   │       ├── user-flow.md
│   │       ├── component-library.md
│   │       ├── screen-factory.md
│   │       ├── microcopy.md
│   │       ├── handoff-notes.md
│   │       ├── data-viz.md
│   │       ├── layout-review.md
│   │       ├── wcag-audit.md
│   │       ├── design-crit.md
│   │       ├── figma-flow.md
│   │       └── export-prototype.md
│   └── settings.local.json
│
├── scripts/
│   └── nlm.sh                       ← Wrapper → notebooklm-py venv
│
├── knowledge/
│   ├── index.md                     ← Index ของ insight atoms
│   └── atoms/                       ← atom-YYYY-MM-DD-[slug].md
│
└── projects/
    ├── _template/                   ← Copy เป็น project ใหม่
    └── [project-name]/
        ├── 01-brief/                ← TOR/Req files
        ├── 02-research/
        │   ├── ba-analysis-[name].md
        │   ├── ux-idea-card-[name].md
        │   ├── ai-questions-[name].md           ← NLM questions
        │   ├── ai-answers-[name].txt            ← NLM batch (auto)
        │   ├── plx-questions-[name].md          ← Perplexity questions
        │   ├── plx-answers-[name].md            ← Perplexity batch (auto)
        │   ├── plx-competitive-[name].md        ← optional — competitor scan
        │   ├── plx-regulation-[name].md         ← optional — compliance
        │   ├── ux-research-doc-[name].md        ← Verified & Approved gate
        │   ├── sitemap-[name].md
        │   ├── screen-inventory-[name].md
        │   ├── user-flow-[name].md
        │   └── audit-report-[name].md
        ├── 03-design/                     ← optional
        │   ├── microcopy-[name].md
        │   └── handoff-notes-[name].md
        ├── 04-figma/                      ← optional
        │   ├── figma-url-[name].md
        │   ├── key-screens-[name].md
        │   ├── code-connect-[name].md
        │   └── figma-flow.md
        ├── 05-prototype/                  ← React + Vite project
        │   ├── package.json
        │   ├── vite.config.ts
        │   ├── tsconfig.json
        │   ├── index.html
        │   └── src/
        │       ├── main.tsx
        │       ├── App.tsx
        │       ├── router.tsx
        │       ├── styles/
        │       │   ├── tokens.css         ← design tokens (CSS variables)
        │       │   └── global.css
        │       ├── components/            ← shared (Layout, Sidebar, Topbar, primitives)
        │       ├── contexts/              ← RoleContext, etc.
        │       └── pages/[Feature]/[Screen].tsx
        ├── 06-export/
        │   └── [name]-prototype-YYYYMMDD.html
        └── 07-design-system/              ← Stage 8–9 (optional, post-audit)
            ├── tokens.json                ← DTCG canonical
            ├── tokens.css                 ← generated
            ├── tokens.ts                  ← generated
            ├── components/                ← .card.md + .png per component
            ├── overview.html              ← single-page gallery
            ├── handoff-package/           ← zip-able dev deliverable
            ├── CHANGELOG.md
            └── figma-sync-log.md
```

---

## Conventions

### File naming
- Project files ใช้ suffix `-[project-name]`: `ba-analysis-ocpb-datasure.md`
- Insight atoms: `atom-YYYY-MM-DD-[kebab-slug].md`
- Screenshots: `prototype-[screen-name].png`, `ref-[source-name].png`

### React Prototype
- **CSS custom properties เสมอ** — `var(--color-primary)`, ห้าม hardcode hex
- **ภาษาไทยทั้งระบบ** — ไม่มี English ใน UI (เว้น code identifier)
- **Mock data สมจริง** — ห้าม "Lorem ipsum", "ข้อมูล 1, 2, 3"
- **Routes ครบทุก screen** — `router.tsx` ต้อง map screen ทั้งหมดจาก Screen Inventory (ใช้ placeholder ก่อนได้ใน Stage 1)
- **Semantic HTML + ARIA** — `<button>` ไม่ใช่ `<div onClick>`, มี `aria-label` ทุก interactive control
- **Tap targets ≥ 44px** — ทุก button/link
- **Back navigation ทุก screen** ยกเว้น root
- **Design tokens** — สี/spacing/font ใช้ CSS variable หรือ `tokens.ts` (mobile)

### Skill prefix
ทุก skill เรียกด้วย `/skills:[name]` เสมอ (consistent กับ folder `.claude/commands/skills/`)

ตัวอย่าง: `/skills:nlm-ask`, `/skills:component-library`, `/skills:screen-factory`

### Knowledge Base — 2-Year Rule
Atom ที่บันทึกต้องผ่านเกณฑ์:
- **Durable** — ยังใช้ได้ใน 2 ปีข้างหน้า
- **Context-independent** — ใช้ได้ข้าม project
- **Actionable** — มี design implication ที่ชัดเจน

เพิ่ม atom แล้วต้องอัปเดต `knowledge/index.md`

---

## Pipeline Commands

### Full Pipeline
```bash
/ux-figma-pipeline [project] [TOR-file]
/ux-figma-pipeline [project] --notebook [notebook-id]
/ux-figma-pipeline [project] --skip-research
/ux-figma-pipeline [project] --skip-perplexity      ← ใช้แค่ NLM
/ux-figma-pipeline [project] --skip-nlm             ← ใช้แค่ Perplexity (ไม่มี TOR)
/ux-figma-pipeline [project] --feature [feature-name]
```

### Setup ใหม่
```bash
cp -r projects/_template projects/[project-name]
```

### NotebookLM
```bash
# Wrapper (แนะนำ)
scripts/nlm.sh list
scripts/nlm.sh ask "[question]"
scripts/nlm.sh login   # ถ้า error account-routing mismatch

# Path ตรง
/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm
```

### Perplexity
```bash
# ต้องตั้ง env ก่อน
export PERPLEXITY_API_KEY="pplx-..."

# เรียกผ่าน MCP tool (Claude เรียกตรง — ไม่มี shell wrapper)
# mcp__perplexity__perplexity_ask
# mcp__perplexity__perplexity_research   ← deep + citations
# mcp__perplexity__perplexity_reason     ← comparative analysis
```

### Skills (เรียกระหว่าง pipeline หรือ ad-hoc)
```bash
# NLM (internal)
/skills:nlm-ask [notebook-id] "[question]"
/skills:nlm-batch-research [project] [notebook-id]

# Perplexity (external)
/skills:plx-ask "[question]" [--recency month|year]
/skills:plx-batch-research [project]
/skills:plx-competitive [project] [competitor1] [competitor2] ...
/skills:plx-regulation [project] [--auto | --topic PDPA]

/skills:user-flow [project]
/skills:component-library init [project]
/skills:component-library add [project] [component]
/skills:screen-factory [project] [feature] [screen1] [screen2] ...
/skills:microcopy [project]
/skills:handoff-notes [project]
/skills:layout-review [project]
/skills:wcag-audit [project] [--fix]
/skills:design-crit [project]
/skills:data-viz [project] [chart-type] [data-spec]
/skills:figma-flow [project]
/skills:export-prototype [project] [--open]
```

### Figma Push (optional, Stage 7)
```bash
/figma-pipeline [project] [figma-file-url]
/figma-pipeline [project] [figma-file-url] --new-file
/figma-pipeline [project] [figma-file-url] --ds-only
/figma-pipeline [project] [figma-file-url] --screens-only
```

### Design System Pipeline (Stage 8–9, post-audit)
```bash
# Stage 8 — Generation (initial setup, run once)
/design-system-pipeline [project] [figma-file-url]
/design-system-pipeline [project] [figma-file-url] --skip-figma
/design-system-pipeline [project] [figma-file-url] --tokens-only

# Stage 9 — Token Sync (recurring, manual)
/design-system-pipeline [project] --pull         # Figma → code
/design-system-pipeline [project] --push         # code → Figma
/design-system-pipeline [project] --sync-status

# หรือเรียก skill แยกตรงๆ
/skills:ds-extract [project]
/skills:ds-cards [project]
/skills:ds-overview [project]
/skills:ds-handoff [project]
/skills:ds-push-figma [project] [figma-url]
/skills:ds-pull-tokens [project]
/skills:ds-push-tokens [project]
```

---

## Pipeline Order — Things to Remember

**Stage order matters:**
1. **Stage 2A + 2B รันคู่ขนาน** — NLM (internal) และ Perplexity (external) ไม่บล็อกกัน
2. **Research → "Verified & Approved" gate (Stage 3.5)** ก่อนไป Site Map (no shortcut)
3. **Site Map → Screen Inventory ก่อน Shell** — ป้องกัน missing screens
4. **`/skills:user-flow` ก่อน Feature Loop** — validate screen inventory
5. **Wireframe Analysis Gate (Step A.5)** — ทุก feature ต้องผ่านก่อน implement
6. **Audit ผ่าน (Stage 6B PASS)** ก่อน export/deliver
7. **DSShowcase route + library adoption ≥ 80% ก่อน Stage 8** — pages ต้อง import จาก `src/components/ui/` จริง (ไม่ inline) และมี `/__ds-showcase` route — DS pipeline Gate 0 จะ STOP ถ้า adoption ต่ำ (UX/UI Producer Step E)
8. **Design System Pipeline (Stage 8) รันหลัง audit ผ่าน** — ห้ามรัน DS pipeline กับ prototype ที่ยังมี hardcoded values หรือ component library ที่หน้าจอไม่ consume

**Design System Sync Rules:**
- **Tokens** — 2-way (Figma ↔ code), manual sync, diff + confirm
- **Components** — 1-way (code → Figma เท่านั้น)
- **Logic/behavior** — code only (Figma ไม่เก็บ)
- **Conflict → STOP** — ติดต่อทีมก่อน resolve อย่าตัดสินใจอัตโนมัติ
- **Backup ก่อน overwrite** — เก็บ 5 backups ล่าสุด

**NotebookLM error "account-routing mismatch":**
```bash
scripts/nlm.sh login
```

**Perplexity errors:**
- `Invalid API key` → ตรวจ `echo $PERPLEXITY_API_KEY` มี value ไหม
- `429 rate limit` → รอ 60 วินาที แล้ว retry (default tier มี limit ต่ำ)
- `MCP not connected` → restart Claude Code (load `settings.local.json` ใหม่)
- ทุก answer ต้องเก็บ citations + URLs — ห้ามทิ้ง

**Figma MCP:**
- Node ID: URL `?node-id=6711-8496` → ใช้ `6711-8496` (hyphen ไม่ใช่ colon)
- Section nodes บางตัวไม่ accessible → ดึงทีละ child frame
- เหมาะกับ extraction/key-screen push ไม่เหมาะสร้าง 100+ frames ทีเดียว

**Context window เต็ม:**
- ดึง design context ทีละ frame
- บันทึก intermediate output ลงไฟล์ก่อน process ต่อ

**Reference projects:**
- `ocpb-datasure` — ผ่าน pipeline ครบทุก stage (HTML era — ตอนนี้ archive reference)
- `ggp-poc` — prototype 4 screens (Factor → AI Suggestion → Analysis → Pipeline)
