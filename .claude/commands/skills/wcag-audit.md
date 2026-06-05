# WCAG Accessibility Audit (React)

ตรวจ React/TSX prototype ตาม WCAG 2.1 AA — รายงาน issues + auto-fix ที่ทำได้

## Usage
```
/skills:wcag-audit [project-name]                    ← ตรวจอย่างเดียว
/skills:wcag-audit [project-name] --fix              ← ตรวจ + แก้ไขอัตโนมัติ
/skills:wcag-audit [project-name] --screen [path]    ← ตรวจเฉพาะหน้า เช่น "approval/queue"
```

> ใช้คู่กับ `design:accessibility-review` (Anthropic system skill) ได้ — skill นี้ให้ project context + auto-fix scripts

---

## Scope

`05-prototype/src/**/*.tsx` + `tokens.css` + `global.css`

ข้าม:
- `node_modules/`
- `vite.config.ts`, `*.config.*`
- `_mocks.ts`

---

## Checklist (WCAG 2.1 AA)

### 1. Color Contrast (1.4.3, 1.4.11)
ดึงค่า CSS variables จาก `tokens.css` แล้วคำนวณ contrast pair:

```bash
grep -E "^\s*--color-" projects/[name]/05-prototype/src/styles/tokens.css
```

```
Normal text (< 18pt):   ratio ≥ 4.5:1
Large text (≥ 18pt):    ratio ≥ 3:1
UI / icons:             ratio ≥ 3:1
```

Pairs ที่ต้องตรวจเสมอ:
- `--color-text` on `--color-background`
- `--color-text` on `--color-surface`
- `--color-text-muted` on `--color-surface`
- `--color-primary` text on white (primary button text)
- `--color-error`, `--color-success`, `--color-warning` on white/surface

Report format:
```
❌ FAIL  — --color-text-muted on --color-background: 3.8:1 (ต้องการ 4.5:1)
✅ PASS  — --color-primary on white: 7.2:1
```

### 2. Tap Target Size (2.5.5)

ตรวจทุก interactive element ใน TSX:

```bash
# หา <button> ที่ไม่มี height class
grep -rn "<button" projects/[name]/05-prototype/src/ --include="*.tsx" | grep -v "h-8\|h-10\|h-12\|min-h"

# หา <div onClick> — ต้องเปลี่ยนเป็น <button>
grep -rn "<div[^>]*onClick" projects/[name]/05-prototype/src/ --include="*.tsx"

# หา <a> ที่อาจไม่มี hit area พอ
grep -rn "<a " projects/[name]/05-prototype/src/ --include="*.tsx" | grep -v "h-\|py-\|p-3\|p-4"
```

```
Minimum:    44×44px (WCAG 2.1 AA)
Recommended: 48×48px (mobile)
```

### 3. Semantic HTML (1.3.1, 4.1.2)

```bash
# Anti-pattern checks
grep -rn "<div[^>]*onClick" src/ --include="*.tsx"        # ❌ ใช้ button แทน
grep -rn "<span[^>]*onClick" src/ --include="*.tsx"       # ❌
grep -rn "<input" src/ --include="*.tsx" | grep -v "label\|aria-label"  # ⚠️ ต้องมี label
grep -rn "<h[1-6]" src/ --include="*.tsx"                 # ตรวจ heading hierarchy
```

Checklist:
- [ ] ทุก clickable element เป็น `<button>` / `<a>` / `<input type="...">`
- [ ] Heading hierarchy ไม่ข้าม (h1 → h2 → h3 ไม่ใช่ h1 → h3)
- [ ] List ใช้ `<ul>` / `<ol>` ไม่ใช่ `<div>` ซ้ำๆ
- [ ] Form input มี `<label htmlFor>` หรือ `aria-label`

### 4. Alternative Text (1.1.1)

```bash
# Image ไม่มี alt
grep -rn "<img" src/ --include="*.tsx" | grep -v "alt="
```

Rules:
- Decorative: `alt=""`
- Informative: `alt="คำอธิบาย"`
- Lucide icons: ถ้า decorative ให้ `aria-hidden="true"`, ถ้า meaningful ให้ wrap ด้วย `<span className="sr-only">` หรือ `aria-label` บน parent

### 5. Keyboard Navigation (2.1.1, 2.4.3)

ตรวจ pattern ที่อาจ block keyboard:
```bash
grep -rn "tabIndex={-1}" src/ --include="*.tsx"            # ⚠️ verify จำเป็น
grep -rn "tabIndex={[1-9]" src/ --include="*.tsx"          # ❌ ไม่ควร > 0
grep -rn "onKeyDown" src/ --include="*.tsx"                # ตรวจ custom handler
```

Modal/dialog ต้องมี focus trap — verify ผ่าน Modal component ที่ใช้:
```bash
grep -rn "<Modal\|<Dialog" src/ --include="*.tsx"
```

### 6. Focus Visible (2.4.7)

```bash
# หา outline-none ที่ไม่มี focus-visible แทน
grep -rn "outline-none\|outline:.*none" src/ --include="*.tsx" --include="*.css" | grep -v "focus-visible"
```

ทุก focus removal ต้องมี `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-primary)]` แทน

### 7. Color Not Sole Indicator (1.4.1)

ตรวจ Badge/Status:
```bash
grep -rn "<Badge" src/ --include="*.tsx"
```

ทุก Badge ต้องมี:
- ✅ Icon + text (ไม่ใช่สีอย่างเดียว)
- ✅ Error state ใน form: icon `<AlertCircle />` + text "กรอกข้อมูลให้ครบ"

### 8. Form Validation (3.3.1, 3.3.3)

```bash
# หา form ที่อาจไม่มี validation
grep -rn "onSubmit\|<form" src/ --include="*.tsx"
```

ทุก form:
- [ ] Required fields แสดง error เมื่อ submit เปล่า
- [ ] Error message ระบุ field + วิธีแก้ (ไม่ใช่แค่ "Invalid")
- [ ] `aria-invalid` + `aria-describedby` ชี้ไป error message
- [ ] Error message ภาษาไทย เข้าใจง่าย

### 9. Language Attribute (3.1.1)

```bash
grep "lang=" projects/[name]/05-prototype/index.html
```

ต้องมี `<html lang="th">` (ภาษาไทยทั้งระบบ)

### 10. Text Resize (1.4.4)

ตรวจ font size hardcode px (ควรใช้ rem/var):
```bash
grep -rn "fontSize:.*[0-9]px\|text-\[1[0-9]px\]" src/ --include="*.tsx" --include="*.css"
```

---

## Auto-Fix Rules (`--fix`)

Claude แก้อัตโนมัติได้:

| Issue | Auto-fix |
|-------|----------|
| `<img>` ไม่มี `alt` | เพิ่ม `alt=""` (decorative) — ถ้าเป็น meaningful ให้ flag manual |
| `<div onClick>` | แทนด้วย `<button type="button" className="...">` |
| `outline-none` ไม่มี focus-visible | เพิ่ม focus-visible classes |
| `<input>` ไม่มี label / aria-label | wrap ด้วย `<label>` หรือเพิ่ม `aria-label` (ใช้ placeholder เป็น fallback) |
| Missing `lang="th"` | เพิ่มใน `index.html` |
| Tap target < 44px | ตรวจหา className → เพิ่ม `min-h-[44px] min-w-[44px]` |

Auto-fix scope ไม่รวม:
- Color contrast (ต้อง design decision)
- Heading hierarchy (ต้อง content rewrite)
- Form validation logic (ต้อง business logic)

---

## Workflow

### STEP 1 — TypeScript ผ่านก่อน
```bash
cd projects/[name]/05-prototype
npx tsc --noEmit
```
ถ้ามี error → หยุด แจ้ง user ก่อน

### STEP 2 — รัน Checks 1–10
รัน grep commands + analysis ใน TSX files

### STEP 3 — ถ้า `--fix` → Auto-fix
ใช้ Edit tool แก้ทีละไฟล์ — ทุก fix ต้องผ่าน TypeScript ใหม่

### STEP 4 — สร้าง Report

`projects/[name]/02-research/wcag-report-[name].md`:

```markdown
# WCAG 2.1 AA Audit Report — [Project Name]
Date: YYYY-MM-DD

## Summary
| Category | Pass | Fail | Warning | Auto-fixed |
|----------|------|------|---------|------------|
| 1. Color Contrast | 12 | 3 | 1 | 0 |
| 2. Tap Targets | 18 | 4 | 0 | 4 |
| 3. Semantic HTML | 22 | 2 | 0 | 2 |
| 4. Alt Text | 8 | 1 | 0 | 1 |
| 5. Keyboard Nav | OK | - | - | - |
| 6. Focus Visible | 14 | 3 | 0 | 3 |
| 7. Color Sole Indicator | 6 | 1 | 0 | 0 |
| 8. Form Validation | 5 | 2 | 0 | 0 |
| 9. Language | OK | - | - | 0 |
| 10. Text Resize | OK | - | - | - |

## 🔴 Critical (ต้องแก้ก่อน deliver)
### Color Contrast: --color-text-muted on --color-background
- Ratio 3.8:1 (ต้องการ 4.5:1)
- Locations: 12 files use `text-[var(--color-text-muted)]` บน background
- Fix: ปรับ token เป็น `#5a6478` (ได้ 5.1:1) หรือใช้สำหรับ large text เท่านั้น

## 🟠 Major
...

## 🟡 Minor
...

## ✅ Auto-fixed ในรอบนี้
- src/pages/Approval/Queue.tsx:42 — `<div onClick>` → `<button>`
- src/components/ui/Card.tsx:18 — เพิ่ม focus-visible style
- ...
```

---

## Output
```
สร้าง: projects/[name]/02-research/wcag-report-[name].md
แก้: ไฟล์ .tsx/.css ที่ระบุใน Auto-fixed (ถ้าใช้ --fix)
```
