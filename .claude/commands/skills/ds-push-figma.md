# DS Push Figma — Push Variables + Components → Figma

Push `tokens.json` เป็น Figma Variables + key components ไปยัง section "🎨 Design System" ใน Figma file ของ prototype + สร้าง Code Connect mappings

## Usage
```
/skills:ds-push-figma [project-name] [figma-file-url]
/skills:ds-push-figma [project-name] [figma-file-url] --tokens-only       ← push variables อย่างเดียว
/skills:ds-push-figma [project-name] [figma-file-url] --components-only   ← push components อย่างเดียว
/skills:ds-push-figma [project-name] [figma-file-url] --dry-run           ← preview ไม่เขียน Figma
```

## Prerequisites

- `tokens.json` พร้อม (รัน `/skills:ds-extract` ก่อน)
- Component cards พร้อม (รัน `/skills:ds-cards` ก่อน)
- Figma file URL ที่ user มีสิทธิ์ edit
- Figma MCP เชื่อมต่อแล้ว

---

## Critical: โหลด skill ก่อนทุกครั้ง (MANDATORY)

ก่อนเรียก `use_figma` ต้องโหลด **2 skills คู่กันเสมอ**:

```
Skill: figma-use               ← HOW: วิธีเรียก Plugin API ให้ถูก (กัน error)
Skill: figma-generate-library  ← WHAT: สร้าง variables/components ระดับ production
```

- `figma-use` — บังคับก่อน `use_figma` ทุกครั้ง (ไม่มีข้อยกเว้น)
- `figma-generate-library` — บังคับสำหรับ Step 3 (variables) + Step 5 (components) เพราะสอน
  ลำดับและโครงสร้างที่ทำให้ component มี variant set + variable binding จริง
  (ถ้าไม่โหลด → component ออกมาเป็น frame เปล่า ใช้งานใน Figma ไม่ได้ — ดู bug P1)

จากนั้นค่อยทำ operations ด้านล่าง

---

## Workflow

### Step 1: Verify file access + Preflight plan tier

```javascript
const me = mcp__claude_ai_Figma__whoami()
mcp__claude_ai_Figma__get_metadata({ url: figmaFileUrl })
```

ตรวจ 2 อย่าง:

**1a. Edit permission** — user แก้ไฟล์ได้ไหม (ถ้าไม่ได้ → STOP)

**1b. Code Connect availability (preflight — กัน bug P2):**
Code Connect ต้องใช้ **Figma Organization/Enterprise plan** เท่านั้น ตรวจตั้งแต่ตอนนี้
(ไม่ใช่ไปรู้ตอน Step 6 หลัง push ทุกอย่างเสร็จแล้ว เหมือน trailbook)

```javascript
// ตรวจจาก whoami / metadata ว่า plan รองรับ Code Connect ไหม
// ถ้าตรวจไม่ได้ตรง ๆ → ลอง get_code_connect_suggestions แบบ probe 1 ครั้ง
//   - สำเร็จ → CODE_CONNECT_ENABLED = true
//   - error "requires Organization/Enterprise" → CODE_CONNECT_ENABLED = false
let CODE_CONNECT_ENABLED = (plan === "org" || plan === "enterprise")
```

- `CODE_CONNECT_ENABLED = true` → Step 6 ทำ Code Connect ตามปกติ
- `CODE_CONNECT_ENABLED = false` → **แจ้ง user ทันที** ว่ารอบนี้ skip Code Connect
  และ Step 6 จะเขียน `.figma.ts` mapping fallback ลง code แทน (ใช้ได้เมื่อ upgrade plan ภายหลัง)

### Step 2: Find or create "🎨 Design System" page

```javascript
mcp__claude_ai_Figma__use_figma({
  prompt: `
    1. Find page with name "🎨 Design System" or "Design System"
    2. If not exists → create new page after current page
    3. Return page ID
  `,
  figma_file_url: figmaFileUrl
})
```

### Step 3: Push variables (DTCG → Figma Variables)

แปลง tokens.json เป็น Figma variable collections:

| DTCG path | Figma collection | Variable mode |
|-----------|------------------|---------------|
| `color.*` | `Color` | Light (default), Dark (ถ้ามี) |
| `spacing.*` | `Spacing` | Default |
| `radius.*` | `Radius` | Default |
| `typography.*` | `Typography` | Default (composite — แตกเป็น sub-vars) |
| `shadow.*` | **Effect Style** (ไม่ใช่ Variable) | — |

> ⚠️ **Shadow เป็น Effect Style ไม่ใช่ Variable** (Figma Variables API ยังไม่รองรับ shadow/effect type)
> - push `shadow.*` เป็น **Effect Styles** (`Shadow/sm`, `Shadow/md`, ...) ผ่าน use_figma สร้าง style
> - component bind shadow ผ่าน **apply effect style** ไม่ใช่ bound variable
> - ใน sync log ให้นับแยก: "Variables: N + Effect Styles: M" (ไม่รวมกัน — trailbook: 87 vars + 5 effect styles)
> - Stage 9 token sync (pull/push) **ไม่ครอบคลุม shadow** เพราะไม่ใช่ variable — ถ้า designer แก้ shadow
>   ต้อง re-run ds-push-figma `--components-only` หรือ manual (1-way code→Figma เหมือน component)

```javascript
mcp__claude_ai_Figma__use_figma({
  prompt: `
    Create or update variable collection "Color":
    - Mode: Light
    - Variables (resolved from tokens):
      ${tokens.color.map(t => `${t.path} = ${t.value}`).join('\n')}

    For typography composites — split into:
    - typography/heading-1/fontFamily
    - typography/heading-1/fontSize
    - typography/heading-1/fontWeight
    - typography/heading-1/lineHeight

    Naming: use "/" separator (e.g., "color/primary/500")
  `
})
```

**Naming convention ใน Figma:**
- `color/primary/500` (Figma แสดงเป็น tree)
- `spacing/md`
- `typography/heading-1/font-size`

### Step 4: Create Foundation frames

ใน page "🎨 Design System" สร้าง frames:

```
🎨 Design System (page)
├── Foundations (frame)
│   ├── Color Palette
│   │   └── Color swatches (bound to variables)
│   ├── Typography Scale
│   │   └── Text samples (bound to typography vars)
│   ├── Spacing Scale
│   ├── Radius Scale
│   └── Shadow Scale
└── Components (frame)
    └── [Component variants]
```

**สำคัญ:** ทุก swatch/sample bind กับ variable — ไม่ใช่ hardcode color

### Step 5: Push key components

> ⚠️ **ก่อนเริ่ม Step นี้ต้องโหลด `figma-generate-library` + `figma-use` แล้ว** (ดู section Critical ด้านบน)
> ถ้ายังไม่โหลด → component จะออกมาเป็น frame เปล่า ไม่มี variant property set / variable binding (bug P1)

สำหรับ component สำคัญ (Button, Card, Input, Badge — top 5–8) ทำ **ทีละตัว** (push → verify → ถัดไป):

#### 5A: Create component (per component)

ตาม pattern ของ `figma-generate-library` — ต้องครบ 3 อย่าง: variant property set, auto-layout, variable bindings

```javascript
mcp__claude_ai_Figma__use_figma({
  prompt: `
    Create a COMPONENT SET "Button" in the Components frame (not a plain frame).
    Define variant properties so Designer can switch variants in the panel:
    - variant: primary | secondary | ghost
    - size: sm | md | lg
    - state: default | hover | active | disabled

    BIND variables (do NOT hardcode hex/px):
    - Background fill → variable color/primary/500 (primary variant)
    - Horizontal/vertical padding → variable spacing/md
    - Corner radius → variable radius/md
    - Text style → typography/body-1 variables

    Use auto-layout (hug contents, gap = spacing/sm).
    Add component description copied from Button.card.md.
  `,
  figma_file_url: figmaUrl
})
```

#### 5B: Verify component is production-grade (NOT placeholder)

หลัง create แต่ละตัว — ตรวจว่าเป็น real component ไม่ใช่ frame เปล่า:

```javascript
const ctx = await mcp__claude_ai_Figma__get_design_context({
  node_id: "[component node ID just created]",
  figma_file_url: figmaUrl
})

// FAIL conditions → rebuild component ก่อนไปตัวถัดไป:
// 1. ไม่มี componentPropertyDefinitions (= frame ธรรมดา ไม่ใช่ component set)
// 2. fill/padding/radius เป็น raw value ไม่ได้ผูก variable (boundVariables ว่าง)
// 3. ไม่มี auto-layout (layoutMode === "NONE")
```

**Component Verification Checklist (ต้องผ่านทุกข้อต่อ component):**

```
[ ] เป็น Component Set (มี componentPropertyDefinitions) — ไม่ใช่ frame เปล่า
[ ] Variant properties สลับได้ใน Figma panel (variant/size/state)
[ ] Fill/stroke ผูก color variable (boundVariables ไม่ว่าง)
[ ] Padding/gap ผูก spacing variable
[ ] Corner radius ผูก radius variable
[ ] Text ผูก typography variable หรือ text style
[ ] มี auto-layout (layoutMode = HORIZONTAL/VERTICAL)
[ ] มี component description จาก .card.md
```

ถ้าข้อใดข้อหนึ่ง fail → อย่าข้ามไป component ถัดไป ให้ rebuild ตัวนั้นก่อน
(component เปล่าที่ push ไปแล้วถือว่าเสีย — Designer ใช้ต่อไม่ได้)

### Step 6: Add Code Connect mappings (conditional — ตาม preflight Step 1b)

**กรณี A — `CODE_CONNECT_ENABLED = true` (Org/Enterprise plan):**

ผูก Figma component ↔ prototype source file ผ่าน MCP:

```javascript
mcp__claude_ai_Figma__get_code_connect_suggestions({ url: figmaFileUrl })

mcp__claude_ai_Figma__add_code_connect_map({
  figma_node_id: "[Button component node ID]",
  code_path: "src/components/ui/Button.tsx",
  example: `<Button variant="primary">บันทึก</Button>`
})

mcp__claude_ai_Figma__send_code_connect_mappings()
```

> Dev ที่ใช้ Figma Dev Mode จะเห็น code snippet ทันทีที่เลือก component

**กรณี B — `CODE_CONNECT_ENABLED = false` (Pro plan หรือต่ำกว่า):**

อย่าเรียก MCP Code Connect (จะ error) — เขียน **`.figma.ts` mapping fallback** ลง code แทน
ที่ `05-prototype/src/components/ui/[Name].figma.ts` ต่อ component:

```typescript
// Button.figma.ts — Code Connect mapping (offline)
// ใช้ได้เมื่อ upgrade เป็น Org/Enterprise plan แล้วรัน `figma connect publish`
import figma from '@figma/code-connect'
import { Button } from './Button'

figma.connect(Button, '[figma-node-url]', {
  props: {
    variant: figma.enum('variant', { primary: 'primary', secondary: 'secondary', ghost: 'ghost' }),
    children: figma.string('label'),
  },
  example: (props) => <Button variant={props.variant}>{props.children}</Button>,
})
```

แล้วบันทึกใน sync log ว่า `Code Connect: deferred (.figma.ts written, requires Org/Enterprise to publish)`

### Step 7: Update sync log + **write per-token baseline** (สำคัญต่อ Stage 9)

เขียน `07-design-system/figma-sync-log.md` — **ต้องมี per-token value baseline** ไม่ใช่แค่ count
(แก้ bug P10: ถ้า log เก็บแค่จำนวน → Stage 9 conflict detection ทำงานไม่ได้ เพราะไม่มีค่าให้เทียบ)

**7a. Human summary section:**
```markdown
## YYYY-MM-DD HH:MM — Initial DS Push

- File: [Figma URL]
- Page: 🎨 Design System (created)
- Variables pushed: 47 (color:24, spacing:6, typography:8, radius:4) + shadow:5 effect styles
- Components pushed: 8 (Button, Card, Input, Select, Badge, Checkbox, ...)
- Code Connect: 8 mappings  |  หรือ: deferred (.figma.ts, Pro plan)
- Direction: code → Figma (initial)
```

**7b. Baseline table (machine — ใช้โดย ds-pull-tokens / ds-push-tokens):**

ต่อ token 1 แถว — เก็บ `value` + `sha256(value)` + `mode` ของ **ตอน push** (= last-sync state)

```markdown
### BASELINE @ YYYY-MM-DD HH:MM (code → Figma)
<!-- machine-readable — last-synced values for 3-way conflict detection -->

| token-path | value | sha256 | mode |
|------------|-------|--------|------|
| color/primary/default | #2d7a47 | a1b2… | light |
| color/accent/default  | #d97706 | c3d4… | light |
| spacing/md            | 16px    | e5f6… | default |
| ...                   | ...     | ...    | ... |
```

> sha256 ใช้เทียบเร็ว; value เก็บไว้แสดง diff. แต่ละ sync ครั้งใหม่ → เขียน BASELINE block ใหม่ต่อท้าย
> (ไม่ลบของเก่า — เก็บ history). `ds-pull/push-tokens` อ่าน **BASELINE block ล่าสุด** เป็น last-sync state

### Step 8: Update component cards with Figma URLs

อ่าน Figma URL ของ component แต่ละตัว แล้ว update `.card.md`:

```markdown
**Figma:** [Button component](https://www.figma.com/file/.../?node-id=...)
```

---

## ห้ามทำ

- ❌ **อย่าเปลี่ยน Figma file strategy กลางคัน** — ทำตาม `--file` ที่ lock ไว้ (`prototype` = page ใน file เดิม; `new` = library file แยก) อย่าสร้าง file ใหม่ถ้า strategy เป็น `prototype`
- ❌ **อย่า overwrite variables ที่มีค่าใน Figma แตกต่างจาก code โดยไม่เตือน** — ถ้ามี conflict ให้ stop + warn
- ❌ **อย่า push component ทุกตัว** — แค่ key components (top 8) เพื่อไม่ให้ file หนัก
- ❌ **อย่า hardcode values** — ทุก color/spacing ต้องเป็น variable reference

---

## Conflict Detection

ก่อน push variables:

```javascript
// 1. อ่าน existing variables
const existing = await get_variable_defs({ figma_file_url })

// 2. Compute conflicts
const conflicts = tokens.filter(t =>
  existing[t.path] && existing[t.path].value !== t.value
)

// 3. ถ้ามี conflict → warn user
if (conflicts.length > 0) {
  console.log("⚠️ Conflict detected:")
  conflicts.forEach(c => console.log(`  ${c.path}: code=${c.codeValue}, figma=${c.figmaValue}`))
  // Ask user: overwrite all / skip conflicts / abort
}
```

---

## Validation

- [ ] Figma file accessible (edit permission)
- [ ] Page "🎨 Design System" exists (created if needed)
- [ ] All variables in `tokens.json` exist in Figma variable collections
- [ ] No hardcoded values in foundation frames (all bound to variables)
- [ ] `figma-generate-library` + `figma-use` skills loaded ก่อน push components
- [ ] Key components (≥ 5) created **as Component Sets** with variant property definitions
- [ ] ทุก component ผ่าน Step 5B Verification Checklist (componentPropertyDefinitions + boundVariables + auto-layout) — ไม่มี placeholder frame หลุดผ่าน
- [ ] Plan tier ตรวจที่ Step 1b แล้ว (ไม่ไปรู้ตอน Step 6)
- [ ] Code Connect: ถ้า Org/Enterprise → mappings sent; ถ้า Pro → `.figma.ts` fallback เขียนครบทุก component
- [ ] `figma-sync-log.md` updated
- [ ] Component cards updated with Figma URLs

---

## Output Summary

```
✅ Pushed to Figma
   📄 Page: 🎨 Design System
   🎨 Variables: 47 (4 collections)
   🧩 Components: 8 (variants + states)
   🔗 Code Connect: 8 mappings

🌐 View: [figma-url]?node-id=[design-system-page-id]

⚠️  Warnings:
   - color.brand.legacy has no usage → skipped
   - Component "Toast" too complex → manual review needed

Next: Designer แก้ที่ Figma → /skills:ds-pull-tokens [project-name]
```

---

## Tips

- **First push ใช้เวลานาน** — 5–15 นาที สำหรับ 50 vars + 8 components. Subsequent updates เร็วกว่ามาก (delta only)
- **Variable modes** — ถ้า prototype มี dark theme → push เป็น 2 modes (Light + Dark) ใน collection เดียว
- **Group naming** — Figma แยก group ตาม "/" ใน variable name (`color/primary/500` แยกเป็น tree)
- **Code Connect ต้องใช้ Dev Mode subscription** — ถ้า team ไม่มี → mappings ก็ยังบันทึก แต่จะ render ใน Code Connect plugin
- **Backup ก่อน push** — Designer อาจ duplicate Figma file ก่อนรันครั้งแรก เผื่อ rollback
