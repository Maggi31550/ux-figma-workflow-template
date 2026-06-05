# 📘 UX Figma Workflow — คู่มือการใช้งาน

> อัปเดตล่าสุด: 2026-05-14

**ติดตั้งครั้งแรก** → ดู [SETUP.md](SETUP.md)

---

## 📁 โครงสร้าง Folder

```
UX Figma Workflow/
│
├── README.md                        ← คู่มือนี้
├── SETUP.md                         ← คู่มือติดตั้งสำหรับสมาชิกใหม่
│
├── .claude/
│   ├── agents/
│   │   ├── ux-researcher.md         ← Stage 1–2: Research, Synthesis
│   │   ├── ux-producer.md           ← Stage 3–5: Prototype, Shell, Feature loop
│   │   ├── ux-auditor.md            ← Stage 6: Quality gates (WCAG, Layout, Heuristic)
│   │   └── figma-publisher.md       ← Figma pipeline: Design System, Screens, Code Connect
│   │
│   ├── commands/
│   │   ├── ux-figma-pipeline.md     ← Pipeline หลัก (Stage 1→6)
│   │   ├── figma-pipeline.md        ← Prototype → Figma (Design System + Key Screens)
│   │   └── skills/                  ← Skill commands (/skills:name)
│   │       ├── nlm-ask.md           ← Quick ask NotebookLM 1 ข้อ
│   │       ├── nlm-batch-research.md← Batch ask ทุกคำถามอัตโนมัติ
│   │       ├── component-library.md ← สร้าง/อัปเดต component library
│   │       ├── screen-factory.md    ← เพิ่ม screens อย่างเร็ว
│   │       ├── user-flow.md         ← User Flow Diagram + Screen Inventory
│   │       ├── wcag-audit.md        ← ตรวจ Accessibility WCAG 2.1 AA
│   │       ├── design-crit.md       ← Heuristic Evaluation (Nielsen's 10)
│   │       ├── layout-review.md     ← Audit Sidebar/Topbar/Breadcrumb
│   │       ├── export-prototype.md  ← Export เป็น single HTML file
│   │       ├── figma-flow.md        ← สร้าง Prototype Flow Guide สำหรับ designer
│   │       └── data-viz.md          ← Charts, Dashboards, Data-heavy screens
│   │
│   └── settings.local.json          ← Permissions + MCP config (ไม่ commit)
│
├── scripts/
│   └── nlm.sh                       ← Wrapper สำหรับ notebooklm-py CLI
│
├── knowledge/
│   ├── index.md                     ← Index ของ Knowledge Base ทั้งหมด
│   └── atoms/                       ← Insight atoms (durable UX insights)
│       └── atom-YYYY-MM-DD-[slug].md
│
└── projects/
    ├── _template/                   ← Template สำหรับ project ใหม่
    └── [project-name]/
        ├── 01-brief/
        ├── 02-research/
        ├── 03-design/
        ├── 04-figma/
        ├── 05-prototype/            ← React app (npm run dev)
        └── 06-export/               ← Single-file HTML export
```

---

## 🔌 Integrations ที่พร้อมใช้

| Tool | ใช้ทำอะไร | Setup |
|------|-----------|-------|
| **Figma MCP** | ดึง/สร้าง design, extract tokens, Code Connect | SETUP.md Step 5 |
| **notebooklm-py** | Auto-research จาก source docs | SETUP.md Step 4 |
| **Playwright MCP** | Browser automation, screenshot | optional |

### NotebookLM CLI
```bash
# wrapper (แนะนำ — path configure ใน scripts/nlm.sh)
scripts/nlm.sh list
scripts/nlm.sh ask "[question]"
scripts/nlm.sh login   # ถ้า error account-routing mismatch
```

---

## 🚀 เริ่ม Project ใหม่

### 1. สร้าง folder structure
```bash
cp -r projects/_template projects/[project-name]
```

### 2. เขียน brief
```
projects/[name]/01-brief/brief.md
```

### 3. รัน pipeline
```
/ux-figma-pipeline [project-name] [brief หรือ description]
```

---

## 🔄 Pipeline หลัก (`/ux-figma-pipeline`)

```
┌─────────────────────────────────────────────────────────┐
│ STAGE 1   UX Researcher                                 │
│ Brief → BA Analysis → UX Idea Card                      │
│ /skills:nlm-ask → ai-answers-[name].txt                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 2   UX Researcher                                 │
│ /skills:nlm-batch-research → Synthesis                  │
│ Research Doc → Narrative Critique                       │
│ ✅ Gate: "Verified & Approved"                          │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 3   UX/UI Producer                                │
│ Site Map → Screen Inventory                             │
│ /skills:user-flow                                       │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 4   UX/UI Producer                                │
│ React Shell + /skills:component-library init            │
│ Design tokens → Router → Layout                         │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 5   UX/UI Producer                                │
│ /skills:nlm-ask (wireframe) → /skills:screen-factory    │
│ /frontend-design (implement) → loop ทุก feature         │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 6   UX/UI Auditor                                 │
│ /skills:layout-review → /skills:wcag-audit              │
│ /skills:design-crit → audit-report-[name].md            │
│ /skills:export-prototype → 06-export/*.html             │
│ ✅ Gate: PASS / ❌ FAIL                                 │
└─────────────────────────────────────────────────────────┘
                         ↓ (optional)
┌─────────────────────────────────────────────────────────┐
│ Figma Pipeline  (/figma-pipeline)                       │
│ Figma Publisher                                         │
│ Design System → Key Screens → Code Connect              │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Commands Quick Reference

### Pipelines
```
/ux-figma-pipeline [project] [brief]
    → Full pipeline: Research → Prototype → Audit → Export

/figma-pipeline [project] [figma-url]
    → Prototype → Figma: Design System + Key Screens + Code Connect
```

### Research
```
/skills:nlm-ask [notebook-id] "[question]"
    → ถาม NotebookLM 1 ข้อ

/skills:nlm-batch-research [project] [notebook-id]
    → ถามทุกคำถามจาก ai-questions-[name].md อัตโนมัติ
```

### Design & Prototype
```
/skills:component-library init [project]
    → สร้าง shared component library

/skills:screen-factory [project] [feature] [screen1] ...
    → เพิ่ม screens ใหม่อย่างรวดเร็ว

/skills:user-flow [project]
    → Mermaid flow diagram + screen inventory

/skills:user-flow [project] --from-prototype
    → reverse-engineer flow จาก prototype

/skills:data-viz [project] [chart-type] [data-spec]
    → Charts, dashboards, data-heavy screens
```

### Quality & Export
```
/skills:layout-review [project] --report
    → Audit Sidebar + Topbar + Breadcrumb

/skills:wcag-audit [project]
    → ตรวจ WCAG 2.1 AA + report

/skills:wcag-audit [project] --fix
    → ตรวจ + แก้ไขอัตโนมัติ

/skills:design-crit [project]
    → Heuristic evaluation (Nielsen's 10)

/skills:export-prototype [project] --open
    → Export เป็น single HTML file แล้วเปิดดู

/skills:figma-flow [project]
    → สร้าง Prototype Flow Guide สำหรับ designer
```

---

## 📋 Workflow สำหรับ Project ขนาดใหญ่ (100–200 Frames)

### แนวทางหลัก: Module-based

```
projects/[name]/05-prototype/
├── index.html           ← Navigation hub (link ไปทุก module)
├── components.html      ← Shared component library
├── tokens.json          ← Design tokens
├── COMPONENTS.md        ← Component documentation
│
├── auth/                ← Login, Register, Forgot PW
├── dashboard/           ← Overview, Analytics
├── [feature-a]/         ← Feature A flow
└── [feature-b]/         ← Feature B flow
```

### ลำดับที่แนะนำ

```
1. /user-flow            → วาง flow ทั้งหมดก่อน (ป้องกัน missing screens)
2. /ux-figma-pipeline    → Research → Design tokens → Handoff notes
3. /component-library    → สร้าง library จาก prototype แรก
4. /screen-factory       → เพิ่ม screens ต่อโดยเร็ว
5. /wcag-audit           → ตรวจก่อน present
6. /design-crit          → Heuristic check ก่อน handoff
```

### เวลาโดยประมาณ

| งาน | เวลา |
|-----|------|
| Setup Design System + Components (ครั้งแรก) | 2–4 ชั่วโมง |
| เพิ่ม 1 feature (3–5 screens) | 15–30 นาที |
| เพิ่ม major flow (10–15 screens) | 1–2 ชั่วโมง |
| WCAG Audit + Fix | 30–60 นาที |
| Design Critique | 20–30 นาที |

---

## 📚 Knowledge Base

### วิธีเพิ่ม Insight Atom ใหม่
1. สร้างไฟล์: `knowledge/atoms/atom-YYYY-MM-DD-[slug].md`
2. อัปเดต index: `knowledge/index.md`

### 2-Year Rule
Atom ที่บันทึกต้องผ่านเกณฑ์:
- **Durable** — ยังใช้ได้ใน 2 ปีข้างหน้า
- **Context-independent** — ใช้ได้ข้าม project
- **Actionable** — มี design implication ที่ชัดเจน

### Atoms ที่มีอยู่ (จาก OCPB DataSure)
| Atom | สรุป |
|------|------|
| Trust Signal 3 Seconds | Status signal ต้องแสดงภายใน 3 วินาที |
| Pre-flight Checklist | แสดง requirements ก่อน form ลด abandonment |
| Auto-Save Draft | Multi-step form ต้อง auto-save ทุก 30 วินาที |
| Actionable Rejection | Rejection ต้องมี guidance ไม่ใช่แค่ error code |
| Mobile Page Weight 200KB | SSR + ≤200KB สำหรับ 3G coverage |
| Complete Status Model | Define ทุก status ก่อนออกแบบ UI |

---

## 🗂️ Projects

| Project | สถานะ | Screens | หมายเหตุ |
|---------|--------|---------|----------|
| **ocpb-datasure** | ✅ Complete | — | ผ่าน pipeline ครบทุก stage (reference project) |
| **ggp-poc** | 🔄 Prototype only | 4 screens | Factor → AI Suggestion → Analysis → Pipeline |
| **one-hris** | ✅ Prototype + Export | 20+ screens | Time/Leave/OT/Approval/HR/Admin — exported 2026-05-14 |

---

## 🔧 NotebookLM — Notebooks ที่มี

```bash
# ดู notebooks ทั้งหมด
scripts/nlm.sh list

# ดู notebooks ปัจจุบัน (2026-05-12)
```

| Notebook ID (ย่อ) | ชื่อ | เจ้าของ |
|-------------------|------|---------|
| 5fd9229b... | Bank Workflow System and Procurement ToR | Shared ✅ |
| f8205f14... | KTC Contract Dashboard and Rate Table | Owner |
| b0432179... | OCPB DataSure System Development ToR | Owner |
| 381e89e6... | Mastering Figma Automation with MCP | Owner |
| e11b2db9... | Automating NotebookLM with Claude Code | Owner |
| 12f10302... | Fintech KYC Onboarding Research | Owner |
| c04c65fd... | Credit Approval Platform | Owner |

> ⚠️ ถ้า error "account-routing mismatch" → `scripts/nlm.sh login`

---

## 🐛 Troubleshooting

### NotebookLM Error: account-routing mismatch
```bash
scripts/nlm.sh login
# เลือก Google account ที่ถูกต้อง
```

### Figma MCP: node ID invalid
- ตรวจ URL format: `?node-id=6711-8496` → ใช้ `6711-8496` (hyphen ไม่ใช่ colon)
- Section nodes บางตัวไม่ accessible — ลองดึงทีละ child frame แทน

### Prototype ใหญ่เกิน / ช้า
- แบ่ง module ออกเป็นไฟล์แยก
- รัน `/component-library init` เพื่อลด code ซ้ำ

### Context window เต็ม
- ดึง design context ทีละ frame (ไม่ใช่ทั้ง section)
- บันทึก intermediate output ลงไฟล์ก่อน process ต่อ

---

## 💡 Tips

- **รัน `/user-flow` ก่อนเสมอ** — วาง screen inventory ก่อนออกแบบ ป้องกัน missing screens
- **Component library = กุญแจของ large projects** — ลงทุนครั้งเดียว ใช้ซ้ำได้ตลอด
- **Mock data ต้องสมจริง** — ห้ามใช้ "Lorem ipsum" หรือ "Data 1, Data 2"
- **CSS variables เสมอ** — ห้าม hardcode สี (#23348d → var(--brand-primary-900))
- **ทุก screen ต้องมี Back** ยกเว้น screen แรก
- **Figma MCP เหมาะกับ extraction** — ไม่เหมาะกับการสร้าง 100+ frames ทีเดียว
