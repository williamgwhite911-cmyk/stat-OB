# StatFlight v1.1 — Changes

## New Protocols (synced across Adult / Peds / OB)

| Protocol | Adult | Peds | OB |
|---|:-:|:-:|:-:|
| Open Fracture | ✅ | ✅ | ✅ (maternal) |
| Laceration / Soft Tissue | — | ✅ | — |
| AAA / Aortic Catastrophe | ✅ | ✅ (rare) | ✅ (maternal) |
| Aortic Dissection | ✅ | ✅ (rare) | ✅ (maternal) |
| Brain Herniation | ✅ | ✅ | ✅ (maternal) |
| Hemorrhagic Shock | ✅ | ✅ | ✅ (maternal) |
| Hemorrhagic Stroke | (existed) | ✅ NEW | (existed via PIH/severe pre) |
| Post-Intubation Sedation | ✅ | ✅ | ✅ |
| Dangerous Agitation | (existed) | ✅ NEW | ✅ NEW (maternal) |
| Anxiolysis | ✅ | ✅ | ✅ (Anxiolysis pre-flight) |

OB protocols include left-lateral-tilt + perimortem c-section reminders. Peds protocols use weight-based dosing via the existing Broselow/Handtevy auto-calc helpers.

## PDF Back Button (fix)

Previously: PHI Protocol PDFs opened in a new browser tab. In standalone PWA mode there was no browser chrome → no way back to the app.

Now: PDFs open in an in-app overlay viewer with:
- Fixed "‹ BACK TO APP" button at top-left
- Escape key closes the viewer
- Iframe-based, so the rest of the app state (selected diagnosis, weights, etc.) is preserved

Infrastructure was added to all three apps (adult/peds/ob). Adult is wired up to the existing `renderProtocolBtn()` function; peds and ob have stub functions ready to wire to PROTOCOL_FILES/PROTOCOL_PAGES when those are populated for those apps.

## Service Worker

Cache version bumped: `statflight-v12` → `statflight-v13`. Existing installs will pick up the new files on next launch + reload.

## Deploying to GitHub

If your repo is already cloned locally:

```bash
# from your StatFlight repo root
cp /path/to/these/outputs/{adult.html,peds.html,ob.html,index.html,sw.js} .
git add adult.html peds.html ob.html index.html sw.js
git commit -m "v1.1 — add open fracture, laceration (peds), aortic/herniation/shock/sedation protocols + in-app PDF back button"
git push origin main
```

If deploying via GitHub Pages, the new SW cache version (`statflight-v13`) will trigger an update on next visit; users may need to fully reload or close/re-open the PWA once.

## Files Changed

- `adult.html` — +7 protocols, PDF overlay viewer, renderProtocolBtn rewired
- `peds.html` — +10 protocols (incl. Open Fracture & Laceration), PDF overlay viewer
- `ob.html` — +8 protocols (maternal-adapted), PDF overlay viewer
- `index.html` — version bump v1.0 → v1.1
- `sw.js` — cache version bump v12 → v13
