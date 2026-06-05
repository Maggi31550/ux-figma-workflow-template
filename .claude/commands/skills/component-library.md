# Component Library Builder (React)

สร้างหรืออัปเดต shared component library ใน React prototype — ทุก screen ใหม่ compose จาก library นี้

## Usage
```
/skills:component-library init [project-name]            ← สร้าง library จาก shell ที่เพิ่งสร้าง
/skills:component-library add [project-name] [component] ← เพิ่ม component ใหม่
/skills:component-library list [project-name]            ← แสดง components ทั้งหมด
/skills:component-library audit [project-name]           ← หา UI ที่ duplicate ระหว่าง pages → extract
```

> เรียกหลัง Stage 1 (Project Shell) ก่อนเริ่ม Feature Loop เสมอ

---

## Mode 1 — `init`

ใช้หลัง ux-producer สร้าง shell เสร็จ — สร้าง primitive components ที่ทุก page จะใช้ซ้ำ

### STEP 1 — Audit Shell
อ่าน:
```
05-prototype/src/styles/tokens.css         ← design tokens
05-prototype/src/components/Layout.tsx     ← shell wrapper
05-prototype/src/components/Sidebar.tsx
05-prototype/src/components/Topbar.tsx
```

### STEP 2 — สร้าง Core Components

สร้างไฟล์ใน `05-prototype/src/components/ui/`:

```
src/components/ui/
├── Button.tsx           ← variant: primary | secondary | danger | ghost | size: sm | md | lg
├── Input.tsx            ← controlled input + error state + label
├── Select.tsx
├── Checkbox.tsx         ← พร้อม hit area ≥ 44px
├── Radio.tsx
├── Card.tsx             ← header + body + footer slots
├── Badge.tsx            ← critical | high | medium | low | success | info
├── Table.tsx            ← header + rows + empty state
├── Stepper.tsx          ← N steps + active state
├── ProgressBar.tsx
├── EmptyState.tsx       ← icon + title + description + CTA
├── Toast.tsx            ← + ToastProvider context
├── Modal.tsx            ← + Esc/overlay close + focus trap
├── Skeleton.tsx
├── FilterTabs.tsx
└── index.ts             ← re-export ทุก component
```

### STEP 3 — Component Pattern

ทุก component:
- TypeScript strict + explicit props type
- ใช้ `var(--color-*)` / `var(--space-*)` ผ่าน Tailwind arbitrary values หรือ inline style — ห้าม hardcode
- Forward ref ทุก primitive (`Button`, `Input`)
- Accessibility ตั้งแต่แรก (`aria-*`, semantic element)
- ภาษาไทยใน default text (เช่น `Toast.tsx` default success = "บันทึกเรียบร้อย")

ตัวอย่าง `Button.tsx`:
```tsx
import { forwardRef, type ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'secondary' | 'danger' | 'ghost'
type Size = 'sm' | 'md' | 'lg'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', loading, children, className = '', ...props }, ref) => {
    const base = 'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
    const variants: Record<Variant, string> = {
      primary: 'bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-dark)] focus-visible:outline-[var(--color-primary)]',
      secondary: 'bg-[var(--color-surface)] text-[var(--color-text)] border border-[var(--color-border)] hover:bg-[var(--color-background)]',
      danger: 'bg-[var(--color-error)] text-white hover:opacity-90',
      ghost: 'text-[var(--color-text)] hover:bg-[var(--color-background)]',
    }
    const sizes: Record<Size, string> = {
      sm: 'h-8 px-3 text-sm min-w-[44px]',
      md: 'h-10 px-4 text-base min-w-[44px]',
      lg: 'h-12 px-6 text-lg min-w-[44px]',
    }
    return (
      <button
        ref={ref}
        className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading ? 'กำลังโหลด...' : children}
      </button>
    )
  }
)
Button.displayName = 'Button'
```

### STEP 4 — Generate COMPONENTS.md

สร้าง `05-prototype/COMPONENTS.md`:
```markdown
# Component Library — [Project Name]

## Available Components
| Component | Path | Props | Usage |
|-----------|------|-------|-------|
| Button | components/ui/Button | variant, size, loading | ทุก action |
| Card | components/ui/Card | header, footer | Container |
| Badge | components/ui/Badge | tone (critical/high/...) | Status |
| ...

## Import Pattern
\`\`\`tsx
import { Button, Card, Badge } from '@/components/ui'
\`\`\`

## Design Token Usage
- สี: `var(--color-primary)`, `var(--color-text)`
- Spacing: `var(--space-4)`
- Font: `var(--text-base)`
```

---

## Mode 2 — `add [component]`

```
/skills:component-library add ggp-poc Tooltip
```

### STEP 1 — ตรวจว่า component ที่ขอมีอยู่แล้วไหม
```bash
grep -l "export.*[Tt]ooltip" src/components/ui/*.tsx
```
ถ้ามีแล้ว → แจ้ง + แสดง path, ไม่สร้างซ้ำ

### STEP 2 — สร้างไฟล์ใหม่
- ใช้ pattern เดิมจาก Button.tsx (forwardRef + variant + size + token usage)
- เพิ่ม `index.ts` re-export

### STEP 3 — Update docs
- เพิ่มแถวใน `COMPONENTS.md`

---

## Mode 3 — `audit`

หา duplicate UI patterns ระหว่าง pages ที่ควร extract เป็น component:

```bash
# หา className ที่ซ้ำ ≥ 3 ครั้ง
grep -rh "className=\"" src/pages/ --include="*.tsx" | sort | uniq -c | sort -rn | head -20

# หา inline JSX ที่ซ้ำ (button styles, card layouts)
```

Output คำแนะนำ:
```
🔍 Found duplicates:
- Card-like div (3+ pages) → ควร extract เป็น <Card>
- Status pill (5+ pages) → ควร extract เป็น <Badge>
```

---

## Rules
- **ห้าม hardcode สี** — ทุกค่าผ่าน `var(--color-*)` หรือ Tailwind token
- **Forward ref ทุก primitive** — รองรับ form library ในอนาคต
- **ภาษาไทย default text** — placeholder, error, empty state
- **WCAG ตั้งแต่แรก** — `aria-label`, focus ring, tap target ≥ 44px
- **TypeScript strict** — explicit props type, no `any`

---

## Output
```
สร้าง/แก้: 05-prototype/src/components/ui/[Component].tsx
แก้: 05-prototype/src/components/ui/index.ts
แก้: 05-prototype/COMPONENTS.md
```
