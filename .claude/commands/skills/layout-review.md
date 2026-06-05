# /layout-review

Audit และแก้ไข Layout Shell (Sidebar + Topbar + Layout wrapper) ของ React prototype

## Usage
```
/layout-review [project-name]
/layout-review [project-name] --fix     ← แก้ไขอัตโนมัติ
/layout-review [project-name] --report  ← รายงานอย่างเดียว ไม่แก้
```

---

## สิ่งที่ตรวจสอบ

### 1. Role-Based Navigation
- [ ] Sidebar filter ตาม role — employee ไม่ควรเห็น Admin/HR sections
- [ ] มี role switcher สำหรับ prototype demo
- [ ] User info ท้าย Sidebar แสดงชื่อ + role จริง (ไม่ hardcode)
- [ ] RoleContext ครอบทั้ง Layout tree

### 2. Breadcrumb Coverage
- [ ] ทุก route ใน `router.tsx` มีรายการใน `breadcrumbMap`
- [ ] Dynamic routes (`:id`, `:slug`) ใช้ `startsWith` matching ไม่ใช่ exact match
- [ ] ไม่มี route ที่แสดง "หน้าหลัก" เพราะหา breadcrumb ไม่เจอ

### 3. Icon Semantics
- [ ] ไม่มี `ChevronRight` ใช้เป็น nav icon (ไม่มีความหมาย)
- [ ] แต่ละ nav item มี icon ที่สื่อความหมายถึง feature นั้นจริงๆ
- [ ] Icon consistent กับ icon ที่ใช้ใน page header

### 4. Interactive Elements ใน Shell
- [ ] Bell / Notification button มี onClick handler
- [ ] Notification dropdown แสดง unread count badge
- [ ] Logout button มี handler (แม้จะเป็น mock ใน prototype)
- [ ] Role switcher dropdown ปิดได้เมื่อคลิก overlay หรือเลือก role แล้ว

### 5. Active State Correctness
- [ ] Active highlight ตรงกับ current route
- [ ] Parent route ไม่ highlight เมื่ออยู่ที่ child route (เช่น `/time/logs` ≠ active `/time`)
- [ ] Dynamic route เช่น `/approval/detail/:id` ต้อง highlight `/approval/queue` ใน sidebar

### 6. Accessibility (WCAG 2.1 AA)
- [ ] `<nav>` ใช้ `aria-label` บน Sidebar และ Topbar breadcrumb
- [ ] Bell button มี `aria-label` บอก unread count
- [ ] Dropdown menus ปิดได้ด้วย Esc key
- [ ] Focus trap ใน modal/dropdown (ถ้ามี)
- [ ] Tap targets ≥ 44px (nav items, buttons)

### 7. Layout Stability
- [ ] `marginLeft` บน content area ตรงกับ `--sidebar-width` token
- [ ] Topbar `position: sticky` ทำงานถูกต้อง (ไม่ scrollหายไปกับ content)
- [ ] Sidebar `position: fixed` ไม่ทับ content ที่ overflow

---

## วิธีตรวจสอบ

### Step 1 — อ่านไฟล์ shell
```
src/components/Layout.tsx
src/components/Sidebar.tsx
src/components/Topbar.tsx
src/router.tsx
src/contexts/RoleContext.tsx (ถ้ามี)
```

### Step 2 — Cross-check breadcrumbs
```bash
# ดึง routes ทั้งหมดจาก router.tsx
grep -n "path:" src/router.tsx

# เทียบกับ breadcrumbMap ใน Topbar.tsx
grep -n "'/[a-z]" src/components/Topbar.tsx
```

### Step 3 — ตรวจ icon imports
```bash
# หา ChevronRight ที่ใช้เป็น nav icon
grep -n "ChevronRight" src/components/Sidebar.tsx
```

### Step 4 — ตรวจ dead buttons
```bash
grep -n "onClick" src/components/Topbar.tsx src/components/Sidebar.tsx
```

### Step 5 — TypeScript check
```bash
npx tsc --noEmit
```

---

## Output

รายงานใน format นี้:

```
## Layout Review — [project-name]

### ✅ ผ่าน
- Role-based nav filtering (4 roles)
- Breadcrumb ครอบคลุมทุก route
- ...

### ❌ ต้องแก้ไข
- [ ] Bell button ไม่มี onClick — Topbar.tsx:62
- [ ] /time/correction/status ไม่มีใน breadcrumbMap — Topbar.tsx
- [ ] ChevronRight ใช้ใน 6 nav items — Sidebar.tsx:32-49

### การแก้ไข
[ถ้าใช้ --fix จะแก้ทันที, ถ้าไม่ใช้ จะแสดงสิ่งที่ต้องทำ]
```

---

## เมื่อไหร่ควรรัน

- หลัง Stage 4 (สร้าง React shell) ก่อนเริ่ม Stage 5
- หลัง Stage 5 ก่อน deliver prototype
- ทุกครั้งที่เพิ่ม route ใหม่เข้า router.tsx
- หลังเปลี่ยน role structure หรือ navigation groups
