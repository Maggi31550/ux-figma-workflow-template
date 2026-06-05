# NotebookLM Quick Ask

Ask one or more UX research questions to an existing NotebookLM notebook and save answers.

## Usage
```
/skills:nlm-ask [notebook-id] "[question]"
/skills:nlm-ask [notebook-id] --file [ai-questions-file.md]   ← ask all questions in file
/skills:nlm-ask --list                                         ← list available notebooks
```

## How to Use

### List notebooks first
```bash
/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm list
```

### Ask a single question
```bash
NLM="/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm"
$NLM use [notebook-id]
$NLM ask "[your question]"
```

### Ask all questions from a file (batch mode)
Claude จะ:
1. อ่านไฟล์ `ai-questions-[name].md`
2. Extract คำถามทีละข้อ (Q1, Q2, Q3...)
3. Loop `notebooklm ask` สำหรับทุกข้อ
4. รวม answers ลงใน `ai-answers-[name].txt`
5. แสดง summary ของ insights ที่ได้

## Output Format (ai-answers-[name].txt)
```
AI RESEARCH ANSWERS — AUTO-GENERATED via NotebookLM CLI
Notebook: [title]
Date: YYYY-MM-DD

─────────────────────────────────────────
Q1: [question]
─────────────────────────────────────────
[answer from NotebookLM with citations]

─────────────────────────────────────────
Q2: [question]
─────────────────────────────────────────
[answer from NotebookLM with citations]
...
```

## Tips
- ถ้า error "account-routing" → รัน `notebooklm login` ใหม่
- ใช้ full UUID เสมอ (ไม่ตัดสั้น)
- `notebooklm ask` จะจำ conversation context ข้ามคำถามได้
- เพิ่ม `--no-context` ถ้าต้องการ fresh answer สำหรับแต่ละข้อ
