# NotebookLM Batch Research

ถามคำถามทั้งหมดจาก ai-questions file เข้า NotebookLM โดยอัตโนมัติ — output เป็น structured research answers พร้อมใช้ใน Stage 2

## Usage
```
/nlm-batch-research [project-name] [notebook-id]
/nlm-batch-research ggp-poc 5fd9229b-1792-480f-8b6a-44cda36fc11a
/nlm-batch-research [project-name] --create "[notebook-title]" --sources [file1] [url2]
```

## NLM CLI Path
```bash
NLM="/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm"
```

---

## Workflow

### STEP 1 — Verify Notebook

```bash
# ตรวจ authentication
$NLM auth check

# Set notebook context
$NLM use [notebook-id]

# ดู sources ที่มี
$NLM source list
```

ถ้า error "account-routing mismatch" → รัน `$NLM login` ก่อน

### STEP 2 — Add Sources (ถ้าเป็น project ใหม่)

```bash
# เพิ่มไฟล์ requirements
$NLM source add projects/[name]/01-brief/req.pdf
$NLM source add projects/[name]/01-brief/brief.md

# เพิ่ม URLs ที่เกี่ยวข้อง
$NLM source add "https://..."

# รอ indexing เสร็จ
$NLM source wait

# เพิ่ม web research (optional)
$NLM source add-research "[project domain] UX patterns 2025" --mode fast
$NLM research wait --import-all
```

### STEP 3 — Extract Questions

อ่าน `projects/[name]/02-research/ai-questions-[name].md`
Parse คำถามทุกข้อ (format: `Q1:`, `Q2:` หรือ `## คำถามที่ N`)

### STEP 4 — Ask All Questions

Loop ถามทุกข้อ บันทึก answers:

```bash
for each question in questions:
    answer = $NLM ask "[question]"
    append to output file
```

**ข้อควรระวัง:**
- ถาม sequential (ไม่ parallel) — NLM จำ conversation context
- ถ้า question เกี่ยวข้องกัน → context จาก Q ก่อนหน้าช่วย
- รอ 2–3 วินาทีระหว่างคำถาม (rate limit)

### STEP 5 — Format Output

สร้าง `projects/[name]/02-research/ai-answers-[name].txt`:

```
AI RESEARCH ANSWERS — AUTO-GENERATED via NotebookLM CLI
════════════════════════════════════════════════════════
Project:  [name]
Notebook: [title]
Date:     YYYY-MM-DD
Source Q: ai-questions-[name].md ([N] questions)
════════════════════════════════════════════════════════

─────────────────────────────────────────
Q1: [คำถาม]
─────────────────────────────────────────
[คำตอบจาก NLM พร้อม citations [1][2][3]]


─────────────────────────────────────────
Q2: [คำถาม]
─────────────────────────────────────────
[คำตอบ...]

...

════════════════════════════════════════════════════════
KEY INSIGHTS SUMMARY (auto-extracted)
════════════════════════════════════════════════════════
• [insight 1]
• [insight 2]
• [insight 3]
...
════════════════════════════════════════════════════════
```

### STEP 6 — Auto-Trigger Stage 2

เมื่อ answers file สร้างเสร็จ:
- แจ้งผู้ใช้: "answers ready — [project-name]"
- ถาม: "ต้องการให้ไป Stage 2 (Research Synthesis) เลยไหม?"
- ถ้า yes → เริ่ม Stage 2 ทันที

---

## Create New Notebook Mode (`--create`)

```bash
# สร้าง notebook ใหม่สำหรับ project
$NLM create "[notebook-title]"

# รับ notebook ID ที่สร้าง
notebook_id = $NLM list --json | jq '.notebooks[0].id'

# เพิ่ม sources ที่ระบุ
for source in sources:
    $NLM source add [source]

$NLM source wait
```

---

## Tips
- **Conversation memory:** NLM จำ context ข้ามคำถาม — เรียงคำถามจาก broad → specific
- **Citation quality:** คำถามที่ specific จะได้ citations ที่แม่นยำกว่า
- **Language:** ถามภาษาไทยหรืออังกฤษก็ได้ — NLM ตอบตามภาษาที่ถาม
- **Rate limit:** ถ้า error timeout ให้รอ 30 วินาทีแล้วลองใหม่

---

## Output
```
สร้าง: projects/[name]/02-research/ai-answers-[name].txt
พร้อมสำหรับ: Stage 2 — Research Synthesis
```
