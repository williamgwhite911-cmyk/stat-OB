═══════════════════════════════════════════════════════════════
  StatFlight — PHI Protocol PDFs
═══════════════════════════════════════════════════════════════

WHAT GOES HERE
--------------
Drop your PHI Clinical Care Guidelines PDFs in this folder,
one per category. Use these exact filenames (case-sensitive):

    protocols/
      PHI_Peds.pdf         (Chapter 5 — Pediatric)
      PHI_Medical.pdf      (Adult medical — DKA, hypoglycemia,
                            tox, hyperK, sepsis, etc.)
      PHI_Trauma.pdf       (Chapter 4 — Trauma, burn, ↑ICP/TBI)
      PHI_Respiratory.pdf  (Chapter 3 — Asthma, croup, RSV)
      PHI_Airway.pdf       (Chapter 2 — SAFER / RSI)
      PHI_OB.pdf           (Maternal / OB)
      PHI_General.pdf      (Chapter 1 / General)

You don't need ALL of them — drop in only what you have. Buttons
for missing files will show a friendly "not installed" message
instead of breaking.


CONFIGURING WHICH PDF + PAGE EACH DIAGNOSIS OPENS
-------------------------------------------------
Open peds.html and find the PROTOCOL_PAGES block near the top
(search for "PROTOCOL_PAGES").

Each diagnosis points to a `src` (which PDF) and a `page`
(starting page in that PDF). Example:

    var PROTOCOL_PAGES = {
      preterm:    { src: 'peds',    label: '...', page: 12 },
      sepsis:     { src: 'peds',    label: '...', page: 47 },
      trauma:     { src: 'trauma',  label: '...', page: 5  },
      burn:       { src: 'trauma',  label: '...', page: 22 },
      dka:        { src: 'medical', label: '...', page: 18 },
      ...
    };

Update the `page:` number for each entry to match the page
in YOUR copy where that protocol begins.

If you want to point a diagnosis at a different file, change
its `src:` to one of: peds, medical, trauma, resp, airway,
ob, general (these keys are defined in PROTOCOL_FILES, just
above PROTOCOL_PAGES — edit there if you rename a file).


ADDING A NEW PROTOCOL FILE
--------------------------
1. Drop the PDF in this folder with a clear name, e.g.
   PHI_Cardiac.pdf
2. In peds.html, add the entry to PROTOCOL_FILES:
       cardiac: 'protocols/PHI_Cardiac.pdf',
3. Reference it from any diagnosis with `src: 'cardiac'`.
4. Add the path to OPTIONAL_ASSETS in sw.js so the service
   worker precaches it for offline use.
5. Bump CACHE_NAME in sw.js (e.g. v4 → v5) so existing
   installs pick up the new file.


OFFLINE USE
-----------
The service worker auto-caches every PDF that exists on the
first online visit, so the protocols are available offline
on the helo / in the field afterward.


DISTRIBUTION
------------
This folder is included in the GitHub Pages bundle. Because
PHI clinical guidelines are proprietary, only share the
deployment URL with PHI staff who are authorized to view the
protocols.


IF YOU SWAP OR ADD A PDF
------------------------
After replacing or adding a PDF, bump the cache version in
sw.js (change CACHE_NAME from 'statflight-v4' to '-v5')
so the service worker re-downloads it on the next visit.
