# UNITED Nights website

Static site for unitednights.com, replacing Squarespace.

- `index.html`: UNITED: The Story (history page). Self-contained: styles, scripts and images are inlined; fonts load from Google Fonts.
- No build step. Any static host serves this folder as-is.

Status: draft, not yet deployed or connected to a domain. Changes go through a pull request reviewed by Jason before merge.

## Site structure (rebuild of the Squarespace site)

- `/` home, `/stories` and each story, `/contact`, `/legal-disclaimer`, `/privacy`, `/history` (UNITED: The Story).
- Same URLs as Squarespace, so existing links keep working. `/contact-2` (unused demo page) and `/home` redirect.
- history.unitednights.com shows `/history` (see `vercel.json`).
- To edit text: change the file in `content/`, run `python3 build.py`, commit the result. A new story is a new file in `content/stories/` plus its name in `POSTS` in `build.py`.
- Forms: `FORM_ENDPOINT` in `assets/site.js` is empty until Luke chooses where submissions go, so the forms currently send nothing.
- Images still load from Squarespace's image server; copy them into this repo before Squarespace is cancelled.
