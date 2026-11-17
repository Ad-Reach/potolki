# CLAUDE.md

Static site for "Центр Плюс" (stretch ceilings, Moscow), domain centro-plus.ru.
`build.py` renders `data.py` (all content) + `src/` (CSS, JS, images) into `dist/`.
Site content is in Russian; keep it that way. Python stdlib only, no dependencies,
no tests, no linter. CI uses Python 3.12.

## Commands

```bash
python3 build.py                          # rebuild dist/ (wipes and recreates it)
python3 -m http.server -d dist            # preview at http://localhost:8000
git status --short dist                   # what the rebuild changed
```

Check that `dist/` matches the sources without touching the working tree
(this is exactly what CI does, minus the git part):

```bash
d=$(mktemp -d) && tar --exclude=.git -cf - . | tar -xf - -C "$d" \
  && python3 "$d/build.py" && diff -rq dist "$d/dist" && echo OK; rm -rf "$d"
```

## The one rule

After ANY change to `src/`, `data.py`, `build.py` or `geo_shapes.json`:
run `python3 build.py` and put `dist/` in the SAME commit as the sources.
CI (`.github/workflows/ci.yml`) rebuilds and fails if `git diff dist` is not empty.
Never edit `dist/` by hand: `build.py` deletes it and copies `src/` over it on every run.

Note: the `?v=` cache-buster on CSS/JS is an md5 of `style.css`, `main.js` and `data.py`.
Any `data.py` edit therefore changes every HTML file in `dist/`. That is expected.

## Deploy and the infra repo

- Push to `main` -> Timeweb App Platform serves `dist/` as is, without building.
- App settings live in a separate repo, `Ad-Reach/infra` (Terraform, `terraform/apps.tf`,
  resource `restapi_object.potolki`): repo `Ad-Reach/potolki`, branch `main`, `index_dir=/dist`,
  auto-deploy on push. Its `build_cmd` is `test -f dist/index.html || (install python3 && python3 build.py)`,
  i.e. a fallback build that only runs when `dist/index.html` is missing.
- So: keep `dist/` committed, keep it at `dist/` with `index.html` at its root, and never
  rename the output directory. Branch, domains, plan and build command are changed in
  `Ad-Reach/infra`, not here. DNS for centro-plus.ru is set by hand at reg.ru (see infra README).
- Work on the branch you were assigned; do not push to `main` unless asked.
  Commit messages in this repo are in Russian; follow that.

## Layout

- `data.py` - every piece of content (see below). `build.py` - HTML templates as f-strings.
- `src/css/style.css`, `src/js/main.js` - plain CSS/JS, copied to `dist/css`, `dist/js`.
- `src/img/p/` - photos as WebP. Each photo `NNNN.webp` has a thumbnail `NNNN-s.webp`.
  Code refers to photos by ID only: `img("4576")` -> `/img/p/4576.webp`, `img("4576", True)` -> `-s.webp`.
  A new photo needs BOTH files. Hero slides are `h01`..`h10`.
- `geo_shapes.json` - map outlines (Moscow region) read by `build.py` for the "География работ" block.
- `dist/` - generated output, committed.
- Pages: `/`, `/katalog/`, `/katalog/<slug>/` (one per `TYPES` item), `/raboty/`, `/akcii/`,
  `/o-kompanii/`, `/kontakty/`, `/stati/`, `/stati/<slug>/` (one per `ARTICLES` item),
  `/politika/`, `/404.html`. Internal links are root-relative and pages end with `/`.

## data.py map

- `SITE` - phone (`phone`, `phone_href`, `wa` must always be changed together), `tg`, address,
  hours, `years`/`works`/`per_month`/`warranty`, review-site links, `hero_interval_ms`.
- `PRICES` - calculator inputs, passed to `main.js` as `window.SITE.prices`.
- `CANVASES` - price cards on catalog pages. Canvas price exists twice: `PRICES["canvas"][k]["m2"]`
  and `CANVASES[i]["p"]`; keep them consistent.
- `TYPES` - one dict per catalog page (slug, name, short, canvas, profile, card, photos, intro, points, adv).
- `MENU`, `FEATURES`, `WHY`, `STEPS`, `PROJECTS`, `MARQUEE`, `HERO`, `WORKS_EXTRA`, `FAQ`, `PROMOS`
  - blocks of the home page and shared sections. Several are tuples; keep the tuple shape.
- `ARTICLES` - dicts with `slug`, `img`, `title`, `sub`, `body`; `body` is a list of `(tag, value)`:
  `("p", text)`, `("h2", text)`, `("ul", [items])`.
- `GEO`, `GEO_CITIES` - cities on the map. `MO_OUTLINE` is defined but not used anywhere.
  `REVIEWS` is empty and not used by `build.py` (reviews are links to Yandex/2GIS/Avito).

## Content and style conventions

- Russian copy: «ёлочки» quotes, long dash with spaces ` — `, `ё` spelled out, `₽`, `м²`.
  Phone format `+7 (965) 384-21-64`.
- Most text goes through `html.escape`, but NOT: `FEATURES`, `WHY`, `STEPS`, `CANVASES`, `SITE` values.
  Do not put `&`, `<`, `>` there without escaping (`&amp;` etc.).
- Some facts are hardcoded in `build.py`, not read from `data.py`: page titles and meta descriptions,
  `© 2014–2026`, "С 2010 года", "гарантия 15 лет" in the home description, header/footer menus,
  the fixed URL list for static pages in `main()` (sitemap). `TYPES` and `ARTICLES` pages get into
  the sitemap automatically. "15 лет" also appears in many strings of `data.py`.
  Before changing a number or contact, `grep` for the old value in `data.py`, `build.py` and `src/js/main.js`.
- Every page needs a unique `<title>`, meta description (<=160 chars), canonical and og tags;
  `page()` generates them from the arguments. Images need `alt`; decorative ones use `alt=""`.
- Mobile breakpoints in CSS: 1180px and 720px. Respect `prefers-reduced-motion`.
- Forms have no backend: `main.js` opens `wa.me/<SITE.wa>?text=...`. Do not add trackers, secrets
  or third-party form services without being asked.

## Do not touch / do not invent

- Do not hand-edit `dist/`. Do not change site code (`build.py`, `src/css`, `src/js`) unless the task asks for it.
- PRICES and CANVASES are placeholder (draft) numbers, as the comment in `data.py` says. Leave them as they are.
  Change a price only to a value the user gave you; never copy numbers from other sites
  (the draft ones came from rumexpert.ru) and never guess.
- Unfilled fields are waiting for data from the owner: `SITE["max"]`, `["email"]`, `["legal"]`,
  direct Yandex/2GIS card links, real reviews. Leave empty; do not fabricate.
- Do not invent business facts (warranty terms, years, addresses, certificates, prices, promo conditions).
  If a fact is not in the repo or the user's message, ask.
- Do not add or delete photos in `src/img/p/` unless asked; check that an ID exists before using it.

## Verifying a change

No automated tests. Run `python3 build.py`, check `git diff --stat dist` shows only what you expect,
open the affected pages through `http.server`, and (for layout work) check widths 375, 768 and 1280.
For a second opinion use the `reviewer` agent; to find where something lives use `explorer`.
Project skills: `add-article`, `update-content`, `release` (see `.claude/skills/`).
