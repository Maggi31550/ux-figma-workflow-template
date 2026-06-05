# DS Extract — Code → tokens.json (DTCG)

Parse prototype `tokens.css` (และ component files) → canonical `tokens.json` ตามมาตรฐาน DTCG (W3C Design Tokens Community Group)

## Usage
```
/skills:ds-extract [project-name]
/skills:ds-extract [project-name] --merge       ← merge เข้า tokens.json ที่มีอยู่
/skills:ds-extract [project-name] --dry-run     ← preview ไม่เขียนไฟล์
/skills:ds-extract [project-name] --3tier       ← upgrade เป็น 3-tier (primitive→semantic→component)
```

### `--3tier` flag (แนะนำสำหรับ project ใหม่)

ใช้ `scripts/token-migration/migrate-to-3tier.py` เพื่อ upgrade structure:

```bash
python3 scripts/token-migration/migrate-to-3tier.py [project-name]
```

Script จะ:
1. Hue analysis — แสดงกลุ่มสีทั้งหมดเพื่อให้ define primitive palette
2. Auto-build alias map (semantic → primitive) จาก hex matching
3. Verify round-trip (CSS output ต้อง identical กับ prototype)
4. เขียน tokens.json 3-tier + tokens.css ใหม่

**เงื่อนไขความสำเร็จ (จาก trailbook):**
- round-trip 0 diff (backward compat)
- `source.cssVar` อยู่ที่ semantic tier เท่านั้น (ไม่มีใน primitive — ไม่งั้น duplicate CSS)
- bank/special colors ที่ไม่มี palette equivalent → hardcode hex ที่ semantic ได้ (ไม่บังคับ alias)

> ดู knowledge atom: `knowledge/atoms/atom-2026-06-02-three-tier-token-architecture.md`

## Input

- `projects/[name]/05-prototype/src/styles/tokens.css` — CSS custom properties
- `projects/[name]/05-prototype/src/styles/tokens.ts` (ถ้ามี, สำหรับ mobile)
- ไฟล์ใน `src/components/` — ดึง computed styles ถ้า token ไม่อยู่ใน tokens.css

## Output

- `projects/[name]/07-design-system/tokens.json` (canonical)
- ถ้า `--dry-run` → แค่ print summary

---

## Extraction Logic

### Step 1: Parse tokens.css

อ่าน `tokens.css`:

```css
:root {
  --color-primary-500: #1A73E8;
  --color-neutral-100: #F5F5F5;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --radius-md: 8px;
  --font-family-base: 'Noto Sans Thai', sans-serif;
}
```

แปลงเป็น nested structure:

```javascript
{
  color: {
    primary: { "500": { value: "#1A73E8" } },
    neutral: { "100": { value: "#F5F5F5" } }
  },
  spacing: {
    sm: { value: "8px" },
    md: { value: "16px" }
  },
  radius: {
    md: { value: "8px" }
  },
  font: {
    family: {
      base: { value: "'Noto Sans Thai', sans-serif" }
    }
  }
}
```

**Naming convention:** `--<category>-<subcategory>-<modifier>` → nested object

#### Round-trip rule — บันทึก source CSS name (วิธีหลัก, แก้ bug P9)

> ทดสอบกับ trailbook พบว่า **การ derive CSS name จาก DTCG path ด้วยกฎอย่างเดียวไม่ครบ** (51/62)
> เพราะ (ก) extract เดิม rename token (`color.text.onPrimary` ↔ `--color-text-inverse`)
> (ข) extract เพิ่มชั้น grouping ที่ CSS ไม่มี (`color.role.hiker.default` ↔ `--color-hiker`)

**กฎหลัก:** ตอน extract ให้บันทึก **ชื่อ CSS variable ต้นทางตรง ๆ** ใน `$extensions` ต่อ token:

```json
{
  "color": { "role": { "hiker": { "default": {
    "$value": "#2d7a47", "$type": "color",
    "$extensions": { "source.cssVar": "--color-hiker" }
  }}}}
}
```

regenerate `tokens.css` = อ่าน `source.cssVar` ตรง ๆ → **round-trip 100% การันตี** ไม่ต้องเดา
(diff vs original ต้อง = 0 เสมอ — ถ้าไม่ใช่ = extract ผิด)

> นี่คือ invariant ที่สำคัญ: tokens.json ที่ extract มาต้อง regenerate กลับเป็น tokens.css เดิมได้ identical
> ถ้า round-trip ไม่ผ่าน = tokens.json ไม่ใช่ source of truth ที่เชื่อถือได้ (เหมือน trailbook ปัจจุบัน)

#### Inference fallback — Mapping Table (สำหรับ token ที่ authored JSON-first ไม่มี source.cssVar)

ถ้า token ไม่มี `source.cssVar` (เช่นสร้างใหม่ใน JSON) → ใช้กฎ derive ต่อไปนี้ (best-effort):

| CSS custom property | DTCG path | กฎ |
|---------------------|-----------|-----|
| `--color-primary` | `color.primary.default` | **leaf `default` → ตัด suffix ใน CSS** |
| `--color-primary-dark` | `color.primary.dark` | join ด้วย `-` |
| `--color-primary-bg` | `color.primary.bg` | join ด้วย `-` |
| `--color-neutral-500` | `color.neutral.500` | **numeric scale คงไว้เป็น key** |
| `--space-4` | `spacing.4` | **prefix alias: CSS `space` ↔ DTCG `spacing`** |
| `--radius-md` | `radius.md` | ตรงตัว |
| `--text-heading-1-size` | `typography.heading-1.fontSize` | composite (ดู Step 3) |

**กฎสรุป:**
1. **Prefix alias** — บาง project ใช้ CSS prefix สั้น (`space`→`spacing`, `text`→`typography`)
   บันทึก alias map ที่ใช้จริงไว้ใน `tokens.json` ใต้ key `$extensions.cssPrefixAlias` เพื่อ regenerate กลับได้ตรง
2. **`default` leaf** — ถ้า DTCG path ลงท้าย `.default` → CSS ตัด suffix (`color.primary.default` → `--color-primary`);
   ขาเข้า: CSS ที่ไม่มี modifier → leaf = `default`
3. **Numeric scale** (`50`,`100`,`500`,`900`) → เก็บเป็น string key ตามเดิม ไม่แปลงเป็น `default`
4. ที่เหลือ join/split ด้วย `-` ตรง ๆ

> ⚠️ ถ้า project มี prefix alias ที่ไม่ได้บันทึก → regenerate จะได้ CSS ชื่อผิด (เช่น `--spacing-4` แทน `--space-4`)
> ทำให้ prototype ที่อ้าง `var(--space-4)` พัง — ต้องบันทึก alias เสมอ

### Step 2: Infer `$type` + add metadata

ตาม DTCG spec:

| CSS value pattern | `$type` |
|-------------------|---------|
| `#RRGGBB`, `rgb()`, `hsl()` | `color` |
| `Npx`, `Nrem`, `Nem` | `dimension` |
| `Nms`, `Ns` | `duration` |
| `cubic-bezier(...)` | `cubicBezier` |
| font-family value | `fontFamily` |
| numeric weight | `fontWeight` |
| `0 Npx Npx ...` (box-shadow) | `shadow` |

### Step 3: Composite tokens (typography, shadow)

ถ้าพบ pattern แบบ:
```css
--text-heading-1-size: 32px;
--text-heading-1-weight: 700;
--text-heading-1-lineheight: 1.2;
--text-heading-1-family: var(--font-family-base);
```

รวมเป็น typography composite:
```json
{
  "typography": {
    "heading-1": {
      "$value": {
        "fontFamily": "{font.family.base}",
        "fontSize": "32px",
        "fontWeight": 700,
        "lineHeight": 1.2
      },
      "$type": "typography"
    }
  }
}
```

> ใช้ `{token.path}` syntax สำหรับ token reference (DTCG alias)

### Step 4: Add `$description`

สำหรับ semantic tokens — generate description จาก usage analysis:

```javascript
// Search across src/ for usage of var(--color-primary-500)
// แล้วเขียน description ที่อธิบาย purpose
```

ถ้าหาไม่เจอ → ใส่ `$description: ""` ให้ user เติมเอง

### Step 5: Output DTCG JSON

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "color": {
    "primary": {
      "500": {
        "$value": "#1A73E8",
        "$type": "color",
        "$description": "Primary CTA — used in 12 places: Button.tsx, Sidebar.tsx, ..."
      }
    }
  },
  "spacing": {
    "md": {
      "$value": "16px",
      "$type": "dimension",
      "$description": "Default gap between sections"
    }
  },
  "typography": {
    "heading-1": {
      "$value": {
        "fontFamily": "{font.family.base}",
        "fontSize": "32px",
        "fontWeight": 700,
        "lineHeight": 1.2
      },
      "$type": "typography"
    }
  }
}
```

### Step 6: Regenerate `tokens.css` + `tokens.ts`

ใช้ tokens.json เป็น source สร้าง:

**tokens.css:**
```css
/* AUTO-GENERATED from tokens.json — do not edit directly */
:root {
  /* color.primary */
  --color-primary-500: #1A73E8;
  /* spacing */
  --spacing-md: 16px;
  /* typography (flattened) */
  --typography-heading-1-font-family: 'Noto Sans Thai', sans-serif;
  --typography-heading-1-font-size: 32px;
  --typography-heading-1-font-weight: 700;
  --typography-heading-1-line-height: 1.2;
}
```

**tokens.ts (mobile):**
```typescript
// AUTO-GENERATED from tokens.json — do not edit directly
export const tokens = {
  color: {
    primary: { 500: '#1A73E8' }
  },
  spacing: { md: 16 },
  typography: {
    heading1: {
      fontFamily: 'Noto Sans Thai',
      fontSize: 32,
      fontWeight: '700' as const,
      lineHeight: 38,
    }
  }
} as const;
```

> Diff vs original `prototype/src/styles/tokens.css` — ถ้า identical = clean extract, ถ้าต่าง = warn user

---

## Hardcoded Value Gate (stop-and-ask, ไม่ warn เฉย ๆ)

ถ้าพบ hardcoded color/spacing/size ใน `src/components/` หรือ `src/pages/` ที่ไม่ได้ใช้ token →
**หยุด** แสดง file:line ทั้งหมด แล้วถาม user: `[fix]` / `[accept-debt]` / `[abort]`
(รายละเอียดใน `design-system-pipeline.md` → STAGE 8 Step 1 Gate) — ห้าม extract ต่อโดยไม่ได้ตัดสินใจ
เพราะ hardcoded value ที่หลุดเข้า DS = token ที่ไม่ตรงกับของจริง (bug P7)

---

## Validation

ก่อนเขียนไฟล์ ตรวจ:

- [ ] ไม่มี hardcoded value ค้าง หรือถ้ามี = ได้รับการ `accept-debt` แล้ว (มี log)
- [ ] ทุก token มี `$value`
- [ ] ทุก token มี `$type` (infer ได้ถูกต้อง)
- [ ] ไม่มี circular alias (`{a.b}` → `{a.c}` → `{a.b}`)
- [ ] ทุก alias `{path}` resolve ได้ (target token มีอยู่)
- [ ] Color values valid hex/rgb/hsl
- [ ] Dimension values มี unit (px/rem/em)

---

## Output Summary

```
✅ Extracted 47 tokens from tokens.css
   - color: 24 tokens (primary, neutral, semantic, status)
   - spacing: 6 tokens
   - radius: 4 tokens
   - typography: 8 composite tokens
   - shadow: 5 tokens

⚠️  3 warnings:
   - color.brand.legacy has no usage in src/ — consider removing
   - typography.body-2 uses hardcoded font-family — should alias {font.family.base}
   - --custom-margin not following naming convention — skipped

📝 Generated:
   - tokens.json (DTCG canonical)
   - tokens.css (regenerated, diff = 0 lines)
   - tokens.ts (mobile-ready)

Next: /skills:ds-cards [project-name]
```

---

## Tips
- รันบ่อยๆ ระหว่าง dev — keep `tokens.json` ในซิงค์
- ถ้า component ใช้ hardcoded color ที่ไม่อยู่ใน tokens → warn (ไม่ extract เป็น token ใหม่อัตโนมัติ)
- DTCG format รองรับ multi-mode (light/dark) — ถ้า prototype มี `:root.dark` ให้ extract เป็น `$modes`
