# figma-flow — Prototype Flow Guide Generator

อ่าน `router.tsx` และ component navigation calls แล้วสร้าง flow guide สำหรับ designer ทำ Figma Prototype connections ด้วยตนเอง

## Usage
```
/skills:figma-flow [project-name]
/skills:figma-flow [project-name] --key-screens-only  ← เฉพาะ screens ใน key-screens-[name].md
```

---

## Workflow

### STEP 1 — อ่าน Router
```bash
cat projects/[name]/05-prototype/src/router.tsx
```
สกัด route list ทั้งหมด

### STEP 2 — ตรวจ Navigation calls ใน components
```bash
grep -rn "navigate(" projects/[name]/05-prototype/src/pages/ | grep -v "node_modules"
grep -rn "to=\"/" projects/[name]/05-prototype/src/pages/ | grep -v "node_modules"
```

สกัด: source component → target route → trigger (button label / action)

### STEP 3 — อ่าน Key Screens (ถ้ามี)
```bash
cat projects/[name]/04-figma/key-screens-[name].md 2>/dev/null || echo "ไม่มี key-screens file"
```

ถ้าใช้ `--key-screens-only` → กรองเฉพาะ connections ระหว่าง key screens

### STEP 4 — สร้าง Flow Map

สร้างไฟล์ `projects/[name]/04-figma/figma-flow.md`:

```markdown
# Figma Prototype Flow Guide — [project-name]
สร้างเมื่อ: [date]
อ้างอิง: router.tsx + navigation calls ใน src/pages/

## วิธีใช้
1. เปิด Figma → เลือก Page "Key Screens [Generated]"
2. ใช้ Prototype Mode (Shift+E)
3. ต่อ connection ตาม flow list ด้านล่าง
4. แต่ละ connection: เลือก element → ลาก hotspot → เลือก destination frame

---

## Flow Connections

### [Feature Group 1]

| From Frame | Trigger | To Frame | Interaction |
|------------|---------|----------|-------------|
| [Screen] [Generated] | ปุ่ม "[label]" | [Screen] [Generated] | On Click → Navigate |
| [Screen] [Generated] | ปุ่มยืนยัน | [Screen] [Generated] — Success | On Click → Navigate |

### [Feature Group 2]
...

---

## Back Navigation (ทุก screen)
ปุ่ม "ยกเลิก" / "กลับ" → navigate กลับ screen ก่อนหน้าเสมอ
ใช้ Figma: Interaction → "Go back" (ไม่ต้องระบุ frame ปลายทาง)

---

## Overlay / Modal (ถ้ามี)
| Trigger | Overlay Frame | Dismiss |
|---------|--------------|---------|
| ... | ... | Click outside → Close overlay |

---

## หมายเหตุ
- Frame ที่ไม่อยู่ใน Key Screens → ไม่ต้องต่อ connection
- Success/Error states → ใช้ Smart Animate ถ้าต้องการ transition
- Flow นี้ครอบคลุมเฉพาะ happy path — edge cases ให้ designer เพิ่มเอง
```

---

## Output

```
projects/[name]/04-figma/
└── figma-flow.md    ← Flow guide พร้อม table สำหรับ designer
```

ไฟล์นี้ถูก reference จาก `figma-pipeline.md` Stage 4D และ comment ใน Figma Prototype Flow page
