# DS Pull Tokens — Figma → Code (Manual + Diff)

ดึง Figma Variables ที่ Designer แก้ → update `tokens.json` + regenerate `tokens.css`/`tokens.ts` ใน prototype. ทุกการเปลี่ยนแปลงต้อง confirm ก่อนเขียนทับ

## Usage
```
/skills:ds-pull-tokens [project-name]
/skills:ds-pull-tokens [project-name] --auto-confirm   ← skip confirm (ใช้ด้วยความระวัง)
/skills:ds-pull-tokens [project-name] --dry-run        ← preview diff อย่างเดียว ไม่เขียน
/skills:ds-pull-tokens [project-name] --filter color   ← pull เฉพาะ category
```

## Prerequisites

- `tokens.json` มีอยู่แล้ว (จาก ds-extract หรือ pull ครั้งก่อน)
- `figma-sync-log.md` มี `**File:**` URL และ BASELINE block
- ไม่ต้องเปิด Figma desktop — อ่าน variables แบบ headless ผ่าน `use_figma` (URL-based)

---

## Workflow

### Step 1: Read Figma file URL

อ่านจาก `07-design-system/figma-sync-log.md` (entry ล่าสุด):

```javascript
const lastSync = parseLastSyncLog()
const figmaUrl = lastSync.fileUrl
```

ถ้าไม่มี → ask user

### Step 2: Pull current Figma variables (headless — ไม่ต้องเปิด Figma desktop)

อ่าน fileKey จาก `figma-sync-log.md` บรรทัด `**File:**` แล้วรัน `use_figma`:

```javascript
// อ่านค่า variables ทุกตัวจากทุก collection (URL-based, ไม่ต้อง select node)
// ทดสอบจริงกับ trailbook 2026-06-02: ทำงานได้ headless ผ่าน use_figma
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const figmaVars = {};
for (const col of collections) {
  const modeId = col.modes[0].modeId;
  for (const vid of col.variableIds) {
    const v = await figma.variables.getVariableByIdAsync(vid);
    let val = v.valuesByMode[modeId];
    if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') {
      const tgt = await figma.variables.getVariableByIdAsync(val.id);
      val = `{${tgt ? tgt.name : val.id}}`;
    } else if (val && typeof val === 'object' && 'r' in val) {
      const h = n => Math.round(n*255).toString(16).padStart(2,'0');
      val = `#${h(val.r)}${h(val.g)}${h(val.b)}`;
    }
    figmaVars[v.name] = val;   // key = "color/primary/default", value = "#2d7a47" หรือ 4 (number)
  }
}
return figmaVars;
```

> ข้อสังเกต: Figma API คืน spacing/radius/font-size เป็น **px-number** (เช่น `4`) ไม่ใช่ string
> — Step 4 normalizer จะจัดการ rem↔px ให้อัตโนมัติ

### Step 3: Convert to DTCG format

แปลง `color/primary/500` → nested `color.primary.500`:

```javascript
{
  color: {
    primary: {
      "500": { $value: "#1A73E8", $type: "color" }
    }
  }
}
```

### Step 4: Compute diff (+ flag code-side changes)

**Unit Normalizer (ต้องทำก่อน eq comparison — พบจาก trailbook live test):**
Figma Variables API คืน spacing/radius/font-size เป็น px-number (`4`) แต่ tokens.json ใช้ rem string (`0.25rem`) → ต้อง normalize ก่อนเทียบ ไม่งั้นจะได้ false positive 27 ตัว

```python
def to_px(s):
    """normalize rem/px/number → float px"""
    s = str(s).strip()
    if s.endswith('rem'): return round(float(s[:-3]) * 16, 4)
    if s.endswith('px'):  return round(float(s[:-2]), 4)
    try: return round(float(s), 4)
    except: return None

def norm_family(s):
    """first font family only, lowercase: "'Noto Sans Thai', sans-serif" → "noto sans thai" """
    return s.split(',')[0].strip().strip("'\"").lower()

def eq(a, b, path=''):
    if 'family' in path: return norm_family(str(a)) == norm_family(str(b))
    if str(a).startswith('#') and str(b).startswith('#'): return str(a).lower() == str(b).lower()
    pa, pb = to_px(a), to_px(b)
    if pa is not None and pb is not None: return abs(pa - pb) < 0.01
    return str(a).lower().strip() == str(b).lower().strip()
```

เทียบ Figma กับ `tokens.json` local. **เพิ่ม:** เทียบ local กับ BASELINE block ล่าสุดด้วย —
ถ้า token ที่ Figma จะเขียนทับมี local ≠ baseline แปลว่า **code ก็แก้ตัวนั้นไว้** (pull จะ clobber)
→ mark token นั้นเป็น ⚠️ ในรายงาน Step 5 ให้ user เห็นก่อน confirm

```javascript
const diff = computeDiff(localTokens, figmaTokens)
// + lookup baseline: ถ้า localTokens[path] !== baseline[path] → diff.changed[i].codeAlsoChanged = true

// diff structure:
{
  added: [
    { path: "color.brand.accent", value: "#FF6B35", type: "color" }
  ],
  changed: [
    { path: "color.primary.500", from: "#1A73E8", to: "#1565C0" }
  ],
  removed: [
    { path: "color.legacy.dark", value: "#000000" }
  ]
}
```

### Step 5: Show diff report

```
═══════════════════════════════════════════
Pull Tokens — Diff Report
Figma → Local
═══════════════════════════════════════════

✨ Added (2):
  + color.brand.accent      #FF6B35
  + spacing.xl              32px

✏️  Changed (3):
  ~ color.primary.500       #1A73E8 → #1565C0   ⚠️ used in 12 places
  ~ color.primary.600       #1557B0 → #0D47A1   ⚠️ used in 8 places
  ~ spacing.md              16px → 12px         ⚠️ used in 47 places

❌ Removed (1):
  - color.legacy.dark       #000000             ✅ no usage in src/

═══════════════════════════════════════════
Impact: 67 component usages affected
Breaking risk: HIGH (spacing.md change cascades widely)
═══════════════════════════════════════════

Continue with pull? [Y/n]:
```

> Usage count ดึงจาก grep `var(--color-primary-500)` ใน `05-prototype/src/`

### Step 6: Confirm + write (unless --auto-confirm)

ถ้า user confirm:

1. **Backup** — copy `tokens.json` → `tokens.json.backup.YYYYMMDD-HHMMSS`
2. **Write** — overwrite `tokens.json` ด้วย merged result
3. **Regenerate** — รัน internal logic ของ `ds-extract` เพื่อสร้าง `tokens.css`/`tokens.ts` ใหม่
4. **Update prototype** — ถ้า `prototype/src/styles/tokens.css` ต่างจาก DS เวอร์ชัน → ask confirm + copy

### Step 7: Append CHANGELOG

`07-design-system/CHANGELOG.md`:

```markdown
## YYYY-MM-DD HH:MM — Pull from Figma

**Direction:** Figma → Code
**Source:** [Figma URL]
**By:** Designer (manual sync)

### Added
- `color.brand.accent` = #FF6B35
- `spacing.xl` = 32px

### Changed
- `color.primary.500`: #1A73E8 → #1565C0
- `color.primary.600`: #1557B0 → #0D47A1
- `spacing.md`: 16px → 12px ⚠️ **breaking** (47 usages)

### Removed
- `color.legacy.dark` (unused)

### Files updated
- tokens.json
- tokens.css
- tokens.ts
- 05-prototype/src/styles/tokens.css (copy)
```

### Step 8: Append sync log

`07-design-system/figma-sync-log.md`:

```markdown
## YYYY-MM-DD HH:MM — Pull Tokens

- Direction: Figma → Code
- Variables pulled: 47
- Added: 2 | Changed: 3 | Removed: 1
- Backup: tokens.json.backup.20260527-143022
- Action required: Test prototype หลัง npm run dev
```

**สำคัญ:** หลัง pull สำเร็จ เขียน **BASELINE block ใหม่ต่อท้าย** (format เดียวกับ ds-push-figma Step 7b)
ที่สะท้อนค่า Figma=code ปัจจุบัน — เป็น last-sync state สำหรับรอบถัดไป (กัน conflict detection ผิด)

### Step 9: Suggest verification

```
✅ Pull complete
   - 6 token changes applied
   - tokens.json + tokens.css + tokens.ts updated
   - 05-prototype/src/styles/tokens.css synced
   - Backup saved

⚠️  Recommended next steps:
   1. cd projects/[name]/05-prototype
   2. npm run dev
   3. ตรวจดู screens ที่ใช้ token ที่เปลี่ยน:
      - Button.tsx (uses color.primary.500)
      - Card.tsx (uses spacing.md)
      - [+ 8 more]
   4. ถ้า visual ไม่เป็นไรตามที่ Designer ตั้งใจ → commit
   5. ถ้าผิดเพี้ยน → /skills:ds-pull-tokens [project] --restore-backup
```

---

## ห้ามทำ

- ❌ **ห้าม pull แล้ว overwrite ทันทีโดยไม่ confirm** (เว้น `--auto-confirm` ที่ user สั่งเอง)
- ❌ **ห้าม pull components** — skill นี้ pull แค่ tokens (components เป็น one-way code→Figma)
- ❌ **ห้ามทิ้ง backup ทันที** — เก็บ 5 backups ล่าสุดเสมอ
- ❌ **ห้าม push back ทันที** — ถ้าต้องการ sync 2 ทาง ใช้ `/skills:ds-push-tokens` แยก

---

## Rollback

ถ้า pull แล้วเสียหาย:

```bash
# Restore backup
cp 07-design-system/tokens.json.backup.YYYYMMDD-HHMMSS \
   07-design-system/tokens.json

# Regenerate CSS/TS
/skills:ds-extract [project-name] --from-json
```

หรือใช้ flag:
```
/skills:ds-pull-tokens [project-name] --restore-backup [timestamp]
```

---

## Validation

ก่อน write `tokens.json` ใหม่:

- [ ] Diff report แสดงครบ (added/changed/removed)
- [ ] User confirm (หรือ --auto-confirm flag)
- [ ] Backup created with timestamp
- [ ] All changed tokens valid (color hex valid, dimension มี unit)
- [ ] No circular aliases introduced
- [ ] tokens.css regenerate ได้ (ไม่มี syntax error)
- [ ] tokens.ts compile ได้ (`tsc --noEmit`)

---

## Tips

- **รัน weekly** — ถ้า Designer ทำงานบ่อย ให้ pull อาทิตย์ละครั้งเพื่อไม่ให้ drift มาก
- **Before pull → commit prototype** — git commit ก่อน เผื่อต้อง rollback
- **Filter pull** — ถ้า Designer แก้แค่ color → `--filter color` ลด diff noise
- **Breaking change protocol** — ถ้า spacing/typography เปลี่ยน → notify dev team ก่อน merge
- **Verify visually** — รัน prototype + เปรียบเทียบ screenshots ก่อน/หลัง
- **Variable mode handling** — ถ้า Figma มี dark mode collection → pull ทั้ง 2 modes แยก ไม่ merge

---

## Output Summary

```
✅ Pulled from Figma
   📊 Diff: 2 added, 3 changed, 1 removed
   💾 Backup: tokens.json.backup.20260527-143022
   🎨 Files updated: 4 (tokens.json/css/ts + prototype)
   📝 CHANGELOG + figma-sync-log updated

⚠️  Breaking changes: 2 (spacing.md cascades to 47 places)

🧪 Test: cd 05-prototype && npm run dev
```
