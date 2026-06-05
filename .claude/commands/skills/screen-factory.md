# Screen Factory (React)

Scaffold 1–5 React screens จาก component library + pattern — เร็ว consistent ใช้ design tokens เต็ม

## Usage
```
/skills:screen-factory [project-name] [feature] [screen1] [screen2] ...
/skills:screen-factory ggp-poc "ModelConfig" "SelectModel" "ModelSettings" "RunPreview"
/skills:screen-factory ggp-poc "Notifications" "Inbox" "Detail" --pattern=list-detail
/skills:screen-factory ggp-poc "Approval" "Queue" --persona=manager
```

## Patterns

| Pattern | `--pattern` | Screens |
|---------|-------------|---------|
| List → Detail | `list-detail` | List with filters + Detail view |
| Wizard / Stepper | `wizard` | Step 1, 2, 3 + Summary + Success |
| Dashboard | `dashboard` | Overview KPIs + Charts + Table |
| Form + Validation | `form` | Form + Error states + Success |
| Empty → Filled | `empty-state` | Empty + Loading + Filled |
| Settings | `settings` | Settings groups + Edit modal |
| Confirmation | `confirm` | Preview → Confirm → Result |

---

## Workflow

### STEP 1 — Verify Prerequisites
```bash
PROJECT_DIR="projects/[name]/05-prototype"

# ต้องมี shell แล้ว
test -f "$PROJECT_DIR/src/router.tsx" || echo "❌ ยังไม่มี shell — รัน Stage 1 ก่อน"

# ต้องมี component library แล้ว
test -f "$PROJECT_DIR/src/components/ui/index.ts" || echo "⚠️ component library ยังไม่ได้ init — รัน /skills:component-library init ก่อน"

# ต้องมี tokens
test -f "$PROJECT_DIR/src/styles/tokens.css" || echo "❌ tokens.css หาย"
```

### STEP 2 — อ่าน Context
- `tokens.css` — design tokens
- `src/components/ui/index.ts` — components ที่ใช้ได้
- `02-research/screen-inventory-[name].md` — Screen Inventory (verify screen names)
- `03-design/microcopy-[name].md` (ถ้ามี) — UI labels, error messages
- `03-design/handoff-notes-[name].md` (ถ้ามี) — layout spec

### STEP 3 — Plan Screens

ต่อ screen สรุป:
- **Path:** `/[feature-kebab]/[screen-kebab]`
- **Components ที่ใช้:** จาก `ui/` (เช่น Card, Button, Table)
- **Mock data:** ข้อมูลสมจริงสำหรับ domain นี้ — ห้าม "ข้อมูล 1, 2, 3"
- **States:** default + loading + empty + error (ถ้า relevant)
- **Navigation:** From / To / Back
- **Persona:** role ที่เข้าถึงได้

### STEP 4 — Scaffold Files

```
src/pages/[Feature]/
├── index.tsx              ← list/overview (default)
├── [Screen1].tsx
├── [Screen2].tsx
└── _mocks.ts              ← mock data ของ feature นี้ (re-use ระหว่าง screens)
```

### STEP 5 — Generate Screen Template

ตัวอย่าง list-detail pattern:

```tsx
// src/pages/Notifications/Inbox.tsx
import { useNavigate } from 'react-router-dom'
import { Card, Badge, EmptyState, Button } from '@/components/ui'
import { Bell, ChevronRight } from 'lucide-react'
import { notifications } from './_mocks'

export default function NotificationsInbox() {
  const navigate = useNavigate()

  if (notifications.length === 0) {
    return (
      <EmptyState
        icon={<Bell />}
        title="ยังไม่มีการแจ้งเตือน"
        description="คุณจะเห็นการแจ้งเตือนที่นี่เมื่อมีกิจกรรมใหม่"
      />
    )
  }

  return (
    <div className="flex flex-col gap-4">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-[var(--color-text)]">
          การแจ้งเตือน
        </h1>
        <Badge tone="info">{notifications.length} รายการ</Badge>
      </header>

      <div className="flex flex-col gap-2">
        {notifications.map((n) => (
          <Card
            key={n.id}
            onClick={() => navigate(`/notifications/${n.id}`)}
            className="cursor-pointer hover:bg-[var(--color-background)]"
          >
            <div className="flex items-center justify-between">
              <div className="flex flex-col gap-1">
                <span className="font-medium">{n.title}</span>
                <span className="text-sm text-[var(--color-text-muted)]">
                  {n.preview}
                </span>
              </div>
              <ChevronRight className="text-[var(--color-text-muted)]" />
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
```

### STEP 6 — Update Router

แก้ `src/router.tsx`:
```tsx
import NotificationsInbox from '@/pages/Notifications/Inbox'
import NotificationsDetail from '@/pages/Notifications/Detail'

// ใน children
{ path: 'notifications', element: <NotificationsInbox /> },
{ path: 'notifications/:id', element: <NotificationsDetail /> },
```

### STEP 7 — Update Sidebar Nav (ถ้าจำเป็น)

ถ้า screen ใหม่ควรอยู่ใน main nav — เพิ่มใน `Sidebar.tsx`:
```tsx
{ path: '/notifications', label: 'การแจ้งเตือน', icon: Bell, roles: ['employee', 'manager'] }
```

### STEP 8 — Update Screen Inventory

แก้ `02-research/screen-inventory-[name].md`:
```markdown
- [x] Inbox — ✅ implemented
- [x] Detail — ✅ implemented
```

### STEP 9 — Quality Check

```bash
cd projects/[name]/05-prototype
npx tsc --noEmit
```

Verify checklist:
- [ ] ทุก screen import จาก `@/components/ui` ไม่ duplicate JSX
- [ ] ทุก path ใน router.tsx จับคู่กับไฟล์จริง
- [ ] Mock data ภาษาไทย สมจริง
- [ ] ใช้ `var(--color-*)` ไม่มี hardcode hex
- [ ] ทุก interactive element มี hit area ≥ 44px (ผ่าน Button default size)
- [ ] Back navigation มีทุก screen ยกเว้น root list

---

## Pattern-Specific Notes

### `wizard`
- ใช้ `<Stepper>` ที่ top
- ปุ่ม "ถัดไป" disable จนกว่า validation จะผ่าน
- "ย้อนกลับ" ทุก step ยกเว้น step 1
- Final step → Success screen พร้อมปุ่ม "เสร็จสิ้น" navigate กลับ root

### `dashboard`
- KPI cards row 1 (3–4 cards)
- Main chart row 2 (full width)
- Secondary 2-column chart/table row 3
- ทุก KPI มี trend arrow + comparison text

### `form`
- Controlled inputs ผ่าน `useState` หรือ `react-hook-form`
- Error message ใต้ field
- Submit disabled ขณะ loading
- Success → toast หรือ redirect

### `list-detail`
- List: filter tabs + search + table/cards
- Empty state เมื่อ filter ไม่เจอ
- Detail: header + sections + actions
- Back button หรือ breadcrumb เสมอ

---

## Rules
- **Mock data สมจริง** — ใช้ชื่อ/วันที่/สถานะที่เหมาะกับ domain
- **ห้าม inline color/spacing** — token ผ่าน CSS variable เสมอ
- **Components จาก library เท่านั้น** — ถ้าไม่มีให้รัน `/skills:component-library add` ก่อน
- **Lucide icons** — ห้าม inline SVG
- **TypeScript strict** — ทุก prop typed

---

## Output
```
สร้าง: src/pages/[Feature]/[Screen].tsx
สร้าง: src/pages/[Feature]/_mocks.ts
แก้: src/router.tsx (เพิ่ม route)
แก้: src/components/Sidebar.tsx (ถ้าจำเป็น)
แก้: 02-research/screen-inventory-[name].md (mark [x])

รายงาน:
  ✅ เพิ่ม [N] screens: [list]
  🔗 Routes: [paths]
  ✅ npx tsc --noEmit ผ่าน
```
