# DS Overview — Single-Page HTML Gallery

สร้าง `overview.html` หน้าเดียวสำหรับให้ทีมเปิดดู Design System ทั้งหมด — tokens swatches + component gallery + token usage matrix

## Usage
```
/skills:ds-overview [project-name]
/skills:ds-overview [project-name] --open    ← เปิดในเบราเซอร์หลังสร้างเสร็จ
```

## Input

- `projects/[name]/07-design-system/tokens.json`
- `projects/[name]/07-design-system/components/*.card.md` + `.png`

## Output

- `projects/[name]/07-design-system/overview.html` — self-contained HTML (รวม CSS/JS inline)

---

## Page Structure

```
overview.html
├── Header
│   ├── Project name
│   ├── Version + last sync date
│   └── Figma link (ถ้ามี)
│
├── Navigation (sticky sidebar)
│   ├── Foundations
│   │   ├── Colors
│   │   ├── Typography
│   │   ├── Spacing
│   │   ├── Radius
│   │   └── Shadow
│   ├── Components (count)
│   └── Resources
│
├── Section: Foundations
│   ├── Color Palette
│   │   └── สำหรับแต่ละ color category:
│   │       ├── Swatch grid (50, 100, 200, ..., 900)
│   │       ├── Hex/HSL values
│   │       └── Contrast indicator (WCAG AA pass/fail)
│   ├── Typography Scale
│   │   └── ตัวอย่าง heading-1 ถึง body-small
│   ├── Spacing Scale
│   │   └── Visual bar showing relative sizes
│   ├── Radius
│   │   └── Rounded box samples
│   └── Shadow
│       └── Elevation samples
│
├── Section: Components
│   └── สำหรับแต่ละ component:
│       ├── Screenshot (.png embedded as <img>)
│       ├── Name + variant count + prop count
│       ├── Link → Component card (.card.md)
│       └── Link → Source code
│
└── Section: Resources
    ├── Figma URL
    ├── Handoff package URL
    ├── Repository URL
    └── Changelog (ล่าสุด 5 entries)
```

---

## Generation Logic

### Step 1: Parse tokens.json

อ่าน tokens แล้ว flatten เป็น sections:
- `color.*` → grouped by category (primary, neutral, status, ...)
- `spacing.*` → ordered by value
- `typography.*` → ordered by size (heading-1 down to body-small)
- `radius.*`, `shadow.*`

> หมายเหตุ: shadow ใน overview แสดง CSS `box-shadow` ตามปกติ แต่ใน **Figma** shadow คือ Effect Style
> ไม่ใช่ Variable (Figma API จำกัด) — ถ้าจะใส่ label ใน overview ให้เขียน "Figma: Effect Style" กำกับ section shadow
> เพื่อให้ dev เข้าใจว่า shadow ไม่ได้ sync ผ่าน token pipeline แบบ color/spacing

### Step 2: Build HTML

ใช้ template HTML แบบ self-contained:

```html
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Project] — Design System</title>
  <style>
    /* === Embed tokens as CSS variables === */
    :root {
      --color-primary-500: #1A73E8;
      --spacing-md: 16px;
      /* ... (all tokens from tokens.json) */
    }

    /* === Layout styles === */
    body {
      font-family: 'Noto Sans Thai', system-ui, sans-serif;
      margin: 0;
      display: grid;
      grid-template-columns: 240px 1fr;
      min-height: 100vh;
    }
    nav.sidebar { position: sticky; top: 0; ... }
    main.content { padding: 32px; max-width: 1200px; }

    /* === Component-specific === */
    .color-swatch { width: 80px; height: 80px; border-radius: 8px; ... }
    .swatch-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 16px; }
    /* ... */
  </style>
</head>
<body>
  <nav class="sidebar">
    <h2>[Project] DS</h2>
    <a href="#colors">Colors</a>
    <a href="#typography">Typography</a>
    ...
  </nav>
  <main class="content">
    <header>
      <h1>[Project] Design System</h1>
      <p>Version 1.0 · Last sync YYYY-MM-DD · <a href="[figma-url]">Open in Figma →</a></p>
    </header>

    <section id="colors">
      <h2>Colors</h2>
      <h3>Primary</h3>
      <div class="swatch-row">
        <div class="swatch-cell">
          <div class="color-swatch" style="background: #E8F0FE"></div>
          <code>primary.50</code>
          <small>#E8F0FE</small>
          <span class="wcag-badge fail">AA fail</span>
        </div>
        <!-- ... -->
      </div>
    </section>

    <section id="typography">...</section>
    <section id="spacing">...</section>
    <section id="components">
      <h2>Components (12)</h2>
      <div class="component-grid">
        <article class="component-card">
          <img src="data:image/png;base64,..." alt="Button variants">
          <h3>Button</h3>
          <p>3 variants · 6 props</p>
          <a href="./components/Button.card.md">View card →</a>
          <a href="../05-prototype/src/components/Button.tsx">Source →</a>
        </article>
        <!-- ... -->
      </div>
    </section>
  </main>
</body>
</html>
```

### Step 3: Embed assets

**Screenshots:**
- Convert PNG → base64 data URL
- Embed inline (HTML self-contained)
- หรือถ้า file ใหญ่เกิน 5 MB → ใช้ relative path `./components/Button.png`

**Fonts:**
- Use Google Fonts CDN: `<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;700&display=swap" rel="stylesheet">`

### Step 4: WCAG contrast check

สำหรับ color swatches — คำนวณ contrast vs `color.neutral.100` (background) และ `color.neutral.900` (text):

```javascript
function contrastRatio(fg, bg) {
  // ใช้ relative luminance formula
}
const ratio = contrastRatio(swatchColor, '#FFFFFF');
const badge = ratio >= 4.5 ? 'AA pass' : ratio >= 3 ? 'AA large' : 'AA fail';
```

### Step 5: Auto-open (optional)

ถ้า `--open` flag:
```bash
open projects/[name]/07-design-system/overview.html
```

---

## Visual Standards

| Element | Spec |
|---------|------|
| Sidebar width | 240px sticky |
| Content max-width | 1200px |
| Section gap | 64px |
| Card padding | 24px |
| Color swatch | 80×80px |
| Border radius | 8px (cards), 4px (swatches) |
| Typography | Noto Sans Thai |
| Background | `color.neutral.50` |
| Card surface | white + subtle shadow |

---

## Sections Required

- [ ] Header — project + version + Figma link
- [ ] Sidebar nav
- [ ] Foundations: Colors, Typography, Spacing, Radius, Shadow
- [ ] Components — grid with screenshots
- [ ] Resources — handoff package + repo
- [ ] Footer — generated timestamp

---

## Output Summary

```
✅ Generated overview.html (1.8 MB self-contained)
   - 47 token swatches/samples
   - 12 component cards
   - WCAG contrast badges
   - Sticky sidebar nav

🌐 Open: file:///.../07-design-system/overview.html

Next: /skills:ds-handoff [project-name]
```

---

## Tips

- **Single file** — เปิดได้แม้ไม่มี server (เหมาะส่ง stakeholder via email/chat)
- **Print-friendly** — ใช้ `@media print` ให้ลายเซ็น sidebar หายไปตอน print PDF
- **Responsive** — ใช้ `grid-template-columns: auto-fill` ให้ component grid ปรับขนาดบน mobile
- **Dark mode** (optional) — ถ้า tokens มี dark mode → toggle button ที่ header
