# Perplexity Batch Research

ถามคำถามทั้งหมดจาก research plan เข้า Perplexity แบบ batch — output เป็น structured external research พร้อมใช้คู่กับ NLM ใน Stage 2

## Usage
```
/skills:plx-batch-research [project-name]
/skills:plx-batch-research [project-name] --file [questions-file.md]
/skills:plx-batch-research [project-name] --model sonar-pro
/skills:plx-batch-research [project-name] --recency month
```

## Input

อ่านจาก `projects/[name]/02-research/plx-questions-[name].md`

ถ้ายังไม่มี — generate จาก `ux-idea-card-[name].md` (External Research Questions section)

## Question File Format

```markdown
# Perplexity Research Plan — [project-name]

## Defaults
- model: sonar-pro
- recency: year

## Q1 — Competitive landscape
[คำถาม]
recency: month

## Q2 — Regulation
[คำถาม]
recency: month
model: sonar-reasoning

## Q3 — Industry trends
[คำถาม]
recency: year
```

> per-question overrides ใช้ key `recency:` `model:` ใต้คำถาม

---

## Workflow

### STEP 1 — Verify MCP connection

ลอง call `mcp__perplexity__perplexity_ask` ด้วย test query สั้นๆ
ถ้า error → แจ้ง user ให้ตรวจ `PERPLEXITY_API_KEY` ใน env

### STEP 2 — Parse questions

อ่าน `plx-questions-[name].md`:
- ดึง defaults จาก `## Defaults` block
- ดึงคำถามทุก `## Q[N]` พร้อม per-question overrides

### STEP 3 — Loop ask

```javascript
// แต่ละ Q เรียก stateless — ไม่เก็บ conversation context
for (const q of questions) {
  const result = await mcp__perplexity__perplexity_ask({
    messages: [{ role: "user", content: q.content }],
    search_recency_filter: q.recency || defaults.recency,
    // model selection ผ่าน tool variant
  });
  // append result + citations ไปไฟล์ output
}
```

**ข้อควรระวัง:**
- Perplexity **stateless** — ไม่จำ context ข้ามคำถาม (ต่างจาก NLM)
- เรียงคำถามแบบไหนก็ได้ ไม่มีผลกับ context
- ใช้ parallel ระวัง — บาง MCP server มี rate limit 5 req/min
- เก็บ citations **ทุก URL** อย่าทิ้ง

### STEP 4 — Format Output

สร้าง `projects/[name]/02-research/plx-answers-[name].md`:

```markdown
# Perplexity Research Answers — [project-name]

**Date:** YYYY-MM-DD
**Model:** sonar-pro (default)
**Total questions:** N

---

## Q1 — [topic]

**Question:** [คำถาม]
**Recency:** month
**Citations:** 5

### Answer

[คำตอบ พร้อม [1] [2] [3] inline]

### Citations

[1] [Title](URL) — YYYY-MM-DD
[2] [Title](URL) — YYYY-MM-DD
...

### Insights (Claude extract)

- [insight 1]
- [insight 2]

---

## Q2 — [topic]
...

---

## Cross-Question Synthesis

[Claude สรุป themes ที่ปรากฏข้าม Q1–Qn — สำคัญสำหรับ Stage 3]

- **Theme A:** [appears in Q1, Q3, Q5]
- **Theme B:** [appears in Q2, Q4]
```

### STEP 5 — Auto-Trigger Stage 3 Synthesis

เมื่อ answers พร้อม:
- แจ้ง user: "Perplexity answers ready — [project-name]"
- ถ้ามี `ai-answers-[name].txt` (NLM) อยู่แล้ว → suggest รัน synthesis ทันที
- ถ้ายังไม่มี → รอ NLM batch เสร็จก่อน

---

## Auto-Generate Questions Mode

ถ้าไม่มี `plx-questions-[name].md` ให้สร้างจาก `ux-idea-card-[name].md`:

อ่าน UX Idea Card → ดึง:
- **Open Questions** → คำถามที่ต้อง external validation
- **Hypotheses** → ต้อง market data confirm
- **Alternative Solutions** → ต้อง competitor reference

แล้วสร้าง 8–12 คำถามครอบคลุม:
- 2–3 คำถาม competitive (apps/services ที่คล้าย)
- 2–3 คำถาม regulation/standard
- 2–3 คำถาม UX patterns
- 1–2 คำถาม statistics/user behavior

---

## Tips
- **คำถามแยกชัดเจน** — Perplexity แม่นกับ specific question มากกว่า compound
- **ระบุปี/ประเทศ** — "Thailand 2025" ดีกว่า "globally"
- **Source language** — ถ้าต้องการ source ภาษาไทย ระบุ "Thai-language sources only"
- **Avoid jargon** — Perplexity index ดีกว่ากับ common terms
- **Rate limit:** ถ้า error 429 → รอ 60 วินาที แล้วลองใหม่

---

## Output

```
สร้าง: projects/[name]/02-research/plx-answers-[name].md
พร้อมสำหรับ: Stage 3 — Research Synthesis (merge กับ NLM answers)
```
