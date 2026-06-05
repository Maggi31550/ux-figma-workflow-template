# Design System Usage Rules

## Setup สำหรับ Project ใหม่

### 1. Link ใน prototype HTML

```html
<head>
  <!-- Step 1: DS base (tokens + component styles) -->
  <link rel="stylesheet" href="../../../knowledge/design-system/base.css">

  <!-- Step 2: Project theme (optional — เฉพาะถ้ามีสีหรือ font ต่าง) -->
  <link rel="stylesheet" href="theme.css">

  <!-- Step 3: Project-specific styles (เฉพาะ screen layout, ไม่ใช่ tokens) -->
  <style> ... </style>
</head>
```

> ลำดับสำคัญ — base.css ต้องมาก่อน theme.css เสมอ

### 2. Copy theme template

```bash
cp "projects/_template/theme.css" "projects/[project-name]/05-prototype/theme.css"
```

แก้เฉพาะบรรทัดที่ต้องการ uncomment ส่วนที่เหลือออก

---

## กฎการ Override

### ✅ สิ่งที่ทำได้ใน theme.css

**Override Layer 2 (Semantic tokens)**
```css
:root {
  /* เพิ่ม primitive ใหม่ก่อน */
  --ds-purple-800: #4C1D95;
  --ds-purple-500: #7C3AED;
  --ds-purple-100: #EDE9FE;

  /* Override semantic ให้ชี้ไป primitive ใหม่ */
  --color-brand-primary:       var(--ds-purple-800);
  --color-brand-primary-mid:   var(--ds-purple-500);
  --color-brand-primary-tint:  var(--ds-purple-100);

  /* เปลี่ยน font */
  --font-body: 'IBM Plex Sans Thai', 'Sarabun', sans-serif;
}
```

Component tokens (`--btn-primary-bg`, `--nav-bg`, ฯลฯ) จะอัปเดตอัตโนมัติ
ไม่ต้องแตะอะไรใน components.html

---

### ⛔ สิ่งที่ห้ามทำ

**ห้าม override Layer 3 ตรงๆ**
```css
/* ❌ อย่าทำ */
:root {
  --btn-primary-bg: #4C1D95;  /* bypass semantic layer */
  --nav-bg: purple;
}
```
เหตุผล: ถ้าทีมอื่น update DS ในอนาคต component tokens จะถูก override และไม่ได้รับ update

**ห้าม hardcode ค่าใน component class**
```css
/* ❌ อย่าทำ */
.ds-btn--primary { background: #4C1D95; }

/* ✅ ทำแบบนี้แทน — override semantic token ใน theme.css */
:root { --color-brand-primary: #4C1D95; }
```

**ห้ามแก้ไขไฟล์ใน knowledge/design-system/ โดยตรง**
ถ้าต้องการเพิ่ม component → แจ้งทีมและ update พร้อม re-audit

---

## เพิ่ม Component ใหม่ที่ไม่มีใน DS

ถ้า project ต้องการ component ที่ไม่มีใน `components.html`:

1. สร้างใน project's `index.html` ก่อน
2. ใช้ Layer 3 tokens (หรือ Layer 2 โดยตรง) ใน CSS
3. ถ้าใช้ใน ≥2 projects → เสนอเพิ่มเข้า DS (พร้อม WCAG check)

```css
/* ✅ Project-specific component ที่ใช้ DS tokens ถูกต้อง */
.cert-qr-card {
  background: var(--card-bg);          /* Layer 3 */
  border: 1px solid var(--card-border); /* Layer 3 */
  border-radius: var(--r-xl);           /* primitive */
  padding: var(--sp-6);                 /* primitive */
}
.cert-qr-card__status {
  color: var(--color-status-active-fg); /* Layer 2 */
}
```

---

## WCAG Requirement ต่อ Project

| สิ่งที่ต้องทำ | เมื่อไหร่ |
|-------------|---------|
| Copy `wcag-theme-check.md` template | ทุก project ใหม่ |
| ตรวจ contrast ratio เฉพาะสีที่ override | ก่อน hand-off |
| ตรวจ alt text, error messages, keyboard nav | ก่อน hand-off |
| Re-audit DS cert | เมื่อ DS เปลี่ยน primitive/component |

ดูรายละเอียด: `knowledge/design-system/wcag-cert.md`

---

## Figma Integration

ใช้ `tokens.json` สำหรับ Figma Variables:

```
Figma → Assets → Libraries → Import variables → เลือก tokens.json
```

หรือผ่าน Token Studio plugin:
```
Plugins → Token Studio → Import → JSON → เลือก tokens.json
```

ถ้า project มี theme override → สร้าง `theme-tokens.json` ที่ merge base + override
แล้ว import ใน Figma เป็น "Mode" ของ variable collection

---

## Token Naming Reference

| CSS Variable | JSON Path | Layer | Override? |
|-------------|-----------|-------|-----------|
| `--ds-blue-900` | `primitive.blue.900` | 1 | ➕ เพิ่มได้ |
| `--color-brand-primary` | `semantic.brand.primary` | 2 | ✅ override ได้ |
| `--btn-primary-bg` | `component.button.primary-bg` | 3 | ⛔ ห้ามแก้ตรง |
| `--sp-4`, `--r-md`, `--shadow-sm` | `primitive.spacing/radius/shadow` | 1 | ➕ global |
