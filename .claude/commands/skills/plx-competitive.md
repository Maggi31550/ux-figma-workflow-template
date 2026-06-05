# Perplexity Competitive Analysis

สแกน competitor apps/services พร้อม feature matrix และ UX pattern reference — ใช้ Perplexity ดึงข้อมูล public ที่ตรวจสอบได้

## Usage
```
/skills:plx-competitive [project-name]
/skills:plx-competitive [project-name] [competitor1] [competitor2] ...
/skills:plx-competitive [project-name] --domain "[product-category]"
/skills:plx-competitive [project-name] --region "Thailand"
```

## Input

Discover competitors โดย:
1. **Explicit list** — argument บอกชื่อโดยตรง
2. **Auto-discover** — ถ้าไม่ระบุ ใช้ `--domain` ให้ Perplexity แนะนำ 5–8 ตัวก่อน
3. **From idea card** — อ่าน `ux-idea-card-[name].md` หา "Alternative Solutions" / "Reference apps"

---

## Workflow

### STEP 1 — Discover Competitors (ถ้ายังไม่ระบุ)

```javascript
mcp__perplexity__perplexity_ask({
  messages: [{
    role: "user",
    content: `ระบุ 5–8 [product-category] services/apps ที่นิยมใน [region] ปี 2025
              พร้อมระบุ:
              - ชื่อ + URL หลัก
              - ขอบเขตที่ทำ (B2B/B2C/Government)
              - กลุ่มผู้ใช้หลัก
              - จุดเด่น 1 ประโยค
              ใช้ source ที่ตรวจสอบได้`
  }],
  search_recency_filter: "year"
})
```

บันทึก competitor list → `02-research/plx-competitive-[name].md` (section "Discovered")

### STEP 2 — Per-Competitor Deep Dive

สำหรับ competitor แต่ละตัว — ถาม Perplexity ด้วย structured prompt:

```javascript
mcp__perplexity__perplexity_research({
  messages: [{
    role: "user",
    content: `วิเคราะห์ [competitor name] (${url}) ในมุม UX/UI:

    1. **Key features** — feature หลัก 5–7 ตัว
    2. **Onboarding flow** — ขั้นตอน sign-up → first value
    3. **Information architecture** — main navigation, page hierarchy
    4. **UI patterns** — design language (modern/classic), color palette, typography
    5. **Strengths** — UX จุดเด่นที่ user ชอบ (จาก review/social)
    6. **Weaknesses** — pain points ที่ user complain
    7. **Pricing/Access model** — free/paid/freemium
    8. **Recent updates** — feature launches ภายใน 12 เดือน

    ใช้ source ภาษาไทยถ้ามี — citations ทุก claim`
  }],
  search_recency_filter: "month",
  return_citations: true
})
```

### STEP 3 — Build Feature Matrix

รวมข้อมูลทุก competitor เป็นตาราง:

```markdown
## Feature Matrix

| Feature | [Comp A] | [Comp B] | [Comp C] | Our Plan |
|---------|----------|----------|----------|----------|
| QR Code scan | ✅ | ✅ | ❌ | ✅ |
| Multi-role admin | ✅ | ❌ | ✅ | ✅ |
| OCR receipt | ❌ | ✅ | ✅ | ✅ (planned) |
| Mobile-first | ✅ | ✅ | ❌ | ✅ |
| API integration | ✅ | ❌ | ✅ | TBD |
| Thai language | ✅ | ⚠️ partial | ❌ | ✅ |
```

### STEP 4 — UX Pattern Extraction

ระบุ pattern ที่ใช้ซ้ำใน 2+ competitors (= proven pattern):

```markdown
## Proven UX Patterns

### Pattern: Dashboard-first landing
**Used by:** Comp A, Comp B, Comp C
**Why it works:** [reason จาก citations]
**Apply to our prototype:** [การปรับใช้]
```

ระบุ pattern ที่ **ไม่ควรใช้** (anti-pattern ที่ user complain):

```markdown
## Anti-Patterns to Avoid

### Anti-pattern: 4-step signup form
**Found in:** Comp B
**User feedback:** "ยาวเกินไป — abandon rate สูง"
**Citation:** [URL]
```

### STEP 5 — Format Output

`projects/[name]/02-research/plx-competitive-[name].md`:

```markdown
# Competitive Analysis — [project-name]

**Date:** YYYY-MM-DD
**Region:** [region]
**Competitors analyzed:** N
**Source:** Perplexity sonar-pro + research mode

---

## Executive Summary

[2–3 ย่อหน้า — landscape overview + ช่องว่างที่ our product fill ได้]

---

## Discovered Competitors

[ตารางย่อ — name, URL, scope, target user]

---

## Per-Competitor Profiles

### [Comp A]
**URL:** [link]
**Model:** [B2B/B2C]

#### Strengths
- [item with [1] citation]

#### Weaknesses
- [item with [1] citation]

#### Notable UX patterns
- [pattern + screenshot URL if available]

[ทำซ้ำสำหรับทุก competitor]

---

## Feature Matrix

[ตาราง side-by-side]

---

## Proven UX Patterns (Apply)

[3–5 patterns]

---

## Anti-Patterns (Avoid)

[2–4 anti-patterns]

---

## Recommended Differentiators

จากการวิเคราะห์ — สิ่งที่ our prototype ควรเน้นเพื่อ stand out:

1. [differentiator 1 พร้อมเหตุผล]
2. [differentiator 2]
3. [differentiator 3]

---

## All Citations

[full list — [1] through [N]]
```

---

## Integration กับ Pipeline

หลัง competitive analysis เสร็จ:

1. **Update UX Idea Card** — เติม "Alternative Solutions" ด้วย proven patterns
2. **Feed into Stage 3 Synthesis** — pain points ของ competitors = ของเราต้องหลีกเลี่ยง
3. **Reference ใน Stage 5 Wireframe** — ตอน implement feature ดู pattern ที่ proven แล้ว

---

## Tips
- **Specific over generic** — "Thai government QR verification apps" ดีกว่า "verification apps"
- **Mix sources** — บางครั้ง app review site (Capterra, G2) มีรายละเอียดมากกว่า official site
- **Screenshot capture** — ถ้า Perplexity ระบุ URL screen → ส่งต่อ Playwright MCP capture ภาพ
- **Citation date** — ถ้า source เก่ากว่า 1 ปี ระบุชัดเจน (feature อาจเปลี่ยนแล้ว)
- **Localization check** — competitor ที่ไม่มี Thai = ช่องว่างให้เรา

---

## Output

```
สร้าง: projects/[name]/02-research/plx-competitive-[name].md
ใช้ใน: Stage 3 Synthesis, Stage 5 Wireframe Analysis Gate
```
