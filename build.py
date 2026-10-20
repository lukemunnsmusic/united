#!/usr/bin/env python3
"""Builds the UNITED Nights site into plain static HTML.

The look matches the live Squarespace site exactly. Do not restyle without Luke's sign-off.

Edit text in content/, then run:  python3 build.py
Output folders (index.html in each) are committed and served as-is by Vercel.
No build step runs on Vercel; nothing outside the standard library is needed.

Content markup (one paragraph per blank-line block):
  ## HEADING              section heading
  > quote                 quote (indented, italic)
  - item                  bullet (consecutive lines form one list)
  [video:YOUTUBE_ID]      embedded YouTube video
  [img:URL|alt text]      image
  **bold**                bold text inside a paragraph
  [text](url)             link inside a paragraph
"""
import html, re, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
SITE = "https://unitednights.com"
CDN = "https://images.squarespace-cdn.com/content/v1/6a6464a7513b006c5a13f402"
HEAD_LOGO = CDN + "/3a0d35ff-cf40-4f06-9450-b90b574a8301/UNITED-Nights-Logo.png?format=1500w"
HERO_LOGO = CDN + "/d2a214ac-598d-423f-b146-5b4c921c97a2/UNITED-Nights-logo-wht.png?format=2500w"
FOOT_LOGO = CDN + "/5ed91b64-1ef2-4ad3-8be6-96c09ab66241/UNITED-Nights-logo-wht.png?format=500w"
LM_LOGO = CDN + "/2416aef0-200d-46e7-bf0f-f6e0e8497199/LUKE-MUNNS-LOGO-footer.png?format=750w"
OG_DEFAULT = "https://static1.squarespace.com/static/6a6464a7513b006c5a13f402/t/6a8668b331e02f46bf595841/1787193523022/united-nights-facebook.jpg?format=1500w"
IG = "https://instagram.com/unitednights.co"
# Aktiv Grotesk (Adobe Fonts). Set ADOBE_KIT to the kit id from Luke's own Adobe Fonts web project;
# until then the browser falls back to Helvetica Neue / Arial.
ADOBE_KIT = ""

NAV = [("HOME", "/"), ("STORIES", "/stories"), ("CONTACT", "/contact")]
IG_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>'
CARET_L = '<svg viewBox="0 0 9 16" aria-hidden="true"><polyline points="7.3,14.7 2.5,8 7.3,1.2"/></svg>'
CARET_R = '<svg viewBox="0 0 9 16" aria-hidden="true"><polyline points="1.6,1.2 6.5,7.9 1.6,14.7"/></svg>'

e = html.escape


def inline(s):
    s = e(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)


def page(path, title, body, desc="", og=OG_DEFAULT, theme=""):
    nav = "".join(
        f'<a href="{href}"{" aria-current=page" if (href == path or (href != "/" and path.startswith(href + "/"))) else ""}>{label}</a>'
        for label, href in NAV)
    mnav = "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    url = SITE + (path if path != "/" else "")
    font = f'\n<link rel="stylesheet" href="https://use.typekit.net/{ADOBE_KIT}.css">' if ADOBE_KIT else ""
    doc = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="UNITED Nights">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(og)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">{font}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body class="{theme}">
<header class="site-head">
  <div class="row">
    <a class="logo" href="/" aria-label="UNITED Nights home"><img src="{HEAD_LOGO}" alt="UNITED Nights" width="210" height="42"></a>
    <nav aria-label="Site">{nav}<a class="ig" href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{IG_SVG}</a></nav>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="menu-panel" aria-label="Menu">{mnav}<a class="ig" href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{IG_SVG}</a></div>
<main>
{body}
</main>
<footer class="site-foot">
  <img class="un" src="{FOOT_LOGO}" alt="UNITED Nights" width="216" height="43" loading="lazy">
  <div class="txt">
    <p>&copy; {datetime.date.today().year} UNITED Nights. All rights reserved.</p>
    <p>UNITED Nights is an independent project led by Luke Munns, signed to <a href="https://worshipcollective.co">WorshipCollective.co</a>. It is not affiliated with Hillsong.</p>
    <p class="links"><a href="/privacy">Privacy</a> | <a href="/legal-disclaimer">Legal</a> | <a href="/contact">Contact</a> | <a href="{IG}">Instagram</a></p>
  </div>
  <a class="lm" href="https://lukemunnsmusic.com/" aria-label="LUKE MUNNS"><img src="{LM_LOGO}" alt="LUKE MUNNS" width="330" height="29" loading="lazy"></a>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = ROOT / "404.html" if path == "/404" else (ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print("built", out.relative_to(ROOT))


def read(name):
    raw = (ROOT / "content" / name).read_text()
    head, _, body = raw.partition("\n---\n")
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    return meta, body.strip()


def blocks(body, heading="h3"):
    out, items = [], []
    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li><p>{inline(i)}</p></li>" for i in items) + "</ul>")
            items.clear()
    for b in re.split(r"\n\s*\n", body):
        b = b.strip()
        lines = b.splitlines()
        if all(l.startswith("- ") for l in lines):
            items.extend(l[2:] for l in lines); continue
        flush()
        if b.startswith("## "):
            out.append(f"<{heading}>{inline(b[3:])}</{heading}>")
        elif b.startswith("> "):
            out.append(f"<blockquote><p>{inline(b[2:])}</p></blockquote>")
        elif m := re.fullmatch(r"\[video:([\w-]+)\]", b):
            out.append(f'<div class="video"><iframe src="https://www.youtube.com/embed/{m.group(1)}?feature=oembed" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
        elif m := re.fullmatch(r"\[img:([^|\]]+)\|?([^\]]*)\]", b):
            out.append(f'<figure><img src="{m.group(1)}?format=1500w" alt="{e(m.group(2))}" loading="lazy"></figure>')
        else:
            out.append(f"<p>{inline(b)}</p>")
    flush()
    return "\n".join(out)


def short_date(d):  # Squarespace style: 22/8/26
    d = datetime.date.fromisoformat(d)
    return f"{d.day}/{d.month}/{d.strftime('%y')}"


def form(kind, button, thanks, message=False, dark=False):
    extra = """
    <div class="field"><label for="f-subject">SUBJECT<span class="req">(required)</span></label><input id="f-subject" type="text" name="subject" required></div>
    <div class="field"><label for="f-message">MESSAGE<span class="req">(required)</span></label><textarea id="f-message" name="message" required></textarea></div>""" if message else ""
    return f"""<form class="sq" data-form="{kind}" data-thanks="{e(thanks)}" novalidate>
    <fieldset>
      <legend>NAME</legend>
      <div class="two">
        <label><span class="sub">First Name <span class="req">(required)</span></span><input type="text" name="first_name" autocomplete="given-name" required></label>
        <label><span class="sub">Last Name <span class="req">(required)</span></span><input type="text" name="last_name" autocomplete="family-name" required></label>
      </div>
    </fieldset>
    <div class="field"><label for="f-email">EMAIL<span class="req">(required)</span></label><input id="f-email" type="email" name="email" autocomplete="email" required></div>
    <label class="check"><input type="checkbox" name="updates" value="Sign up for news and updates"> Sign up for news and updates</label>{extra}
    <div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
    <button class="btn" type="submit">{button}</button>
    <p class="form-note" role="status" aria-live="polite"></p>
  </form>"""


# ---------- pages ----------

def home():
    body = f"""<section class="bleed hero dark">
  <div class="media" aria-hidden="true"><iframe src="https://www.youtube.com/embed/hqK0pqV-c9c?autoplay=1&mute=1&loop=1&playlist=hqK0pqV-c9c&controls=0&playsinline=1&rel=0&disablekb=1&iv_load_policy=3&cc_load_policy=0" title="" tabindex="-1" allow="autoplay; encrypted-media"></iframe></div>
  <img class="logo-big" src="{HERO_LOGO}" alt="UNITED Nights" width="671" height="134">
</section>
<section class="intro"><div class="frame"><div class="col c-main">
  <h2><strong>A new chapter. A new BEGINNING. A new SOUND. </strong></h2>
  <p>For many of us, <strong>the UNITED story began with young people gathering</strong> - powerful prayer meetings, loud and passionate praise, intimate moments of worship - hands raised and hearts abandoned.</p>
  <p>A generation hungry and desperate for <strong>the tangible presence of God</strong>, lifting up the name of Jesus with one heart, one voice and one sound.</p>
  <p><strong>THE SOUND OF FREEDOM.</strong><br><strong>THE SOUND OF CHAINS FALLING.</strong><br><strong>THE SOUND OF REVIVAL.</strong></p>
  <p>In 2027, <strong>a new and independent chapter begins.</strong></p>
  <p><strong>UNITED Nights</strong> is a new gathering of worshippers, songwriters, musicians and creatives seeking God and making space for encounters with His presence.</p>
  <p>We are not trying to recreate yesterday. We honour what God has done in the past, but we are looking forward to the future - <strong>a clean slate, new wine and a fresh outpouring of the Holy Spirit.</strong></p>
  <p>We are simply making room for <strong>whatever God wants to do next.</strong></p>
  <p><strong>JOIN US ON THE JOURNEY.</strong></p>
  <p><strong>COME WITH US ON A NEW ADVENTURE.</strong></p>
</div></div></section>
<section class="bleed join dark">
  <div class="media" aria-hidden="true"><img src="{CDN}/7e289948-8475-493e-90b6-b7a68c406ac9/united-form-bg.jpg?format=2500w" alt="" loading="lazy"></div><div class="shade"></div>
  <div class="frame" style="width:100%">
    <div class="col c-wide" style="margin-bottom:31px"><p class="large"><strong>THE JOURNEY IS JUST BEGINNING</strong></p><p>Receive occasional updates about new music, gatherings and what comes next.</p></div>
    <div class="col c-form">{form("signup", "JOIN THE JOURNEY", "Thank you. You're on the journey with us.", dark=True)}</div>
  </div>
</section>"""
    page("/", "UNITED Nights | Worship Gatherings & New Music", body,
         "UNITED Nights is a new independent Christian worship gathering bringing together worshippers, songwriters, musicians and creatives to seek God and make room for His presence. A new chapter begins in 2027.")


POSTS = ["why-united-nights", "the-blessing-movement"]


def stories():
    posts = []
    for slug in POSTS:
        meta, body = read(f"stories/{slug}.txt")
        posts.append((slug, meta, body))
    posts.sort(key=lambda p: p[1]["date"], reverse=True)

    items = "".join(f"""
  <article class="story">
    <a class="img" href="/stories/{slug}"><img src="{m['image']}?format=1500w" alt="{e(m['title'])}" loading="lazy"></a>
    <div>
      <div class="meta"><time datetime="{m['date']}">{short_date(m['date'])}</time></div>
      <h1><a href="/stories/{slug}">{e(m['title'])}</a></h1>
      <p>{e(m['excerpt'])}</p>
      <a class="more" href="/stories/{slug}">Read More</a>
    </div>
  </article>""" for slug, m, _ in posts)
    page("/stories", "STORIES — UNITED Nights", f'<section class="stories"><div class="frame">{items}\n</div></section>', "",
         og="https://static1.squarespace.com/static/6a6464a7513b006c5a13f402/t/6a8507b3762f55650d9e2518/1787103155141/UNITED-stories.jpg?format=1500w",
         theme="light")

    for i, (slug, m, body) in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        # Squarespace convention: "Previous" (left) is the newer story, "Next" (right) the older one.
        nav = ""
        if newer:
            nav += f'<a class="prev" href="/stories/{newer[0]}">{CARET_L}<span><span class="hp">Previous</span><h2>{e(newer[1]["title"])}</h2></span></a>'
        if older:
            nav += f'<a class="next" href="/stories/{older[0]}"><span><span class="hp">Next</span><h2>{e(older[1]["title"])}</h2></span>{CARET_R}</a>'
        page(f"/stories/{slug}", f"{m['title']} — UNITED Nights", f"""<article class="post"><div class="inner">
  <h1 class="title">{e(m['title'])}</h1>
  <h4>{e(m['subtitle'])}</h4>
{blocks(body)}
  <h3>UNITED STORIES</h3>
  <p>Stories from where we've been, what we're building now, and what's ahead.</p>
</div></article>
<nav class="pager" aria-label="More stories"><div class="row">{nav}</div></nav>""", m["excerpt"], og=m["image"] + "?format=1500w", theme="light")


def contact():
    body = f"""<section class="bleed banner banner-contact dark">
  <div class="media" aria-hidden="true"><img src="{CDN}/2f6517ce-938d-4263-bf4a-95d4ec717ff0/united-contact-banner.jpg?format=2500w" alt=""></div><div class="shade"></div>
  <div class="frame" style="width:100%"><div class="col c-banner"><h1>CONTACT</h1><h3>Bookings, partnerships, <br>collaborations + enquiries</h3></div></div>
</section>
<section class="block"><div class="frame">
  <div class="col c-contact-head" style="margin-bottom:clamp(12px, calc(7.914px + 1.0476vw), 23px)"><h3>THE NEXT CHAPTER STARTS<br>WITH A CONVERSATION.</h3></div>
  <div class="col c-contact-form">{form("contact", "Submit", "Thank you. We've received your message and will be in touch.", message=True)}</div>
</div></section>"""
    page("/contact", "CONTACT — UNITED Nights", body, "")


def legal():
    meta, body = read("legal-disclaimer.txt")
    page("/legal-disclaimer", "LEGAL / DISCLAIMER — UNITED Nights", f"""<section class="bleed banner banner-legal dark">
  <div class="media" aria-hidden="true"><img src="{CDN}/86c8ff0c-b213-49d1-95cd-fdf4fd0a4370/united-nights-banner.jpg?format=2500w" alt=""></div><div class="shade"></div>
  <div class="frame" style="width:100%"><h2 style="margin-inline:var(--pad)">LEGAL / DISCLAIMER</h2></div>
</section>
<section class="block-legal"><div class="frame"><div class="col c-legal legal">
{blocks(body, heading="h4")}
</div></div></section>""", "")


def privacy():
    meta, body = read("privacy.txt")
    page("/privacy", "PRIVACY — UNITED Nights", f"""<section class="bleed banner banner-privacy">
  <div class="media" aria-hidden="true"><img src="{CDN}/9502a1d7-8e92-4ca3-b0ff-c946e85981db/united-privacy-policy.jpg?format=2500w" alt=""></div>
  <div class="frame" style="width:100%"><div class="col c-privacy-title"><h1>PRIVACY POLICY</h1></div></div>
</section>
<section class="block"><div class="frame"><div class="col c-centre legal">
<p><strong>{e(meta['effective'])}</strong></p>
{blocks(body, heading="h4")}
</div></div></section>""", "", theme="ink")


def notfound():
    page("/404", "Page Not Found — UNITED Nights", """<section class="post"><div class="inner">
  <h1 class="title">Page not found</h1>
  <p>We couldn't find the page you were looking for. <a href="/">Return home</a>.</p>
</div></section>""", "", theme="light")


if __name__ == "__main__":
    home(); stories(); contact(); legal(); privacy(); notfound()
