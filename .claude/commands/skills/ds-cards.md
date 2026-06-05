# DS Cards — Component Cards (Markdown + Screenshot)

สร้าง component card 1 ไฟล์ต่อ component — มี screenshot จาก prototype จริง + variant table + props + states + a11y notes

## Usage
```
/skills:ds-cards [project-name]
/skills:ds-cards [project-name] [component-name]      ← 1 component
/skills:ds-cards [project-name] --refresh-screenshots ← regenerate ภาพอย่างเดียว
```

## Input

- `projects/[name]/05-prototype/src/components/` — source components
- `projects/[name]/07-design-system/tokens.json` — token reference
- Running dev server (สำหรับ screenshot)

## Output

```
projects/[name]/07-design-system/components/
├── Button.card.md
├── Button.png            ← screenshot
├── Card.card.md
├── Card.png
└── ...
```

---

## Workflow

### Step 1: Discover components + classify

Scan `src/components/`:
- Top-level `*.tsx` files = primitive components (Button, Card, Input, Badge, ...)
- ข้าม subfolders ที่ดูเหมือน feature (`pages/`, `layouts/`)
- ข้าม `index.ts`, types, hooks

**Classify ต่อ component — visual หรือ structural:**

| ประเภท | เกณฑ์ | Screenshot? |
|--------|-------|-------------|
| **visual** | มี visual styling ของตัวเอง (สี, border, bg, typography) | ✅ ต้องมี `.png` |
| **structural** | เป็น wrapper/layout ล้วน — render `<Outlet/>` หรือ `{children}` โดยไม่มี visual ของตัวเอง (เช่น `ContainedLayout` = max-width wrapper) | ❌ skip screenshot |

> structural component ยังต้องมี `.card.md` (อธิบาย purpose + layout spec + composition)
> แต่ใส่ note `> **Structural component** — no screenshot (layout wrapper, no own visual)` แทนภาพ
> **ห้ามให้ validation fail** เพราะ structural ไม่มี `.png` (แก้ bug P5: ContainedLayout)

### Step 2: Parse component metadata

แต่ละ component file อ่าน:
- **Props interface/type** — extract field names, types, defaults, JSDoc
- **Variants** — หา discriminated union ใน prop types (`variant: 'primary' | 'secondary'`)
- **States** — หา handlers/states (`onClick`, `disabled`, `loading`)
- **Token usage** — grep `var(--...)` ใน inline styles หรือ class names
- **A11y attributes** — หา `aria-*`, `role`, `tabIndex`

### Step 3: Generate screenshot

ใช้ Playwright MCP:

```javascript
// 1. Start dev server (ถ้ายังไม่ running)
// 2. Navigate ไปหน้า showcase (สร้าง dynamic ถ้าไม่มี)
// 3. Screenshot แต่ละ variant ในกรอบเดียว
mcp__playwright__browser_navigate({ url: "http://localhost:5173/__ds-showcase/Button" })
mcp__playwright__browser_take_screenshot({ filename: "Button.png", fullPage: false })
```

**Showcase route strategy:**
- ถ้า prototype มี `/__ds-showcase/[name]` route → ใช้เลย
- ถ้าไม่มี → สร้าง temporary HTML render โดย import component + render variants ในกรอบ 1200×600
- บันทึก PNG ลง `07-design-system/components/[Name].png`

### Step 4: Generate card markdown

ต่อ component สร้าง `.card.md` ตาม template นี้:

```markdown
# [ComponentName]

![Variants](./[ComponentName].png)

**Source:** [src/components/[ComponentName].tsx](../../../05-prototype/src/components/[ComponentName].tsx)
**Figma:** [Component link]({figma-component-url-or-tbd})
**Last sync:** {YYYY-MM-DD}
**Tokens used:** {N} (`color.primary.500`, `spacing.md`, `radius.md`)

---

## Variants

| Variant | Use case | Primary token |
|---------|----------|---------------|
| `primary` | Main CTA | `color.primary.500` |
| `secondary` | Alt action | `color.neutral.700` |
| `ghost` | Tertiary | transparent |

## Props

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `variant` | `'primary'\|'secondary'\|'ghost'` | `'primary'` | – | Visual style |
| `size` | `'sm'\|'md'\|'lg'` | `'md'` | – | Touch target |
| `disabled` | `boolean` | `false` | – | Disable interaction |
| `loading` | `boolean` | `false` | – | Show spinner |
| `onClick` | `(e: MouseEvent) => void` | – | ✅ | Click handler |
| `children` | `ReactNode` | – | ✅ | Button label |

## States

| State | Visual | Token |
|-------|--------|-------|
| Default | Solid bg | `color.primary.500` |
| Hover | Darker bg | `color.primary.600` |
| Active | Darker bg | `color.primary.700` |
| Focus | 2px ring | `color.primary.300` |
| Disabled | 50% opacity | – |
| Loading | Spinner + bg dim | `color.primary.500` + 80% opacity |

## Accessibility

- ✅ Semantic `<button>` element
- ✅ Min tap target: 44×44px (size `md` and up)
- ✅ `aria-label` required ถ้า icon-only (Claude เช็คใน source)
- ✅ Loading state: `aria-busy="true"`
- ⚠️ ตรวจสอบ contrast ratio ของ `ghost` variant บน background ต่างๆ

## Usage

```tsx
import { Button } from '@/components/Button';

<Button variant="primary" onClick={handleSave}>
  บันทึก
</Button>

<Button variant="ghost" size="sm" disabled>
  ยกเลิก
</Button>

<Button variant="primary" loading>
  กำลังบันทึก...
</Button>
```

## Do / Don't

✅ **Do** — ใช้ `primary` ปุ่มเดียวต่อ section/dialog (main CTA)
✅ **Do** — label ใช้ verb ภาษาไทย ("บันทึก", "ส่ง", "ค้นหา")
✅ **Do** — ใช้ `loading` แทน disable ปุ่มเมื่อรอ response

❌ **Don't** — ใช้ `primary` กับ destructive action (ใช้ `danger` variant แทน)
❌ **Don't** — ใช้ "OK" หรือ "Submit" — เป็น label ที่ user ไม่รู้ผลลัพธ์
❌ **Don't** — ใช้ icon-only ปุ่มโดยไม่ใส่ `aria-label`

## Changelog

| Date | Change | By |
|------|--------|-----|
| {YYYY-MM-DD} | Initial card from prototype v1.0 | ds-pipeline |
```

### Step 5: Update index

สร้าง/อัปเดต `07-design-system/components/README.md`:

```markdown
# Component Cards

Auto-generated from prototype. รัน `/skills:ds-cards [project]` เพื่อ refresh

| Component | Variants | Props | Card | Source |
|-----------|----------|-------|------|--------|
| Button | 3 | 6 | [Button.card.md](./Button.card.md) | [Button.tsx](../../05-prototype/src/components/Button.tsx) |
| Card | 2 | 4 | [Card.card.md](./Card.card.md) | [Card.tsx](../../05-prototype/src/components/Card.tsx) |
```

---

## Validation

- [ ] ทุก component ใน `src/components/*.tsx` (top-level) มี `.card.md`
- [ ] ทุก **visual** component มี matching `.png` (screenshot) — **structural** ได้รับการยกเว้น (มี note แทน)
- [ ] Token usage ตรวจสอบได้ใน `tokens.json` (ไม่มี hardcoded color ที่ไม่ใช่ token)
- [ ] ไม่มี English ใน "Usage" examples — ตัวอย่างใช้ภาษาไทย

---

## Tips

- **Showcase route แนะนำสร้างใน prototype** — `/src/pages/__DSShowcase/index.tsx` ที่ list ทุก component พร้อม variant matrix
- **Screenshot ต้องเป็น light theme** — ถ้า prototype มี dark mode ต้อง force light ก่อน screenshot
- **Composite components** (Form, Modal) ทำ card แยกต่างหากได้ — แต่ flag ว่า "composite" ใน card
- **Skip primitives** ที่เป็น re-export จาก lib (เช่น Lucide icon) — ทำ card เฉพาะ component ที่เราเขียนเอง

---

## Output Summary

```
✅ Generated 12 component cards
   - Primitives: Button, Card, Input, Select, Badge, Avatar, Checkbox, Radio
   - Composites: FormField, Modal, Toast, Notification

📷 Screenshots:
   - 12 PNGs at 1200×600
   - Total size: 1.4 MB

⚠️  Warnings:
   - Card.tsx uses hardcoded #888 — should reference color.neutral.500
   - Avatar.tsx missing aria-label for icon fallback

Next: /skills:ds-overview [project-name]
```
