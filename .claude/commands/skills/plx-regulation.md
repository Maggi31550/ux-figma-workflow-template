# Perplexity Regulation & Compliance Research

ตรวจกฎหมาย/มาตรฐาน/ระเบียบ ที่เกี่ยวข้องกับ project — ออก compliance checklist พร้อม citations ของ official sources

## Usage
```
/skills:plx-regulation [project-name] "[topic]"
/skills:plx-regulation [project-name] --auto                 ← extract topics จาก BA Analysis
/skills:plx-regulation [project-name] --jurisdiction "Thailand"
/skills:plx-regulation [project-name] --topic PDPA --topic WCAG
```

## Use Cases

- **Data protection** — PDPA (Thailand), GDPR
- **Accessibility** — WCAG 2.1/2.2, มาตรฐาน ETDA
- **Industry-specific** — สคบ. (consumer), ธปท. (banking), อย. (food/drug)
- **Standards** — ISO 27001, มอก., ISO 9001
- **Government UX** — มาตรฐาน eGovernment, DGA

---

## Workflow

### STEP 1 — Identify Relevant Regulations

**Mode A: Manual** — user ระบุ topic ตรง argument

**Mode B: Auto-extract** — อ่าน `ba-analysis-[name].md` หา:
- Industry/sector (banking, healthcare, gov)
- Data types ที่จัดการ (personal, financial, health)
- User groups (children, elderly, disabled)
- Geography (Thailand-only, regional, global)

แล้ว map → relevant regulation list

### STEP 2 — Research Each Topic

ใช้ `perplexity_research` (สำคัญ — ต้องการ depth + citations):

```javascript
mcp__perplexity__perplexity_research({
  messages: [{
    role: "user",
    content: `[topic] ใน [jurisdiction] — ระบุ:

    1. **ชื่อกฎหมาย/มาตรฐาน** ฉบับล่าสุด (พร้อม พ.ศ./ปี)
    2. **Effective date** — เริ่มบังคับเมื่อไหร่
    3. **Scope** — ใครต้อง comply, ครอบคลุมอะไร
    4. **Key requirements** — ข้อหลักที่กระทบ UX/UI design
    5. **Penalty/Risk** — ถ้าไม่ compliant
    6. **Recent amendments** — แก้ไขใน 12 เดือนล่าสุด
    7. **Official source** — URL ของหน่วยงานทางการ
    8. **UX implication** — มีผลต่อ design ยังไง (consent screen, data display, accessibility)

    ใช้ official sources เป็นหลัก (ราชกิจจานุเบกษา, หน่วยงานกำกับดูแล) — citations ทุกข้อ`
  }],
  search_recency_filter: "month",
  return_citations: true
})
```

> **ใช้ `month` filter เสมอ** สำหรับ regulation — กฎหมายอัปเดตบ่อย

### STEP 3 — Build Compliance Checklist

แต่ละ topic แปลงเป็น actionable checklist สำหรับ design/dev:

```markdown
## PDPA Compliance Checklist

### Consent
- [ ] **Explicit consent** — แสดง consent screen ก่อนเก็บข้อมูล
  - UX implication: ห้าม pre-checked checkbox
  - Citation: [1] มาตรา 19 PDPA
- [ ] **Granular consent** — แยก consent ตามวัตถุประสงค์
- [ ] **Withdraw consent** — มี UI ให้ user ถอน consent ได้ตลอด

### Data Subject Rights
- [ ] **Right to access** — user ขอดูข้อมูลของตนได้
- [ ] **Right to delete** — มี flow ลบ account + ข้อมูล
- [ ] **Data portability** — export ข้อมูลเป็น machine-readable

### Notification
- [ ] **Privacy policy** — link ในทุก signup form
- [ ] **Breach notification** — มี flow แจ้งเตือนภายใน 72 ชม.

[etc.]
```

### STEP 4 — Cross-Reference กับ Prototype Plan

อ่าน screen inventory (ถ้ามี) — flag screens ที่ต้อง implement compliance:

```markdown
## Screen-Level Compliance Mapping

| Screen | Regulation | Required UX Element |
|--------|------------|---------------------|
| Signup | PDPA §19 | Consent checkbox (unchecked default) |
| Profile | PDPA §30 | "Export my data" button |
| Profile | PDPA §33 | "Delete my account" with confirm |
| All forms | WCAG 1.3.1 | Label + aria-label ทุก input |
| All buttons | WCAG 2.5.5 | Min size 44×44px |
| All pages | WCAG 1.4.3 | Contrast ratio ≥ 4.5:1 |
```

### STEP 5 — Format Output

`projects/[name]/02-research/plx-regulation-[name].md`:

```markdown
# Regulation & Compliance Research — [project-name]

**Date:** YYYY-MM-DD
**Jurisdiction:** [region]
**Topics covered:** [list]

---

## Executive Summary

[1–2 ย่อหน้า — risk level + key compliance requirements]

---

## Per-Topic Analysis

### [Regulation 1 — e.g., PDPA]

#### Overview
[ชื่อเต็ม, พ.ศ., effective date, oversight body]

#### Scope
[ใครต้อง comply]

#### Key Requirements (UX/UI relevant)
[list with citations]

#### Recent Updates (12 mo)
[any amendments]

#### Penalty
[fine/risk]

#### Official Source
[1] [URL ของกฎหมายต้นฉบับ]

#### UX Implications
[bullet list — แต่ละข้อ map กับ design decision]

[ทำซ้ำสำหรับทุก topic]

---

## Compliance Checklists

[per-regulation checklists — actionable]

---

## Screen-Level Mapping

[ตาราง screen × requirement]

---

## High-Risk Areas

จุดที่ต้องระวังพิเศษ — ถ้า skip จะมี legal/reputation risk สูง:

1. [risk 1 + mitigation]
2. [risk 2 + mitigation]

---

## All Citations

[full list with dates]
```

---

## Integration กับ Pipeline

หลัง regulation research เสร็จ:

1. **Update screen inventory** — เพิ่ม compliance requirements ต่อ screen
2. **Update microcopy** — consent text, privacy notice, error messages
3. **Update WCAG audit checklist** — auditor agent ใช้ requirements เหล่านี้
4. **Reference ใน handoff notes** — dev ต้องรู้ก่อน implement

---

## Tips
- **Official sources only** — ราชกิจจานุเบกษา, หน่วยงานทางการ. ไม่ใช้ blog/law firm summary เป็น primary
- **ระบุปีของกฎหมาย** — "PDPA พ.ศ. 2562" ไม่ใช่ "PDPA"
- **Cross-check Thai + English** — บางครั้ง English version มีรายละเอียดต่างจากต้นฉบับไทย
- **Date sensitivity** — ถ้า citation เก่ากว่า 6 เดือน → re-verify
- **อย่ายัด WCAG ทั้งเล่ม** — focus เฉพาะ Level AA criteria ที่ใช้กับ project

---

## Output

```
สร้าง: projects/[name]/02-research/plx-regulation-[name].md
ใช้ใน: Stage 5 Wireframe Analysis Gate, Stage 5B WCAG Audit
```
