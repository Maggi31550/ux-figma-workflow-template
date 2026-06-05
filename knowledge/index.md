# Global Knowledge Base — UX Figma Workflow

Cross-project UX insights. All atoms pass the 2-Year Rule — durable, context-independent findings reusable across projects.

## Atoms Index
<!-- Format: - [Title](atoms/filename.md) — one-line summary -->

### Design System Engineering — 2026-06-02
- [3-Tier Token Architecture](atoms/atom-2026-06-02-three-tier-token-architecture.md) — Migration recipe (primitive→semantic→component) + tricky cases (hue overlap, unit normalizer, Figma alias) verified กับ trailbook จริง. Script: `scripts/token-migration/migrate-to-3tier.py`

### OCPB DataSure — 2026-05-12
- [Trust Signal Must Land Within 3 Seconds](atoms/atom-2026-05-12-trust-signal-3-seconds.md) — Consumers abandon QR scan result pages that do not display a dominant status signal (icon + colour + text) within 3 seconds of load.
- [A Pre-flight Checklist Before the Form Reduces Mid-Flow Abandonment](atoms/atom-2026-05-12-preflight-checklist-reduces-abandonment.md) — Showing document requirements before the first input field prevents uncompletable sessions and reduces abandonment on multi-step compliance forms.
- [Auto-Save Draft Is Non-Negotiable for Multi-Step Compliance Forms](atoms/atom-2026-05-12-save-draft-non-negotiable.md) — Forms requiring physical documents always span multiple sessions; auto-save every 30 seconds plus a "save and return" action are structural requirements, not enhancements.
- [Structured Rejection Reasons With Corrective Guidance Reduce Repeat-Error Resubmissions](atoms/atom-2026-05-12-actionable-rejection-reduces-resubmission-errors.md) — A dropdown of categorised rejection codes plus per-code guidance notes converts vague review feedback into a self-service correction checklist.
- [Consumer-Facing Verification Pages Must Target ≤200 KB Total Weight and LCP ≤2.5s on 3G](atoms/atom-2026-05-12-mobile-page-weight-200kb-3g.md) — Rural 3G constraints make SSR, inline critical CSS, and no render-blocking JS mandatory for any public verification page targeting mixed-connectivity populations.
- [Define the Complete Status Model Before Designing Any Status UI](atoms/atom-2026-05-12-complete-status-model-before-ui.md) — Certification systems always evolve to more states; defining PENDING / ACTIVE / SUSPENDED / REVOKED / EXPIRED / NOT_FOUND before design prevents costly retrofitting.

