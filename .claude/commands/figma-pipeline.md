# Figma Pipeline — Prototype → Figma

**Thin wrapper เรียก Figma Publisher agent.**
นำ React prototype ที่ build แล้วเข้า Figma แบบ selective + safe

## Usage
```
/figma-pipeline [project-name] [figma-file-url]
/figma-pipeline [project-name] [figma-file-url] --new-file     ← สร้าง Figma file ใหม่
/figma-pipeline [project-name] [figma-file-url] --screens-only ← ข้าม Design System
/figma-pipeline [project-name] [figma-file-url] --ds-only      ← ทำเฉพาะ Design System
```

---

## How this command works

Command นี้เป็น **thin wrapper** — โครงสร้าง pipeline เต็มอยู่ที่ agent spec:

```
.claude/agents/figma-publisher.md
```

เมื่อรัน command นี้:
1. Spawn **Figma Publisher** subagent (Task tool with subagent_type="Figma Publisher")
2. ส่ง argument (`project-name`, `figma-file-url`, flags) เข้า agent
3. Agent ใช้ Figma MCP + ทำตาม stage 1–4 ที่กำหนดใน spec

---

## Stages Overview (รายละเอียดดูใน agent spec)

| Stage | งาน | Skill ที่ใช้ |
|-------|-----|----------------|
| 1 | Design System Setup — sync tokens.css → Figma Variables | `figma-use` (system) — mandatory before `use_figma` calls |
| 2 | Key Screen Selection — 5–8 screens + user confirm | (no skill) |
| 3 | Screen Generation — สร้าง frames | `figma-generate-design` (system) |
| 4 | Code Connect + Prototype Flow guide | `figma-code-connect` (system) + `/skills:figma-flow` |

---

## Prerequisites

ก่อนรัน:
- ✅ `projects/[name]/05-prototype/` build ได้และ TypeScript ผ่าน
- ✅ `screen-inventory-[name].md` มีอยู่
- ✅ `tokens.css` มี design tokens ครบ
- ✅ Audit รอบสุดท้าย (Stage 5B) PASS แล้ว (optional แต่แนะนำ)

---

## ⚠️ Pipeline Principles

- **One-way:** prototype → Figma เท่านั้น ไม่ sync กลับ
- **Selective:** สร้างเฉพาะ 5–8 Key Screens
- **Labelled:** ทุก auto-generated frame มี `[Generated]` suffix
- **Manual flow:** Prototype connections ระหว่าง frame ทำ manual โดย designer
- **Variables first:** ถ้า Design System ยังไม่พร้อม จะไม่สร้าง screen

---

## Output

```
Figma File:
├── Page: "Design System [Generated]"
│   └── Variables: Color, Typography, Spacing, Radius
├── Page: "Key Screens [Generated]"
│   ├── [Screen 1] [Generated]
│   └── ... (5–8 screens)
└── Page: "⚠️ Prototype Flow — Manual Required"

projects/[name]/04-figma/
├── figma-url-[name].md
├── key-screens-[name].md
├── code-connect-[name].md
└── figma-flow.md
```

---

## ดูเพิ่ม

- Agent spec เต็ม: `.claude/agents/figma-publisher.md`
- Flow guide skill: `.claude/commands/skills/figma-flow.md`
- System skills ที่ใช้: `figma-use`, `figma-generate-design`, `figma-code-connect`, `figma-generate-library`
