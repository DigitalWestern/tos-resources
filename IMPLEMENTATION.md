# Design System Implementation Guide

**Branch:** `feature/design-system`
**Status:** Ready to implement — drop these files into the repo and follow the steps below.

---

## What the UI Kit Is

The UI Kit (`ui_kits/website/index.html`) is a **design prototype** — a high-fidelity visual reference built in React/JSX for fast iteration. It is **not** production code.

The live site (`tosresources.com`) is **plain HTML + CSS + vanilla JS** with no build step. To implement these designs you translate the visual patterns in the prototype into the existing HTML/CSS/JS files.

---

## Files to Copy Into the Repo

### 1. `css/brand-tokens.css` ← NEW FILE

Drop this into `css/` alongside `site.css`. Load it **before** `site.css` in every page's `<head>`:

```html
<link rel="stylesheet" href="css/brand-tokens.css">
<link rel="stylesheet" href="css/site.css">
```

Contents: see `css/brand-tokens.css` in this design system project.

### 2. Update `css/site.css` — Brand Color Tokens

Add these lines at the top of the `:root` block in `site.css`:

```css
:root {
  /* ── Brand palette (from logo) ──── */
  --color-brand-navy:  #1b3560;
  --color-brand-teal:  #2e9d9a;
  --color-brand-gold:  #ecc94b;
  --color-brand-slate: #9baab8;

  /* Remap existing accent to navy */
  --color-accent:       #1b3560;
  --color-accent-hover: #142848;
  --color-header-bg:    #1b3560;
}
```

This alone will shift the masthead and all buttons from charcoal to brand navy.

---

## Component-by-Component Implementation

### NavBar / Header

**Current:** `#1a1a1a` charcoal masthead, plain text wordmark.

**Target:**
- Background: `--color-brand-navy` (`#1b3560`)
- Add the 3px gradient rule below the nav:
  ```css
  .page-nav::after {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, #2e9d9a, #ecc94b, #2e9d9a);
  }
  ```
- Active nav tab: background `#2e9d9a` (teal), no underline
- Wordmark: add `<span class="nav-tos">TOS</span><span class="nav-resources">Resources</span>` with:
  ```css
  .nav-tos      { color: #ffffff; font-weight: 700; }
  .nav-resources { color: #2e9d9a; font-weight: 400; }
  ```

### Hero / Page Intro

**Current:** Plain white background, dark text headline.

**Target (homepage hero):**
```css
.hero {
  background: linear-gradient(135deg, #0f2340 0%, #1b3560 60%, #1f4a6e 100%);
  padding: 80px 32px 72px;
  position: relative;
  overflow: hidden;
}
.hero h1 { color: #ffffff; }
.hero p   { color: rgba(255,255,255,0.72); }
```

Add decorative circle (logo echo) as a pseudo-element:
```css
.hero::before {
  content: '';
  position: absolute;
  right: 60px; top: -60px;
  width: 340px; height: 340px;
  border-radius: 50%;
  border: 2px solid #2e9d9a;
  opacity: 0.15;
  pointer-events: none;
}
```

### Cards

**Current:** Flat white cards, border darkens on hover.

**Target:** Keep flat style. Add teal top-border on hover:
```css
.card:hover {
  border-color: var(--color-border-strong);
  border-top-color: var(--color-brand-teal);
  border-top-width: 3px;
  box-shadow: 0 8px 24px rgba(27,53,96,0.10);
  transform: translateY(-2px);
}
```

### Buttons

**Current:** Charcoal `#1a1a1a` fill.

**Target:** Teal fill for primary actions:
```css
.btn-primary,
.download-btn,
.download-btn.primary {
  background: var(--color-brand-teal);
  border-color: var(--color-brand-teal);
  color: #ffffff;
}
.btn-primary:hover,
.download-btn:hover {
  background: #237d7a;
  border-color: #237d7a;
}
```

### Reading Progress Bar

**Current:** `#2563eb` blue.

**Target:** Teal gradient:
```css
.reading-progress {
  background: linear-gradient(90deg, #2e9d9a, #ecc94b);
}
```

### Back-to-Top Button (Mobile)

The current `back-to-top` button is a plain circle. Replace with a ring-progress version:

```html
<!-- Replace existing back-to-top button with this -->
<div id="back-to-top-wrap" style="position:fixed;bottom:24px;right:20px;z-index:40;opacity:0;transition:opacity 0.3s,transform 0.3s;transform:scale(0.6);">
  <button id="back-to-top" aria-label="Back to top" style="width:52px;height:52px;border-radius:50%;background:#1b3560;border:none;cursor:pointer;position:relative;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(27,53,96,0.4);">
    <svg id="back-to-top-ring" width="52" height="52" style="position:absolute;top:0;left:0;transform:rotate(-90deg);">
      <circle cx="26" cy="26" r="22" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="3.5"/>
      <circle id="ring-progress" cx="26" cy="26" r="22" fill="none" stroke="#2e9d9a" stroke-width="3.5"
        stroke-dasharray="138.2" stroke-dashoffset="138.2" stroke-linecap="round"/>
    </svg>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" style="position:relative;z-index:1;">
      <polyline points="18 15 12 9 6 15"/>
    </svg>
  </button>
</div>
```

Add this JS to `js/site.js`:
```js
(function () {
  var wrap = document.getElementById('back-to-top-wrap');
  var btn  = document.getElementById('back-to-top');
  var ring = document.getElementById('ring-progress');
  if (!wrap || !btn || !ring) return;
  var circ = 2 * Math.PI * 22; // 138.2

  window.addEventListener('scroll', function () {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var pct = h > 0 ? window.scrollY / h : 0;
    ring.style.strokeDashoffset = circ - pct * circ;
    var visible = pct > 0.06;
    wrap.style.opacity  = visible ? '1' : '0';
    wrap.style.transform = visible ? 'scale(1)' : 'scale(0.6)';
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
```

---

## Section Rhythm (Key Layout Patterns)

| Section type       | Background            | Padding (desktop) |
|--------------------|-----------------------|-------------------|
| Hero               | Navy gradient         | 80px 32px         |
| Stats bar          | `--color-brand-navy`  | 20px 32px         |
| Cards/pathways     | `#ffffff`             | 72px 32px         |
| Downloads list     | `#f4f8f8` (teal tint) | 72px 32px         |
| Community callout  | `--color-brand-navy`  | 72px 32px         |
| Disclaimer         | `#ffffff`             | 40px 32px         |
| Footer             | `#122444` (navy dark) | 48px 32px         |

Alternate white and tinted/navy sections for visual rhythm. Never two navy sections in a row.

---

## Git Commands

```bash
# From the repo root on your machine
git checkout -b feature/design-system
git add css/brand-tokens.css
git add IMPLEMENTATION.md
git commit -m "feat: brand token CSS + design system implementation guide"
git push origin feature/design-system
```

Then open a PR on GitHub from `feature/design-system` → `main`.

---

## What Stays the Same

- **Font:** Times New Roman everywhere — no change needed.
- **Card border-radius:** 4px — no change.
- **Content structure:** All HTML content, headings, body copy — untouched.
- **Accessibility:** All ARIA labels, focus states, drawer behaviour — untouched.
- **Mobile drawer:** Keep existing JS; only visual CSS changes (background → navy, active link → teal left-border).
