/* ============================================================
   TOS Resources — Shared site script

   Currently owns the mobile nav drawer: hamburger toggle,
   drawer open/close, body-scroll lock, Esc/backdrop to close,
   focus trap, and auto-populating the "On this page" list
   from the current page's H2 headings.

   Loaded with `defer` so the DOM is ready when this runs.
   ============================================================ */
(function () {
    var toggle = document.querySelector('.nav-toggle');
    var drawer = document.querySelector('.drawer');
    var backdrop = document.querySelector('.drawer-backdrop');
    var closeBtn = document.querySelector('.drawer-close');

    if (!toggle || !drawer || !backdrop) {
        return;
    }

    var body = document.body;
    var lastFocus = null;

    function focusableElements() {
        return drawer.querySelectorAll(
            'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
    }

    function openDrawer() {
        lastFocus = document.activeElement;
        body.classList.add('drawer-open');
        toggle.setAttribute('aria-expanded', 'true');
        drawer.setAttribute('aria-hidden', 'false');
        var first = focusableElements()[0];
        if (first) {
            window.setTimeout(function () { first.focus(); }, 50);
        }
    }

    function closeDrawer() {
        body.classList.remove('drawer-open');
        toggle.setAttribute('aria-expanded', 'false');
        drawer.setAttribute('aria-hidden', 'true');
        if (lastFocus && typeof lastFocus.focus === 'function') {
            lastFocus.focus();
        }
    }

    function isOpen() {
        return body.classList.contains('drawer-open');
    }

    toggle.addEventListener('click', function () {
        if (isOpen()) { closeDrawer(); } else { openDrawer(); }
    });

    backdrop.addEventListener('click', closeDrawer);

    if (closeBtn) {
        closeBtn.addEventListener('click', closeDrawer);
    }

    document.addEventListener('keydown', function (e) {
        if (!isOpen()) { return; }
        if (e.key === 'Escape') {
            e.preventDefault();
            closeDrawer();
            return;
        }
        if (e.key === 'Tab') {
            var items = focusableElements();
            if (items.length === 0) { return; }
            var first = items[0];
            var last = items[items.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });

    // Close the drawer after navigating to an in-page anchor. Clicking
    // a link to another page will navigate and close implicitly; this
    // handles same-page hash links (the "On this page" section).
    drawer.addEventListener('click', function (e) {
        var link = e.target.closest('a');
        if (!link) { return; }
        var href = link.getAttribute('href') || '';
        if (href.charAt(0) === '#') {
            closeDrawer();
        }
    });

    // Close if viewport grows past the desktop breakpoint while the
    // drawer is open (prevents a stuck scroll lock on rotation/resize).
    var desktopMQ = window.matchMedia('(min-width: 900px)');
    function handleBreakpoint(mq) {
        if (mq.matches && isOpen()) {
            closeDrawer();
        }
    }
    if (desktopMQ.addEventListener) {
        desktopMQ.addEventListener('change', handleBreakpoint);
    } else if (desktopMQ.addListener) {
        desktopMQ.addListener(handleBreakpoint);
    }

    // Populate the "On this page" list from H2 headings in the main
    // content. Skips headings inside the drawer, header, and nav.
    var onpageList = drawer.querySelector('.drawer-onpage');
    if (onpageList) {
        var usedIds = new Set();
        document.querySelectorAll('h2, h1').forEach(function (h) {
            if (h.id) { usedIds.add(h.id); }
        });

        function slugify(text) {
            var base = text
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .trim()
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-');
            if (!base) { base = 'section'; }
            var candidate = base;
            var i = 2;
            while (usedIds.has(candidate)) {
                candidate = base + '-' + i;
                i++;
            }
            usedIds.add(candidate);
            return candidate;
        }

        var headings = Array.prototype.slice.call(document.querySelectorAll('h2'));
        headings = headings.filter(function (h) {
            if (drawer.contains(h)) { return false; }
            if (h.closest('.header-bar, .page-nav, .drawer, .drawer-backdrop')) {
                return false;
            }
            if (!h.textContent.trim()) { return false; }
            return true;
        });

        headings.forEach(function (h) {
            if (!h.id) {
                h.id = slugify(h.textContent);
            }
            var a = document.createElement('a');
            a.href = '#' + h.id;
            a.textContent = h.textContent.trim();
            onpageList.appendChild(a);
        });

        // Hide the "On this page" label if we found no headings.
        var label = drawer.querySelector('.drawer-onpage-label');
        if (headings.length === 0 && label) {
            label.style.display = 'none';
            var divider = drawer.querySelector('.drawer-divider');
            if (divider) { divider.style.display = 'none'; }
        }
    }
})();
