# EN Homepage Missing Content Fix
**2026-06-05 11:29 HKT** | commit `353b405`

## Problem
User reported English homepage (`en/index.html`) showing missing content compared to Chinese homepage.

## Root Cause
The "Why Choose" section's 4th card **(Butler Service System)** was missing a closing `</div>` tag after `<a class="service-link" href="management.html">Learn Management →</a>`.

This caused the 5th card (Industry Authority Certification) and 6th card (Exclusive Membership Ecosystem) to be nested inside Card 4 instead of being direct children of the `.services-grid` CSS Grid container. In a grid layout, non-direct children lose grid positioning and display incorrectly or not at all.

## Fix
Added the missing `</div>` after the "Learn Management →" link in `en/index.html`.

## Verification
Full structural comparison between CN and EN index.html - all element counts match:
- 12 sections ✅
- 12 service-cards ✅
- 16 yacht-cards ✅
- 6 mgmt-cards ✅
- 3 news-cards ✅
- 4 stat-items ✅
- 12 flow-steps ✅
- 7 footer-cols ✅
