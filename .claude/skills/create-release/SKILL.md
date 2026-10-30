---
name: create-release
description: Prepare a bu1ld0r release — bump the version, check the docs, compile, smoke-test, write release notes; the tag push makes CI build and publish it
---

# Release Skill

When the user invokes this skill (e.g. "do a release", "prep a release", "release skill"), execute the following steps **in order**. Do not skip steps. Do not batch steps that require user input.

(Adapted from grymmjack/neon-caster's create-release skill, itself from grymmjack/DRAW's.)

---

## Step 1 — Determine version bump

Ask the user:

> "Is this a **major**, **minor**, or **patch** release?"
> (major = breaking/large new features, minor = new features, patch = bug fixes / polish)

Parse the current version from `CORE/APP.BI`:

```
CONST APP_VERSION$ = "X.Y.Z"
```

Compute the new version:

- **major** → `(X+1).0.0`
- **minor** → `X.(Y+1).0`
- **patch** → `X.Y.(Z+1)`

If no `v*` tag exists yet, also offer releasing the current version as it is (the first release).

Show the user: `Current: X.Y.Z → New: A.B.C` and confirm before proceeding.

---

## Step 2 — Collect changes

Run:

```bash
git log --oneline --no-merges $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD
```

If no tags exist, compare against the very first commit (and include that commit's own work).

Also check **merged pull requests** since the last tag:

```bash
gh pr list --repo grymmjack/bu1ld0r --state merged --limit 20 --json number,title,body,mergedAt,headRefName --jq '.[] | "PR #\(.number): \(.title) | Branch: \(.headRefName) | Merged: \(.mergedAt[0:10])\n\(.body)\n---"'
```

Filter to PRs merged **after** the last tag date (`git log --format="%ci" -1 <tag>`).

Also run `git status --short`: Rick often has a lot of **uncommitted and untracked** work (new `.BI`/`.BM` files). Review it and the **current conversation history** for features and fixes not yet in the log.

Produce a deduplicated, categorised list of changes:

- **New Features** — new shapes, tools, modes, panel buttons, keys, export options
- **Improvements** — refinements to existing features, speed, the UI, the docs
- **Bug Fixes** — defects corrected
- **Internal / Refactoring** — code structure, tests, CI (not user-facing)
- **Breaking Changes** — anything that changes `.bld` files (models, prefabs), `bu1ld0r.cfg` keys, the export's files, or default keys

---

## Step 3 — Update the version in `CORE/APP.BI`

Replace `CONST APP_VERSION$ = "X.Y.Z"` with `CONST APP_VERSION$ = "A.B.C"`. (It shows at the top right of the window.)

---

## Step 4 — Update `README.md`

Review `README.md` against the change list from Step 2:

- The opening feature paragraphs (add new features, update changed ones, remove removed ones).
- **Workflows**: a new tool or mode may want its own short section.
- **Keys**: regenerate it from the in-program HELP — `python3 tools/readme_keys.py --write` (it replaces what's between `<!-- keys:start -->` and `<!-- keys:end -->`). If HELP doesn't mention a new key, add it to HELP (`HelpAdd` in `UI/UI.BM`) first.
- **In detail**: the bullet for each changed feature; cfg keys (`name=` in bu1ld0r.cfg) that were added or removed.
- **Command line**, if arguments changed.
- The screenshots in `docs/screenshots/` if the program has visibly changed a lot (note only — do not retake automatically).
- Do not rewrite sections that are still accurate.

Also check `PLAN.md`: mark finished stages done, if any.

---

## Step 5 — Compile verification

```bash
~/git/qb64pe/qb64pe -w -x bu1ld0r.bas -o bu1ld0r.test.run 2>&1 | grep -E 'Output:|in use|LINE|Caused|rror'
```

Confirm `Output: .../bu1ld0r.test.run` appears and nothing else (QB64PE reports most mistakes as `Name already in use` plus a `LINE nnnn:`). CI builds with the QB64-PE commit pinned as `QB64PE_REF` in `.github/workflows/build-release.yml`; if the local `~/git/qb64pe` has moved on (`git -C ~/git/qb64pe rev-parse HEAD`), say so and ask whether to update the pin. Report any errors and fix before continuing. Then `mv bu1ld0r.test.run bu1ld0r.run`.

---

## Step 6 — Smoke test, as CI does

From a clean copy (never the repo's own folder: Rick may have bu1ld0r running from it, and the test writes `export/`), never on Rick's display:

```bash
P=/tmp/claude-1000/bu1ld0r-rel; rm -rf $P; mkdir -p $P/bu1ld0r/prefabs
cp bu1ld0r.run $P/bu1ld0r/ && cp -r prefabs/starter $P/bu1ld0r/prefabs/
cd $P/bu1ld0r && env -u WAYLAND_DISPLAY -u DBUS_SESSION_BUS_ADDRESS QT_QPA_PLATFORM=xcb \
  timeout -k 5 60 xvfb-run -a -s "-screen 0 1920x1080x24" ./bu1ld0r.run \
  prefabs/starter/lamp.bld --export --shot "$PWD/smoke.png" --quit; echo "exit $?"
```

It must exit 0 and leave `smoke.png` (look at it) and a non-empty `export/lamp.obj`. Then check nothing is left running (`ps -eo pid,etime,args | grep -E 'bu1ld0r|Xvfb'`) — stop only test copies, never `/home/grymmjack/git/bu1ld0r/bu1ld0r.run`.

---

## Step 7 — Output release notes in chat

Print the following markdown block in chat so the user can copy it to the GitHub release:

---

```markdown
## bu1ld0r vA.B.C

> Released YYYY-MM-DD

### New Features

- ...

### Improvements

- ...

### Bug Fixes

- ...

### Breaking Changes

- ...

```

---

## Step 8 — Tell the user how it ships

Releases are built by GitHub Actions, not by hand. The download is built from **what's in git**, so list exactly what must be committed: new untracked source files (`git status --short | grep '^??'`), and the data that ships (`prefabs/starter/`; anything else in `prefabs/`, `pictures/` or `models/` only if the user wants it in every download — ask). Tell the user the commands (do not run them), e.g.:

```bash
git add -A CORE MODEL VIEW UI OUT tools docs .github .claude/skills prefabs/starter \
  _ALL.BI _ALL.BM bu1ld0r.bas README.md PLAN.md CLAUDE.md .gitignore
git commit -m "bu1ld0r vA.B.C"
git tag -a vA.B.C -m "bu1ld0r vA.B.C"
git push && git push origin vA.B.C
```

Pushing the `vA.B.C` tag runs `.github/workflows/build-release.yml`: it builds Windows, macOS (Apple silicon) and Linux, smoke-tests Linux (opens the starter lamp, exports it), and publishes the release with the three downloads. Once it's up, the notes from Step 7 can go on top of the generated ones:

```bash
gh release edit vA.B.C --notes-file notes.md
```

To try the builds without releasing: Actions tab → Build bu1ld0r → Run workflow (leave "Create a GitHub release" off), after pushing the commit.

---

## Rules

- **Always ask** before applying a version bump (Step 1). Never assume.
- **Never auto-commit, tag or push**. The user commits and tags; the tag push publishes the release.
- If a step produces no changes (e.g. README is already accurate), state that explicitly and move on.
- If the git log is empty (no commits since last tag), say so and rely on `git status` and the conversation history for the change list.
- Keep release notes **user-facing**: omit internal refactors unless they affect users (`.bld` format changes, cfg renames, etc.).
- Date in release notes should be today's date in `YYYY-MM-DD` format.
