# StatFlight Changes

## Default drug concentrations updated

Stock concentrations updated to match program supply:

| Drug | New default stock | New per-mL | Math change |
|---|---|---|---|
| **Ketamine** | 500 mg / 5 mL | **100 mg/mL** (was 50) | mL = mg ÷ 100 (was ÷ 50) |
| **Fentanyl** | 250 mcg / 5 mL | 50 mcg/mL (unchanged) | none |
| **Midazolam** | 10 mg / 2 mL | 5 mg/mL (unchanged) | none |
| **Hydromorphone** | 2 mg/mL | 2 mg/mL (was "2 or 4") | none |

Ketamine concentration doubles — every volume calculation updated:
- adult.html: ketamineAnalgesic, ketamineInd, ketamineAgit drug cards;
  renderRsiMaxDose table calc; ketamine drip mix description
- peds.html: ketamineAnalgesic, ketamineInd (incl. giveBox rule with
  '100 mg/mL stock'); renderRsiMaxDose table calc
- ob.html: ketamineInd (incl. volume label '100 mg/mL'); renderRsiMaxDose;
  ketamine drip mix description
- pain-protocol.html: sub-label for the ketamine med block
- ketamine-chart.html: header concentration block; footnote;
  dynamic JS calc (rRsiMl, rAgitMl, rInfMl → /100); 80 KET RSI
  static cells × 2 + 40 KET AGIT + 40 KET INF = 160 ketamine cells
  recomputed via Python script. ROC RSI cells preserved (already at
  /10 from previous v49 update).

SW cache bumped v56 → v57.

## Trauma Star Analgesia replaces PHI protocol in the analgesia diagnosis (per-tab filtered)

The Pain Management diagnosis in each app now links to the Trauma Star
Analgesia Protocol page (pain-protocol.html) filtered to that app's
population — so the Adult tab shows the Adult-only section, Peds the
Peds-only section, and OB the OB Addendum (non-labor + labor).

pain-protocol.html now supports two URL params:
- `?role=adult` — hides Pediatric column + OB addendum
- `?role=peds` — hides Adult column + OB addendum
- `?role=ob` — hides all main med blocks + Adjunctive Analgesia header,
  shows only the OB Addendum (with non-labor and labor sub-blocks)
- `?embed=1` — hides the page topbar (used by in-app iframe overlay)

A small role-color badge appears at the top of the filtered view
(green for adult, cyan for peds, pink for ob).

In-app integration:
- Each app (adult/peds/ob) gets a small HTML iframe overlay with a
  BACK TO APP button and Escape-to-close
- renderPlan() in each app prepends a purple proto-style button when
  the selected diagnosis is `pain_mgmt` (and OB also for `labor_pain`)
- Button opens pain-protocol.html?role=<adult|peds|ob>&embed=1 inside
  the iframe overlay — fully offline-capable via the existing SW cache

SW cache bumped v55 → v56.

## Add Ketorolac + IV Acetaminophen (Tylenol) to pain protocol

Two non-narcotic adjuncts added across pain-protocol.html and the in-app
pain_mgmt entries:

### Ketorolac (Toradol) — NSAID
- Adult: 15 mg IV over 30-60 sec
- Peds (≥ 2 yr): 0.5 mg/kg IV over 30-60 sec, max 15 mg
- Indications: mild-moderate pain (musculoskeletal, renal colic, headache);
  opioid-sparing in poly-trauma
- AVOID: renal impairment / AKI, GI bleed / ulcer, coagulopathy, severe
  asthma, hypovolemia / hemorrhagic shock, pregnancy > 20 wk
  (strict > 28 wk), peds < 2 yr

### Acetaminophen IV (Ofirmev) — NEW non-narcotic, non-NSAID
- Adult (≥ 50 kg): 1000 mg IV over 15 min q 6 hr
- Adult / peds (< 50 kg, ≥ 2 yr): 15 mg/kg IV over 15 min q 6 hr
- Peds (2-12 yr): 15 mg/kg q 6 hr, max 75 mg/kg / 24 hr (max 3.75 g)
- MAX adult: 4 g per 24 hr from ALL acetaminophen sources combined
- SAFE in pregnancy at all gestational ages — preferred non-opioid in OB
- AVOID / reduce: hepatic impairment, chronic alcohol use, malnutrition
- Infuse over 15 min — do not bolus push

Drug cards added/restored:
- adult.ketorolac (restored)
- adult.acetaminophenIV (new)
- peds.ketorolac (restored, with age ≥2 yr requirement)
- peds.acetaminophenIV (new, with age-based dosing)
- ob.acetaminophenIV (new, called out as safe in pregnancy)

Drug map updates:
- adult.pain_mgmt: + ketorolac + acetaminophenIV
- peds.pain_mgmt: + ketorolac + acetaminophenIV
- ob.pain_mgmt: + acetaminophenIV
- ob.labor_pain: + acetaminophenIV (opioid-sparing for labor)

pain-protocol.html — two new med blocks under Adjunctive Analgesia
(Ketorolac and Acetaminophen IV) with INDICATION / CONTRA / NOTE tags.
OB addendum updated: both non-labor and labor sub-blocks now include
Acetaminophen IV as the OB-preferred non-opioid; ketorolac/NSAID
restriction by GA preserved.

SW cache bumped v54 → v55.

## Pain protocol: PHI document FORMAT, Trauma Star content (no morphine, no ketorolac)

Per user clarification — keep the PHI document visual format (banner,
Adult/Pediatric two-column bullets, NOTE/CAUTION callouts) but revert
all content to Trauma Star doses. Morphine and ketorolac removed — not
carried by program.

pain-protocol.html now shows:
- Trauma Star branded banner (purple "TRAUMA STAR" block)
- Section 1.0 Analgesia heading + general guidelines intro
- Fentanyl: 0.5-1 mcg/kg adult / 1-2 mcg/kg peds (max 100 mcg single)
- Hydromorphone: 0.2-0.8 mg adult (0.5-1.5 opioid-tolerant) /
  0.01-0.02 mg/kg peds
- Adjunctive Ketamine sub-dissociative: 0.1-0.3 mg/kg low tier /
  0.3-0.5 mg/kg high tier (adult + peds); peds IN 1-1.5 mg/kg
- 4 NOTEs + CAUTION callout for ketamine (refractory/Naltrexone/
  Buprenorphine indications, psychosis caution, slow-push warning,
  contraindicated in pregnancy)
- OB Addendum with non-labor and labor sub-blocks
- Reassess + Document tiles

In-app pain_mgmt protocols (adult/peds/ob) reverted to Trauma Star
content. Drug cards reverted: ketamineAnalgesic back to two-tier
0.1-0.3 / 0.3-0.5 range; hydromorphone back to 0.2-0.8 / 0.5-1.5
opioid-tolerant. Ketorolac drug card removed from adult + peds.

Drug map for pain_mgmt: fentanylBolus + hydromorphone + ketamineAnalgesic.

SW cache bumped v53 → v54.

## Pain protocol rebuilt to PHI 5.1.2 Analgesia format (Rev 23, 23 Jan 2025)

`pain-protocol.html` rewritten to mirror the PHI Health Clinical Care
Guidelines section 5.1.2 verbatim:

- PHI document-style banner (PHI HEALTH logo block, section title,
  Rev/Date metadata)
- "5.1.2 Analgesia" section heading
- General Guidelines intro paragraph (verbatim from PHI doc)
- Each medication: Adult column / Pediatric column with bulleted doses
  - Fentanyl: 0.5–2 mcg/kg IBW IV over 1 min, IM, NAS — repeat q 10 min PRN
  - Morphine: 2–10 mg adult / 0.05–0.2 mg/kg peds (max 10 mg single)
  - Hydromorphone: 0.2–1 mg adult / 0.01–0.02 mg/kg peds — max total 4 mg
- "Adjunctive Analgesia" subsection
  - Ketamine sub-dissociative 0.1–0.3 mg/kg IBW; max single 30 mg;
    NOTE × 3 (refractory to opioids · Naltrexone/Buprenorphine ·
    not advised in psychosis); CAUTION callout for slow push
  - Ketorolac 15 mg adult / 0.5 mg/kg peds (max 15 mg)
- OB addendum below — institutional guidance not in PHI 5.1.2: non-labor
  vs labor pain with ketamine contraindication and NSAID gestational-age
  limits
- Reassess + Document tiles at bottom
- Print stylesheet: portrait letter, 0.4" margins, monochrome-friendly

In-app pain_mgmt protocols updated to PHI doses (adult / peds / ob).
Drug cards (adult + peds): ketamineAnalgesic simplified to single
0.1–0.3 mg/kg range with 30 mg cap; hydromorphone updated to PHI
0.2–1 mg adult / 0.01–0.02 mg/kg peds with 4 mg total cap; new
ketorolac card added.

SW cache bumped v52 → v53.

## New: One-page Trauma Star Pain Protocol (pain-protocol.html)

Standalone reference card covering Adult, OB Non-Labor, OB Labor, and Peds
on a single landscape page. Mirrors the meds in the existing diagnosis
cards (Fentanyl → Ketamine analgesic → Hydromorphone), with ketamine
explicitly contraindicated for both OB variants.

Each medication block shows:
- **When** (indication)
- **Dose** (with weight-based math where applicable)
- **Reassess** (timing + what to monitor)
- **Document** (exactly what to chart)

Plus a top-of-page differentiation callout (broken-bone vs labor pain)
and bottom-of-page reassess + document checklists. Print stylesheet
formats to landscape letter at 0.3" margins.

New homepage card on index.html links to it (purple gradient, "PAIN" icon).
Added to SW cache list. Cache bumped v51 → v52.

## Diagnosis picker condensed to a dropdown (Adult / Peds / OB)

The diagnosis grid (~30 cards per app stacked in multiple rows by category)
is now a single `<select>` with `<optgroup>` per category. Saves ~80% of
the vertical space on mobile. Tap the dropdown → pick from grouped lists.

Behavior unchanged — selecting a diagnosis still triggers the same render
chain (drug panel, plan, burn map / diagnosis drugs). `state.dx` /
`state.m.dx` are preserved.

SW cache bumped v50 → v51.

## Trauma Star Pain Protocol (Adult / Peds / OB)

New diagnosis card under a new "PAIN / ANALGESIA" category in all three apps.

**Adult & Peds — stepwise:**
- Step 1 — Fentanyl
- Step 2 — Ketamine (analgesic / sub-dissociative dose)
- Step 3 — Hydromorphone (Dilaudid)

Both new drug cards added: `ketamineAnalgesic` (weight-based, with low and high dose tiers) and `hydromorphone`. Peds variant includes weight-based calc and an IN ketamine route.

**OB — split into two distinct protocols (with broken-bone vs labor differentiation built into the picture text):**

`pain_mgmt` (Non-Labor):
- Step 1 — Fentanyl
- Step 2 — Hydromorphone
- **KETAMINE CONTRAINDICATED** for analgesia in pregnancy
- NSAIDs avoid after 20 wks; strictly avoid after 28 wks
- Use lowest effective dose

`labor_pain`:
- First-line: Neuraxial (epidural / spinal) with anesthesia/OB
- Systemic fallback: Fentanyl 50-100 mcg IV q30-60 min, Hydromorphone 0.5-1 mg IV q2-3 hr
- NO ketamine
- Avoid near planned delivery (neonatal respiratory depression — be ready w/ neonatal naloxone 0.1 mg/kg)
- Left-lateral tilt >20 wks

SW cache bumped v49 → v50.

## Rocuronium dose change (Adult / OB / Peds / Ketamine chart)

PHI IV RSI dose updated from 1.5 mg/kg IBW (Adult / OB) and 1.2 mg/kg IV (Peds)
to **1 mg/kg** across all three apps and the shared Ketamine + Roc quick-chart.

Updated every spot the dose surfaces:
- Safer-checklist text in each app
- `rocRSI` / `rocuroniumRSI` / `rocPeds` drug-card function (dose calculation + label rows + giveBox rule)
- `renderRsiMaxDose` auto-calculated dose table
- RSI sequence callout
- Ketamine + Roc Quick Chart: header label, dose card, dynamic calc (`wt * 1.0`), explanatory footnote
- Ketamine chart static reference table — all 120 ROC RSI dose cells recomputed from `weight × 1 mg`

IM dose unchanged (2 mg/kg IBW IM, onset ~5 min). OB rebolus unchanged (0.15–0.3 mg/kg PRN).

SW cache bumped v48 → v49 so installed PWAs pick up the new dose.

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
