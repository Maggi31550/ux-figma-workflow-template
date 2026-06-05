# DS Push Tokens — Code → Figma (Delta Only)

Sync token changes ที่ทำใน code กลับเข้า Figma — push เฉพาะ delta (ไม่ recreate ทั้ง collection) + confirm ก่อนเขียน

## Usage
```
/skills:ds-push-tokens [project-name]
/skills:ds-push-tokens [project-name] --dry-run            ← preview ไม่ push
/skills:ds-push-tokens [project-name] --filter color       ← push เฉพาะ category
/skills:ds-push-tokens [project-name] --force              ← skip conflict detection
```

## เมื่อไหร่ใช้

- Dev/Designer แก้ token ใน prototype `tokens.json` แล้วอยาก sync ไป Figma
- หลัง pull tokens แล้ว rebase/merge มี conflict — push เพื่อ resolve
- Test color/spacing ใหม่ใน code → ตัดสินใจ keep → push

> หมายเหตุ: skill นี้ push **tokens อย่างเดียว** ไม่ push component changes (component ใช้ `ds-push-figma` แทน)

---

## Prerequisites

- `tokens.json` อยู่ในสภาพ valid
- Figma file URL บันทึกใน `figma-sync-log.md`
- มี edit permission ใน Figma file

---

## Workflow

### Step 1: Read both sides (headless — ไม่ต้องเปิด Figma desktop)

```javascript
const localTokens = readTokensJson(`07-design-system/tokens.json`)
// อ่าน Figma variables แบบ URL-based ผ่าน use_figma (ไม่ใช้ get_variable_defs ที่ selection-based)
// ใช้ script เดียวกับ ds-pull-tokens Step 2 ทุกประการ — return figmaVars object
const figmaVars = /* result of use_figma Step 2 script */
```

### Step 2: Compute delta (code vs Figma)

**Unit Normalizer (ต้องทำก่อน eq comparison — พบจาก trailbook live test):**
ใช้ normalizer เดียวกับ ds-pull-tokens Step 4 (`to_px`, `norm_family`, `eq`) — copy ใส่ script ก่อนเสมอ
เพื่อป้องกัน false positive: Figma API คืน `4` (px-number), code มี `0.25rem` → eq = true

```javascript
const delta = computeDiff(figmaVars, localTokens)

// delta:
{
  toAdd: [...],      // มีใน code ไม่มีใน Figma
  toChange: [...],   // ค่าต่างกัน
  toRemove: [...]    // มีใน Figma ไม่มีใน code
}
```

### Step 3: Show push report

```
═══════════════════════════════════════════
Push Tokens — Delta Report
Code → Figma
═══════════════════════════════════════════

📤 To Add (3):
  + color.success.500       #34A853
  + color.success.600       #2D8E47
  + spacing.xs              4px

✏️  To Update (2):
  ~ color.primary.500       Figma=#1565C0 → Code=#1A73E8
  ~ radius.lg               Figma=12px → Code=16px

🗑️  To Remove (1) ⚠️ destructive:
  - color.brand.legacy      (orphan in Figma)

═══════════════════════════════════════════
Push to Figma? [Y/n/show-conflicts]:
```

### Step 4: Conflict detection (3-way diff)

**Conflict** = ทั้ง Figma และ code เปลี่ยนหลัง sync ครั้งล่าสุด → ไม่รู้ว่าฝ่ายไหนเป็นเวอร์ชันที่ต้องการ

ใช้ **3-way diff** จาก BASELINE block ล่าสุดใน `figma-sync-log.md` (เขียนโดย ds-push-figma Step 7b):

```
baseline = ค่าตอน last-sync (จาก BASELINE table — column value/sha256)
figma    = ค่าใน Figma ตอนนี้ (use_figma headless — Step 1 script)
code     = ค่าใน tokens.json ตอนนี้

per token:
  figma == baseline && code == baseline → no change
  figma != baseline && code == baseline → Figma เปลี่ยนฝ่ายเดียว (pull ก่อน)
  figma == baseline && code != baseline → code เปลี่ยนฝ่ายเดียว → ✅ push ได้ปลอดภัย
  figma != baseline && code != baseline → ⚠️ CONFLICT (ทั้งคู่เปลี่ยน)
```

> เทียบเร็วด้วย sha256; ถ้า BASELINE block ไม่มี (project เก่าก่อน S2-1) → เตือน user ว่า
> conflict detection ใช้ไม่ได้ ให้ `--force` หลัง backup แล้วระบบจะเขียน baseline ใหม่

```
⚠️  CONFLICT DETECTED (1):
  ~ color.primary.500
    Last synced:  #1565C0 (2026-05-20)
    Figma now:    #0D47A1 (changed by Designer after sync)
    Code now:     #1A73E8 (changed by Dev after sync)

  Both sides changed since last sync.
  Resolution: [k]eep-code / [f]igma-wins / [a]bort: _
```

ถ้า `--force` → use code value (override Figma) แต่บันทึก warning ใน log

### Step 5: Push delta (incremental)

**ห้าม recreate collection** — update เฉพาะ variables ที่ต้องเปลี่ยน:

```javascript
// MANDATORY: load figma-use skill first
// Skill: figma-use

mcp__claude_ai_Figma__use_figma({
  prompt: `
    Update variable collection in this Figma file:

    ADD variables (create if not exists):
    ${delta.toAdd.map(t => `- ${t.path} = ${t.value}`).join('\n')}

    UPDATE variables (existing — modify value only):
    ${delta.toChange.map(t => `- ${t.path}: ${t.figmaValue} → ${t.codeValue}`).join('\n')}

    DELETE variables (warn user first):
    ${delta.toRemove.map(t => `- ${t.path}`).join('\n')}

    Naming convention: "/" separator (color/primary/500)
    Do NOT recreate the collection. Update in place.
  `,
  figma_file_url: figmaUrl
})
```

### Step 6: Update foundation frames

ถ้า color/spacing/typography เปลี่ยน — update visual swatches/samples ใน "🎨 Design System" page ให้ตรงกับ variable ใหม่:

```javascript
// Find swatch nodes bound to changed variables
// Update their fill/text/etc — but since they bind to variables, Figma จะ auto-update
// แค่ verify ว่า binding ยังถูกต้อง
```

### Step 7: Update sync log

`07-design-system/figma-sync-log.md`:

```markdown
## YYYY-MM-DD HH:MM — Push Tokens

- Direction: Code → Figma
- Variables: 3 added, 2 updated, 1 removed
- Conflicts: 0
- Source commit: [git SHA if available]
```

**สำคัญ:** หลัง push สำเร็จ เขียน **BASELINE block ใหม่ต่อท้าย** (format เดียวกับ ds-push-figma Step 7b)
ที่สะท้อนค่าปัจจุบันทั้งชุด — นี่จะเป็น last-sync state สำหรับ sync ครั้งถัดไป
(ถ้าไม่เขียน → conflict detection รอบหน้าใช้ baseline เก่าผิด)

`07-design-system/CHANGELOG.md`:

```markdown
## YYYY-MM-DD HH:MM — Push to Figma

**Direction:** Code → Figma
**By:** [user/dev]

### Pushed
- Added: color.success.500, color.success.600, spacing.xs
- Updated: color.primary.500, radius.lg
- Removed: color.brand.legacy

### Files
- tokens.json (unchanged — source of push)
- Figma variables synced
```

### Step 8: Verify

Re-read Figma variables ด้วย use_figma script เดียวกับ Step 1 (headless) แล้วเทียบกับ delta:

```javascript
// รัน use_figma Step 1 script อีกครั้ง → ได้ verified object
// เทียบ normalized eq กับ localTokens
const verificationDiff = computeDeltaWithNormalizer(verified, localTokens)

if (verificationDiff.toAdd.length + verificationDiff.toChange.length === 0) {
  return "✅ Verified: Figma matches code"
} else {
  return { warning: "⚠️ Verification failed — some variables not updated", diff: verificationDiff }
}
```

---

## ห้ามทำ

- ❌ **ห้าม recreate variable collection** — update in place (Figma จะ break component bindings)
- ❌ **ห้าม push โดยไม่ตรวจ conflict** เว้น `--force`
- ❌ **ห้าม push components** — ใช้ `ds-push-figma` แยกสำหรับ components
- ❌ **ห้าม overwrite Figma mode (light/dark)** ถ้า code มี mode เดียว — เพิ่มเป็น mode ใหม่แทน

---

## Edge Cases

### Variables ที่ alias กัน

ถ้า code มี:
```json
{
  "color": {
    "text": { "primary": { "$value": "{color.neutral.900}" } }
  }
}
```

Push เป็น **alias variable** ใน Figma (variable พึ่ง variable อื่น) — ไม่ resolve เป็น hex

### Composite tokens (typography)

DTCG typography composite ต้อง split เป็น sub-variables ใน Figma:
- `typography/heading-1/font-family`
- `typography/heading-1/font-size`
- `typography/heading-1/font-weight`
- `typography/heading-1/line-height`

(Figma ยังไม่ support composite variable แบบ DTCG โดยตรง — ใช้ separate vars + apply เป็นชุดที่ Text node)

---

## Validation

- [ ] `tokens.json` valid (no syntax error, all values valid)
- [ ] Delta computed correctly (ไม่มี false positive)
- [ ] Conflicts shown to user (ถ้ามี)
- [ ] Variables pushed incrementally (ไม่ recreate)
- [ ] Verification confirms Figma matches code
- [ ] Sync log + CHANGELOG updated

---

## Output Summary

```
✅ Pushed to Figma
   📤 Added: 3 | Updated: 2 | Removed: 1
   ⚠️  Conflicts: 0
   🔁 Direction: Code → Figma
   ✓ Verification passed

📝 Logs updated:
   - figma-sync-log.md
   - CHANGELOG.md

🌐 View changes: [figma-url]?node-id=[design-system-page]
```

---

## Tips

- **Push หลัง commit** — commit code ก่อน push เผื่อ rollback
- **Small batches** — แทนที่จะ push 50 token change ทีเดียว แยกเป็น 5–10 ครั้ง (ลด blast radius ถ้าผิดพลาด)
- **Conflict — pause + discuss** — ถ้ามี conflict อย่ารีบ resolve เอง ติดต่อฝ่ายที่แก้ Figma คุยกันก่อน
- **Component bindings** — เปลี่ยน variable value จะ propagate ไปทุก component ที่ bind อยู่ — ระวัง breaking change
- **--force ใช้เฉพาะ emergency** — เช่น Figma value ผิด ต้อง revert มาตรงกับ code ทันที
