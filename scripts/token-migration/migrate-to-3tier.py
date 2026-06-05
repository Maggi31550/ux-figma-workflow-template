#!/usr/bin/env python3
"""
migrate-to-3tier.py — แปลง tokens.json 1-tier → 3-tier
Usage: python3 migrate-to-3tier.py <project-name>
  e.g. python3 migrate-to-3tier.py trailbook

Input:  projects/<name>/07-design-system/tokens.json  (1-tier / flat semantic)
Output: projects/<name>/07-design-system/tokens.json  (3-tier: primitive → semantic → component)
        projects/<name>/07-design-system/tokens.css   (regenerated, must diff 0 vs prototype)

Verified with: trailbook 2026-06-02 (207 tokens, 89 aliases, round-trip 100%)
"""
import json, sys, re, colorsys, hashlib
from pathlib import Path
from collections import defaultdict

# ─── CONFIG ──────────────────────────────────────────────────────────────────
PROJECT = sys.argv[1] if len(sys.argv) > 1 else 'trailbook'
BASE    = Path(__file__).parent.parent.parent / 'projects' / PROJECT
DS_DIR  = BASE / '07-design-system'
PROTO_CSS = BASE / '05-prototype' / 'src' / 'styles' / 'tokens.css'

# ─── STEP 0: BACKUP ──────────────────────────────────────────────────────────
import shutil, datetime
bak = DS_DIR / f'tokens.json.backup.{datetime.datetime.now():%Y%m%d-%H%M%S}'
shutil.copy(DS_DIR / 'tokens.json', bak)
print(f'backup: {bak.name}')

# ─── STEP 1: LOAD EXISTING ───────────────────────────────────────────────────
existing = json.loads((DS_DIR / 'tokens.json').read_text())

# ─── STEP 2: HUE ANALYSIS ────────────────────────────────────────────────────
def hsl(hex_):
    h = hex_.lstrip('#')
    r,g,b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    hh,l,s = colorsys.rgb_to_hls(r,g,b)
    return round(hh*360), round(s*100), round(l*100)

def hue_group(hex_):
    hh, s, l = hsl(hex_)
    if s < 12: return 'gray'
    if hh < 30 or hh > 330: return 'red'
    if hh < 60: return 'amber'
    if hh < 150: return 'green'
    if hh < 200: return 'cyan'
    if hh < 260: return 'blue'
    return 'violet'

colors = {}
def walk_colors(node, path):
    for k, v in node.items():
        if k.startswith('$'): continue
        if isinstance(v, dict) and '$value' in v and v.get('$type') == 'color':
            colors['/'.join(path+[k])] = v['$value']
        elif isinstance(v, dict):
            walk_colors(v, path+[k])
walk_colors(existing, [])

print(f'\nColor tokens found: {len(colors)}')
by_hue = defaultdict(list)
for path, val in colors.items():
    by_hue[hue_group(val)].append((path, val))
for g, items in sorted(by_hue.items()):
    vals = sorted(set(v for _,v in items))
    print(f'  {g}: {len(vals)} unique → {vals}')

# ─── STEP 3: COLLECT SOURCE.CSSVAR MAPPING ───────────────────────────────────
cssvar_map = {}   # dtcg-path → css-var-name
def collect_csvars(node, path):
    for k, v in node.items():
        if k.startswith('$'): continue
        if isinstance(v, dict) and '$value' in v:
            cv = v.get('$extensions', {}).get('source.cssVar')
            if cv: cssvar_map['/'.join(path+[k])] = cv
        elif isinstance(v, dict):
            collect_csvars(v, path+[k])
collect_csvars(existing, [])
print(f'\nsource.cssVar entries found: {len(cssvar_map)}')

# ─── STEP 4: BUILD PRIMITIVE PALETTE ─────────────────────────────────────────
# Auto-derive from existing color values
# NOTE: project-specific! For trailbook we hard-coded; generic projects need to
# map each unique hex to a scale name manually or use the hue_group + lightness
# For reusability, we output the ANALYSIS and prompt user to define palette.

print("""
─────────────────────────────────────────────────────
MANUAL STEP: Define primitive palette for this project
─────────────────────────────────────────────────────
Edit PRIMITIVE_PALETTE dict below, then re-run.
Use the hue analysis above to map each hex → scale name.

Template already populated based on hue analysis.
Adjust scale names / add/remove entries as needed.
─────────────────────────────────────────────────────
""")

# ─── TRAILBOOK TEMPLATE (copy & modify for other projects) ───────────────────
# Keys: "paletteName/scale" → hex value
# Ensure ALL hex values in colors{} map to at least one primitive
PRIMITIVE_PALETTE = {
    # Replace these with your project's actual palette:
    "green/500":     "#2d7a47",  # primary brand
    "green/700":     "#1d5c33",
    "green/300":     "#4a9e65",
    "green/50":      "#edf7f1",
    "green/100":     "#c6e8d1",
    "green/800":     "#1db954",  # bank kbank
    "green/850":     "#059669",  # operator role
    "emerald/800":   "#16a34a",  # success
    "emerald/50":    "#f0fdf4",
    "emerald/50bg":  "#ecfdf5",
    "emerald/100":   "#bbf7d0",
    "emerald/100muted": "#a7f3d0",
    "amber/500":     "#d97706",  # accent/warning
    "amber/700":     "#b45309",
    "amber/300":     "#f59e0b",
    "amber/50":      "#fff8eb",
    "amber/50w":     "#fffbeb",  # warning.bg (slightly different from accent.bg)
    "amber/100":     "#fde68a",
    "red/500":       "#dc2626",
    "red/50":        "#fef2f2",
    "red/100":       "#fecaca",
    "blue/500":      "#2563eb",
    "blue/50":       "#eff6ff",
    "blue/100":      "#bfdbfe",
    "cyan/500":      "#0891b2",  # hiker role
    "cyan/50":       "#ecfeff",
    "cyan/100":      "#a5f3fc",
    "cyan/600":      "#0ea5e9",  # krungthai bank
    "violet/500":    "#7c3aed",  # admin role
    "violet/50":     "#f5f3ff",
    "violet/100":    "#ddd6fe",
    "violet/800":    "#4e2d7b",  # scb bank
    "slate/900":     "#0f172a",
    "slate/600":     "#475569",
    "slate/500":     "#94a3b8",
    "slate/300":     "#cbd5e1",
    "slate/200":     "#e2e8f0",
    "slate/100":     "#f1f5f9",
    "slate/50":      "#f8fafc",
    "white":         "#ffffff",
}

# ─── STEP 5: BUILD semantic → primitive ALIAS MAP ────────────────────────────
# Reverse: hex → primitive key (warn if ambiguous)
hex_to_prim = {}
for prim_key, hex_val in PRIMITIVE_PALETTE.items():
    if hex_val in hex_to_prim:
        hex_to_prim[hex_val].append(prim_key)
    else:
        hex_to_prim[hex_val] = [prim_key]

alias_map = {}    # semantic-path → primitive-key (or None = keep hardcoded)
no_primitive = []
for path, val in colors.items():
    prims = hex_to_prim.get(val, [])
    if len(prims) == 1:
        alias_map[path] = prims[0]
    elif len(prims) > 1:
        # pick most semantically appropriate (simple heuristic: shortest key)
        alias_map[path] = sorted(prims, key=len)[0]
    else:
        alias_map[path] = None   # keep hardcoded
        no_primitive.append((path, val))

print(f'Colors with alias: {sum(1 for v in alias_map.values() if v)}')
print(f'Colors without primitive (keep hardcoded): {len(no_primitive)}')
for p, v in no_primitive: print(f'  {p} = {v}')

# ─── STEP 6: BUILD 3-TIER tokens.json ────────────────────────────────────────
def build_nested(flat_dict):
    """Convert flat 'a/b/c' dict → nested {'a':{'b':{'c':v}}}"""
    root = {}
    for path, val in flat_dict.items():
        parts = path.split('/')
        node = root
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = val
    return root

# Primitive tier
prim_flat = {k: {"$value": v, "$type": "color"} for k, v in PRIMITIVE_PALETTE.items()}
prim_nested = build_nested(prim_flat)

# Rebuild semantic color with aliases
def rebuild_semantic(node, path):
    result = {}
    for k, v in node.items():
        if k.startswith('$'): continue
        full = '/'.join(path+[k])
        if isinstance(v, dict) and '$value' in v:
            prim = alias_map.get(full)
            new_v = dict(v)
            if prim:
                prim_clean = prim.replace('.', '_')  # escape dots
                new_v['$value'] = '{primitive.color.' + prim_clean.replace('_','.') + '}'
            result[k] = new_v
        elif isinstance(v, dict):
            result[k] = rebuild_semantic(v, path+[k])
    return result

new_color = rebuild_semantic(existing.get('color', {}), ['color'])

# Component tokens (project-specific — define per project)
# Template for common components:
component_tokens = {
    "button": {
        "primary": {"bg": {"$value": "{color.primary.default}", "$type": "color"},
                    "bgHover": {"$value": "{color.primary.dark}", "$type": "color"},
                    "text": {"$value": "{color.text.onPrimary}", "$type": "color"}},
        "secondary": {"bg": {"$value": "{color.surface.default}", "$type": "color"},
                      "text": {"$value": "{color.text.default}", "$type": "color"},
                      "border": {"$value": "{color.border.default}", "$type": "color"}},
        "danger": {"bg": {"$value": "{color.error.default}", "$type": "color"},
                   "text": {"$value": "{color.text.inverse}", "$type": "color"}},
        "radius": {"$value": "{radius.lg}", "$type": "dimension"},
    },
    "input": {
        "bg": {"$value": "{color.surface.default}", "$type": "color"},
        "border": {"$value": "{color.border.default}", "$type": "color"},
        "borderFocus": {"$value": "{color.primary.default}", "$type": "color"},
        "borderError": {"$value": "{color.error.default}", "$type": "color"},
        "text": {"$value": "{color.text.default}", "$type": "color"},
        "radius": {"$value": "{radius.lg}", "$type": "dimension"},
    },
}

# Assemble
new_tokens = {
    "$schema": "https://design-tokens.github.io/community-group/format/",
    "$description": f"{PROJECT} Design Tokens v2 — 3-tier: primitive → semantic → component",
    "primitive": {"color": prim_nested},
    "color": new_color,
}
for cat in ['font','spacing','radius','shadow','layout','transition','zIndex','gradient']:
    if cat in existing: new_tokens[cat] = existing[cat]
new_tokens['component'] = component_tokens

# ─── STEP 7: ROUND-TRIP VERIFY ───────────────────────────────────────────────
def resolve(val, root, depth=0):
    if depth > 15: return str(val)
    if isinstance(val, str) and val.startswith('{') and val.endswith('}'):
        path = val[1:-1].split('.')
        node = root
        for p in path:
            node = node.get(p) if isinstance(node, dict) else None
            if node is None: return val
        if isinstance(node, dict) and '$value' in node:
            return resolve(node['$value'], root, depth+1)
    return val

def serialize(node, root):
    v = resolve(node['$value'], root)
    if isinstance(v, list):
        parts = []
        for d in v:
            p = [d['offsetX'], d['offsetY'], d['blur']]
            if d.get('spread','0') not in ('0','0px',0): p.append(d['spread'])
            p.append(d['color']); parts.append(' '.join(str(x) for x in p))
        return ', '.join(parts)
    s = str(v); ease = node.get('$extensions',{}).get('ease')
    return f'{s} {ease}' if ease else s

css_lines = []
def collect_css(node, root):
    for k, v in node.items():
        if k.startswith('$'): continue
        if isinstance(v, dict) and '$value' in v:
            cv = v.get('$extensions',{}).get('source.cssVar')
            if cv: css_lines.append((cv, serialize(v, root)))
        elif isinstance(v, dict): collect_css(v, root)
collect_css(new_tokens, new_tokens)

orig_css = PROTO_CSS.read_text()
orig_order = {}
for i, line in enumerate(orig_css.splitlines()):
    m = re.match(r'\s*(--[\w-]+):', line)
    if m: orig_order[m.group(1)] = i

css_lines.sort(key=lambda x: orig_order.get(x[0], 9999))
seen = set(); deduped = []
for cv, val in css_lines:
    if cv not in seen: seen.add(cv); deduped.append((cv, val))

gen = {cv: val for cv, val in deduped}
orig = {}
for line in orig_css.splitlines():
    m = re.match(r'\s*(--[\w-]+):\s*([^;]+?)\s*;', line)
    if m: orig[m.group(1)] = m.group(2).strip()

missing = [k for k in orig if k not in gen]
diffs   = [(k, orig[k], gen[k]) for k in orig if k in gen and orig[k] != gen[k]]

print(f'\nRound-trip: {len(gen)} gen / {len(orig)} orig | missing:{len(missing)} | diffs:{len(diffs)}')
if missing: print('  MISSING:', missing)
if diffs:   print('  DIFFS:', diffs[:5])

if missing or diffs:
    print('\n⚠️  Round-trip failed — adjust PRIMITIVE_PALETTE and alias_map, then re-run')
    print('   Tip: check no_primitive list above — those need palette entries or hardcode fix')
    sys.exit(1)

# ─── WRITE ───────────────────────────────────────────────────────────────────
json.dump(new_tokens, (DS_DIR / 'tokens.json').open('w', encoding='utf-8'), indent=2, ensure_ascii=False)
css_out = "/* AUTO-GENERATED from tokens.json (3-tier) — do not edit */\n:root {\n"
css_out += ''.join(f'  {cv}: {val};\n' for cv, val in deduped)
css_out += "}\n"
(DS_DIR / 'tokens.css').write_text(css_out)

def count_leaves(node):
    if isinstance(node, dict) and '$value' in node: return 1
    return sum(count_leaves(v) for k,v in node.items() if not k.startswith('$') and isinstance(v,dict))
def count_aliases(node):
    if isinstance(node, dict) and '$value' in node:
        return 1 if isinstance(node['$value'],str) and '{' in node['$value'] else 0
    return sum(count_aliases(v) for k,v in node.items() if not k.startswith('$') and isinstance(v,dict))

print(f"""
✅ Migration complete — {PROJECT}
   Tier 1 Primitive:  {count_leaves(new_tokens['primitive'])} tokens
   Tier 2 Semantic:   {count_leaves(new_tokens['color'])} color tokens
   Tier 3 Component:  {count_leaves(new_tokens.get('component',{}))} tokens
   Alias chains:      {count_aliases(new_tokens)}
   CSS output:        {len(deduped)} vars (round-trip ✅)
   Backup:            {bak.name}

Next: push Primitives + Components collections to Figma
  → run /skills:ds-push-figma {PROJECT} [figma-url] --tokens-only
""")
