---
name: release
description: Prepare a release of the Центр Плюс site - rebuild dist/, verify it matches the sources, and commit sources and dist/ together. Run only when the user explicitly asks to release, commit or ship changes.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(python3 build.py), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(ls:*), Bash(test:*), Bash(mktemp:*), Bash(tar:*), Bash(diff:*), Bash(rm -rf /tmp/*)
---

# Release

Deploy model: pushing to `main` makes Timeweb App Platform serve the committed `dist/` as is, with no build.
CI fails if `dist/` differs from a fresh build. So `dist/` must be rebuilt and committed together with the sources.
(App settings are in the `Ad-Reach/infra` repo; nothing to do there for a content release.)

## Steps

1. `git status --short` and `git branch --show-current`. Know what is changed and where you are.
   If there is nothing to release, say so and stop.
2. `python3 build.py`. It must print `built N pages`. Any traceback: stop and report it.
3. Verify:
   - `test -f dist/index.html` and `test -f dist/sitemap.xml`.
   - `git status --short`: every changed source has matching `dist/` changes, and no unrelated files
     (scratch files, `__pycache__`) are about to be added.
   - `git diff --stat -- dist | tail -5`: the dist change is plausible for the source change.
     Reminder: any `data.py`, `style.css` or `main.js` edit changes the `?v=` hash in all HTML files.
   - Optional but recommended: run the `reviewer` agent on the diff and read its blocking findings.
4. Show the user the summary: files changed, dist files changed, reviewer result.
5. Commit: `git add` the specific changed sources plus `dist/` (`git add -A dist`), then commit with a short
   Russian message describing the change (match the history, e.g. "Главная: новый блок ..."), in ONE commit.
   Follow any commit-trailer rules from the session instructions.
6. Push only to the branch you were assigned for this session (`git push -u origin <branch>`).
   Never push to `main` unless the user explicitly says so in this conversation. Do not open a pull request unless asked.
7. Final report: commit hash, branch, whether CI-equivalent check passed. If the user pushed to `main`,
   tell them the live site updates after App Platform picks up the push.
