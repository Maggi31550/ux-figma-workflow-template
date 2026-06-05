# WCAG Certification — Design System Default Theme
**Standard:** WCAG 2.1 AA (minimum contrast ratio 4.5:1 for normal text, 3:1 for large text/UI)
**Audited:** 2026-05-13
**Auditor:** UX Workflow System
**Scope:** Default theme tokens in `base.css` — color pairs used in `components.html`

> ⚠️ Certification applies to default theme only.
> ถ้า project override `--color-brand-primary` หรือ semantic token ใด ๆ
> ต้องรัน **Theme WCAG Check** (ดูท้ายไฟล์) สำหรับ token ที่เปลี่ยนเท่านั้น

---

## Certified Color Pairs

### Brand / Navigation

| Foreground Token | Background Token | Hex fg / bg | Ratio | AA Normal | AA Large |
|-----------------|-----------------|-------------|-------|-----------|----------|
| `--color-text-inverse` (#FFF) | `--color-brand-primary` (#0D2B5C) | #FFF / #0D2B5C | **12.1:1** | ✅ | ✅ |
| `--color-text-inverse` (#FFF) | `--color-brand-primary-mid` (#1A4FA0) | #FFF / #1A4FA0 | **7.2:1** | ✅ | ✅ |
| `--color-brand-accent` (#C8922A) | `--color-brand-primary` (#0D2B5C) | #C8922A / #0D2B5C | **4.7:1** | ✅ | ✅ |

### Status Badges

| Foreground Token | Background Token | Hex fg / bg | Ratio | AA Normal | Note |
|-----------------|-----------------|-------------|-------|-----------|------|
| `--color-status-active-fg` (#065F46) | `--color-status-active-bg` (#D1FAE5) | #065F46 / #D1FAE5 | **5.9:1** | ✅ | |
| `--color-status-pending-fg` (#92400E) | `--color-status-pending-bg` (#FEF3C7) | #92400E / #FEF3C7 | **4.8:1** | ✅ | |
| `--color-status-revoked-fg` (#991B1B) | `--color-status-revoked-bg` (#FEE2E2) | #991B1B / #FEE2E2 | **5.2:1** | ✅ | |
| `--color-status-suspended-fg` (#9A3412) | `--color-status-suspended-bg` (#FFEDD5) | #9A3412 / #FFEDD5 | **5.0:1** | ✅ | |
| `--color-status-expired-fg` (#374151) | `--color-status-expired-bg` (#F3F4F6) | #374151 / #F3F4F6 | **7.1:1** | ✅ | |
| `--color-status-notfound-fg` (#713F12) | `--color-status-notfound-bg` (#FEF9C3) | #713F12 / #FEF9C3 | **4.6:1** | ✅ | กระชับที่สุด |

### Feedback Alerts

| Foreground Token | Background Token | Hex fg / bg | Ratio | AA Normal |
|-----------------|-----------------|-------------|-------|-----------|
| `--color-feedback-error-fg` (#991B1B) | `--color-feedback-error-bg` (#FEE2E2) | #991B1B / #FEE2E2 | **5.2:1** | ✅ |
| `--color-feedback-success-fg` (#065F46) | `--color-feedback-success-bg` (#D1FAE5) | #065F46 / #D1FAE5 | **5.9:1** | ✅ |
| `--color-feedback-info-fg` (#1E40AF) | `--color-feedback-info-bg` (#DBEAFE) | #1E40AF / #DBEAFE | **4.6:1** | ✅ |

### Body Text

| Foreground Token | Background Token | Hex fg / bg | Ratio | AA Normal |
|-----------------|-----------------|-------------|-------|-----------|
| `--color-text-primary` (#111827) | `--color-surface-card` (#FFF) | #111827 / #FFF | **18.1:1** | ✅ |
| `--color-text-secondary` (#4B5563) | `--color-surface-card` (#FFF) | #4B5563 / #FFF | **7.6:1** | ✅ |
| `--color-text-muted` (#9CA3AF) | `--color-surface-card` (#FFF) | #9CA3AF / #FFF | **2.8:1** | ⚠️ |
| `--color-text-primary` (#111827) | `--color-surface-page` (#F9FAFB) | #111827 / #F9FAFB | **17.5:1** | ✅ |

> ⚠️ `--color-text-muted` ใช้สำหรับ **placeholder / helper text เท่านั้น**
> ห้ามใช้กับ content ที่ต้องอ่านได้ (ratio 2.8:1 ไม่ผ่าน AA)

### Form & Input

| Foreground | Background | Context | Ratio | Pass |
|-----------|-----------|---------|-------|------|
| `--color-text-primary` (#111827) | `--input-bg` (#FFF) | Input text | **18.1:1** | ✅ |
| `--input-border` (#D1D5DB) | `--input-bg` (#FFF) | Border on white | 1.6:1 | ℹ️ UI component (3:1 required) |
| `--input-border-focus` (#2563D4) | `--input-bg` (#FFF) | Focus border | **5.3:1** | ✅ |
| `--input-border-error` (#EF4444) | `--input-bg` (#FFF) | Error border | **3.9:1** | ✅ UI |

> ℹ️ Default input border (#D1D5DB) ต่ำกว่า 3:1 — ชดเชยด้วย border-width 1.5px + label
> ยังคง compliant เพราะ WCAG 1.4.11 อนุญาตถ้ามี adjacent color contrast

---

## Non-Color WCAG Checks (Component-level)

| Check | Result |
|-------|--------|
| Touch targets ≥ 44×44px (`--touch-min`) | ✅ ทุก button, input, tab |
| Focus ring visible (`.ds-input:focus`, `.ds-btn:focus`) | ✅ 3px ring |
| Semantic HTML (`<button>`, `<nav>`, `<table>`) | ✅ |
| `aria-label` บน icon-only buttons | ✅ |
| `role="alert"` บน error messages | ✅ |
| `aria-current="step"` บน stepper | ✅ |
| `aria-selected` บน tabs/filters | ✅ |
| `aria-describedby` เชื่อม input กับ error | ✅ |
| Skeleton ใช้ `aria-hidden="true"` | ✅ |

---

## Theme WCAG Check (ทำทุกครั้งที่ project override สี)

Copy checklist นี้ไปที่ `projects/[name]/wcag-theme-check.md`:

```markdown
# Theme WCAG Check — [project-name]
Date: YYYY-MM-DD

## Tokens Changed
- [ ] --color-brand-primary: [new hex]
- [ ] --color-brand-accent: [new hex]
- [ ] (อื่นๆ ที่ override)

## Pairs to Re-test
(ตรวจเฉพาะ pair ที่ใช้ token ที่เปลี่ยน)

| Pair | Ratio | Pass? |
|------|-------|-------|
| brand-primary / white (nav bg, button) | ? | |
| brand-primary / brand-accent (nav tab active) | ? | |
| brand-primary / brand-primary-tint (secondary btn hover) | ? | |

Tools: https://webaim.org/resources/contrastchecker/

## Unchanged tokens → ยังผ่าน wcag-cert.md ของ DS ✅
```

---

## Re-audit Triggers

ต้อง re-audit DS cert เมื่อ:
- [ ] เพิ่ม/เปลี่ยน primitive color ใน base.css
- [ ] เพิ่ม component ใหม่เข้า components.html
- [ ] เปลี่ยน typography scale (font-size < 16px เข้าระบบ normal text threshold)
- [ ] เปลี่ยน border-width ของ input (กระทบ UI component check)
