# Workflow Simulation — Large Project (100–200 Frames)

> ตัวอย่างนี้ใช้ระบบ "สคบ. GovPortal Plus" (สมมติ) เป็น project ที่มี 4 personas  
> และ 6 feature modules — รวม ~140 frames  
> ทุก command ที่แสดงเป็น command จริงในระบบนี้

---

## ก่อนเริ่ม: ทำไม 100–200 Frames ถึงต่างออกไป

| ขนาด | ≤30 frames | 50–80 frames | **100–200 frames** |
|------|-----------|--------------|---------------------|
| Strategy | Single file | Single file + components | **Module-based** |
| /screen-factory | ทีละ feature | ทีละ module | Batch per sprint |
| Figma | 1–2 pages | 2–3 pages | Pages per module |
| Research | 1 NLM notebook | 1 notebook | **Notebook per module** |
| Agents | Sequential | Sequential | **Parallel agents** |
| Risk | ต่ำ | ปานกลาง | Missing screens, drift |

**Rule of thumb:** ถ้า frame count > 80 → ต้องวางสถาปัตยกรรมก่อนออกแบบ

---

## Phase 0 — Architecture (ก่อนสร้างอะไรทั้งนั้น)

### 0.1 Frame Budget Breakdown

```
/user-flow govportal-plus
```

Output target:

```
## Module Breakdown

| Module | Happy Path | States | Edge Cases | TOTAL |
|--------|-----------|--------|------------|-------|
| Auth (Login, ThaID, OTP) | 6 | 8 | 4 | 18 |
| Onboarding (first-time) | 5 | 4 | 2 | 11 |
| Dashboard (3 personas) | 6 | 9 | 3 | 18 |
| Product Registration (biz) | 12 | 15 | 8 | 35 |
| QR Scan + Certificate (consumer) | 5 | 8 | 4 | 17 |
| Staff Review Queue | 8 | 12 | 6 | 26 |
| Settings + Profile | 4 | 6 | 2 | 12 |
| Shared: Errors + Empty States | — | — | 8 | 8 |
|  | | | **TOTAL** | **145** |
```

> ขั้นตอนนี้สำคัญที่สุด — ทีมมักลืม States และ Edge Cases จนทำให้ขาด 30–40 frames
> ใช้ตารางนี้เป็น "frame budget" ตลอด project

### 0.2 Figma Page Architecture (ก่อนสร้าง frame ใด ๆ)

```
Page 0: 🗂️ INDEX          ← navigation map, component library overview
Page 1: 🧩 Design System  ← tokens, colors, typography (สร้างก่อนสุด)
Page 2: 🔑 Auth           ← 18 frames
Page 3: 🏠 Dashboard      ← 18 frames
Page 4: 📦 Registration   ← 35 frames (module ที่ใหญ่สุด)
Page 5: 📱 QR Certificate ← 17 frames
Page 6: 👨‍💼 Staff Review   ← 26 frames
Page 7: ⚙️ Settings       ← 12 frames
Page 8: 🚨 Errors         ← 8 frames shared
Page 9: 🔬 Prototype Flow ← prototype connections (ทำหลังสุด)
```

### 0.3 Frame Naming Convention (enforce จากวันแรก)

```
[Module]-[Feature]-[Screen]-[State]

ตัวอย่าง:
  REG-Wizard-Step1-Default
  REG-Wizard-Step1-Validation-Error
  REG-Wizard-Step1-Loading
  QR-Scan-Result-Active
  QR-Scan-Result-Revoked
  STF-Queue-List-Empty
  STF-Queue-Detail-ReviewModal-Open
```

> ถ้า naming ไม่ consistent ตั้งแต่แรก → ไม่สามารถค้นหา frame ได้ใน 145 frames
> Figma search ใช้ได้ดีก็ต่อเมื่อ names ถูก format

---

## Phase 1 — Research at Scale (Module-level NLM)

### กลยุทธ์: Research per Module (ไม่ใช่ project-level เดียว)

```
# Module ใหญ่ต้องการ dedicated notebook
/nlm-batch-research govportal-plus --create "Registration Module Research" \
  --sources brief.md competitor-registration-flows.pdf

/nlm-batch-research govportal-plus --create "Staff Review Research" \
  --sources brief.md thai-gov-review-processes.pdf

# Module เล็กรวมกันได้
/nlm-batch-research govportal-plus --create "Auth + Onboarding Research" \
  --sources brief.md thaid-api-docs.pdf
```

### คำถาม Research ที่ scale-specific

สำหรับ 100–200 frame projects ต้องถามเพิ่ม:

```markdown
## Scale-specific Research Questions

Q-SCALE-1: Flow boundaries — เมื่อ user เปลี่ยน module ข้อมูล session ถูก handle อย่างไร?
Q-SCALE-2: Error recovery — ถ้า user drop-off กลางทาง saved state ถูกต้อง?
Q-SCALE-3: Cross-module navigation — user ต้องการ back ข้าม module บ่อยไหม?
Q-SCALE-4: Role-based variation — กี่ % ของ screens แตกต่างระหว่าง personas?
Q-SCALE-5: Progressive complexity — user ใหม่ vs. expert ต้องการ UI ต่างกันไหม?
```

---

## Phase 2 — Component Library (สร้างก่อนสร้าง screen ทุกหน้า)

### สิ่งที่เกิดขึ้นถ้าข้ามขั้นนี้

โดยทั่วไปถ้าเริ่ม screen โดยไม่มี component library:
- Screen 1–30: ออกแบบ inline, copy-paste
- Screen 31–60: สังเกตว่า card ดูไม่ consistent
- Screen 61+: refactor ใหม่ทั้งหมด (เสียเวลา 2–3 วัน)

### วิธีที่ถูกต้อง

```
# สร้าง component library จาก prototype ที่มีอยู่
/component-library init govportal-plus

# เพิ่ม components ที่ต้องการเฉพาะ project นี้
/component-library add govportal-plus "cert-status-badge"     # ACTIVE/PENDING/REVOKED
/component-library add govportal-plus "thaid-login-button"    # ปุ่ม ThaID branded
/component-library add govportal-plus "upload-dropzone"       # drag + tap to upload
/component-library add govportal-plus "review-action-bar"     # Approve/Reject/Hold
/component-library add govportal-plus "qr-preview-card"       # QR + cert info
```

### Component Library Checklist สำหรับ 100+ frames

```markdown
### Core (ต้องมีก่อนเริ่ม frame ใด ๆ)
- [ ] c-nav — navbar + tab menu
- [ ] c-bottom-bar — back + action
- [ ] c-card — generic content card
- [ ] c-badge — status colors
- [ ] c-toast — notification

### Module-specific (สร้างก่อน module นั้น)
- [ ] c-stepper — ก่อน Registration module
- [ ] c-table + c-filter-tabs — ก่อน Staff Review module
- [ ] c-chart — ก่อน Analytics module
- [ ] c-qr-display — ก่อน QR module

### Scale helpers (ต้องมีสำหรับ 100+ frames)
- [ ] c-skeleton — loading state ทุก screen
- [ ] c-empty-state — ทุก list screen
- [ ] c-error-boundary — network/server error
- [ ] c-session-expired — timeout overlay
```

---

## Phase 3 — Screen Factory (Batch Generation)

### กลยุทธ์: Sprint-based batching

ไม่ควรสร้างทุก screen พร้อมกัน — แบ่งเป็น sprint 2 สัปดาห์:

```
Sprint 1: Auth + Onboarding (29 frames) — foundation
Sprint 2: Dashboard (18 frames) — skeleton ที่ทุก persona เห็น
Sprint 3: Registration (35 frames) — module ใหญ่สุด
Sprint 4: QR + Staff Review (43 frames) — consumer + staff
Sprint 5: Settings + Errors (20 frames) — polish
```

### ตัวอย่าง Sprint 3 — Registration Module

```
/screen-factory govportal-plus "Product Registration" \
  "Business Info" "Product Details" "Upload Documents" \
  "Review & Confirm" "Payment" "Success" \
  --pattern=wizard
```

Screen Factory จะสร้าง:

```
REG-Wizard-Step1-Default         ← Business Info (happy path)
REG-Wizard-Step1-Validation      ← validation errors highlighted
REG-Wizard-Step1-Loading         ← skeleton while fetching business data
REG-Wizard-Step2-Default         ← Product Details
REG-Wizard-Step2-AutoFill        ← autocomplete suggestion state
REG-Wizard-Step2-Validation      ← required fields error
REG-Wizard-Step3-Default         ← Upload Documents empty
REG-Wizard-Step3-Uploading       ← progress state
REG-Wizard-Step3-Complete        ← all docs uploaded
REG-Wizard-Step3-Error           ← file type error
REG-Wizard-Step4-Default         ← Review & Confirm
REG-Wizard-Step4-EditModal       ← modal: edit section
REG-Wizard-Step5-Default         ← Payment method select
REG-Wizard-Step5-Processing      ← payment loading
REG-Wizard-Step5-Error           ← payment failed
REG-Wizard-Success               ← success + next steps
```

เพิ่มเติม (edge cases ที่ต้องขอแยก):

```
/screen-factory govportal-plus "Registration Edge Cases" \
  "Draft Saved" "Session Expired Warning" "Duplicate Product" \
  "Rejected Application" "Re-submission" \
  --pattern=form
```

### ความเร็วจริงๆ ของ Screen Factory

| Module | Frames | ใช้คำสั่ง | เวลาประมาณ |
|--------|--------|-----------|------------|
| Auth | 18 | 2 commands | 15 นาที |
| Dashboard | 18 | 2 commands | 12 นาที |
| Registration | 35 | 4 commands | 35 นาที |
| QR Certificate | 17 | 2 commands | 15 นาที |
| Staff Review | 26 | 3 commands | 25 นาที |
| Settings | 12 | 1 command | 8 นาที |
| Errors | 8 | 1 command | 5 นาที |
| **TOTAL** | **134** | **15 commands** | **~115 นาที** |

vs. ถ้าไม่มี component library → ~3–4 วัน

---

## Phase 4 — Figma Integration at Scale

### การ push screens เข้า Figma

สำหรับ 100+ frames **ห้าม push ทีเดียว** — push ทีละ module:

```
Sprint 1: /figma-generate-design govportal-plus --module auth --page 2
Sprint 2: /figma-generate-design govportal-plus --module dashboard --page 3
Sprint 3: /figma-generate-design govportal-plus --module registration --page 4
...
```

เหตุผล:
- Figma API timeout ถ้าส่งข้อมูลมากเกินไปในครั้งเดียว
- ทีม QA สามารถ review แต่ละ module ได้เลย โดยไม่ต้องรอทุก module
- ถ้ามี design change ตอนกลาง → แก้เฉพาะ module นั้น ไม่กระทบอื่น

### Figma Design System Page (Page 1) — สร้างก่อนสุด

```
Design System page ต้องมี:
├── Color Styles (จาก tokens.json)
│   ├── Brand/Primary-900: #23348d
│   ├── Brand/Secondary-700: #089241
│   ├── Status/Active: #089241
│   ├── Status/Pending: #f59e0b
│   └── Status/Revoked: #d92d20
├── Text Styles
│   ├── Heading/2XL, XL, LG
│   ├── Body/MD, SM
│   └── Label/MD, SM (Bold)
├── Effect Styles
│   ├── Shadow/Card
│   └── Shadow/Modal
└── Component Previews
    └── (thumbnails ทุก component จาก library)
```

---

## Phase 5 — Parallel Agent Strategy

### กรณีที่ได้ประโยชน์จาก Parallel Agents

สมมติ Research phase กำลังทำ Registration module ใน NLM
ขณะเดียวกัน Producer agent สามารถ:

```
Agent A (Researcher): NLM research → Registration flow insights
Agent B (Producer):   Build component library + Auth module screens (ไม่ต้อง wait)
```

ใน Claude Code ทำได้โดยตั้ง Agent ด้วย subagent_type ที่ต่างกัน
(ดู .claude/agents/ux-researcher.md และ ux-producer.md)

### ตัวอย่าง Parallel Work Plan

```
Week 1, Day 1-2:
  ┌─ Agent: Researcher ─────────────────────┐
  │ Stage 1: Brief + Research Questions     │
  │ Stage 1.5: NLM — Auth + Onboarding      │
  └─────────────────────────────────────────┘
  ┌─ Agent: Producer ───────────────────────┐
  │ /component-library init govportal-plus  │
  │ Add scale-specific components           │
  └─────────────────────────────────────────┘

Week 1, Day 3-5:
  ┌─ Agent: Researcher ─────────────────────┐
  │ Stage 1.5: NLM — Registration module    │
  │ Stage 2: Synthesis (Auth + Onboarding)  │
  └─────────────────────────────────────────┘
  ┌─ Agent: Producer ───────────────────────┐
  │ /screen-factory Auth module (18 frames) │
  │ /screen-factory Onboarding (11 frames)  │
  └─────────────────────────────────────────┘
```

---

## Phase 6 — Quality Control at Scale

### WCAG Audit — ทำแบบ Module ไม่ใช่ทั้งหมดพร้อมกัน

```
/wcag-audit govportal-plus --module auth
/wcag-audit govportal-plus --module registration
```

สิ่งที่ตรวจเฉพาะ large projects:

```markdown
### Scale-specific WCAG Checks

1. Focus management ข้าม modules
   → ทุก modal/overlay ต้อง trap focus
   → ทุก route change ต้อง announce ด้วย aria-live

2. Consistent labeling ข้าม 134 frames
   → "ถัดไป" ต้องเป็น "ถัดไป" ทุกที่ (ไม่ใช่บางที่เป็น "Next")
   → Status badge text ต้อง consistent (ACTIVE ≠ Active ≠ กำลังใช้งาน)

3. Color contrast สำหรับ Status badges
   → ACTIVE (green on white): ratio ≥ 4.5:1
   → PENDING (amber on white): ratio ≥ 4.5:1 ← มักพลาด

4. Form error messages
   → ทุก validation error ต้อง associated กับ input ด้วย aria-describedby
   → ไม่ใช่แค่ border สีแดง
```

### Design Critique — ทำหลัง Sprint

```
/design-crit govportal-plus --sprint 3 --module registration
```

ใน large project มักพบ:
- Registration wizard มี cognitive load สูงเกิน (too many fields per step)
- Staff Review ขาด bulk action (ทำได้ครั้งละ 1 เท่านั้น — bottleneck)
- Dashboard ของ 3 personas ต่างกันน้อยเกิน (lost personalization)

---

## Common Failure Modes at Scale (และวิธีป้องกัน)

### ❌ Failure 1: "Frame Drift"
**อาการ:** Screens ที่สร้างในสัปดาห์ที่ 1 ดูต่างจากสัปดาห์ที่ 3  
**สาเหตุ:** ไม่มี component library / ไม่ enforce design tokens  
**ป้องกัน:** `/component-library update` ทุกครั้งที่ token เปลี่ยน

### ❌ Failure 2: "Missing State Syndrome"
**อาการ:** Dev hand-off แล้วพบว่า 40% ของ states ไม่มี design  
**สาเหตุ:** วางแผน frame count แค่ happy path  
**ป้องกัน:** ใช้ตาราง Module Breakdown (Phase 0.1) ก่อนออกแบบ

### ❌ Failure 3: "Parallel Confusion"
**อาการ:** Agent A กำลัง research Registration ขณะที่ Agent B ออกแบบไปแล้ว  
**สาเหตุ:** Parallel work โดยไม่ sync handoff  
**ป้องกัน:** Research ต้อง "Verified & Approved" ก่อน Producer เริ่ม module นั้น

### ❌ Failure 4: "Figma File Bloat"
**อาการ:** Figma file หนัก ⇒ lag ⇒ ทีมทำงานช้า  
**สาเหตุ:** รูปภาพ/asset ไม่ compress + ไม่ใช้ components  
**ป้องกัน:** ทุก image ≤200KB, ใช้ Figma components ไม่ใช่ paste

### ❌ Failure 5: "NLM Context Overflow"
**อาการ:** NLM answers ใน Q11+ เริ่ม vague / ไม่ accurate  
**สาเหตุ:** notebook context เต็ม (too many sources)  
**ป้องกัน:** ≤10 sources per notebook, แบ่ง notebook ตาม module

---

## Milestone Checkpoints

```
✅ M0: Architecture complete
   → Frame budget table ✓
   → Figma page structure ✓
   → Naming convention ✓

✅ M1: Foundation ready
   → Component library (core set) ✓
   → Design System page in Figma ✓
   → Auth module: 18 frames ✓

✅ M2: Half-way
   → Dashboard: 18 frames ✓
   → Registration: 35 frames ✓
   → Research "Verified & Approved" for all modules ✓

✅ M3: Full coverage
   → All 134 frames created ✓
   → WCAG audit passed (all modules) ✓
   → Prototype links connected ✓

✅ M4: Hand-off ready
   → /wcag-audit --full passed ✓
   → /design-crit --full reviewed ✓
   → Handoff notes updated ✓
   → Microcopy finalized ✓
```

---

## Quick Reference — Commands สำหรับ Large Projects

```bash
# Phase 0: วางสถาปัตยกรรม
/user-flow [project]                         # สร้าง frame budget

# Phase 1: Research (per module)
/nlm-batch-research [project] --create "[Module] Research" --sources [files]

# Phase 2: Component Library
/component-library init [project]
/component-library add [project] [component]

# Phase 3: Screen Factory (per sprint)
/screen-factory [project] "[Module]" "[S1]" "[S2]" ... --pattern=[p]

# Phase 4: Figma (per module, not all at once)
/figma-generate-design [project] --module [module] --page [N]

# Phase 5: Quality Gates
/wcag-audit [project] --module [module]
/design-crit [project] --sprint [N]

# Tracking
/user-flow [project] --from-prototype       # ตรวจว่า prototype ครบ flow
```

---

*วันที่สร้าง: 2026-05-13 | ใช้ร่วมกับ ocpb-datasure เป็น reference scale ขนาดเล็ก (20 frames)*
