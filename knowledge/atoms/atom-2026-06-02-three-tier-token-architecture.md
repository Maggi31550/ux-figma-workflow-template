---
name: three-tier-token-architecture
description: 3-tier token structure (primitive → semantic → component) + migration recipe ที่ verified กับ trailbook จริง
metadata:
  type: project
---

# 3-Tier Design Token Architecture

## หลักการ

| Tier | Purpose | ตัวอย่าง | CSS output? |
|------|---------|---------|------------|
| **1 Primitive** | raw scale value | `primitive.color.green.500 = #2d7a47` | ❌ ไม่ต้อง |
| **2 Semantic** | purpose-based alias → primitive | `color.primary.default = {primitive.color.green.500}` | ✅ `--color-primary` |
| **3 Component** | component-specific alias → semantic | `component.button.primary.bg = {color.primary.default}` | optional |

**Why:** เปลี่ยน brand color ที่ primitive เดียว → semantic + component อัปเดตอัตโนมัติทั้งระบบ

## Migration recipe (verified trailbook 2026-06-02)

### Input: 1-tier tokens.json (semantic hardcoded)
```json
{ "color": { "primary": { "default": { "$value": "#2d7a47" } } } }
```

### Output: 3-tier tokens.json (alias chain)
```json
{
  "primitive": { "color": { "green": { "500": { "$value": "#2d7a47" } } } },
  "color":     { "primary": { "default": { "$value": "{primitive.color.green.500}" } } },
  "component": { "button": { "primary": { "bg": { "$value": "{color.primary.default}" } } } }
}
```

### Invariant ที่ต้องรักษา
- CSS output ต้อง **identical** กับ tokens.css เดิม (backward compat — prototype ไม่พัง)
- `source.cssVar` อยู่ที่ **semantic tier เท่านั้น** — primitive ไม่มี (ไม่งั้น duplicate CSS vars)
- round-trip verify: `diff tokens.css prototype/src/styles/tokens.css` → 0 diff

## Tricky cases (พบจาก trailbook)

### 1. Hue overlap — success ≠ primary green
```
primary.default  = green/500 (#2d7a47)   ← Trail Green
success.default  = emerald/800 (#16a34a) ← ต้องแยก palette!
```
ถ้าใช้ scale เดียวกัน success.bg (#f0fdf4) ≠ primary.bg (#edf7f1) → ต้องสร้าง `emerald` scale แยก

### 2. Warning.bg ≠ Accent.bg (amber ไม่ใช่ scale เดียว)
```
accent.bg  = amber/50  = #fff8eb
warning.bg = amber/50w = #fffbeb  ← ต้องแยก key (ห้ามมี dot ใน key)
```

### 3. Bank colors ไม่มี palette equivalent → ใช้ exact hex
```
bank.bbl = #1a4f9c  (ไม่มีใน blue scale)
bank.ttb = #f97316  (ไม่มีใน orange scale)
```
→ ยอมรับเป็น hardcode ที่ semantic tier (ไม่บังคับ alias ถ้า palette ไม่ตรง)

### 4. Unit normalizer สำหรับ Figma sync
Figma API คืน spacing/radius เป็น px-number (`4`) แต่ tokens.json ใช้ rem (`0.25rem`)
→ ต้อง normalize ก่อน diff:
```python
def to_px(s):
    if str(s).endswith('rem'): return round(float(str(s)[:-3]) * 16, 4)
    try: return round(float(str(s).replace('px','')), 4)
    except: return None
```

## Figma collections (3-tier → 6 collections)
```
Before: Colors(50), Spacing(12), Radius(6), Typography(19)
After:  + Primitives(40), + Components(39) = 166 total
```
- Semantic "Colors" collection: wire 48/50 vars เป็น VARIABLE_ALIAS → Primitives
- "Components" collection: alias → Colors semantic (2-hop)
- Alias chain verified: component → semantic → primitive = 3-hop ✅

## Reusable scripts
ดู `scripts/token-migration/migrate-to-3tier.py` — script ที่ใช้กับ trailbook
(รับ tokens.json 1-tier → output 3-tier พร้อม hue analysis + round-trip verify)

**Why:** สำหรับ project ใหม่ที่เริ่ม DS จาก prototype existing → รัน script นี้ก่อน push Figma
