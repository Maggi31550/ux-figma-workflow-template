# Microcopy Generator

สร้าง / รีวิว UI text ทั้งระบบของ project — labels, error messages, empty states, CTAs — ภาษาไทยที่ตรงบริบทธุรกิจและ persona

## Usage
```
/skills:microcopy [project-name]                 ← generate ทั้ง project (จาก research + screen inventory)
/skills:microcopy [project-name] --feature [f]   ← เฉพาะ feature
/skills:microcopy [project-name] --review        ← ตรวจ existing UI text + แนะนำแก้
/skills:microcopy [project-name] --pattern [p]   ← เฉพาะ pattern เช่น "error-messages", "empty-states", "ctas"
```

> ใช้คู่กับ `design:ux-copy` (Anthropic system skill) — skill นี้รวบรวม project context + persona + tone-of-voice แล้วส่งต่อ

---

## Inputs

อ่าน:
- `02-research/ux-research-doc-[name].md` — personas, pain points, tone preference
- `02-research/ba-analysis-[name].md` — business goal, scope, terminology ที่ client ใช้
- `02-research/screen-inventory-[name].md` — screens ที่ต้อง copy
- `05-prototype/src/pages/**/*.tsx` (สำหรับ `--review`) — current text ใน UI

---

## Output Structure

สร้าง `projects/[name]/03-design/microcopy-[name].md`:

```markdown
# Microcopy — [Project Name]
Date: YYYY-MM-DD | Persona: [primary persona] | Tone: [formal/friendly/...]

## Tone of Voice
- **Formality:** ทางการ (สำหรับระบบราชการ) / กึ่งทางการ / กันเอง
- **Vocabulary:** ใช้คำที่ user ในวงการนี้คุ้นเคย
- **Length:** กระชับ, ไม่เกิน 1 บรรทัดสำหรับ label
- **Emotion:** ห้ามใช้ตัวอักษรภาษา emoji-heavy ในข้อความทางการ

---

## 1. Navigation Labels
| Path | Label (ใน Sidebar) | Page Title (h1) | Breadcrumb |
|------|-------------------|-----------------|-----------|
| /dashboard | หน้าหลัก | ภาพรวม | หน้าหลัก |
| /approval/queue | คำขออนุมัติ | คำขออนุมัติที่รอตรวจสอบ | คำขออนุมัติ |
| ... |

## 2. Button Labels (CTAs)
| Action | Primary CTA | Secondary | Destructive |
|--------|-------------|-----------|-------------|
| Save | บันทึก | ยกเลิก | - |
| Submit form | ส่งคำขอ | บันทึกร่าง | - |
| Delete | - | - | ลบ |
| Approve | อนุมัติ | ส่งกลับแก้ไข | ปฏิเสธ |

## 3. Form Labels & Hints
| Field | Label | Placeholder | Hint | Error (Required) | Error (Invalid) |
|-------|-------|-------------|------|------------------|-----------------|
| email | อีเมล | example@domain.com | สำหรับรับการแจ้งเตือน | กรุณากรอกอีเมล | รูปแบบอีเมลไม่ถูกต้อง |
| nationalId | เลขประจำตัวประชาชน | 1-2345-67890-12-3 | 13 หลัก | กรุณากรอกเลขประจำตัวประชาชน | เลขประจำตัวประชาชนไม่ถูกต้อง |
| ... |

## 4. Empty States
| Screen | Title | Description | CTA |
|--------|-------|-------------|-----|
| Inbox (no notifications) | ยังไม่มีการแจ้งเตือน | คุณจะเห็นการแจ้งเตือนที่นี่เมื่อมีกิจกรรมใหม่ | (none) |
| Approval Queue (empty) | ไม่มีคำขอที่รอตรวจสอบ | คำขอใหม่จะปรากฏที่นี่ทันที | กลับสู่หน้าหลัก |
| ... |

## 5. Loading States
| Context | Text |
|---------|------|
| Initial page load | กำลังโหลด... |
| Form submit | กำลังบันทึก... |
| Search | กำลังค้นหา... |
| Long async (>5s) | กำลังประมวลผล โปรดรอสักครู่... |

## 6. Success / Error Toast
| Event | Message |
|-------|---------|
| Save success | บันทึกข้อมูลเรียบร้อย |
| Submit success | ส่งคำขอเรียบร้อย หมายเลขอ้างอิง: {ref} |
| Network error | เชื่อมต่อไม่ได้ กรุณาลองใหม่ |
| Permission denied | คุณไม่มีสิทธิ์ในการดำเนินการนี้ |
| Session expired | เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่ |

## 7. Confirmation Dialogs
| Action | Title | Body | Confirm | Cancel |
|--------|-------|------|---------|--------|
| Delete record | ยืนยันการลบ | ข้อมูลนี้จะถูกลบถาวร ไม่สามารถกู้คืนได้ | ลบ | ยกเลิก |
| Reject approval | ยืนยันการปฏิเสธ | กรุณาระบุเหตุผลการปฏิเสธ | ปฏิเสธ | ยกเลิก |

## 8. Inline Validation (real-time)
| Field | Rule | Feedback |
|-------|------|----------|
| password (length) | < 8 ตัวอักษร | ต้องการอย่างน้อย 8 ตัวอักษร |
| password (strength) | ไม่มีตัวเลข | ควรมีตัวเลขอย่างน้อย 1 ตัว |
| ... |
```

---

## `--review` Mode

อ่าน `src/pages/**/*.tsx` แล้วหา:

1. **English text ที่ตกค้าง** — ต้องเป็นภาษาไทย
   ```bash
   grep -rnE ">[A-Z][a-z]+( [A-Z][a-z]+)*<" src/pages/ --include="*.tsx"
   ```

2. **Lorem ipsum / "ข้อมูล 1, 2"** — ต้อง replace
   ```bash
   grep -rnE "Lorem|ข้อมูล [0-9]|Data [0-9]" src/pages/ --include="*.tsx"
   ```

3. **คำที่ใช้ไม่ consistent** — เช่น "ลบ" / "เอาออก" / "ลบทิ้ง" สลับกัน
   ```bash
   # extract all visible text tokens และนับ frequency
   ```

4. **Error messages ที่ไม่ actionable** — เช่น "Invalid", "Error" อย่างเดียว

Output: รายงาน + แนะนำการแก้ พร้อม patch script (sed/Edit)

---

## Rules

- **ภาษาไทยเท่านั้น** — เว้น code identifier และ format mask (เช่น `example@domain.com`)
- **เป็น user-centric ไม่ใช่ system-centric** — "บันทึกเรียบร้อย" ✅, "Persisted successfully" ❌
- **Error message ต้องบอก WHY + HOW** — สาเหตุ + วิธีแก้
- **Tone consistent กับ persona** — ภาคราชการใช้ทางการ, consumer app ใช้กันเอง
- **ห้ามใช้ "กรุณา" ทุกประโยค** — เก็บไว้สำหรับ critical action เท่านั้น
- **ตัวเลข format ตาม locale** — `1,250 บาท` ไม่ใช่ `1250`

---

## Output

```
สร้าง: projects/[name]/03-design/microcopy-[name].md
(ถ้า --review) แก้: src/pages/**/*.tsx — text ที่ไม่ตรง spec
```
