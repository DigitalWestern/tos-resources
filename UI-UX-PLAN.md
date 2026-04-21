# TOS Resources — UI/UX Improvement Plan

**Branch:** `feature/ui-ux-improvements`
**Date:** April 20, 2026

---

## 1. Navbar Size Inconsistency Across Pages (High Priority)

### Problem
The horizontal nav bar (desktop, >= 900px) is visually larger on the Home and Literature pages than on all other pages. When navigating between pages, the header jumps in size.

### Root Cause
Each page defines `.page-nav a` styles in its own inline `<style>` block, and two pages use different values than the rest:

| Pages | `padding` | `font-size` |
|-------|-----------|-------------|
| `index.html`, `literature.html` | `12px 20px` | `0.76rem` |
| All other 7 pages | `12px 16px` | `0.72rem` |

### Fix
Standardize all 9 pages to the **same** values. The topic-page values (`12px 16px`, `0.72rem`) are the better fit — 8 nav links need to be compact to avoid wrapping on narrower desktop screens.

Alternatively, move these properties into `css/site.css` so they're defined once and the inline rules can be removed from all 9 pages. This is the cleaner long-term approach since the nav is identical across every page.

### Files to Change

**Option A — Quick fix (change 2 files):**
- `index.html` line ~82: change `padding: 12px 20px` → `12px 16px`, line ~85: change `font-size: 0.76rem` → `0.72rem`
- `literature.html` line ~82: change `padding: 12px 20px` → `12px 16px`, line ~85: change `font-size: 0.76rem` → `0.72rem`

**Option B — Consolidate into site.css (recommended):**
- Add standardized `.page-nav a { padding: 12px 16px; font-size: 0.72rem; }` rules to `css/site.css` under the existing `.page-nav a` block
- Remove the duplicate `.page-nav a` padding/font-size declarations from the inline `<style>` blocks in all 9 HTML files (keeping only properties that aren't already in site.css)

### Verification
Open two pages side-by-side (e.g., Home and Diagnosis) and confirm the navbar height is pixel-identical. Click through all 9 pages and verify no visual jump.

---

## 2. Reading Progress Bar for Long Content Pages (Medium Priority)

### Problem
Content pages like Diagnosis (~15 min), Conservative (~18 min), Community Discussion (~20 min), and Surgery (~20 min) are very long with no progress indicator. Patients have no sense of how much content remains.

### Why This Matters for TOS Patients
- Reading stamina is often reduced in chronic pain patients
- Starting a 20-minute article without knowing its length creates anxiety
- Users may abandon content that could help them

### Fix
Add a thin reading progress bar at the very top of content pages. A narrow horizontal line (3-4px) fixed to the top of the viewport that fills left-to-right as the user scrolls.

### Design
- **Color:** Charcoal (`#1a1a1a`) to match the institutional monochrome palette — no accent colors
- **Height:** 3px
- **Position:** `position: fixed; top: 0; left: 0; z-index: 150` — sits above page content but below the nav drawer (z-index 200/201)
- **Width:** Dynamically calculated as `(scrollY / (documentHeight - viewportHeight)) * 100%`
- **Transition:** None needed — scroll events fire frequently enough for smooth updates
- **Accessibility:** `aria-hidden="true"` (decorative, doesn't need screen reader announcement), `prefers-reduced-motion` should NOT disable this (it's informational, not animation)

### Pages to Add This To
Only the long-form content pages (6 total):
1. `diagnosis.html`
2. `conservative.html`
3. `community-discussion.html`
4. `medications.html`
5. `surgery.html`
6. `outreach.html`

**Not** on: `index.html` (short), `literature.html` (paginated list, not an article), `methodology.html` (short-ish)

### Implementation

**CSS (add to `css/site.css`):**
```css
.reading-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--color-accent);
    width: 0%;
    z-index: 150;
    pointer-events: none;
}
```

**HTML (add to each of the 6 pages, immediately after `<body>`):**
```html
<div class="reading-progress" aria-hidden="true"></div>
```

**JS (add to `js/site.js` or inline on each page):**
```js
(function () {
    var bar = document.querySelector('.reading-progress');
    if (!bar) return;
    window.addEventListener('scroll', function () {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = h > 0 ? (window.scrollY / h * 100) + '%' : '0%';
    }, { passive: true });
})();
```

### Verification
Open a long page (e.g., Surgery), scroll through, and confirm the bar fills from 0% to 100%. Check that it doesn't interfere with the sticky nav or the mobile drawer. Check on mobile.

---

## 3. ZIP Download Button — Accessibility + Progress Feedback (Medium Priority)

### Problem
The "Download All Resources (.zip)" button on the homepage changes text to "Preparing download..." during ZIP creation, but:
- No screen reader announcement
- No visual progress indicator for slow mobile connections

### Fix

**A. Screen reader live announcement:**
Add an `aria-live="polite"` region near the button that gets populated with status text when the ZIP starts building and when it completes. This way assistive tech announces the state change.

```html
<span class="sr-only" aria-live="polite" id="zip-status"></span>
```

Update the existing ZIP JS to set `#zip-status` text at key moments:
- On click: `"Preparing download. This may take a moment."`
- On complete: `"Download ready."`
- On error: `"Download failed. Please try again."`

**B. Visual progress (simple approach):**
Rather than a true progress bar (JSZip doesn't expose per-file progress easily), add a lightweight CSS animation to the button itself during preparation — e.g., a subtle pulsing border or a small inline spinner. This signals "working" without needing byte-level tracking.

### Files to Change
- `index.html` — add the `aria-live` region, add the spinner/pulse CSS, update the ZIP-building JS to set status text

### Verification
- Use VoiceOver (macOS) or a screen reader to confirm the announcement fires
- Click the ZIP button on a throttled connection (Chrome DevTools → Network → Slow 3G) and confirm the visual feedback is clear

---

## 4. Visual Diversity — Illustrations + Diagrams (Lower Priority)

### Problem
The site is entirely text-based. No illustrations, diagrams, anatomical images, or videos break up the dense medical content.

### Why This Matters
- Anatomical diagrams help patients understand their condition and communicate with doctors
- Exercise demonstration images/videos on the Conservative page would be far more useful than text descriptions alone
- Visual variety reduces cognitive fatigue during long reading sessions
- Many TOS patients report cognitive symptoms ("brain fog") — visuals are easier to process than dense text

### Approach
This is the most complex item and should be scoped carefully. The site is static (no build step), so images must be lightweight, properly licensed, and committed to the repo.

### Proposed Additions (phased)

**Phase A — Anatomical diagram on Diagnosis page:**
- A simple line diagram of the thoracic outlet showing the three compression sites (interscalene triangle, costoclavicular space, pec minor / subpectoral space)
- Options: commission a simple SVG illustration, use a Creative Commons licensed diagram, or create a labeled SVG by hand
- Place it in the hero or first section of `diagnosis.html` as a visual anchor
- Add `files/images/` directory for site images

**Phase B — Exercise illustrations on Conservative page:**
- Key exercises (serratus wall slides, scalene stretches, pec minor doorway stretch, nerve glides) with simple position illustrations or photos
- Could be static images or short embedded video links (YouTube embeds would add no repo weight)
- Place inline within each exercise section

**Phase C — Provocative test illustrations on Diagnosis page:**
- Simple diagrams showing arm positions for EAST, Roos, Adson's, Wright's tests
- Helps patients understand what the doctor is doing and reference it later

### Design Constraints
- All images must match the institutional monochrome aesthetic (grayscale or muted tones preferred)
- SVG preferred for diagrams (scales perfectly, tiny file size, can use site CSS variables)
- Photos should be compressed to < 100KB each
- All images need `alt` text describing what's shown
- Consider `loading="lazy"` for below-fold images
- No stock-photo feel — clinical/educational tone

### Licensing Considerations
- Original SVG illustrations: no licensing concern
- Creative Commons images: must verify license allows modification and commercial use (CC BY or CC BY-SA)
- Medical textbook diagrams: almost always copyrighted — cannot use without permission
- AI-generated illustrations: viable option for simple anatomical diagrams, but should be reviewed for accuracy by someone with anatomical knowledge

### Files to Change
- Create `files/images/` directory
- `diagnosis.html` — add diagram(s)
- `conservative.html` — add exercise illustrations
- Potentially `surgery.html` — add approach diagrams (transaxillary vs. supraclavicular)

### Verification
Test all images on mobile (proper sizing, not overflowing), confirm alt text is meaningful, check page load times haven't ballooned.

---

## Implementation Order

1. **Navbar fix** — smallest change, highest annoyance factor, do first
2. **Reading progress bar** — straightforward CSS/JS addition, big UX win for patients
3. **ZIP download accessibility** — focused change to one page
4. **Visual diversity** — ongoing effort, start with Phase A (one diagram on Diagnosis)

## Branch Strategy

```
git checkout -b feature/ui-ux-improvements
```

All 4 items ship on this single branch. Commit each fix separately with clear messages so they can be reviewed or reverted independently if needed. Push and PR to `main` when complete.
