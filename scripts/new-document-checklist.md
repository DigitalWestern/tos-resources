# New Document Checklist — tosresources.com

> **Read this before adding, updating, or removing any document from the site.**
>
> The site is a single `index.html` file with all CSS and JS inline. Every document is referenced in multiple places throughout that file. Missing any one of them will cause a broken download, a missing search result, or an incorrect file count. This checklist ensures nothing gets missed.

---

## How the Site Works

The site is a static single-file HTML page hosted on GitHub Pages. There is no build step, no framework, and no server — just `index.html` and the files in `files/`. Every feature that references documents is wired up manually inside `index.html`:

| Feature | What it does | Where in `index.html` |
|---------|-------------|----------------------|
| **Download cards** | Visual card with title, description, "See what's inside" dropdown, and download buttons | HTML body, inside `<div class="cards">` containers |
| **Full-text search** | Client-side brute-force search across embedded text from all documents | `var TOS_SEARCH_DATA` JS array (~line 2207) |
| **Search synonyms** | Maps medical abbreviations to full names and vice versa | `var TOS_SYNONYMS` JS object (after search data) |
| **Download All ZIP** | Client-side ZIP generation via JSZip, bundles every file | `var files = [...]` array in the download-all click handler (~line 2568) |
| **File count note** | "All N files bundled into a single download" text | `<p class="download-all-note">` (~line 2114) |
| **Stats bar** | "382 Reddit posts · N free resources · ~X min reading" | `<p class="stats-line">` (~line 2123) |
| **Guided flow** | 4-step suggested path for new visitors, mentions how many docs are searchable | `<div class="guided-flow">` (~line 1840) |
| **GoatCounter analytics** | Tracks individual file downloads automatically | Auto-wired to any element with class `download-btn` — no manual setup needed |
| **Card icon CSS** | Each document type has a color-coded icon class | Light mode CSS (~line 136+) and dark mode CSS (~line 1576+) |

---

## Checklist: Adding a New Document

Complete every step. Do not skip any — they are all load-bearing.

### 1. Place the files

- [ ] Add the `.docx` file to `files/`
- [ ] Add the `.pdf` file to `files/` (use LibreOffice headless to convert: `/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir files/ files/YOUR_FILE.docx`)
- [ ] Verify both files exist and are non-zero size

### 2. Add CSS for the card icon (if using a new color class)

Each document type has a unique icon color. If reusing an existing class (like `doc` or `checklist`), skip this step. If creating a new one:

- [ ] Add the light mode CSS rule:
  ```css
  .card-icon.YOURCLASS {
      background: #xxxxxx;
      color: #xxxxxx;
  }
  ```
  Location: after the existing `.card-icon.*` rules (~line 136–155)

- [ ] Add the dark mode CSS rule:
  ```css
  .card-icon.YOURCLASS {
      background: #xxxxxx;
      color: #xxxxxx;
  }
  ```
  Location: inside the `@media (prefers-color-scheme: dark)` block, after existing dark `.card-icon.*` rules (~line 1576–1610)

- [ ] Add `.download-btn.YOURCLASS` and `.download-btn.YOURCLASS:hover` to the existing comma-separated download button CSS selector lists. There are **two sets** — one in the main CSS and one in the dark mode media query. Search for `.download-btn.expanded` to find both.

### 3. Add the download card HTML

Cards are grouped in `<div class="cards">` containers under section labels. The site has three sections:
- **Reports & Guides** (`#reports`) — research documents
- **Exercise Trackers** (`#trackers`) — spreadsheets
- **Expanded Findings** — supplemental research

Add the card in the appropriate section. Copy the HTML pattern from an existing card with `.docx` + `.pdf` downloads:

```html
<div class="card">
    <div class="card-icon YOURCLASS">
        <svg>...</svg>  <!-- pick an appropriate icon -->
    </div>
    <h2>Document Title</h2>
    <p class="description">One-sentence description.</p>
    <span class="file-type">Word (.docx) &amp; PDF</span>
    <span class="last-updated">Added Mon DD, YYYY</span>
    <span class="reading-time">~X min read</span>
    <details class="card-preview">
        <summary>See what's inside</summary>
        <ul class="card-preview-list">
            <li>Section heading from document</li>
            <li>Another section heading</li>
            <!-- one <li> per major section/heading in the document -->
        </ul>
    </details>
    <div class="download-buttons">
        <a href="files/YOUR_FILE.docx" download class="download-btn YOURCLASS">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            .docx
        </a>
        <a href="files/YOUR_FILE.pdf" download class="download-btn YOURCLASS download-btn-pdf">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            .pdf
        </a>
    </div>
</div>
```

**Notes:**
- The `download-btn` class triggers GoatCounter tracking automatically — no extra JS needed.
- Only add an `id` attribute if the card needs to be linked from the guided flow section.
- The "See what's inside" list should mirror the actual headings in the document.

### 4. Add to the search corpus

The search corpus is a JS array called `TOS_SEARCH_DATA` (~line 2207). Each document is an object with a `title`, `downloadPath`, `colorClass`, and `sections` array.

- [ ] Add a new entry to the `TOS_SEARCH_DATA` array:
  ```javascript
  {
      title: "Your Document Title",
      downloadPath: "files/YOUR_FILE.docx",
      colorClass: "YOURCLASS",
      sections: [
          { heading: "Section Name", text: "Plain text content of this section stripped of formatting. Keep it as one continuous string. Include key terms people might search for." },
          // one entry per major section of the document
      ]
  }
  ```

**Important notes about search corpus text:**
- Strip all markdown/formatting — plain text only
- No quotes inside the text (or escape them)
- Include medical terms, drug names (brand AND generic), abbreviations — these are what people search for
- Each section's text should be a meaningful chunk (a paragraph to a few paragraphs)

### 5. Add search synonyms (if applicable)

The synonym map is `TOS_SYNONYMS` (right after `TOS_SEARCH_DATA`). It maps search terms to equivalent terms so users find results regardless of which name they use.

- [ ] For any new medical terms, drug names, or abbreviations introduced by the document, add bidirectional synonym entries:
  ```javascript
  "gabapentin": ["neurontin"],
  "neurontin": ["gabapentin"],
  ```

**Pattern:** Always make synonyms bidirectional. If A maps to B, B should also map to A.

### 6. Add to the Download All ZIP

The ZIP is built client-side from a `files` array in the download-all button click handler (~line 2568).

- [ ] Add both file paths to the array:
  ```javascript
  'files/YOUR_FILE.docx',
  'files/YOUR_FILE.pdf',
  ```

### 7. Update counts

Three places display counts that must stay in sync:

- [ ] **Download-all note** (~line 2114): Update `"All N files bundled into a single download"` — count is total individual files (each .docx, .pdf, and .xlsx counts as one)
- [ ] **Stats bar** (~line 2123): Update `"N free resources"` to match the new total and update `"~X min reading"` (estimate ~14 min per new research doc)
- [ ] **Guided flow** (~line 1867): If the text says "across all N documents" update the number (this refers to searchable documents only, not exercise spreadsheets)

### 8. Verify

Run these checks before committing:

- [ ] Open `index.html` in a browser locally
- [ ] Confirm the new card appears in the correct section
- [ ] Click "See what's inside" — confirm it expands with the right section list
- [ ] Click both download buttons — confirm the files download
- [ ] Search for a term unique to the new document — confirm results appear
- [ ] Search for a synonym — confirm it finds the right content
- [ ] Click "Download All Resources (.zip)" — confirm the ZIP contains the new files
- [ ] Check dark mode (toggle system appearance) — confirm the card icon has proper colors

---

## Checklist: Updating an Existing Document

When a document's content changes (not just metadata):

- [ ] Replace the `.docx` file in `files/`
- [ ] Regenerate the `.pdf` from the updated `.docx`
- [ ] Update the search corpus text in `TOS_SEARCH_DATA` to reflect new/changed content
- [ ] Update the "See what's inside" list if section headings changed
- [ ] Update the `<span class="last-updated">` date on the card
- [ ] Add any new synonyms for new terms introduced
- [ ] Update reading time estimate if the document length changed significantly

---

## Checklist: Removing a Document

- [ ] Delete the `.docx` and `.pdf` from `files/`
- [ ] Remove the card HTML from the cards container
- [ ] Remove the entry from `TOS_SEARCH_DATA`
- [ ] Remove the files from the ZIP `files` array
- [ ] Remove any synonyms that were only relevant to this document
- [ ] Remove the CSS class if it was unique to this document (both light and dark mode)
- [ ] Update the download-all note count
- [ ] Update the stats bar count and reading time
- [ ] Update the guided flow document count text

---

## Quick Reference: File Locations in `index.html`

These are approximate line numbers as of April 2026. They will shift as the file is edited — use the search strings to find them reliably.

| What | Search for | ~Line |
|------|-----------|-------|
| Card icon CSS (light) | `.card-icon.doc {` | 136 |
| Card icon CSS (dark) | `@media (prefers-color-scheme: dark)` then `.card-icon.doc` | 1576 |
| Download button CSS | `.download-btn.doc,` | 206 |
| Guided flow | `<div class="guided-flow">` | 1840 |
| Reports cards section | `<div id="reports"` | 1886 |
| Trackers cards section | `<div id="trackers"` | 2031 |
| Expanded cards section | `<div class="section-label expanded">` | 2065 |
| Download-all ZIP | `var files = [` | 2568 |
| File count note | `download-all-note` | 2114 |
| Stats bar | `stats-line` | 2123 |
| Search corpus | `var TOS_SEARCH_DATA` | 2207 |
| Synonym map | `var TOS_SYNONYMS` | 2328 |
| GoatCounter | `data-goatcounter` | 2187 |

---

## Existing Color Classes

| Class | Used by | Light bg | Light text | Dark bg | Dark text |
|-------|---------|----------|------------|---------|-----------|
| `doc` | Community Research Report | `#ede8e0` | `#5c3d2e` | `#2a2520` | `#c49a6c` |
| `surgical` | Surgical Outcomes | `#ede0e8` | `#5c2e4a` | `#2a2025` | `#bb8faa` |
| `checklist` | Diagnostic Checklist | `#ede8e0` | `#5c4a2e` | `#2a2520` | `#c4a86c` |
| `medications` | Medications Guide | `#e0e8ed` | `#2e4a5c` | `#202530` | `#6ca8c4` |
| `sheet` | Exercise Tracker | `#e4ede0` | `#3d5c2e` | `#222a1f` | `#8dbb6c` |
| `sheet-alt` | Exercise Tracker (No Nerve Flossing) | `#e4ede0` | `#3d5c2e` | `#222a1f` | `#8dbb6c` |
| `expanded` | Expanded Findings | `#ede8e0` | `#5c3d2e` | `#2a2520` | `#c49a6c` |
