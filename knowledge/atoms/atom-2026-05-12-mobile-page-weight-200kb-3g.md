---
id: atom-2026-05-12-mobile-page-weight-200kb-3g
tags: [performance, mobile, 3g, rural, page-weight, lcp, accessibility]
source: OCPB DataSure UX Research Doc, 2026-05-12
verified-by: UX Researcher
valid-until: ~2028
---

# Consumer-Facing Verification Pages Must Target ≤200 KB Total Weight and LCP ≤2.5s on 3G

**Category:** Principle

**Source:** OCPB DataSure research, 2026-05-12

**2-Year Check:** 5G rollout in rural Thailand is a multi-decade infrastructure project. The population most likely to be deceived by unverified products — lower-income, rural consumers — is also least likely to have 4G+ coverage. Google's LCP threshold of 2.5s is a published Core Web Vitals standard that has been stable since 2020. Both constraints will remain in force through 2028.

In regions served by 3G (estimated 1–5 Mbps), a consumer-facing verification page that exceeds 200 KB total payload or takes more than 2.5 seconds to reach Largest Contentful Paint will be abandoned before the status is seen. SSR with inline critical CSS, no render-blocking JavaScript on the verification route, and deferred loading of secondary content are the minimum architectural requirements for this page. Heavy hero images, web fonts downloaded before render, and client-side data fetching all violate this constraint.

**Applies to:** Any government or public-interest verification page targeting mixed-connectivity populations. QR scan results, certificate lookups, public health product checks, product recall notices.
