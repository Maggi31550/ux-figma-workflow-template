# Perplexity Quick Ask

ถาม Perplexity 1 คำถามและบันทึก answer พร้อม citations — ใช้สำหรับงาน external research ที่ต้องการ web sources

## Usage
```
/skills:plx-ask "[question]"
/skills:plx-ask "[question]" --recency [day|week|month|year]
/skills:plx-ask "[question]" --model [sonar|sonar-pro|sonar-reasoning]
/skills:plx-ask "[question]" --save [output-file.md]
```

## Tool Mapping

| Mode | MCP tool | When |
|------|----------|------|
| Quick fact | `mcp__perplexity__perplexity_ask` (`sonar`) | คำถามทั่วไป, definitions |
| Deep research | `mcp__perplexity__perplexity_research` (`sonar-pro`) | competitive scan, market data |
| Comparative reasoning | `mcp__perplexity__perplexity_reason` (`sonar-reasoning`) | pros/cons, trade-off analysis |

> ถ้า tool name จริงต่างจากนี้ ให้ `mcp__perplexity__*` แล้วเช็คตอน connect ครั้งแรก

## How to Use

### Single question
```javascript
// default model = sonar
mcp__perplexity__perplexity_ask({
  messages: [{ role: "user", content: "[question]" }]
})
```

### With recency filter (สำคัญสำหรับ regulation/trends)
```javascript
mcp__perplexity__perplexity_ask({
  messages: [{ role: "user", content: "[question]" }],
  search_recency_filter: "month"   // day | week | month | year
})
```

### Deep research mode
```javascript
mcp__perplexity__perplexity_research({
  messages: [{ role: "user", content: "[question]" }],
  return_citations: true
})
```

## Output Format

ถ้า `--save [file]` ระบุ ให้บันทึกเป็น markdown:

```markdown
# Perplexity Answer — [YYYY-MM-DD]

**Question:** [question]
**Model:** sonar-pro
**Recency:** month
**Date:** YYYY-MM-DD HH:MM

---

## Answer

[คำตอบจาก Perplexity พร้อม [1] [2] [3] inline]

---

## Citations

[1] [Title](URL) — [publication date if available]
[2] [Title](URL)
[3] [Title](URL)

---

## Key Takeaways (Claude สรุปเพิ่ม)

- [insight 1 — durable, context-independent]
- [insight 2]
- [insight 3]
```

## Citation Hygiene — ทุก answer ต้องผ่าน

| เกณฑ์ | ตรวจ |
|-------|------|
| URL ใช้งานได้ | ทุก citation มี URL จริง ไม่ใช่ broken link |
| Date ระบุ | ถ้า source มีวันที่ ให้บันทึก |
| Authority | ตรวจว่า source เป็น primary (รัฐบาล, มาตรฐาน, official) หรือ secondary (blog, opinion) |
| Recency match | ถ้า topic เป็น regulation/trend → ต้องมี source ภายใน 12 เดือน |

## Recency Filter Guide

| Topic | Recommended filter |
|-------|--------------------|
| Regulation / law update | `month` |
| Industry trends | `year` |
| UX patterns | `year` |
| Competitor activity | `month` |
| Statistics / surveys | `year` |
| Historical / definitions | (no filter) |

## Tips
- ใช้ภาษาไทยถามได้ — Perplexity ตอบภาษาเดียวกับคำถาม
- คำถาม specific จะได้ citations แม่นยำกว่า "tell me about X" ทั่วๆ ไป
- ถ้า answer มี hallucination warning → ลด temperature หรือเปลี่ยน model เป็น `sonar-pro`
- ไม่เก็บ conversation context ข้ามคำถาม (ต่างจาก NLM) — ทุก ask เป็น stateless
