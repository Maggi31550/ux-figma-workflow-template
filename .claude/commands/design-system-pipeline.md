# Design System Pipeline

Pipeline สำหรับสร้าง Design System จาก prototype ที่เสร็จแล้ว — Generation (Stage 8) + 2-way Token Sync (Stage 9)

## Usage

### Stage 8 — Generation (initial setup)
```bash
/design-system-pipeline [project-name] [figma-file-url]
/design-system-pipeline [project-name] [figma-file-url] --skip-figma     ← gen docs only
/design-system-pipeline [project-name] [figma-file-url] --tokens-only    ← skip components
/design-system-pipeline [project-name] [figma-file-url] --update         ← incremental (เพิ่ม component ใหม่)
/design-system-pipeline [project-name] [figma-file-url] --file prototype  ← page ใน prototype Figma file (default)
/design-system-pipeline [project-name] --file new                         ← สร้าง DS library file แยกใหม่
```

> **`--file` — เลือก Figma strategy (ต้องตัดสินใจก่อนรัน เพื่อกัน drift, bug P6):**
> | ค่า | ผล | เมื่อใช้ |
> |-----|-----|---------|
> | `prototype` (default) | สร้าง page "🎨 Design System" ใน Figma file ของ prototype | project เดียว, designer ทำงานต่อใน file เดิม |
> | `new` | สร้าง Figma file แยกสำหรับ DS โดยเฉพาะ (เช่น `Design-Systems-MCP`) | ต้องการ publish เป็น Figma library / reuse ข้าม project |
>
> ⚠️ **ห้าม mix** — ถ้า initial push ใช้ `prototype` แล้ว Stage 9 sync ต้องชี้ file เดิมเสมอ
> (เก็บ file URL + strategy ใน `figma-sync-log.md`) trailbook ใช้ `new` (`Design-Systems-MCP`)

> **`--update`** — ใช้เมื่อเพิ่ม component ใหม่หลัง initial push แล้ว (ไม่ rebuild ทั้งชุด):
> - **skip** ds-extract (tokens ไม่เปลี่ยน — ถ้าเปลี่ยนใช้ Stage 9 push แทน)
> - **ds-cards** เฉพาะ component ที่ยังไม่มี `.card.md`
> - **ds-overview** regenerate (รวมของใหม่)
> - **ds-handoff** regenerate
> - **ds-push-figma** push เฉพาะ component ใหม่ (delta) — ไม่แตะ variable/component เดิม
> แก้ bug P11: trailbook ต้อง manual re-run ทั้ง Stage 8 ตอนเพิ่ม 14 components รอบสอง

### Stage 9 — Sync (recurring)
```bash
/design-system-pipeline [project-name] --pull                 ← Figma → code
/design-system-pipeline [project-name] --push                 ← code → Figma
/design-system-pipeline [project-name] --sync-status          ← compare without writing
```

---

## Prerequisites

| Check | Required |
|-------|----------|
| Prototype audit (Stage 6B) PASS | ✅ Yes |
| **Component library complete (Readiness Gate ผ่าน)** | ✅ Yes — ดู Gate 0 |
| Figma file URL with edit permission | ✅ Yes (Stage 8) |
| Figma MCP connected | ✅ Yes |
| Stage 9 sync: Figma MCP connected | ✅ Yes — อ่าน variables แบบ **headless** ผ่าน `use_figma` (URL-based) ไม่ต้องเปิด Figma desktop |
| `tokens.css` ใน prototype มี structure ที่ extract ได้ | ✅ Yes |
| Dev server runnable (for screenshots) | ✅ Yes (Stage 8) |

ถ้า prototype ยังไม่ผ่าน audit → รัน `/ux-figma-pipeline` ให้จบก่อน

---

## GATE 0 — Component Readiness (รันก่อน Stage 8 เสมอ)

> **ทำไมต้องมี gate นี้:** ถ้า component library ยังไม่ครบ/ไม่ถูกใช้จริงตอนเริ่ม Stage 8 →
> DS ที่ extract ออกมาจะ "ไม่ตรงกับหน้าจอจริง" และต้องวน Stage 8 ซ้ำเมื่อแก้ทีหลัง
> (bug P3 — trailbook วน 3 รอบ; ตรวจพบว่า 0/42 feature pages ใช้ library เลย แม้ library จะมี 14 components)

Gate นี้มี **3 สัญญาณ** — adoption เป็นตัวหลัก เพราะ "library ที่ครบแต่หน้าจอไม่ใช้" ก็ไร้ความหมาย

### สัญญาณ 1 (หลัก) — Library Adoption

```bash
cd projects/[name]/05-prototype
# feature pages ทั้งหมด (ไม่นับ showcase)
TOTAL=$(find src/pages -name "*.tsx" ! -path "*__DSShowcase*" | wc -l | tr -d ' ')
# pages ที่ import จาก component library จริง
ADOPT=$(grep -rl "@/components/ui\|@/components" src/pages/ 2>/dev/null | grep -v __DSShowcase | wc -l | tr -d ' ')
echo "adoption: $ADOPT / $TOTAL"
```

### สัญญาณ 2 — Used-but-missing (broken imports)

```bash
# component ที่ pages import (รองรับ multiline import block)
awk '/import \{/{f=1;b=""} f{b=b$0" "} /from .@\/components/{print b;f=0}' \
  $(grep -rl "@/components" src/pages/) 2>/dev/null \
  | grep -oE "\b[A-Z][a-zA-Z]+\b" | sort -u
# เทียบกับไฟล์จริง:
ls src/components/ui/*.tsx src/components/*.tsx 2>/dev/null | xargs -n1 basename | sed 's/.tsx//'
# diff = component ที่ import แต่ไม่มีไฟล์ = used_but_missing
```

### สัญญาณ 3 — Inline candidates (markup ที่ควรเป็น component)

```bash
# pages ที่มี raw element ซ้ำ ๆ แทนที่จะใช้ component library
grep -rlE "<button" src/pages/ 2>/dev/null | grep -v __DSShowcase | wc -l   # raw <button>
```

### ตัดสินผล gate

```
═══════════════════════════════════════════
Gate 0 — Component Readiness
═══════════════════════════════════════════
Library components:   14 (ui/) + 6 (shells)
Adoption:             0 / 42 feature pages   ❌
used_but_missing:     0
inline_candidates:    41 pages with raw <button>
═══════════════════════════════════════════
Verdict: STOP — library not adopted by pages
```

| สัญญาณ | เกณฑ์ | ผล |
|--------|-------|-----|
| **Adoption** | < 50% feature pages ใช้ library | 🔴 **STOP** — DS จะไม่ตรงหน้าจอจริง |
| **Adoption** | 50–80% | 🟡 WARN + ถาม user |
| **used_but_missing** | > 0 | 🔴 **STOP** — broken import, สร้าง component ก่อน |
| **inline_candidates** | สูง (เทียบ adoption ต่ำ) | 🟡 WARN — มี markup ที่ควร refactor เป็น component |
| ทั้งหมดผ่าน | adoption ≥ 80%, missing = 0 | 🟢 **PASS** → Stage 8 |

**เมื่อ STOP:**
- ส่งกลับ UX/UI Producer ให้ refactor pages ไปใช้ component library
  (`/skills:component-library add` + แก้ pages ให้ import แทน inline)
- ถ้า user ยืนยันจะรันทั้งที่ adoption ต่ำ → บันทึก decision + adoption % ลง CHANGELOG
  ว่า "DS รอบนี้สะท้อน library ไม่ใช่หน้าจอจริง" (scope limitation)

> Gate นี้ทำที่ระดับ pipeline command — ก่อนเรียก `/skills:ds-extract`

---

## STAGE 8 — Design System Generation
**Agent: Design System Publisher**

รันครั้งเดียวต่อ project (initial setup) — 5 steps sequential

### Step 1: Extract tokens
```
/skills:ds-extract [project-name]
```

อ่าน `prototype/src/styles/tokens.css` → สร้าง `tokens.json` (DTCG format) + regenerate `tokens.css`/`tokens.ts`

**Gate (Hardcoded Values) — ไม่ปล่อยผ่านเงียบ ๆ (แก้ bug P7):**
ถ้าพบ hardcoded color/spacing/size ใน components หรือ pages → แสดง file:line ทั้งหมด แล้ว **หยุดถาม user**:

```
⚠️  พบ hardcoded values 3 จุด (ไม่ได้ใช้ token):
  - PublicNavbar.tsx:24   height: 64px   (token --topbar-height = 60px)
  - ContainedLayout.tsx:8 maxWidth: 1280 (ไม่มี token)
  - Card.tsx:31           #888           (ใกล้เคียง color.neutral.500)

จะจัดการอย่างไร?
  [fix]         แก้ให้ใช้ token ก่อน extract (แนะนำ — DS จะสะอาด)
  [accept-debt] ยอมรับเป็น technical debt — extract ตามที่เป็น + log ลง CHANGELOG ว่าค้างไว้
  [abort]       หยุด pipeline กลับไปแก้ที่ prototype เอง
```

- ห้าม extract ต่อโดยไม่ได้ตัดสินใจ — hardcoded value ที่หลุดเข้า DS = token ที่ไม่ตรงของจริง
- `accept-debt` → บันทึกรายการใน CHANGELOG section "Known Issues" + tag `accepted-debt`

### Step 2: Generate component cards
```
/skills:ds-cards [project-name]
```

- Discover `src/components/*.tsx` (primitives + composites)
- Screenshot ทุก component variant
- สร้าง `[Name].card.md` + `[Name].png`

**Gate:** ทุก component ต้องมี matching card + screenshot

### Step 3: Build overview gallery
```
/skills:ds-overview [project-name]
```

สร้าง `overview.html` หน้าเดียวรวม:
- Color swatches + WCAG contrast badges
- Typography scale
- Spacing/radius/shadow samples
- Component gallery (embed screenshots)

### Step 4: Package handoff
```
/skills:ds-handoff [project-name]
```

สร้าง `handoff-package/` พร้อมส่ง dev:
- tokens (json, css, ts, js)
- Component cards + types
- README พร้อม integration guide
- Figma URL

### Step 5: Push to Figma
```
/skills:ds-push-figma [project-name] [figma-file-url]
```

ใน Figma file ของ prototype สร้าง page "🎨 Design System":
- Variables (color, spacing, typography, radius, shadow)
- Foundation frames (visual gallery bound to variables)
- Key components (Button, Card, Input, ... top 8)
- Code Connect mappings

**Gate (Stage 8):**
- [ ] `tokens.json` valid DTCG
- [ ] ทุก component มี card + screenshot
- [ ] `overview.html` open ได้
- [ ] `handoff-package/` ครบ
- [ ] Figma page created + variables pushed

---

## STAGE 9 — Token Sync (Recurring)
**Agent: Design System Publisher**

รันเมื่อมีการเปลี่ยนแปลง — manual trigger เท่านั้น

### Pull (Figma → Code)
*ใช้เมื่อ: Designer แก้ tokens ใน Figma*

```
/skills:ds-pull-tokens [project-name]
```

Workflow:
1. Read Figma variables
2. Compute diff vs local `tokens.json`
3. Show diff report (added/changed/removed + impact analysis)
4. User confirm → write
5. Backup + regenerate CSS/TS
6. Update prototype `tokens.css`
7. Update CHANGELOG + sync log

### Push (Code → Figma)
*ใช้เมื่อ: Dev แก้ tokens ใน code → ส่งกลับ Figma*

```
/skills:ds-push-tokens [project-name]
```

Workflow:
1. Read local + Figma
2. Compute delta + detect conflicts
3. Show push report
4. User confirm → push incremental
5. Update sync log

### Sync Status
```
/design-system-pipeline [project-name] --sync-status
```

**Headless — รันได้เลย ไม่ต้องเปิด Figma desktop** (ทดสอบจริงกับ trailbook 2026-06-02)

ลำดับงาน:
1. อ่าน `figma-sync-log.md` → fileKey + BASELINE block ล่าสุด
2. รัน `use_figma` (URL-based) → Figma variables snapshot สด ๆ
3. อ่าน `tokens.json` → code values
4. รัน **3-way diff** (baseline / figma-now / code-now) ด้วย unit normalizer (rem↔px, font-family)
5. แสดงรายงาน:

```
╔══════════════════════════════════════════════════
║  Stage 9 — Sync Status  [project]
║  Baseline: YYYY-MM-DD HH:MM
╠══════════════════════════════════════════════════
║  Tokens compared:  87
║  ✅ In-sync:        87
║  ⚠️  Figma changed: 0   (Designer แก้ใน Figma)
║  ⚠️  Code changed:  0   (Dev แก้ใน code)
║  ⛔ Conflict:       0   (ทั้งคู่เปลี่ยน)
╠══════════════════════════════════════════════════
║  RECOMMENDATION: ไม่ต้อง sync — ทุกอย่าง in-sync ✅
╚══════════════════════════════════════════════════
```

> **Unit normalizer (จำเป็น):** Figma API คืน spacing/radius/font-size เป็น px-number (`4`) แต่
> tokens.json ใช้ rem string (`0.25rem`) → ต้อง normalize ก่อนเทียบ ไม่งั้นได้ false positive
> (ดู ds-pull-tokens Step 4 สำหรับ normalizer code)

---

## Conflict Resolution

ถ้า pull/push พบ conflict (ทั้ง 2 ฝั่งแก้หลัง last sync):

```
⚠️  CONFLICT — both sides changed since last sync
  ~ color.primary.500
    Last synced:  #1565C0 (2026-05-20)
    Figma now:    #0D47A1 (Designer change)
    Code now:     #1A73E8 (Dev change)

Resolution options:
  [k] Keep code value (override Figma)
  [f] Figma wins (override code)
  [a] Abort sync — discuss with team first
  [m] Manual merge (open both files)
```

**Default policy:** Abort ถ้ามี conflict — ติดต่อทีมก่อน resolve (ไม่ใช่ตัดสินใจอัตโนมัติ)

---

## Output Structure

```
projects/[name]/07-design-system/
├── tokens.json                          ← DTCG canonical (source of truth)
├── tokens.json.backup.YYYYMMDD-HHMMSS   ← rotation (keep 5)
├── tokens.css                           ← generated (web)
├── tokens.ts                            ← generated (mobile)
├── components/
│   ├── Button.card.md
│   ├── Button.png
│   ├── Card.card.md
│   ├── Card.png
│   └── README.md                        ← index
├── overview.html                        ← gallery (open in browser)
├── handoff-package/
│   ├── README.md
│   ├── tokens/ (json/css/ts/js/scss)
│   ├── components/ (cards + pngs + types)
│   ├── types/design-system.d.ts
│   ├── figma-url.txt
│   └── overview.html
├── handoff-package-vYYYY.MM.DD.zip     ← bundle (optional)
├── CHANGELOG.md                         ← human-readable history
└── figma-sync-log.md                    ← machine log (last-sync timestamps)
```

---

## Pipeline Flow Diagram

```
PROTOTYPE READY (Stage 6B PASS)
       ↓
   ┌───────────────────────────────────┐
   │ STAGE 8 — Generation (run once)   │
   │                                   │
   │  ds-extract       → tokens.json   │
   │       ↓                           │
   │  ds-cards         → components/   │
   │       ↓                           │
   │  ds-overview      → overview.html │
   │       ↓                           │
   │  ds-handoff       → package/      │
   │       ↓                           │
   │  ds-push-figma    → 🎨 in Figma   │
   └───────────────────────────────────┘
       ↓
   📤 DELIVER TO DEV TEAM
   📤 SHARE OVERVIEW WITH STAKEHOLDERS
       ↓
   ┌───────────────────────────────────┐
   │ STAGE 9 — Token Sync (recurring)  │
   │                                   │
   │  Designer แก้ Figma                │
   │       ↓                           │
   │  ds-pull-tokens   ← manual run    │
   │       ↓                           │
   │  Update prototype + commit        │
   │                                   │
   │  OR                               │
   │                                   │
   │  Dev แก้ code                      │
   │       ↓                           │
   │  ds-push-tokens   ← manual run    │
   │       ↓                           │
   │  Designer pull ใน Figma           │
   └───────────────────────────────────┘
```

---

## Things to Remember

1. **Token Sync Direction Rules:**
   - **Tokens** — 2-way (Figma ↔ code)
   - **Components** — 1-way (code → Figma เท่านั้น)
   - **Logic/behavior** — code only (Figma ไม่เก็บ)

2. **Manual sync only** — ไม่มี auto-watch, ไม่มี git hook
3. **Diff before write** — ทุก pull/push ต้อง confirm
4. **Backup ก่อน overwrite** — เก็บ 5 backups ล่าสุด
5. **Conflict = stop** — ไม่ตัดสินใจอัตโนมัติ
6. **Figma file strategy เลือกด้วย `--file`** — `prototype` (page ใน file เดิม, default) หรือ `new` (library file แยก); lock ตลอด project
7. **DTCG format** — ทุก output token ใช้ W3C Design Tokens spec

---

## Common Errors

**"Page '🎨 Design System' not found":**
- Stage 9 ต้องรันหลัง Stage 8 (push-figma) เสมอ
- ถ้า Designer ลบ page → รัน `/skills:ds-push-figma` ใหม่

**"Figma variables count doesn't match tokens.json":**
- Designer อาจเพิ่ม variable เองใน Figma → pull ก่อน push
- หรือ variable ใน Figma มี name ผิด convention → ตรวจ "/" separator

**"Conflict detection failed":**
- `figma-sync-log.md` หาย → ไม่รู้ baseline. Solution: ใช้ `--force` หลัง backup, แล้วเริ่ม sync log ใหม่

**"Screenshot generation failed":**
- Dev server ไม่ start → `cd 05-prototype && npm install && npm run dev`
- ตรวจ port ที่ใช้ — default 5173

**"Code Connect mapping failed":**
- ต้องใช้ Figma Dev Mode subscription
- ถ้าไม่มี → mappings บันทึกใน code (`.figma.ts`) ใช้ภายหลังได้
