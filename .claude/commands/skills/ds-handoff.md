# DS Handoff — Dev Handoff Package

Package design system สำหรับส่ง dev team — รวม tokens (multi-format), component cards, types, Figma link, integration guide

## Usage
```
/skills:ds-handoff [project-name]
/skills:ds-handoff [project-name] --zip       ← bundle เป็น .zip
/skills:ds-handoff [project-name] --platform web|mobile|both  ← เลือก format
```

## Input

- `07-design-system/tokens.json`
- `07-design-system/components/*.card.md` + `.png`
- `07-design-system/overview.html`
- `04-figma/figma-url-[name].md` (ถ้ามี)
- `05-prototype/src/components/` (สำหรับ TypeScript types)

## Output

```
07-design-system/handoff-package/
├── README.md                ← integration guide
├── tokens/
│   ├── tokens.json          ← DTCG canonical
│   ├── tokens.css           ← web (CSS custom properties)
│   ├── tokens.ts            ← TypeScript const
│   ├── tokens.js            ← plain JS (no types)
│   └── tokens.scss          ← SCSS variables (optional)
├── components/
│   ├── Button.card.md
│   ├── Button.png
│   ├── Button.types.ts      ← extracted prop types
│   ├── Card.card.md
│   └── ...
├── types/
│   └── design-system.d.ts   ← rolled-up type declarations
├── figma-url.txt            ← clickable URL
├── overview.html            ← copy ของ gallery
└── CHANGELOG.md
```

ถ้า `--zip` → bundle เป็น `[project]-design-system-vYYYY.MM.DD.zip`

---

## Generation Steps

### Step 1: Copy + transform tokens

จาก `tokens.json` (DTCG) สร้าง variants:

**tokens.css** (web):
```css
/* AUTO-GENERATED — do not edit. Source: tokens.json */
:root {
  --color-primary-500: #1A73E8;
  --spacing-md: 16px;
  /* ... */
}
```

**tokens.ts** (TypeScript):
```typescript
// AUTO-GENERATED — do not edit. Source: tokens.json
export const tokens = {
  color: {
    primary: { '500': '#1A73E8' } as const,
  },
  spacing: { md: 16 } as const,
} as const;

export type ColorToken = keyof typeof tokens.color;
export type SpacingToken = keyof typeof tokens.spacing;
```

**tokens.js** (plain ES module):
```javascript
// AUTO-GENERATED
export const tokens = { /* ... */ };
```

**tokens.scss** (optional):
```scss
$color-primary-500: #1A73E8;
$spacing-md: 16px;
```

### Step 2: Extract component types

จาก `src/components/[Name].tsx` extract:
- Props interface (export ชื่อ `[Name]Props`)
- Variant unions
- Public exports

สร้าง `handoff-package/components/[Name].types.ts`:

```typescript
// AUTO-EXTRACTED from prototype src/components/Button.tsx
export type ButtonVariant = 'primary' | 'secondary' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  onClick: (e: React.MouseEvent) => void;
  children: React.ReactNode;
}
```

### Step 3: Roll-up declaration file

สร้าง `handoff-package/types/design-system.d.ts`:

```typescript
import type { ButtonProps } from '../components/Button.types';
import type { CardProps } from '../components/Card.types';
// ...

export interface DesignSystem {
  tokens: typeof import('./tokens').tokens;
  components: {
    Button: ButtonProps;
    Card: CardProps;
    // ...
  };
}

export { ButtonProps, CardProps };
```

### Step 4: Generate README

`handoff-package/README.md`:

```markdown
# [Project] Design System — Handoff Package

**Version:** 1.0.0
**Generated:** YYYY-MM-DD HH:MM
**Source:** [Prototype repository](../../05-prototype/)
**Figma:** [Design file URL]

---

## Quick Start

### Web (React + CSS)

\`\`\`bash
# 1. Copy tokens
cp tokens/tokens.css src/styles/

# 2. Import in your app root
import './styles/tokens.css';

# 3. Use CSS variables
.button-primary {
  background: var(--color-primary-500);
  padding: var(--spacing-md);
}
\`\`\`

### Mobile (React Native / Expo)

\`\`\`bash
# 1. Copy tokens
cp tokens/tokens.ts src/styles/

# 2. Import + use
import { tokens } from './styles/tokens';

<View style={{ backgroundColor: tokens.color.primary['500'] }} />
\`\`\`

### TypeScript types

\`\`\`bash
cp -r types/ src/types/design-system/
\`\`\`

---

## Tokens Reference

ดู `tokens/tokens.json` สำหรับรายการเต็ม หรือเปิด `overview.html`

| Category | Count | File |
|----------|-------|------|
| Color | 24 | tokens.json → `color.*` |
| Spacing | 6 | tokens.json → `spacing.*` |
| Typography | 8 | tokens.json → `typography.*` |
| Radius | 4 | tokens.json → `radius.*` |
| Shadow | 5 | tokens.json → `shadow.*` |

---

## Components Reference

[count] components — แต่ละ component มี `.card.md` + screenshot + types

| Component | Variants | Props | Card |
|-----------|----------|-------|------|
| Button | 3 | 6 | [Button.card.md](./components/Button.card.md) |
| Card | 2 | 4 | [Card.card.md](./components/Card.card.md) |

---

## Updating

ทีม Design จะ update tokens ผ่าน Figma แล้ว sync กลับด้วย:

\`\`\`bash
/skills:ds-pull-tokens [project]
\`\`\`

หลัง sync ใหม่ — replace `tokens/` ใน package นี้แล้ว `npm install` ใหม่

---

## Conventions

- ✅ ใช้ CSS variable / token constant เสมอ — ห้าม hardcode hex/px
- ✅ ภาษาไทยทั้ง UI labels — ไม่มี English (เว้น code identifier)
- ✅ ทุก interactive ≥ 44×44px (WCAG)
- ✅ Semantic HTML — `<button>`, `<nav>`, `<main>` ใช้ตาม role
- ❌ ห้ามแก้ไฟล์ใน `tokens/` หรือ `components/` ใน package นี้ตรงๆ —
   ถ้าต้องแก้ → กลับไปที่ prototype หรือ Figma แล้ว re-export

---

## Support

- Design questions: ทีม Design (Figma)
- Component bugs: GitHub issue (prototype repo)
- Token updates: ต้องผ่าน Designer sync
\`\`\`

### Step 5: Bundle (ถ้า --zip)

```bash
cd projects/[name]/07-design-system
zip -r [name]-design-system-v$(date +%Y.%m.%d).zip handoff-package/
```

ขนาดเฉลี่ย: 1.5–3 MB (รวม screenshots)

---

## Validation

- [ ] tokens/ มี 4–5 ไฟล์ (json, css, ts, js, optional scss)
- [ ] ทุก component มี matching `.card.md`, `.png`, `.types.ts`
- [ ] README.md มี Quick Start ที่ copy-paste แล้วใช้ได้
- [ ] figma-url.txt มี URL จริง (ไม่ใช่ placeholder)
- [ ] CHANGELOG.md มี entry ของ release นี้
- [ ] Zip (ถ้ารัน) ขนาด < 10 MB

---

## Tips

- **Versioning** — semver: bump minor เมื่อเพิ่ม token, bump major เมื่อ rename/delete (breaking)
- **Distribution** — ส่ง zip ผ่าน Slack/email หรือ upload ไป shared drive
- **Repository pattern** — ถ้า dev team ใช้ monorepo → ผ่าน private npm package แทน zip
- **CDN** — ถ้าต้องการ host tokens online → upload tokens.css ไป CDN แล้วใส่ `<link>` ใน prototype

---

## Output Summary

```
✅ Generated handoff package
   📂 /handoff-package/
      ├── README.md (2.1 KB)
      ├── tokens/ (5 files, 14 KB)
      ├── components/ (36 files: 12 cards + 12 PNGs + 12 types)
      ├── types/design-system.d.ts (3 KB)
      ├── figma-url.txt
      ├── overview.html (1.8 MB)
      └── CHANGELOG.md

📦 Bundle: [name]-design-system-v2026.05.27.zip (1.9 MB)

📤 Ready to ship to dev team

Next: /skills:ds-push-figma [project-name] [figma-file-url]
```
