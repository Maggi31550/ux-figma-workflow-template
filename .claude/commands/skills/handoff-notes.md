# Design Handoff Notes Generator

สร้าง / sync handoff spec สำหรับ developer และ designer — design tokens, component props, layout rules, interaction states, responsive breakpoints

## Usage
```
/skills:handoff-notes [project-name]                   ← generate จาก research + brief
/skills:handoff-notes [project-name] --sync            ← sync กับ prototype ที่มีอยู่ (extract from code)
/skills:handoff-notes [project-name] --feature [name]  ← เฉพาะ feature
```

> ใช้คู่กับ `design:design-handoff` (Anthropic system skill) — skill นี้ produce project-specific spec file

---

## Inputs

- `01-brief/` — TOR/Req files (สี hex, font, design reference)
- `02-research/ba-analysis-[name].md` — terminology, scope
- `02-research/ux-research-doc-[name].md` — personas, design directions
- `05-prototype/src/styles/tokens.css` (สำหรับ `--sync`)
- `05-prototype/src/components/ui/` (สำหรับ `--sync`)

---

## Output Structure

สร้าง `projects/[name]/03-design/handoff-notes-[name].md`:

```markdown
# Handoff Notes — [Project Name]
Date: YYYY-MM-DD | Status: [Draft / Approved]

## 1. Design Tokens

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | #23348d | Main CTA, active state, brand presence |
| `--color-primary-dark` | #1a276e | Hover/pressed state |
| `--color-secondary` | #089241 | Success, secondary CTA |
| `--color-error` | #d92d20 | Error, destructive action |
| `--color-warning` | #e59b1c | Warning, caution |
| `--color-text` | #1a1a2e | Body text |
| `--color-text-muted` | #6b7280 | Secondary text, hint |
| `--color-surface` | #ffffff | Card, modal background |
| `--color-background` | #f5f6fa | Page background |
| `--color-border` | #e5e7eb | Divider, input border |

### Typography
- **Font family:** Noto Sans Thai (Google Fonts), fallback sans-serif
- **Scale:**
  | Token | Size | Line height | Usage |
  |-------|------|-------------|-------|
  | `--text-xs` | 12px | 1.4 | Caption, helper text |
  | `--text-sm` | 14px | 1.5 | Body small, table cells |
  | `--text-base` | 16px | 1.5 | Body default |
  | `--text-lg` | 18px | 1.4 | Subheading |
  | `--text-xl` | 20px | 1.3 | h3 |
  | `--text-2xl` | 24px | 1.3 | h2 |
  | `--text-3xl` | 30px | 1.2 | h1 |
- **Weights:** 400 regular, 500 medium, 600 semibold, 700 bold

### Spacing (4px base)
| Token | Value |
|-------|-------|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-12` | 48px |

### Radius
| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 6px | Input, small button |
| `--radius-md` | 8px | Card, button |
| `--radius-lg` | 12px | Modal, large card |
| `--radius-full` | 9999px | Pill, badge |

### Shadows
| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,0.05) | Subtle elevation (card) |
| `--shadow-md` | 0 4px 6px rgba(0,0,0,0.07) | Hover state |
| `--shadow-lg` | 0 10px 15px rgba(0,0,0,0.1) | Modal, dropdown |

---

## 2. Layout Rules

### Grid
- **Container max-width:** 1280px (desktop), full-width below 1024px
- **Sidebar width:** 240px (collapsed: 64px)
- **Topbar height:** 56px
- **Page content padding:** 24px (desktop), 16px (mobile)

### Breakpoints
| Name | Min width | Use |
|------|-----------|-----|
| mobile | 0 | base |
| tablet | 640px | 2-col forms |
| desktop | 1024px | sidebar + content |
| wide | 1280px | max container |

### Responsive patterns
- Sidebar collapses เป็น drawer ที่ < 1024px
- Form 2-col → 1-col ที่ < 640px
- Table → card list ที่ < 768px

---

## 3. Component Specs

### Button
- **Variants:** primary | secondary | danger | ghost
- **Sizes:** sm (32px) | md (40px) | lg (48px)
- **States:** default, hover, active, focus, disabled, loading
- **Min width:** 44px (tap target)
- **Padding:** sm: 12px, md: 16px, lg: 24px (horizontal)
- **Loading:** spinner + text "กำลังโหลด..."

### Input
- **Height:** md (40px), sm (32px)
- **Border:** 1px solid `--color-border`, focus: `--color-primary`
- **Error state:** border `--color-error` + error message ใต้ field
- **Label:** above field, 14px, 500 weight
- **Hint:** below field, 12px, `--color-text-muted`

### Card
- **Padding:** 16px (default), 24px (large)
- **Background:** `--color-surface`
- **Border:** 1px solid `--color-border` หรือ shadow-sm
- **Radius:** 8px

### Badge
- **Tones:** critical (red), high (orange), medium (yellow), low (gray), success (green), info (blue)
- **Format:** icon + text (ห้ามสีอย่างเดียว)
- **Size:** 24px height, 12px padding horizontal

(... ครบทุก component ใน `src/components/ui/`)

---

## 4. Interaction States

### Hover
- Button: background darker shade
- Card (clickable): background `--color-background`
- Link: underline

### Focus
- Outline 2px solid `--color-primary`, offset 2px
- Visible only via keyboard (`focus-visible`)
- ห้าม `outline: none` ที่ไม่มี alternative

### Active / Pressed
- Button: bg primary-dark, scale(0.98) optional

### Disabled
- Opacity 50%, cursor not-allowed
- ห้ามมีปฏิกิริยา hover/active

### Loading
- Spinner ใน button (replace text)
- Skeleton placeholder ใน list/card
- Page-level loader สำหรับ initial load

---

## 5. Animation

- **Duration:** 150ms (micro), 250ms (default), 400ms (page transition)
- **Easing:** ease-out (default), ease-in-out (back-and-forth)
- **Library:** Motion (`motion/react`) — `<motion.div>` สำหรับ transition
- ห้าม animate > 60fps cost (large layout shift, blur ที่ผูกกับ scroll)

---

## 6. Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| Contrast | ดูตาราง color tokens — ทุก pair pass 4.5:1 |
| Tap target | ≥ 44×44px ทุก button/link |
| Focus ring | `focus-visible:outline-2 focus-visible:outline-[var(--color-primary)]` |
| Keyboard | Tab order ตามลำดับ visual, Esc ปิด modal |
| Form labels | `<label htmlFor>` หรือ `aria-label` |
| Color not sole indicator | Badge/Status: icon + text |
| Language | `<html lang="th">` |

---

## 7. Mock Data Patterns

- **ชื่อบุคคล (ไทย):** ใช้ชื่อสมมติที่สมจริง เช่น "สมชาย ใจดี", "ปัทมา ศรีวงศ์"
- **เลขประจำตัว:** ขึ้นต้น `1-XXXX-XXXXX-XX-X` (mock เท่านั้น)
- **วันที่:** `15 พ.ค. 2569` (Thai Buddhist year)
- **เงิน:** `1,250.00 บาท`
- **สถานะ:** ใช้คำที่เป็นทางการของ domain นั้นๆ

---

## 8. Edge Cases

| Case | Handling |
|------|----------|
| Empty list | EmptyState component พร้อม CTA |
| Loading > 5s | แสดง "กำลังประมวลผล โปรดรอ" |
| Network error | Banner ด้านบน + ปุ่ม "ลองอีกครั้ง" |
| Session expired | Modal + redirect ไป login หลัง 5s |
| Permission denied | แสดงข้อความ "คุณไม่มีสิทธิ์" + ปุ่มกลับ |
| Long text overflow | text-overflow: ellipsis + tooltip on hover |

---

## 9. Hand-off Checklist

ก่อนส่ง dev:
- [ ] tokens.css ครบทุก token ที่ระบุ
- [ ] Component library พร้อมใช้งาน (`src/components/ui/`)
- [ ] Screen Inventory ทุก screen มี wireframe หรือ Figma frame
- [ ] Microcopy ครบทุก action / state (ดู `microcopy-[name].md`)
- [ ] User flow diagram (ดู `user-flow-[name].md`)
- [ ] Audit report PASS (ดู `audit-report-[name].md`)
```

---

## `--sync` Mode

อ่าน prototype code แล้ว extract:
- Tokens จาก `tokens.css`
- Component variants จาก `src/components/ui/*.tsx` (parse props type)
- Breakpoints จาก `tailwind.config` / CSS media queries

Output: เปรียบเทียบกับ handoff-notes ปัจจุบัน → highlight diff

---

## Output
```
สร้าง: projects/[name]/03-design/handoff-notes-[name].md
```
