# UNITED Nights website

Static site for unitednights.com, replacing Squarespace.

- `index.html`: UNITED: The Story (history page). Self-contained: styles, scripts and images are inlined; fonts load from Google Fonts.
- No build step. Any static host serves this folder as-is.

Status: draft, not yet deployed or connected to a domain. Changes go through a pull request reviewed by Jason before merge.

## Site structure (rebuild of the Squarespace site)

- `/` home, `/stories` and each story, `/contact`, `/legal-disclaimer`, `/privacy`, `/history` (UNITED: The Story).
- Same URLs as Squarespace, so existing links keep working. `/contact-2` (unused demo page) and `/home` redirect.
- history.unitednights.com redirects `/` to `/history` (see `vercel.json`). A rewrite cannot do this: Vercel serves the root index.html before it applies rewrites.
- To edit text: change the file in `content/`, run `python3 build.py`, commit the result. A new story is a new file in `content/stories/` plus its name in `POSTS` in `build.py`.
- Forms: post to the Hub (lmm-hub `/api/united/website-form`): each submission becomes a UNITED contact in the Hub, mirrors to the UNITED Google Sheet and emails hello@unitednights.com. `FORM_ENDPOINT` in `assets/site.js` stays empty, so forms send nothing, until lmm-hub PR #106 is merged and live.
- Font: Aktiv Grotesk loads from Luke's Adobe Fonts web project (`ADOBE_KIT` in `build.py`). Never add font files to this public repo.
- Images still load from Squarespace's image server; copy them into this repo before Squarespace is cancelled.
