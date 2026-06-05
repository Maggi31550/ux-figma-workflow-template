# Design System

โฟลเดอร์นี้สร้างโดยอัตโนมัติเมื่อรัน `/design-system-pipeline [project] [figma-url]`

จะมี:
- `tokens.json` — DTCG canonical (source of truth)
- `tokens.css`, `tokens.ts` — generated for prototype
- `components/` — component cards (.md + .png + .types.ts)
- `overview.html` — single-page gallery สำหรับทีม
- `handoff-package/` — package ส่ง dev
- `CHANGELOG.md` — token change history
- `figma-sync-log.md` — sync timestamps

## รัน Pipeline

```bash
# Initial setup (run once)
/design-system-pipeline [project] [figma-file-url]

# Recurring sync
/design-system-pipeline [project] --pull       # Figma → code
/design-system-pipeline [project] --push       # code → Figma
/design-system-pipeline [project] --sync-status
```

ดู [`.claude/commands/design-system-pipeline.md`](../../../.claude/commands/design-system-pipeline.md) สำหรับรายละเอียดเต็ม
