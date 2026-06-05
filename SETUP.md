# SETUP.md — ติดตั้ง UX Figma Workflow

> สำหรับสมาชิกใหม่ที่ต้องการใช้ pipeline นี้บนเครื่องของตัวเอง  
> ใช้เวลาติดตั้งประมาณ 30–60 นาที (ส่วนใหญ่รอ download)

---

## สิ่งที่ต้องมีก่อน

| เครื่องมือ | ใช้ทำอะไร | ต้องการไหม |
|-----------|-----------|------------|
| Claude Code CLI | รัน pipeline ทั้งหมด | **จำเป็น** |
| Node.js v20+ | รัน prototype dev server | **จำเป็น** |
| notebooklm-py | Internal research automation (NLM) | ถ้าใช้ research stage |
| Perplexity API key | External research — competitors, regulation | ถ้าใช้ research stage |
| Figma account | Push design ขึ้น Figma | ถ้าใช้ figma-pipeline |
| Figma MCP | เชื่อม Claude → Figma | ถ้าใช้ figma-pipeline |
| Google account | สำหรับ NotebookLM | ถ้าใช้ research stage |

---

## STEP 1 — รับ Workflow Folder

### วิธี A: Git (แนะนำ)
```bash
git clone [repo-url] "UX Figma Workflow"
cd "UX Figma Workflow"
```

### วิธี B: Zip
แตก zip แล้ว rename folder เป็น `UX Figma Workflow`

> ⚠️ ชื่อ folder สำคัญ — บาง path ใน scripts อ้างอิงชื่อนี้

---

## STEP 2 — ติดตั้ง Claude Code

```bash
npm install -g @anthropic/claude-code
```

ตรวจสอบ:
```bash
claude --version
```

> ต้องการ API key จาก [claude.ai](https://claude.ai) — login แล้วรัน `claude` ครั้งแรกเพื่อ authenticate

---

## STEP 3 — ติดตั้ง Node.js

ตรวจก่อนว่ามีหรือยัง:
```bash
node --version   # ต้องการ v20+
npm --version
```

ถ้ายังไม่มี → ดาวน์โหลด [nodejs.org](https://nodejs.org) (เลือก LTS)

---

## STEP 4 — ติดตั้ง notebooklm-py (ถ้าใช้ Research stage)

```bash
# ติดตั้ง Python venv
cd ~
python3 -m venv notebooklm-py/.venv
source notebooklm-py/.venv/bin/activate
pip install notebooklm-py

# ทดสอบ
notebooklm --version
```

### อัปเดต script ให้ชี้มาที่เครื่องของคุณ

แก้ไขไฟล์ `scripts/nlm.sh`:
```bash
# เปลี่ยนบรรทัดแรกจาก:
NLM_BIN="/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm"

# เป็น path ของคุณ เช่น:
NLM_BIN="$HOME/notebooklm-py/.venv/bin/notebooklm"
```

### Login Google account
```bash
scripts/nlm.sh login
# เลือก Google account ที่ใช้ NotebookLM
```

---

## STEP 5 — ตั้งค่า Perplexity API (ถ้าใช้ External Research)

Perplexity ใช้สำหรับ external research (competitors, regulation, web trends) ใน Stage 2B

### 5A: สร้าง API Key
1. ไปที่ [perplexity.ai/account/api/keys](https://www.perplexity.ai/account/api/keys)
2. Add credit ขั้นต่ำ $5 และผูกบัตร
3. สร้าง API Key → Copy

### 5B: ตั้ง Environment Variable
```bash
# เพิ่มใน ~/.zshrc หรือ ~/.zprofile
export PERPLEXITY_API_KEY="pplx-..."

# reload shell
source ~/.zshrc
```

ตรวจสอบ:
```bash
echo $PERPLEXITY_API_KEY
```

### 5C: เพิ่ม MCP ใน Claude Code settings

แก้ไข `.claude/settings.local.json` เพิ่ม section นี้:
```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@chatmcp/server-perplexity-ask"],
      "env": {
        "PERPLEXITY_API_KEY": "pplx-..."
      }
    }
  }
}
```

> ราคาประมาณ: batch research 1 ครั้ง ≈ $0.30–0.80 | ครบ pipeline 1 project ≈ $3–5

**Fallback ถ้าไม่มี API key:** ใช้ `--skip-perplexity` flag ใน pipeline หรือรัน plx-* skills ด้วย Perplexity web UI แทน

---

## STEP 6 — ตั้งค่า Figma MCP (ถ้าใช้ Figma pipeline)

### 6A: สร้าง Figma API Token
1. เปิด Figma → Account Settings → Security
2. สร้าง Personal Access Token
3. Copy token ไว้

### 6B: เพิ่ม MCP ใน Claude Code settings

แก้ไข `.claude/settings.local.json` (ถ้าไม่มีให้สร้าง):
```json
{
  "mcpServers": {
    "Figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_API_KEY": "YOUR_FIGMA_TOKEN_HERE"
      }
    }
  }
}
```

> ⚠️ อย่า commit `settings.local.json` — มี token อยู่ (ไฟล์นี้อยู่ใน .gitignore แล้ว)

### 6C: ทดสอบ Figma MCP
เปิด Claude Code แล้วลองพิมพ์:
```
/figma-pipeline --help
```
ถ้า MCP เชื่อมได้จะเห็น tool list

---

## STEP 7 — เปิด Claude Code ใน Folder

```bash
cd "UX Figma Workflow"
claude
```

Claude Code จะอ่าน `CLAUDE.md` และโหลด agents/commands อัตโนมัติ

---

## STEP 8 — สร้าง Project แรก

```bash
# สร้าง folder structure จาก template
cp -r projects/_template projects/[your-project-name]

# เขียน brief
# projects/[your-project-name]/01-brief/brief.md
```

แล้วรัน pipeline:
```
/ux-figma-pipeline [your-project-name] [brief description]
```

---

## Troubleshooting

### `claude: command not found`
```bash
npm install -g @anthropic/claude-code
# หรือใช้ npx: npx @anthropic/claude-code
```

### `scripts/nlm.sh: Permission denied`
```bash
chmod +x scripts/nlm.sh
```

### NotebookLM error: `account-routing mismatch`
```bash
scripts/nlm.sh login
# เลือก Google account ที่ถูกต้อง
```

### Figma MCP ไม่ตอบสนอง
- ตรวจว่า `FIGMA_API_KEY` ใน settings.local.json ถูกต้อง
- token หมดอายุ → สร้างใหม่ใน Figma Account Settings

### Prototype `npm run dev` error
```bash
cd projects/[name]/05-prototype
npm install   # ติดตั้ง dependencies ก่อน
npm run dev
```

---

## ไฟล์ที่ต้องแก้ตามเครื่องของคุณ

| ไฟล์ | สิ่งที่ต้องแก้ |
|------|--------------|
| `scripts/nlm.sh` | Path ของ notebooklm-py binary |
| `.claude/settings.local.json` | Figma API token (และ MCP config อื่นๆ) |

ไฟล์อื่นๆ ทั้งหมดใช้ร่วมกันได้โดยไม่ต้องแก้
