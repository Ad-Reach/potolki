---
name: update-content
description: Change contacts, prices, promotions (акции), FAQ, stats or other content of the Центр Плюс site in data.py, then rebuild dist/. Use when asked to update a phone, address, hours, messenger link, price, promo, FAQ answer or similar text.
allowed-tools: Read, Grep, Glob, Edit, Bash(python3 build.py), Bash(git status:*), Bash(git diff:*)
---

# Update site content

All content lives in `data.py`; some facts are also hardcoded in `build.py` and `src/js/main.js`.
Make the smallest change that does what was asked, then rebuild.

## Hard rules

- Use only values the user gave you in this conversation (or a file they pointed to). Never guess, round,
  "fix" or infer a value, and never copy values from other websites.
- **Prices:** `PRICES` and `CANVASES` hold placeholder numbers (see the comment in `data.py`). Leave them untouched
  unless the user gives specific new values. Never take numbers from rumexpert.ru or any other site.
  Do not remove the "черновые" comment on your own.
- Empty fields (`SITE["max"]`, `["email"]`, `["legal"]`, review-site card links, `REVIEWS`) stay empty until the user
  supplies the data. Setting `max` or `email` makes new UI appear (a MAX button, an email row); mention that.
- If the user's request is ambiguous or the value is missing, ask before editing.

## Where things are (check with grep before editing)

| What | Where |
|---|---|
| Phone | `SITE["phone"]`, `["phone_href"]` (`+7...` digits), `["wa"]` (digits, no `+`): change all three together |
| Telegram / MAX / email | `SITE["tg"]`, `["max"]`, `["email"]` |
| Address, hours | `SITE["address"]`, `["hours_calls"]`, `["hours_office"]` (the map iframe uses the address) |
| Years / works / per month / warranty | `SITE["years"]`, `["works"]`, `["per_month"]`, `["warranty"]`; values like `"16+"` are split into a number and a suffix for the counter animation, so keep the digits-first form. These numbers are ALSO written inside strings: "15 лет" appears in many `data.py` strings and in the `build.py` home page description; "С 2010 года" and `© 2014–2026` are hardcoded in `build.py` |
| Calculator prices | `PRICES` (min, lamp, corner, canvas `m2`, profile `m`), read by `src/js/main.js` |
| Price cards on catalog pages | `CANVASES` (`p` per canvas); keep equal to `PRICES["canvas"][k]["m2"]` where they describe the same thing |
| Promotions | `PROMOS` tuples `(big text, title, description, css class)`; also mentioned in `MENU`, `WHY`, header promo in `build.py` ("Светильники в подарок!") and `FAQ` |
| FAQ | `FAQ` tuples `(question, answer)`; two columns are built by alternating items |
| City count | `GEO_CITIES` (e.g. "48+") must match the number of entries in `GEO` the user intends to show |

## Steps

1. `grep -rn "<old value>" data.py build.py src/js/main.js` to list every occurrence; decide with the user which to change.
2. Edit. Keep tuple/dict shapes. Fields `FEATURES`, `WHY`, `STEPS`, `CANVASES`, `SITE` are inserted without HTML escaping:
   write `&amp;` instead of `&`, no raw `<`/`>`.
3. `python3 build.py`.
4. Check: `git diff -- data.py build.py src` is only what was asked; `grep` the new value in `dist/` (e.g. `dist/index.html`,
   `dist/kontakty/index.html`) and the OLD value is gone from `dist/` everywhere it should be.
5. Report the old and new values side by side and where each was changed. Do not commit unless asked; use `release` for that.
