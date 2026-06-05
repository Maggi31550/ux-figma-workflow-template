# Export Prototype — Single File

Build React prototype เป็น HTML ไฟล์เดียว เปิดได้โดยไม่ต้องรัน server

## Usage
```
/skills:export-prototype [project-name]
/skills:export-prototype [project-name] --open     ← เปิดไฟล์หลัง export เสร็จ
/skills:export-prototype [project-name] --clean    ← revert vite.config หลัง build
```

---

## Workflow

### STEP 1 — ตรวจสอบ Prerequisites

```bash
cd projects/[name]/05-prototype

# ตรวจ TypeScript ก่อน build
npx tsc --noEmit
```

- ❌ มี type error → หยุด แจ้ง error ให้แก้ก่อน
- ✅ ผ่าน → ไป STEP 2

---

### STEP 2 — ตรวจ Router Type

```bash
grep "createBrowserRouter\|createHashRouter" src/router.tsx
```

ถ้าพบ `createBrowserRouter` → เปลี่ยนเป็น `createHashRouter` ก่อน build:

```bash
sed -i '' 's/createBrowserRouter/createHashRouter/g' src/router.tsx
```

> `createBrowserRouter` ใช้ History API ต้องการ server — จะ 404 ทันทีเมื่อเปิดด้วย `file://`
> `createHashRouter` ใช้ `#` ใน URL — ทำงานได้โดยไม่ต้อง server

---

### STEP 3 — ติดตั้ง vite-plugin-singlefile

```bash
# ตรวจว่ามีอยู่แล้วหรือยัง
grep -c "vite-plugin-singlefile" package.json || npm install -D vite-plugin-singlefile
```

---

### STEP 3 — อัปเดต vite.config.ts

อ่าน `vite.config.ts` ปัจจุบัน แล้วเพิ่ม plugin:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  resolve: {
    alias: { '@': '/src' },
  },
  build: {
    target: 'esnext',
    assetsInlineLimit: 100000000,
    chunkSizeWarningLimit: 100000000,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
  },
})
```

ถ้าใช้ `--clean` ให้ backup ไฟล์เดิมก่อน:
```bash
cp vite.config.ts vite.config.ts.bak
```

---

### STEP 4 — Build

```bash
npm run build
```

ตรวจว่า `dist/index.html` มีอยู่และขนาดสมเหตุสมผล (ควรได้ > 100KB):
```bash
ls -lh dist/index.html
```

---

### STEP 5 — Copy Output

```bash
# สร้าง export folder ถ้ายังไม่มี
mkdir -p ../../../projects/[name]/06-export

# Copy พร้อมชื่อที่อ่านง่าย + timestamp
cp dist/index.html "../../../projects/[name]/06-export/[name]-prototype-$(date +%Y%m%d).html"
```

ไฟล์ output: `projects/[name]/06-export/[name]-prototype-YYYYMMDD.html`

---

### STEP 6 — Cleanup (ถ้าใช้ --clean)

```bash
# Revert vite.config กลับเป็นเวอร์ชันก่อน build
mv vite.config.ts.bak vite.config.ts
```

ถ้าไม่ใช้ `--clean` → คง `vite-plugin-singlefile` ไว้ใน config (build ครั้งต่อไปจะได้ single file อัตโนมัติ)

---

### STEP 7 — ถ้าใช้ --open

```bash
open "../../../projects/[name]/06-export/[name]-prototype-$(date +%Y%m%d).html"
```

---

## Output

```
projects/[name]/
└── 06-export/
    └── [name]-prototype-YYYYMMDD.html   ← ส่งให้ client ได้เลย
```

**ขนาดที่คาดหวัง:** 500KB – 2MB ขึ้นอยู่กับจำนวน screens และ assets

---

## ข้อจำกัดที่ควรแจ้ง client

- ไฟล์ใช้ React Router — navigation ทำงานได้ปกติภายในไฟล์
- ไม่มี backend จริง — ข้อมูลทั้งหมดเป็น mock data
- รูปภาพภายนอก (CDN) ต้องการ internet connection
- Google Fonts ต้องการ internet connection — ถ้าต้องการ offline สมบูรณ์ให้ embed font ก่อน build
