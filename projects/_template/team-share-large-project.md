# เราทำ UX Project ขนาดใหญ่ยังไงให้ไม่ตาย 🗂️

> สรุปจากการจำลอง workflow สำหรับ project ที่มี 100–200 frames  
> แชร์ให้ทีมเพื่อใช้เป็น reference ก่อนเริ่ม project ใหม่

---

## ปัญหาที่ทุกคนเจอ (แต่ไม่ค่อยพูดถึง)

พอ project ใหญ่ขึ้น ปัญหาไม่ได้ scale เป็นเส้นตรง — มันระเบิด

- Screen 1–30: ทุกอย่างดูดี
- Screen 31–60: เริ่มสังเกตว่า card แต่ละหน้าไม่เหมือนกัน
- Screen 61+: กลับไป refactor ใหม่หมด เสียเวลา 2–3 วัน

ปัญหาจริงไม่ใช่ "ออกแบบช้า" แต่คือ **ไม่มีโครงสร้าง** รองรับตั้งแต่ต้น

---

## สิ่งที่เราเรียนรู้

### 1. นับ frame ให้ครบก่อนเริ่ม

สิ่งที่ทีมมักลืม: **States** และ **Edge Cases**

จากตัวอย่าง module "Product Registration":

| สิ่งที่คิดว่ามี | สิ่งที่ต้องออกแบบจริง |
|---------------|----------------------|
| 5 steps ของ wizard | 5 × default state |
| | 5 × validation error state |
| | 5 × loading state |
| | Success screen |
| | Draft saved screen |
| | Session expired |
| | Duplicate product error |
| **5 frames** | **22 frames** |

ถ้าไม่นับตั้งแต่ต้น → Dev hand-off แล้วพบว่าขาด design ไป 40%

---

### 2. สร้าง Component Library ก่อนสร้าง Screen ใด ๆ

คิดว่า "เดี๋ยวค่อย extract" — ไม่ทัน

ถ้ามี component library ก่อน:
- Screen ใหม่แต่ละหน้า = **compose ไม่ใช่สร้างใหม่**
- เปลี่ยน token ที่เดียว → อัปเดตทุก screen อัตโนมัติ
- ทีมทุกคน pull จาก library เดียวกัน → ไม่ drift

ใน Figma: สร้าง **Design System page** ก่อนเป็นหน้าแรก แล้วค่อย push screens

---

### 3. แบ่ง Figma เป็น Page ต่อ Module

อย่า dump ทุก frame ไว้ page เดียว

```
Page 0: INDEX (navigation map)
Page 1: Design System
Page 2: Auth (18 frames)
Page 3: Dashboard (18 frames)
Page 4: Registration (35 frames)
Page 5: QR Certificate (17 frames)
...
```

ข้อดี: ทีม QA review ทีละ module ได้เลย ไม่ต้องรอให้ครบ 145 frames

---

### 4. ตั้ง Naming Convention วันแรก ไม่เช่นนั้นเสียใจทีหลัง

```
[Module]-[Feature]-[Screen]-[State]

ตัวอย่าง:
  REG-Wizard-Step1-Default
  REG-Wizard-Step1-Validation-Error
  STF-Queue-List-Empty
```

Figma search ใช้ได้ดีก็ต่อเมื่อ name ถูก format ตั้งแต่แรก

---

### 5. Research ต้องแยกตาม Module

NLM (หรือ AI research tool ที่ใช้) มี context จำกัด  
ถ้าใส่ทุก requirement ลง notebook เดียว → คำตอบใน Q10+ เริ่ม vague

วิธีที่ดีกว่า: **1 notebook ต่อ 1 module ใหญ่**  
Research Auth ก็ notebook Auth, Research Registration ก็ notebook Registration

---

### 6. Parallel Work ได้ — แต่ต้องมี sync point

ไม่จำเป็นต้องทำทีละ module เสร็จแล้วค่อยทำต่อ

ตัวอย่าง:
- **คนที่ 1 (Research):** กำลัง research Registration module
- **คนที่ 2 (Design):** สร้าง screens ของ Auth module ที่ research เสร็จแล้ว

แต่มีกติกาเดียว: **ห้ามออกแบบ module ที่ยังไม่ผ่าน research approval**  
ไม่งั้น design assumptions ผิด → ต้อง rework

---

## สรุป Checklist ก่อนเริ่ม Project ≥100 Frames

```
□ นับ frame budget: happy path + states + edge cases (ทุก module)
□ วาง Figma page structure ก่อน push frame แรก
□ ตั้ง naming convention เป็นลายลักษณ์อักษร
□ สร้าง component library (core set) ก่อนออกแบบ screen ใด ๆ
□ แบ่ง research เป็น notebook ต่อ module
□ กำหนด milestone checkpoints (ไม่ใช่แค่ deadline รวม)
```

---

## ตัวเลขที่น่าสนใจ

จากการจำลอง 134 frames (6 modules):

- สร้าง screens ด้วย screen-factory: **~2 ชั่วโมง** (vs. 3–4 วันถ้าไม่มี component library)
- คำสั่งที่ใช้รวม: 15 คำสั่ง
- จำนวน sprint: 5 sprint (2 สัปดาห์ต่อ sprint)
- WCAG audit: ทำทีละ module ไม่ใช่ทั้ง project พร้อมกัน

---

*ถ้าอยากดูรายละเอียดเต็ม → ดูที่ `projects/_template/large-project-workflow.md`*
