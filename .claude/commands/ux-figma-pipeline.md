# UX → React Pipeline

Pipeline อัตโนมัติตั้งแต่ TOR/Req → BA Analysis → Research → React Prototype

## Usage
```
/ux-figma-pipeline [project-name] [TOR-file-path]
/ux-figma-pipeline [project-name] --notebook [notebook-id]   ← มี NLM notebook อยู่แล้ว
/ux-figma-pipeline [project-name] --skip-research            ← ข้าม research (มีข้อมูลแล้ว)
/ux-figma-pipeline [project-name] --skip-perplexity          ← ใช้แค่ NLM (ไม่ทำ external)
/ux-figma-pipeline [project-name] --skip-nlm                 ← ใช้แค่ Perplexity (ถ้าไม่มี TOR)
/ux-figma-pipeline [project-name] --feature [feature-name]   ← เพิ่ม feature เดียว (ไม่ต้อง full run)
```

## Research Tools

```bash
NLM="/Users/socket9/Desktop/UX Figma Workflow/scripts/nlm.sh"
# Perplexity ผ่าน MCP — ตรวจ PERPLEXITY_API_KEY ใน env ก่อนใช้
```

| Stage | NLM | Perplexity |
|-------|-----|------------|
| 1 — BA Analysis | ✅ Primary | — |
| 1.5 — Idea Card + Questions | สร้าง ai-questions | สร้าง plx-questions |
| 2A — Internal Research | ✅ Batch ask | — |
| 2B — External Research | — | ✅ Batch + competitive + regulation |
| 3 — Synthesis | Merge ทั้ง 2 sources | Merge ทั้ง 2 sources |

---

## STAGE 1 — BA Analysis (NLM + TOR)
**Agent: UX Researcher**

### Step A: Setup Notebook
```bash
# ถ้าไม่มี notebook:
$NLM create "[project-name] UX Research"
$NLM source add [TOR-file-path]
$NLM source wait   # รอ indexing

# ถ้ามี notebook อยู่แล้ว (--notebook flag):
$NLM use [notebook-id]
$NLM source list
```

### Step B: BA Analysis Prompt
ส่ง prompt นี้เข้า NLM ทันที:

```
คุณต้องเป็น BA และ UX/UI ที่สามารถบรีฟงานเพื่อส่งต่อการทำงานให้กับตำแหน่งอื่นๆ ให้เข้าใจได้ง่าย
คุณต้องทำให้ระบบมีความใช้งานง่าย เป็นมิตรกับผู้ใช้งาน พร้อมทั้งคำนึงถึงความถูกต้องของข้อมูล
และสามารถแนะนำหรือแก้ไขปัญหาโดยเสนอวิธีที่ดีและง่ายต่อการใช้งานและไม่เกินความเป็นจริง
ให้ถอดข้อมูลระบบจากเอกสารที่แนบและทำกระบวนการดังนี้:
1. Clarify Business Goal & User Goal
2. Define User Persona
3. Define Scope & Assumption
4. Define Functional Requirements
5. Define Data Requirement
6. User Journey & Flow
```

```bash
$NLM ask "[prompt ด้านบน]"
```

**Output:** บันทึกคำตอบทั้งหมดลง `02-research/ba-analysis-[name].md`

---

## STAGE 1.5 — UX Idea Card + Research Questions (Dual)
**Agent: UX Researcher**

อ่าน `ba-analysis-[name].md` แล้วสร้าง 3 outputs:

### UX Idea Card
- **Context & Goal** — สรุป Business + User Goal จาก BA Analysis
- **Alternative Solutions** — เสนอ 2–3 แนวทางที่ง่ายกว่า หรือ innovative กว่า TOR (สำหรับเสนอ client)
- **Open Questions** — แยก internal (NLM) vs external (Perplexity)
- **Hypotheses** — สมมติฐานเกี่ยวกับ user behavior
- **External Research Topics** — รายการสำหรับ Perplexity

### AI Questions (NLM)
คำถาม 10–15 ข้อสำหรับ NLM — ต้องตอบได้จาก TOR/docs:
- User pain points และ mental models
- Edge cases ที่ TOR อาจไม่ได้ระบุ
- Data validation และ error scenarios
- Workflow ที่ซับซ้อน

### Perplexity Questions
คำถาม 8–12 ข้อสำหรับ Perplexity — ต้องการ outside knowledge:
- 2–3: **Competitive landscape** (apps/services ใกล้เคียง)
- 2–3: **Regulation/standards** ที่กระทบ design
- 2–3: **Latest UX patterns** ในวงการปี 2025
- 1–2: **Statistics/user behavior**

> สำคัญ: คำถาม 2 ชุดอย่าซ้ำกัน — NLM ตอบจากเอกสาร, Perplexity ตอบจาก web

**Outputs:**
- `02-research/ux-idea-card-[name].md`
- `02-research/ai-questions-[name].md`
- `02-research/plx-questions-[name].md`

---

## STAGE 2A — NLM Auto-Research (Internal)
**Agent: UX Researcher** — รันคู่ขนานกับ 2B

```
/skills:nlm-batch-research [project-name] [notebook-id]
```

**Output:** `02-research/ai-answers-[name].txt`

---

## STAGE 2B — Perplexity Auto-Research (External)
**Agent: UX Researcher** — รันคู่ขนานกับ 2A

### Step 1: Batch research (default)
```
/skills:plx-batch-research [project-name]
```

### Step 2: Competitive scan (ถ้ามี competitors)
```
/skills:plx-competitive [project-name]
```

### Step 3: Regulation/compliance (ถ้า regulated industry)
```
/skills:plx-regulation [project-name] --auto
```

**Outputs:**
- `02-research/plx-answers-[name].md` — general external Q/A พร้อม citations
- `02-research/plx-competitive-[name].md` — feature matrix + UX patterns
- `02-research/plx-regulation-[name].md` — compliance checklist

> ถ้า `--skip-perplexity` flag → ข้าม Stage 2B ทั้ง stage

---

## STAGE 3 — Research Synthesis (Merge Internal + External)
**Agent: UX Researcher**

รับ inputs ทั้งหมดแล้วสังเคราะห์:

**Inputs:**
- `ba-analysis-[name].md` — TOR understanding
- `ai-answers-[name].txt` — NLM internal grounding
- `plx-answers-[name].md` — Perplexity external context
- `plx-competitive-[name].md` (ถ้ามี)
- `plx-regulation-[name].md` (ถ้ามี)

**Synthesis:**
1. รวม insights ทุก source เป็น Research Doc
2. จัด Personas (เสริมด้วย market data จาก Perplexity)
3. Rank pain points ตาม severity — เช็คว่า competitors แก้ pain เหล่านี้ยังไง
4. Map regulation requirements → screen-level implications
5. สรุป Recommended Design Directions (avoid anti-patterns จาก competitive scan)

**Output:** `02-research/ux-research-doc-[name].md` ประกอบด้วย:
- Executive Summary
- User Personas & Scenarios
- Key Pain Points (ranked, with competitor reference)
- Competitive Landscape Summary (ถ้ามี)
- Compliance Requirements (ถ้ามี)
- Recommended Design Directions
- Citation Index (NLM source IDs + Perplexity URLs with dates)

---

## STAGE 3.5 — Narrative Critique (Gate)
**Agent: UX Researcher**

ทบทวน `ux-research-doc-[name].md` จากมุมมอง third-party:

1. **Narrative flow** — user story ไหลสมเหตุสมผลไหม?
2. **Blind spots** — มีอะไรที่ทีมอาจมองข้าม?
3. **Fact-check** — citation ตรวจสอบได้จริงไหม? (NLM source IDs + Perplexity URLs)
4. **Source diversity** — claim สำคัญมาจาก source เดียวหรือไม่? ต้อง cross-validate
5. **Recency** — Perplexity citation เก่ากว่า 12 เดือนสำหรับ trends/regulation → re-verify

**ถ้าผ่าน:** พิมพ์ `"Verified & Approved"` แล้วไปต่อ Stage 4 (Site Map)
**ถ้าไม่ผ่าน:** ระบุ issue ชัดเจน — แก้ไข Stage 3 หรือ re-run skill ที่ตรงกับปัญหา

---

## STAGE 4 — Site Map + Screen Inventory (NLM)
**Agent: UX Researcher → UX/UI Producer**

### Step A: ขอ Site Map จาก NLM
```bash
$NLM ask "จากข้อมูลระบบทั้งหมดที่วิเคราะห์ไว้ ให้สร้าง Site Map ของระบบ โดยแสดง:
1. โครงสร้าง Navigation หลักทุกระดับ
2. แต่ละ Menu/Feature มี Screen อะไรบ้าง
3. ระบุ User Role ที่เข้าถึงแต่ละส่วน"
```

### Step B: แปลง Site Map → Screen Inventory
Claude parse คำตอบจาก NLM แล้วสร้าง Screen Inventory ที่มีโครงสร้าง:

```markdown
## Screen Inventory

### [Feature A]
- [ ] Screen 1 — [description]
- [ ] Screen 2 — [description]

### [Feature B]
- [ ] Screen 1 — [description]
```

**Outputs:**
- `02-research/sitemap-[name].md`
- `02-research/screen-inventory-[name].md`

---

## STAGE 4.5 — Design Specs (optional แต่แนะนำ)
**Agent: UX/UI Producer**

หลัง Site Map + Screen Inventory ก่อนลงมือ shell ให้สร้าง spec sheets:

```
/skills:microcopy [project-name]        ← labels, errors, empty states ภาษาไทยทั้งระบบ
/skills:handoff-notes [project-name]    ← design tokens, component specs, layout rules
```

Output:
- `03-design/microcopy-[name].md`
- `03-design/handoff-notes-[name].md`

> ใช้คู่กับ system skills `design:ux-copy` และ `design:design-handoff` ได้

---

## STAGE 5 — React Project Shell
**Agent: UX/UI Producer**

อ่าน Screen Inventory + BA Analysis + handoff-notes แล้วสร้าง React project:

### Tech Stack
```json
{
  "react": "^19.0.0",
  "typescript": "^5.0.0",
  "vite": "^6.0.0",
  "tailwindcss": "^4.0.0",
  "react-router-dom": "^7.0.0",
  "lucide-react": "latest",
  "motion": "latest"
}
```

### Project Structure
```
05-prototype/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── router.tsx              ← routes ครบทุก screen จาก Screen Inventory
    ├── styles/
    │   ├── tokens.css          ← design tokens (colors, fonts, spacing)
    │   └── global.css
    ├── components/             ← shared components
    │   ├── Layout.tsx          ← shell: sidebar/topnav + outlet
    │   ├── Navbar.tsx
    │   └── Sidebar.tsx
    └── pages/                  ← หนึ่ง folder ต่อ feature
        ├── [Feature]/
        │   ├── index.tsx       ← list/overview screen
        │   └── [Screen].tsx
        └── ...
```

### Design Tokens (จาก BA Analysis)
- Font: Noto Sans Thai
- สี Primary, Secondary จาก TOR/brief
- CSS custom properties ใน `tokens.css`

### Shell Requirements
- Layout component พร้อม sidebar + topnav
- Routes ครบทุก feature (placeholder page แต่ละ screen)
- ภาษาไทยทั้งระบบ
- Responsive (mobile-first)

**Output:** `05-prototype/` — React project ที่ `npm run dev` ได้เลย

---

## STAGE 6 — Feature Loop (NLM Wireframe → Analyze → Implement → Verify)
**Agent: UX/UI Producer**

Loop ทุก feature ใน Screen Inventory — **4 steps ต่อ feature, ห้ามข้าม Step A.5 และ Step D**

### ต่อ Feature/Menu:

---

**Step A: ขอ Wireframe Text จาก NLM**
```bash
$NLM ask "ออกแบบ Wireframe Text Layout สำหรับ [Feature Name] โดย:
1. ระบุ User Journey ของ feature นี้ตั้งแต่ต้นจนจบ
2. แต่ละ Screen มี UI Elements อะไรบ้าง (Form fields, Tables, Buttons, Cards)
3. ระบุ Data ที่แสดงในแต่ละ Element
4. ระบุ Action และ Validation rules
5. Error states และ Edge cases"
```

---

**Step A.5: Wireframe Analysis Gate** ← **REQUIRED ก่อน implement เสมอ**

อ่าน Wireframe ที่ได้จาก NLM แล้ว Claude วิเคราะห์ตาม 5 มิติก่อนลงมือ code:

| มิติ | สิ่งที่ตรวจ | ผลที่ต้องการ |
|---|---|---|
| **UX Flow completeness** | มี Empty state, Loading state, Error state ครบไหม? มี success feedback ทุก action? | ระบุ state ที่ขาด แล้วเพิ่มใน spec |
| **Data / Validation consistency** | Field names, required rules, business logic ตรงกับ BA Analysis ไหม? | Map field ไปหา FR ที่ตรงกัน |
| **Thai context & terminology** | Label ภาษาไทยถูกต้องตามบริบทองค์กร? ใช้คำทางการหรือคำทั่วไปเหมาะสมไหม? | แก้คำที่ผิดบริบทก่อน implement |
| **Cross-screen consistency** | Pattern (badge, button variant, card layout) เหมือนกับ screen อื่นที่ทำไปแล้วไหม? | บันทึก pattern ที่ใช้แล้วให้สอดคล้อง |
| **Usability principles** | ตามหลัก Nielsen: Visibility of status, Error prevention, Minimal design? Action ที่ destructive มี Confirm ไหม? | ระบุ heuristic violation พร้อมวิธีแก้ |

**Output ของ Step A.5:** สรุปเป็น "Refined Implementation Spec" สั้นๆ — อธิบายสิ่งที่จะ implement พร้อม notes ที่ขาดจาก wireframe

---

**Step B: Claude implement React Screen**
จาก Refined Implementation Spec (ไม่ใช่ NLM wireframe โดยตรง):
- สร้าง/อัปเดต component ใน `src/pages/[Feature]/`
- ใช้ design tokens จาก `tokens.css` — ห้าม hardcode สี
- ใช้ Lucide React สำหรับ icons, Motion สำหรับ transitions
- Mock data สมจริงภาษาไทย — ห้าม Lorem ipsum
- Form validation + error messages ครบ
- **ทุกปุ่มที่กดได้ต้องมี feedback** — ใช้ `Notification` component หรือ state transition

---

**Step C: Connect routing**
- เชื่อม screen ใหม่เข้า `router.tsx`
- ตรวจว่า `navigate()` ทุกจุดชี้ไปหา path ที่มีอยู่จริงใน router
- เพิ่ม Sidebar link ถ้า screen นั้นควรเข้าถึงได้จาก nav

---

**Step D: Action Verification** ← **REQUIRED หลัง implement ทุก feature**

ตรวจ Interactive elements ทุกตัวในหน้าที่เพิ่งทำ:

```
Buttons:
[ ] ทุก onClick มี handler (ไม่ใช่ empty function หรือ dead button)
[ ] Primary action (submit/save) → Success screen หรือ notification
[ ] Destructive action (delete/reject) → มี confirm step
[ ] Secondary action (cancel/back) → navigate ถูก route
[ ] Export/Download → มี feedback (notification หรือ state change)

Forms:
[ ] Required fields แสดง error เมื่อ submit โดยไม่กรอก
[ ] Validation rules ทำงานถูกต้อง (date range, cap limit ฯลฯ)
[ ] Submit success → ไปหน้าถูกต้องหรือแสดง success state

Navigation:
[ ] ทุก navigate() path มีอยู่ใน router.tsx
[ ] Back button ทุกจุดนำกลับหน้าที่ถูกต้อง
[ ] Sidebar link ครอบคลุม screen นี้

TypeScript:
[ ] npx tsc --noEmit ไม่มี error ใหม่
```

**ทำซ้ำ Step A → A.5 → B → C → D จนครบทุก feature ใน Screen Inventory**

---

## STAGE 6B — UX/UI Full Audit (หลัง Feature Loop ครบ)
**Agent: UX/UI Auditor**

รัน 1 ครั้งหลังจาก implement ครบทุก screen ก่อนส่งมอบ  
Agent spec เต็มอยู่ที่ `.claude/agents/ux-auditor.md`

### Audit ที่รัน (ตามลำดับ)
1. **TypeScript & Build** — `npx tsc --noEmit` ต้องผ่าน 100% ก่อนไปต่อ
2. **Visual Consistency** — token usage, ไม่มี hardcoded hex/px
3. **Layout Shell** — breadcrumb coverage, role-based nav, active states
4. **Responsive Layout** — form-body centering, page-cols, grid auto-fill
5. **WCAG 2.1 AA** — tap targets, color contrast, semantic HTML, focus ring
6. **UX Heuristics** — Nielsen H1/H3/H5/H8/H9 ทุก screen
7. **Cross-screen Flow** — navigate() targets, back buttons, dead ends

### Gate Decision
- ✅ **PASS** → ไป Quality Checklist แล้วส่งมอบได้
- ❌ **FAIL** → แก้ไข Critical issues แล้วรัน audit ซ้ำ

Output: `02-research/audit-report-[name].md`

---

## Quality Checklist (ก่อน Done)
```
[ ] npm run dev ไม่มี error
[ ] TypeScript ไม่มี type error
[ ] ทุก route ใน Screen Inventory มี page แล้ว (ไม่มี Placeholder เหลือ)
[ ] ทุก navigate() ในทุก page ชี้ไปหา route ที่มีจริง
[ ] ทุกปุ่มมี feedback — ไม่มี dead button
[ ] ภาษาไทยทั้งระบบ ไม่มี Lorem ipsum / "Data 1, Data 2"
[ ] Mock data สมจริง
[ ] CSS ใช้ tokens ไม่มี hardcode color นอก tokens.css
[ ] WCAG: ทุก interactive element ≥ 44px tap target
[ ] Responsive: ใช้ grid auto-fill / flex wrap ไม่มี fixed pixel width ที่แตกบน mobile
[ ] Sidebar nav ครอบคลุมทุก screen สำคัญ
```

---

## STAGE 7 — Export Single-File Prototype
**Skill: `/skills:export-prototype`**

รันหลัง Audit ผ่าน (Stage 6B PASS) เพื่อส่งมอบให้ client

---

## STAGE 8–9 — Design System Pipeline (optional, post-audit)
**Command: `/design-system-pipeline`**

หลังจาก export prototype แล้ว ถ้าต้องการสร้าง Design System deliverable สำหรับ dev team + Figma 2-way token sync:

```bash
# Stage 8 — Generation (initial)
/design-system-pipeline [project-name] [figma-file-url]

# Stage 9 — Token Sync (recurring)
/design-system-pipeline [project-name] --pull       # Figma → code
/design-system-pipeline [project-name] --push       # code → Figma
```

Output: `07-design-system/` พร้อม tokens (DTCG) + component cards + overview.html + handoff package + Figma library section

ดูรายละเอียดเต็มที่ [`.claude/commands/design-system-pipeline.md`](./design-system-pipeline.md)

```
/skills:export-prototype [project-name] --open
```

ขั้นตอนที่ skill รัน:
1. `npx tsc --noEmit` — ตรวจ TypeScript อีกครั้ง
2. ติดตั้ง `vite-plugin-singlefile` (ถ้ายังไม่มี)
3. อัปเดต `vite.config.ts` ให้ inline JS + CSS ทั้งหมด
4. `npm run build` → `dist/index.html`
5. Copy ไปที่ `06-export/[name]-prototype-YYYYMMDD.html`

Output: ไฟล์ HTML เดียว เปิดได้เลยใน browser ไม่ต้องรัน server

---

## Output Summary

```
projects/[name]/
├── 01-brief/
│   └── [TOR file]
├── 02-research/
│   ├── ba-analysis-[name].md           ← Stage 1
│   ├── ux-idea-card-[name].md          ← Stage 1.5
│   ├── ai-questions-[name].md          ← Stage 1.5 (NLM)
│   ├── plx-questions-[name].md         ← Stage 1.5 (Perplexity)
│   ├── ai-answers-[name].txt           ← Stage 2A (NLM batch)
│   ├── plx-answers-[name].md           ← Stage 2B (Perplexity batch)
│   ├── plx-competitive-[name].md       ← Stage 2B (optional)
│   ├── plx-regulation-[name].md        ← Stage 2B (optional)
│   ├── ux-research-doc-[name].md       ← Stage 3 (Verified & Approved)
│   ├── sitemap-[name].md               ← Stage 4
│   ├── screen-inventory-[name].md      ← Stage 4
│   └── audit-report-[name].md         ← Stage 6B
├── 03-design/                          ← optional (microcopy, handoff)
├── 04-figma/                           ← optional
├── 05-prototype/                       ← Stage 5–6
│   ├── package.json
│   ├── src/
│   │   ├── router.tsx
│   │   ├── components/
│   │   └── pages/[Feature]/
│   └── README.md
├── 06-export/                          ← Stage 7
│   └── [name]-prototype-YYYYMMDD.html  ← ส่งให้ client ได้เลย
└── 07-design-system/                   ← Stage 8–9 (optional)
    ├── tokens.json                     ← DTCG canonical
    ├── tokens.{css,ts}                 ← generated
    ├── components/*.card.md + .png
    ├── overview.html
    ├── handoff-package/                ← dev deliverable
    ├── CHANGELOG.md
    └── figma-sync-log.md
```

---

## Pipeline Flow Diagram

```
STAGE 1   BA Analysis (NLM)
   ↓
STAGE 1.5  UX Idea Card + AI Questions + Perplexity Questions
   ↓
   ├─── STAGE 2A: NLM Auto-Research (internal)  ┐
   └─── STAGE 2B: Perplexity Auto-Research      │  (parallel)
                  + Competitive + Regulation    ┘
   ↓
STAGE 3   Research Synthesis (merge internal + external)
   ↓
STAGE 3.5  Narrative Critique  ← Verified & Approved gate
   ↓
STAGE 4   Site Map + Screen Inventory
   ↓
STAGE 4.5  Design Specs (optional)
   ↓
STAGE 5   React Shell
   ↓
STAGE 6   Feature Loop (per feature: Wireframe → A.5 gate → Implement → Verify)
   ↓
STAGE 6B  UX/UI Full Audit  ← PASS gate
   ↓
STAGE 7   Export Single-File HTML
   ↓
STAGE 8   Design System Generation (optional)
   ├─ ds-extract → tokens.json (DTCG)
   ├─ ds-cards → component cards
   ├─ ds-overview → overview.html
   ├─ ds-handoff → handoff package
   └─ ds-push-figma → "🎨 Design System" page
   ↓
STAGE 9   Token Sync (recurring, manual)
   ├─ ds-pull-tokens (Figma → code)
   └─ ds-push-tokens (code → Figma)
```
