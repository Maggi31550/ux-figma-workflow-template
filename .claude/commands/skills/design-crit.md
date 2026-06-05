# Design Critique — Heuristic Evaluation (React)

วิเคราะห์ React screens ด้วย Nielsen's 10 Heuristics + UX best practices — output critique พร้อม severity rating

## Usage
```
/skills:design-crit [project-name]                       ← critique ทุก pages
/skills:design-crit [project-name] --screen [path]       ← เช่น "approval/queue"
/skills:design-crit [project-name] --feature [name]      ← critique เฉพาะ feature
/skills:design-crit [project-name] --quick               ← top 5 issues
```

> ใช้คู่กับ `design:design-critique` (Anthropic system skill) ได้ — skill นี้ให้ project-specific context

---

## Scope

อ่าน:
- `05-prototype/src/pages/**/*.tsx`
- `05-prototype/src/components/**/*.tsx`
- `02-research/ux-research-doc-[name].md` (สำหรับเทียบกับ user goal)
- `02-research/screen-inventory-[name].md` (สำหรับ context)

---

## Framework: Nielsen's 10 + React-specific Patterns

### H1 — Visibility of System Status
ตรวจใน code:
```bash
# หา async action ที่ไม่มี loading state
grep -rn "fetch(\|await " src/pages/ --include="*.tsx" | grep -v "useState.*[Ll]oading\|isLoading"

# หา button ที่ submit form แต่ไม่มี disabled state
grep -rn "type=\"submit\"" src/pages/ --include="*.tsx"
```

Checklist:
- [ ] ทุก async action มี loading indicator
- [ ] Form submit button disabled + แสดง spinner ขณะ submitting
- [ ] Toast notification หลัง action สำเร็จ
- [ ] Progress bar/Stepper แสดง step ปัจจุบันชัดเจน
- [ ] Empty state แยกจาก loading state ชัดเจน

### H2 — Match Real World
- [ ] ใช้ภาษาที่ user ใช้ ไม่ใช่ developer jargon (เช่น "บันทึก" ไม่ใช่ "Persist")
- [ ] Date format `DD/MM/YYYY` (Thai locale) ไม่ใช่ ISO
- [ ] เลขเงิน format `1,250 บาท` ไม่ใช่ `1250`
- [ ] Icon ตรงกับความหมายที่ user คุ้นเคย (ถังขยะ = ลบ, ดินสอ = แก้ไข)

### H3 — User Control and Freedom
```bash
# หา destructive action
grep -rn "delete\|remove\|reject\|cancel" src/pages/ --include="*.tsx" -i | head
```

Checklist:
- [ ] ทุก form มี "ยกเลิก" หรือ "กลับ"
- [ ] Modal/Dialog ปิดด้วย Esc key + overlay click + ปุ่ม X
- [ ] Destructive action (`delete`, `reject`) ต้องมี confirm step
- [ ] Multi-step form มี "ย้อนกลับ" ทุก step ยกเว้น step 1

### H4 — Consistency and Standards
```bash
# หา button variant ที่ใช้ผิดบทบาท (เช่น primary > 1 ตัวในหน้าเดียวกัน)
grep -rn "variant=\"primary\"" src/pages/ --include="*.tsx"
```

Checklist:
- [ ] Primary action 1 ตัวต่อ screen (CTA ที่ชัดที่สุด)
- [ ] ใช้ component จาก `ui/` library สม่ำเสมอ — ไม่มี inline duplicate
- [ ] Back/Next button placement consistent ทุกหน้า (ตัวอย่าง: Back ซ้าย, Next ขวา)
- [ ] Terms ตรงกัน (ไม่ใช่ "ลบ" บางที่ "เอาออก" บางที่)

### H5 — Error Prevention
- [ ] Confirm dialog ก่อน destructive
- [ ] Form validation แบบ inline (ไม่รอ submit)
- [ ] Disable ปุ่มที่ยังกดไม่ได้ + tooltip อธิบายเหตุผล
- [ ] Default values ที่ปลอดภัย (เช่น filter "วันนี้" แทน "ทั้งหมด")

### H6 — Recognition over Recall
- [ ] Filter/Search ใน list ที่ยาว ≥ 10 items
- [ ] Recent items / favorites
- [ ] Breadcrumb ทุกหน้า (ผ่าน Topbar)
- [ ] Active state ใน Sidebar ชัดเจน

### H7 — Flexibility and Efficiency
- [ ] Bulk actions ใน list (select all + bulk delete/approve)
- [ ] Keyboard shortcuts (`Cmd+S` save, `Esc` close)
- [ ] Filter persistence ระหว่าง navigation
- [ ] URL params สำหรับ filter (สามารถ share link)

### H8 — Aesthetic and Minimalist Design
- [ ] Information hierarchy ชัด (heading > subheading > body)
- [ ] Whitespace พอ — ไม่ cramped
- [ ] ไม่มีข้อมูลซ้ำซ้อนใน screen เดียวกัน
- [ ] Primary CTA โดดเด่นกว่า secondary actions

### H9 — Help Users Recover from Errors
ตรวจ error messages:
```bash
grep -rn "error\|invalid" src/pages/ --include="*.tsx" | grep -i "message\|text" | head
```

Checklist:
- [ ] Error message ระบุ **สาเหตุ** + **วิธีแก้** เป็นภาษาไทย
- [ ] ไม่ใช้ "Invalid input" / "Error 500" อย่างเดียว
- [ ] Field error อยู่ใกล้ field ที่ error (ไม่ใช่ top of page)
- [ ] มีปุ่ม "ลองอีกครั้ง" สำหรับ network/server error

### H10 — Help and Documentation
- [ ] Tooltip บน complex field
- [ ] Empty state มี guidance + CTA (ไม่ใช่แค่ "ไม่มีข้อมูล")
- [ ] Inline hints ใต้ field ที่ต้องการ format เฉพาะ (เช่น "วัน/เดือน/ปี")

---

## React-Specific Checks

### State Management
```bash
# หา useState ที่อาจขาด useEffect cleanup
grep -rn "useEffect" src/pages/ --include="*.tsx" -A 3 | grep -B 1 "fetch\|setTimeout\|setInterval"
```

### Re-render Performance
```bash
# หา inline function ใน list render ที่อาจ cause re-render
grep -rn "\.map.*=>" src/pages/ --include="*.tsx" | grep "onClick={() =>"
```

### Form Pattern
- [ ] Controlled inputs ทุกตัว (ไม่มี uncontrolled mix)
- [ ] Form error state แสดงผลทันที (ไม่รอ blur)

---

## Severity Rating

| Rating | ความหมาย | ต้องแก้ |
|--------|----------|---------|
| 🔴 Critical | Block user task completion | ก่อน launch |
| 🟠 Major | Significant frustration | Sprint นี้ |
| 🟡 Minor | Workaround มี | Backlog |
| 🟢 Cosmetic | Polish | Optional |

---

## Workflow

### STEP 1 — อ่าน Context
- Research doc → user personas + goals
- Screen inventory → coverage check

### STEP 2 — Heuristic Scan (H1–H10)
ใช้ grep + read .tsx ทีละไฟล์ — บันทึก findings พร้อม `file:line`

### STEP 3 — Cross-screen Consistency Check
- Button variants: หา primary > 1 ใน screen เดียวกัน
- Terms consistency: ทำ word frequency จาก JSX text
- Pattern reuse: เช็คว่า empty state ใช้ `<EmptyState>` ทุกที่

### STEP 4 — สร้าง Report

`projects/[name]/02-research/design-crit-[name].md`:

```markdown
# Design Critique Report — [Project Name]
Date: YYYY-MM-DD | Evaluator: Claude (Heuristic Evaluation)

## Executive Summary
**Overall Score: [X]/10**
Critical: [N] | Major: [N] | Minor: [N] | Cosmetic: [N]

## Top 3 Issues to Fix Now
1. 🔴 [Screen X] ไม่มี loading state ใน submit button → user ไม่รู้ว่ากำลังทำงาน
   - Fix: ใช้ `<Button loading={isSubmitting}>` (component มีอยู่แล้ว)
   - Effort: 5 min/screen

2. 🔴 [Screen Y] Destructive action ไม่มี confirm
   - Fix: เพิ่ม `<ConfirmModal>` ก่อน delete
   - Effort: 30 min

3. 🟠 [3 screens] ใช้ "เอาออก" / "ลบ" / "ลบทิ้ง" สลับกัน
   - Fix: standardize เป็น "ลบ" ทั้งระบบ
   - Effort: 15 min

## Findings by Heuristic

### H1 — Visibility of System Status
✅ Stepper ใน Approval flow ชัดเจน
❌ [Approval/Detail.tsx:84] ปุ่ม "อนุมัติ" ไม่มี loading state
   - Severity: 🟠 Major
   - Fix: ใช้ `<Button loading={mutating}>`

...

## Positive Findings (Keep These)
- Sidebar nav role-based filtering ทำงานดี
- Toast notification dismiss อัตโนมัติ ไม่รบกวน
- Color tokens consistent

## Recommendations Priority
| Priority | Action | Effort | Files affected |
|----------|--------|--------|----------------|
| P1 | เพิ่ม loading states ทุก async action | 2h | 8 files |
| P2 | เพิ่ม confirm dialog ก่อน destructive | 1h | 3 files |
```

---

## Output
```
สร้าง: projects/[name]/02-research/design-crit-[name].md
```
