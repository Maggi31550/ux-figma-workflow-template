# Data Visualization Builder

สร้าง charts, dashboards, และ data-heavy screens สำหรับ prototype — ใช้ Canvas API + SVG ไม่ต้องการ library ภายนอก

## Usage
```
/data-viz [project-name] [chart-type] [data-spec]
/data-viz ggp-poc line-chart "Domestic CPO Price ช่วง Jan-Dec 2025"
/data-viz ggp-poc dashboard "Overview: revenue, users, conversion"
/data-viz ggp-poc --screen [screen-id]    ← เพิ่ม viz ลงใน screen ที่มีอยู่
```

---

## Chart Types ที่รองรับ

### 1. Line Chart (`line-chart`)
เหมาะกับ: time series, trends, price movements
```
ใช้: SVG path + polyline
Options: single line / multi-line / area fill
Interactions: hover tooltip, zoom range
```

### 2. Bar Chart (`bar-chart`)
เหมาะกับ: comparison, categorical data, rankings
```
ใช้: SVG rect
Options: vertical / horizontal / stacked / grouped
Interactions: hover highlight, click drill-down
```

### 3. Donut / Pie Chart (`donut-chart`)
เหมาะกับ: proportion, composition (≤6 categories)
```
ใช้: SVG arc path
Options: donut / pie / gauge
Interactions: hover segment expand, center label
```

### 4. Heatmap (`heatmap`)
เหมาะกับ: density, frequency matrix, calendar view
```
ใช้: SVG rect grid
Options: color scale (sequential / diverging)
Interactions: hover cell value
```

### 5. KPI Cards (`kpi-cards`)
เหมาะกับ: dashboard summary, metrics overview
```
ใช้: HTML/CSS
Options: trend arrow, sparkline, comparison period
```

### 6. Data Table + Mini Chart (`table-spark`)
เหมาะกับ: list with trend indicators (เช่น GGP-POC Pipeline)
```
ใช้: HTML table + inline SVG sparkline
Options: sortable columns, expandable rows
```

### 7. Confidence Meter (`confidence-meter`)
เหมาะกับ: AI confidence scores, risk levels, ratings
```
ใช้: CSS + SVG arc
Options: circular / linear / bar
```

---

## Workflow

### STEP 1 — Understand Data Context

อ่านจาก:
- Brief / research doc — ข้อมูลจริงที่ระบบจะแสดง
- Existing prototype screens — ดูว่า data แสดงอย่างไรอยู่แล้ว
- Handoff notes — design tokens, color system

### STEP 2 — Generate Realistic Mock Data

**กฎ: ไม่ใช้ random data** — ใช้ข้อมูลที่ดูสมจริงสำหรับ domain นั้น

ตัวอย่างสำหรับ GGP-POC:
```js
const cpoPriceData = [
  { month: 'Jan', value: 118.5 }, { month: 'Feb', value: 121.3 },
  { month: 'Mar', value: 119.8 }, { month: 'Apr', value: 125.2 },
  { month: 'May', value: 122.7 }, { month: 'Jun', value: 128.9 },
  { month: 'Jul', value: 131.4 }, { month: 'Aug', value: 127.6 },
  { month: 'Sep', value: 133.1 }, { month: 'Oct', value: 129.8 },
  { month: 'Nov', value: 135.6 }, { month: 'Dec', value: 138.2 },
];
```

### STEP 3 — Build Chart Component

สร้าง self-contained chart function:

```js
function renderLineChart(container, data, options = {}) {
  const { width = 600, height = 200, color = '#23348d', 
          fillColor = '#f0f5fe', showGrid = true } = options;
  
  // Scale calculations
  const minVal = Math.min(...data.map(d => d.value));
  const maxVal = Math.max(...data.map(d => d.value));
  const xStep = width / (data.length - 1);
  const yScale = height / (maxVal - minVal);
  
  // Generate SVG path
  const points = data.map((d, i) => 
    `${i * xStep},${height - (d.value - minVal) * yScale}`
  ).join(' ');
  
  // SVG output with hover tooltips
  container.innerHTML = `
    <svg viewBox="0 0 ${width} ${height + 40}" ...>
      <!-- Grid lines -->
      <!-- Area fill -->
      <!-- Line -->
      <!-- Data points + tooltips -->
      <!-- X-axis labels -->
    </svg>
  `;
}
```

### STEP 4 — Integrate into Screen

เพิ่ม chart container เข้าไปใน screen ที่ถูกต้อง:

```html
<!-- ใน screen HTML -->
<div class="chart-container" id="chart-cpo-price">
  <!-- renderLineChart() จะ inject SVG ตรงนี้ -->
</div>
```

```js
// ใน script section
document.addEventListener('DOMContentLoaded', () => {
  renderLineChart(
    document.getElementById('chart-cpo-price'),
    cpoPriceData,
    { color: 'var(--brand-primary-900)', height: 180 }
  );
});
```

### STEP 5 — Responsive + Accessible

- Chart resize ตาม container width (ResizeObserver)
- `role="img"` + `aria-label` บน SVG
- Tooltip ทำงานด้วย keyboard (focus + Enter)
- Color scheme ใช้ design tokens เสมอ

---

## Dashboard Layout Pattern

สำหรับ screens ที่มี multiple charts:

```html
<div class="dashboard-grid">
  <!-- Row 1: KPI Cards (4 cards) -->
  <div class="kpi-row">
    <div class="kpi-card" data-trend="up">
      <div class="kpi-label">Biodiesel Demand Index</div>
      <div class="kpi-value">138.2</div>
      <div class="kpi-change positive">↑ 4.2% vs last month</div>
    </div>
    ...
  </div>
  
  <!-- Row 2: Main Chart (full width) -->
  <div class="chart-main" id="chart-main"></div>
  
  <!-- Row 3: Secondary Charts (2 columns) -->
  <div class="chart-secondary-grid">
    <div id="chart-left"></div>
    <div id="chart-right"></div>
  </div>
</div>
```

---

## CSS Tokens สำหรับ Charts

```css
:root {
  /* Chart colors — sequential */
  --chart-1: var(--brand-primary-900);   /* #23348d */
  --chart-2: var(--brand-secondary-700); /* #089241 */
  --chart-3: #0c8cd0;   /* blue */
  --chart-4: #e59b1c;   /* amber */
  --chart-5: #d92d20;   /* red */
  
  /* Chart areas */
  --chart-fill-1: #f0f5fe;
  --chart-fill-2: #f0fdf4;
  
  /* Grid */
  --chart-grid: var(--gray-200);
  --chart-axis: var(--gray-300);
  --chart-label: var(--gray-500);
}
```

---

## Output
```
แก้ไข: projects/[name]/05-prototype/index.html  ← เพิ่ม chart screen/component
สร้าง: projects/[name]/05-prototype/charts.js   ← chart functions (reusable)
```
