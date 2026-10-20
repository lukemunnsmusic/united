#!/usr/bin/env python3
"""Builds the UNITED Nights site into plain static HTML.

Edit text in content/, then run:  python3 build.py
Output folders (index.html in each) are committed and served as-is by Vercel.
No build step runs on Vercel; nothing outside the standard library is needed.

Content markup (one paragraph per blank-line block):
  ## HEADING              section heading
  > quote                 blockquote
  - item                  bullet (consecutive lines form one list)
  [video:YOUTUBE_ID]      embedded YouTube video
  [img:URL|alt text]      image
  [text](url)             link inside a paragraph
"""
import html, re, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
SITE = "https://unitednights.com"
CDN = "https://images.squarespace-cdn.com/content/v1/6a6464a7513b006c5a13f402"
LOGO = CDN + "/d2a214ac-598d-423f-b146-5b4c921c97a2/UNITED-Nights-logo-wht.png"
OG_DEFAULT = "https://static1.squarespace.com/static/6a6464a7513b006c5a13f402/t/6a8668b331e02f46bf595841/1787193523022/united-nights-facebook.jpg?format=1500w"
IG = "https://instagram.com/unitednights.co"
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Libre+Franklin:wght@400;500;700&family=Michroma&display=swap"

NAV = [("HOME", "/"), ("STORIES", "/stories"), ("HISTORY", "/history"), ("CONTACT", "/contact")]
IG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

e = html.escape


def inline(s):
    s = e(s, quote=False)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)


def page(path, title, body, desc="", og=OG_DEFAULT, extra_head=""):
    nav = "".join(
        f'<a href="{href}"{" aria-current=page" if (href == path or (href != "/" and path.startswith(href + "/"))) else ""}>{label}</a>'
        for label, href in NAV)
    url = SITE + (path if path != "/" else "")
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(og)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#060607">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/site.css">{extra_head}
</head>
<body>
<header class="site-head gut">
  <div class="w">
    <a class="brand" href="/" aria-label="UNITED Nights home"><img src="{LOGO}" alt="UNITED Nights" width="160" height="30"></a>
    <button class="burger" aria-label="Menu" aria-expanded="false">{BURGER}</button>
    <nav class="menu" aria-label="Site">{nav}<a class="ig" href="{IG}" aria-label="Instagram" rel="noopener">{IG_SVG}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-foot gut">
  <div class="w">
    <p>&copy; {datetime.date.today().year} UNITED Nights. All rights reserved.</p>
    <p>UNITED Nights is an independent project led by Luke Munns, signed to WorshipCollective.co. It is not affiliated with Hillsong.</p>
    <nav aria-label="Footer"><a href="/privacy">Privacy</a><span>|</span><a href="/legal-disclaimer">Legal</a><span>|</span><a href="/contact">Contact</a><span>|</span><a href="{IG}" rel="noopener">Instagram</a></nav>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    if path == "/404":
        out = ROOT / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print("built", out.relative_to(ROOT))


def read(name):
    raw = (ROOT / "content" / name).read_text()
    head, _, body = raw.partition("\n---\n")
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    return meta, body.strip()


def blocks(body):
    out, items = [], []
    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for b in re.split(r"\n\s*\n", body):
        b = b.strip()
        lines = b.splitlines()
        if all(l.startswith("- ") for l in lines):
            items.extend(l[2:] for l in lines); continue
        flush()
        if b.startswith("## "):
            out.append(f"<h3>{inline(b[3:])}</h3>")
        elif b.startswith("> "):
            out.append(f"<blockquote>{inline(b[2:])}</blockquote>")
        elif m := re.fullmatch(r"\[video:([\w-]+)\]", b):
            vid = m.group(1)
            out.append(f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="Video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
        elif m := re.fullmatch(r"\[img:([^|\]]+)\|?([^\]]*)\]", b):
            out.append(f'<figure><img src="{m.group(1)}?format=1500w" alt="{e(m.group(2))}" loading="lazy"></figure>')
        else:
            out.append(f"<p>{inline(b)}</p>")
    flush()
    return "\n".join(out)


def nice_date(d):
    return datetime.date.fromisoformat(d).strftime("%-d %B %Y")


def lead_form(kind, button, thanks, message=False):
    extra = """
      <div class="field"><label for="f-subject">Subject (required)</label><input id="f-subject" name="subject" required></div>
      <div class="field"><label for="f-message">Message (required)</label><textarea id="f-message" name="message" required></textarea></div>""" if message else ""
    return f"""<form class="lead" data-form="{kind}" data-thanks="{e(thanks)}" novalidate>
      <div class="row2">
        <div class="field"><label for="f-first">First name (required)</label><input id="f-first" name="first_name" autocomplete="given-name" required></div>
        <div class="field"><label for="f-last">Last name (required)</label><input id="f-last" name="last_name" autocomplete="family-name" required></div>
      </div>
      <div class="field"><label for="f-email">Email (required)</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>{extra}
      <label class="check"><input type="checkbox" name="updates" value="yes"{" checked" if kind == "signup" else ""}> Sign up for news and updates</label>
      <div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn solid" type="submit">{button}</button>
      <p class="form-note" role="status" aria-live="polite"></p>
    </form>"""


# ---------- pages ----------

def home():
    body = f"""<section class="hero gut">
  <div class="bg" aria-hidden="true"><iframe src="https://www.youtube-nocookie.com/embed/hqK0pqV-c9c?autoplay=1&mute=1&loop=1&playlist=hqK0pqV-c9c&controls=0&playsinline=1&modestbranding=1&rel=0" title="" tabindex="-1" allow="autoplay; encrypted-media"></iframe></div>
  <div class="w inner">
    <img class="logo rv" src="{LOGO}?format=1500w" alt="UNITED Nights" width="560" height="105">
    <h1 class="rv">A new chapter. A new beginning. A new sound.</h1>
  </div>
</section>
<section class="gut" style="padding-block:clamp(80px,14vh,150px)">
  <div class="narrow stack" style="text-align:center">
    <p class="rv">For many of us, the UNITED story began with young people gathering - powerful prayer meetings, loud and passionate praise, intimate moments of worship - hands raised and hearts abandoned.</p>
    <p class="rv">A generation hungry and desperate for the tangible presence of God, lifting up the name of Jesus with one heart, one voice and one sound.</p>
    <p class="ring rv">THE SOUND OF FREEDOM.<br>THE SOUND OF CHAINS FALLING.<br>THE SOUND OF REVIVAL.</p>
    <p class="rv"><strong style="color:var(--paper)">In 2027, a new and independent chapter begins.</strong></p>
    <p class="rv">UNITED Nights is a new gathering of worshippers, songwriters, musicians and creatives seeking God and making space for encounters with His presence.</p>
    <p class="rv">We are not trying to recreate yesterday. We honour what God has done in the past, but we are looking forward to the future - a clean slate, new wine and a fresh outpouring of the Holy Spirit.</p>
    <p class="rv">We are simply making room for whatever God wants to do next.</p>
    <p class="ring rv">JOIN US ON THE JOURNEY.<br>COME WITH US ON A NEW ADVENTURE.</p>
  </div>
</section>
<section class="join gut" id="join">
  <div class="ph" style="background-image:url('{CDN}/7e289948-8475-493e-90b6-b7a68c406ac9/united-form-bg.jpg?format=2500w')"></div>
  <div class="w">
    <div class="head"><h2 class="rv">The journey is just beginning</h2><p class="rv">Receive occasional updates about new music, gatherings and what comes next.</p></div>
    {lead_form("signup", "Join the journey", "Thank you. You're on the journey with us.")}
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

    cards = "".join(f"""
    <a class="card rv" href="/stories/{slug}">
      <div class="img"><img src="{m['image']}?format=1000w" alt="" loading="lazy"></div>
      <div class="meta">{e(m['author'])} &middot; {nice_date(m['date'])}</div>
      <h2>{e(m['title'])}</h2>
      <p>{e(m['excerpt'])}</p>
      <span class="more">Read more</span>
    </a>""" for slug, m, _ in posts)
    page("/stories", "STORIES — UNITED Nights", f"""<section class="post-head gut"><div class="w"><span class="label"><b>&#9679;</b>&nbsp; United stories</span><h1 style="margin-top:14px">Stories</h1><p style="margin-top:14px">Stories from where we've been, what we're building now, and what's ahead.</p></div></section>
<section class="gut"><div class="w cards">{cards}
</div></section>""", "Stories from where we've been, what we're building now, and what's ahead.",
         og="https://static1.squarespace.com/static/6a6464a7513b006c5a13f402/t/6a8507b3762f55650d9e2518/1787103155141/UNITED-stories.jpg?format=1500w")

    for i, (slug, m, body) in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = ""
        if older:
            nav += f'<a class="prev" href="/stories/{older[0]}"><span class="dir">Previous</span><span class="t">{e(older[1]["title"])}</span></a>'
        if newer:
            nav += f'<a class="next" href="/stories/{newer[0]}"><span class="dir">Next</span><span class="t">{e(newer[1]["title"])}</span></a>'
        page(f"/stories/{slug}", f"{m['title']} — UNITED Nights", f"""<article class="gut">
  <header class="narrow post-head">
    <div class="meta"><a href="/stories" style="text-decoration:none">Stories</a> &middot; {e(m['author'])} &middot; {nice_date(m['date'])}</div>
    <h1>{e(m['title'])}</h1>
    <p class="sub">{e(m['subtitle'])}</p>
  </header>
  <div class="narrow prose">
{blocks(body)}
  </div>
  <div class="narrow postnav">
    <h3 style="font-size:20px">United stories</h3>
    <p>Stories from where we've been, what we're building now, and what's ahead.</p>
    <div class="row">{nav}</div>
  </div>
</article>""", m["excerpt"], og=m["image"] + "?format=1500w")


def contact():
    body = f"""<section class="banner gut">
  <div class="ph" style="background-image:url('{CDN}/2f6517ce-938d-4263-bf4a-95d4ec717ff0/united-contact-banner.jpg?format=2500w')"></div>
  <div class="w inner"><h1 class="rv">Contact</h1><p class="sub rv">Bookings, partnerships, collaborations + enquiries</p></div>
</section>
<section class="gut" style="padding-block:clamp(70px,12vh,130px)">
  <div class="w">
    <div class="head" style="text-align:center;margin-bottom:34px"><h2 class="rv">The next chapter starts<br>with a conversation.</h2></div>
    {lead_form("contact", "Submit", "Thank you. We've received your message and will be in touch.", message=True)}
  </div>
</section>"""
    page("/contact", "CONTACT — UNITED Nights", body, "Bookings, partnerships, collaborations and enquiries for UNITED Nights.")


def doc(slug, desc):
    meta, body = read(f"{slug}.txt")
    eff = f'<p class="eff">{e(meta["effective"])}</p>' if "effective" in meta else ""
    html_body = blocks(body).replace("<h3>", "<h2>").replace("</h3>", "</h2>")
    page(f"/{slug}", f"{meta['title']} — UNITED Nights", f"""<article class="gut doc"><div class="narrow">
  <h1>{e(meta['title'])}</h1>{eff}
{html_body}
</div></article>""", desc)


def notfound():
    page("/404", "Page not found — UNITED Nights", """<section class="gut doc"><div class="narrow" style="text-align:center;display:grid;gap:22px;justify-items:center">
  <h1>Page not found</h1><p>That page has moved or no longer exists.</p><a class="btn solid" href="/">Back to home</a>
</div></section>""", "Page not found.")


if __name__ == "__main__":
    home(); stories(); contact()
    doc("legal-disclaimer", "Legal information and disclaimer for UNITED Nights.")
    doc("privacy", "How UNITED Nights collects, uses and protects personal information.")
    notfound()
