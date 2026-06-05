---
id: atom-2026-05-12-complete-status-model-before-ui
tags: [information-architecture, status-model, states, certification, ux-process]
source: OCPB DataSure UX Research Doc, 2026-05-12
verified-by: UX Researcher
valid-until: ~2028
---

# Define the Complete Status Model Before Designing Any Status UI

**Category:** Principle

**Source:** OCPB DataSure research, 2026-05-12

**2-Year Check:** Certification systems always evolve toward more states over time — active, suspended, revoked, expired are a structural minimum for any regulatory scheme. Retrofitting a 2-state UI (pass/fail) to handle 5+ states after launch creates technical debt and confusing user experiences. This principle applies as long as digital certification systems exist.

A certification or verification system that designs UI for only "approved" and "not found" will inevitably encounter states it cannot communicate: suspension pending investigation, revocation after approval, expiry, and data-sync lag between databases. Defining the complete state machine — PENDING / ACTIVE / SUSPENDED / REVOKED / EXPIRED / NOT_FOUND — before any screen is designed prevents retrofitting and ensures every state has a corresponding visual treatment, error message, and user action. Each state should have a distinct icon, colour token, and microcopy set.

**Applies to:** Any system that issues digital credentials, certificates, badges, or regulatory status: product certification, professional licences, vehicle inspection records, food safety ratings, event tickets.
