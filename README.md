# NH Value Creation Bridge

Single-file web app that turns BP assumptions (entry → exit) into a memo-ready **value creation bridge** in NORD Holding colours: sales growth, EBITDA margin, multiple rerating, deleveraging.

**Live website:** https://nord-holding.github.io/value-bridge/
(also runs offline: double-click `index.html`, or drop it on the V-drive)

## How to use

1. Fill the assumptions matrix — **green = input, white = calculated**. Columns: Entry (platform) | + Add-ons | = PF entry | Exit. Arrow keys / Enter move between cells; comma or dot decimals both work.
2. The waterfall, MOIC/IRR stats and bridge table update live. Hover a bar to see its formula.
3. Export: **Download PNG** (3000×1800, white background) or **Copy PNG** straight into the memo; SVG and Excel-paste (TSV) also available.
4. **Copy share link** — all inputs are encoded in the URL fragment, so a pasted link reopens the exact case. Nothing is ever uploaded; all computation is client-side.

## M&A convention (important)

Add-ons are consolidated **pro-forma at entry**:

- acquired sales / EBITDA build on top of the platform entry base,
- consideration (EV paid) adds to entry EV → **blends the entry multiple down**,
- the debt-funded part adds to entry net debt; the equity-funded rest counts as invested at entry.

Growth bars are therefore **organic vs the PF base**, and the multiple-rerating bar carries the blend-down arbitrage back to the exit multiple. Enter BP add-on totals in the *+ Add-ons* column — do not bury them in Exit only.

## Methodology (ties by construction)

With `S`=sales, `E`=EBITDA, `x`=EV/EBITDA, `N`=net debt, `m`=margin; subscript `0ᴾᶠ` = pro-forma entry, `1` = exit:

```
S0pf = S0 + Sacq          E0pf = E0 + Eacq
EV0pf = E0·x0 + consideration        N0pf = N0 + debt-funded part
x0pf = EV0pf / E0pf   (blended entry multiple)
Eq0pf = EV0pf − N0pf

Sales growth      = (S1 − S0pf) · m0pf · x0pf
EBITDA margin     = (m1 − m0pf) · S1 · x0pf
Multiple rerating = (x1 − x0pf) · E1
Deleveraging      = N0pf − N1

Identity: Eq0pf + all bars = E1·x1 − N1 = Eq1   (checked live — "bridge ties ✓" badge)
```

Toggle available for a combined bar: `EBITDA growth = (E1 − E0pf) · x0pf` instead of the sales × margin split.

Returns: `gross MOIC = (Eq1 + distributions) / Eq0pf`; `gross IRR = MOIC^(1/years) − 1` (flows assumed at entry/exit). Figures are gross of fund fees and carry.

## Files

| File | Purpose |
|---|---|
| `index.html` | The website / offline app — single file, zero dependencies |
| `app.html` | claude.ai artifact variant, generated from the markers in `index.html` |

Regenerate `app.html` after editing `index.html`:

```bash
awk '/ARTIFACT-START/{f=1;next}/ARTIFACT-END/{f=0}f' index.html > app.html
```

## Privacy note

The page is statically hosted (GitHub Pages) and fully client-side: deal inputs live only in the user's browser (`localStorage`) and in share-link URL **fragments**, which are never transmitted to the server.
