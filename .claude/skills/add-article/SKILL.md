---
name: add-article
description: Add a new article to the "Статьи" section of the Центр Плюс site (entry in ARTICLES in data.py, rebuild, verify). Use when asked to publish, add or write a new article/blog post.
allowed-tools: Read, Grep, Glob, Edit, Bash(python3 build.py), Bash(git status:*), Bash(git diff:*)
---

# Add an article

An article is one dict in `ARTICLES` in `data.py`. `build.py` then creates `/stati/<slug>/`, adds it to
`/stati/`, to the "Полезные статьи" blocks and to `sitemap.xml` automatically. No template change is needed.

## Inputs (ask if missing, do not invent)

- Title and the article text, or a topic plus the facts to use. Do not make up business facts
  (warranty terms, prices, norms, standards, years, certificates). Use only what the user gave you,
  what is already in `data.py`, or generic non-numeric statements. Ask when a fact is needed and absent.
- Photo ID. Pick an existing ID from `src/img/p/` that has both `NNNN.webp` and `NNNN-s.webp`
  (`ls src/img/p | grep -c`; `ls src/img/p/NNNN*`). Prefer the ID the user names; do not add new image files.

## Steps

1. Read the existing `ARTICLES` entries in `data.py` to match tone and structure.
2. Add a dict at the END of `ARTICLES` (the order of the list is the display order; ask the user if they want it first):
   ```python
   {"slug": "latin-kebab-case", "img": "4620", "title": "...", "sub": "...",
    "body": [("p", "..."), ("h2", "..."), ("p", "..."), ("ul", ["...", "..."])]},
   ```
   - `slug`: lowercase latin transliteration, hyphens, unique among articles and not clashing with other `/stati/` paths.
   - `title`: shown as H1 and `<title>` (`<title> — Центр Плюс` is appended). Keep it short enough for a search snippet (~60 chars).
   - `sub`: becomes the meta description and the card text. One or two sentences, <=160 characters.
   - `body`: tuples `("p", text)`, `("h2", text)`, `("ul", [items])`. Text is HTML-escaped, so write plain text, no tags.
     Start with a `p`, no `h1`. Russian typography: «ёлочки», ` — `, `ё`.
3. Run `python3 build.py`.
4. Verify: `git status --short` shows `data.py` plus `dist/` changes only; `dist/stati/<slug>/index.html` exists;
   `grep -c "<slug>" dist/sitemap.xml` is 1; the new `<title>` and meta description are right.
   Remember that every `data.py` edit changes the `?v=` hash, so all HTML files in `dist/` change; that is expected.
5. Report what was added and the preview command (`python3 -m http.server -d dist`, then `/stati/<slug>/`).
   Do not commit unless asked; if asked, use the `release` skill so `dist/` goes into the same commit.
