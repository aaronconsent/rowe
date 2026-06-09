#!/usr/bin/env python3
"""Build the Rowe site from a manifest. Static HTML in/out.

Run: python3 build.py
Writes pages into site/ at the slugs defined below.
"""
from pathlib import Path

SITE_DIR = Path(__file__).parent / "site"

# Bump this when CSS changes to force browsers to reload the stylesheet.
CSS_VERSION = "4"

# ---- Illustrations (vintage engraving — generated via Recraft API) -----------
# To regenerate or add new illustrations, see generate_illustrations.py.

def _img(name: str, alt: str = "") -> str:
    return f'<img src="/assets/img/{name}.svg" alt="{alt}" loading="lazy" decoding="async">'

SVGS = {
    "pine":     _img("pine",     "Longleaf pine, vintage engraving"),
    "hardwood": _img("hardwood", "Oak hardwood, vintage engraving"),
    "dozer":    _img("dozer",    "Bulldozer, vintage engraving"),
    "mulcher":  _img("mulcher",  "Forestry mulcher, vintage engraving"),
    "pond":     _img("pond",     "Farm pond with cattails, vintage engraving"),
    "lake":     _img("lake",     "Lake with dock, vintage engraving"),
    "road":     _img("road",     "Country road with pines, vintage engraving"),
    "compass":  _img("compass",  "Compass rose, vintage engraving"),
    "mark":     _img("mark",     "Rowe Land, Timber & Dozer pine emblem"),
}
ICON = lambda key: SVGS.get(key, "")


# ---- Shared chrome -----------------------------------------------------------

# noindex toggle for the dev domain. Flip DEV_NOINDEX to False on launch.
DEV_NOINDEX = True

CANONICAL_BASE = "https://www.rowelandtimber.com"
PHONE_DISPLAY = "(936) 239-2664"
PHONE_TEL = "+19362392664"

def head(title: str, description: str, slug: str, extra_jsonld: str = "") -> str:
    canonical = f"{CANONICAL_BASE}{slug}"
    robots = '<meta name="robots" content="noindex,nofollow">\n' if DEV_NOINDEX else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{robots}<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_VERSION}">
<meta name="theme-color" content="#2a4a32">
{extra_jsonld}
</head>
<body>"""

HEADER = f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">
      <span class="brand-mark">{SVGS['mark']}</span>
      <span class="brand-text">Rowe Land, Timber &amp; Dozer<small>Livingston, TX · Polk County</small></span>
    </a>
    <nav class="nav">
      <a href="/timber/">Timber</a>
      <a href="/land/">Land &amp; Dozer</a>
      <a href="/guides/">Guides</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a class="phone-cta" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
    </nav>
  </div>
</header>"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div><h4>Rowe Land, Timber &amp; Dozer Services</h4>
        <p>668 Twin Creeks Dr<br>Livingston, TX 77351<br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
      </div>
      <div><h4>Services</h4>
        <p><a href="/timber/">Timber sales &amp; consulting</a><br>
        <a href="/land/">Land clearing &amp; dozer work</a></p>
      </div>
      <div><h4>Service area</h4>
        <p><a href="/service-area/">Polk, San Jacinto, Trinity, Tyler, Angelina &amp; Walker counties</a> · Lake Livingston</p>
      </div>
    </div>
    <p class="fineprint">© Rowe Land, Timber &amp; Dozer Services. Owner-operated in Livingston, Texas.</p>
  </div>
</footer>
</body>
</html>
"""

LOCALBUSINESS_JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Rowe Land, Timber & Dozer Services",
  "telephone": "+1-936-239-2664",
  "address": {"@type": "PostalAddress","streetAddress": "668 Twin Creeks Dr","addressLocality": "Livingston","addressRegion": "TX","postalCode": "77351","addressCountry": "US"},
  "areaServed": ["Polk County, TX","San Jacinto County, TX","Trinity County, TX","Tyler County, TX","Angelina County, TX","Walker County, TX","Lake Livingston"],
  "url": "https://www.rowelandtimber.com/"
}
</script>"""

# ---- Schema helpers ----------------------------------------------------------

import json as _json
import html as _html

def jsonld(obj) -> str:
    return f'<script type="application/ld+json">{_json.dumps(obj, separators=(",", ":"))}</script>'

def breadcrumb_jsonld(trail):
    """trail = [(name, slug), ...] in display order (Home → ... → current)."""
    items = []
    for i, (name, slug) in enumerate(trail, start=1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": f"{CANONICAL_BASE}{slug}"})
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})

def faq_jsonld(qa_pairs):
    """qa_pairs = [(question, answer_plaintext), ...]."""
    return jsonld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa_pairs
        ],
    })

def service_jsonld(name, description, slug, area_served=None):
    area = area_served or ["Polk County, TX", "Lake Livingston", "San Jacinto County, TX",
                          "Trinity County, TX", "Tyler County, TX", "Angelina County, TX", "Walker County, TX"]
    return jsonld({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "provider": {"@type": "LocalBusiness", "name": "Rowe Land, Timber & Dozer Services",
                     "telephone": "+1-936-239-2664",
                     "address": {"@type": "PostalAddress", "streetAddress": "668 Twin Creeks Dr",
                                 "addressLocality": "Livingston", "addressRegion": "TX",
                                 "postalCode": "77351", "addressCountry": "US"}},
        "areaServed": area,
        "url": f"{CANONICAL_BASE}{slug}",
    })

def article_jsonld(headline, description, slug, datePublished="2026-06-09", dateModified="2026-06-09"):
    return jsonld({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "datePublished": datePublished,
        "dateModified": dateModified,
        "author": {"@type": "Person", "name": "Bob Rowe"},
        "publisher": {"@type": "Organization", "name": "Rowe Land, Timber & Dozer Services",
                      "logo": {"@type": "ImageObject", "url": f"{CANONICAL_BASE}/assets/img/mark.svg"}},
        "mainEntityOfPage": f"{CANONICAL_BASE}{slug}",
    })


# ---- Breadcrumb + FAQ rendered HTML ------------------------------------------

def breadcrumb_html(trail):
    parts = []
    for i, (name, slug) in enumerate(trail):
        if i < len(trail) - 1:
            parts.append(f'<a href="{slug}">{name}</a>')
        else:
            parts.append(f'<span aria-current="page">{name}</span>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><div class="wrap">{" › ".join(parts)}</div></nav>'

def faq_html(qa_pairs, h2="Frequently asked questions"):
    items = "".join(
        f'<details class="faq-item"><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
        for q, a in qa_pairs
    )
    return f'<section class="section-bone"><div class="wrap"><h2>{h2}</h2><div class="faq-list">{items}</div></div></section>'


# ---- Page helpers ------------------------------------------------------------

def service_hero(eyebrow, h1, lede, cta_label, cta_type, cta_class="btn", icon=None):
    art = f'<div class="hero-art">{SVGS[icon]}</div>' if icon and icon in SVGS else ""
    hero_class = "hero hero-illustrated" if art else "hero"
    return f"""<section class="{hero_class}">
  <div class="wrap">
    <div>
      <p class="eyebrow-line">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <p><a class="{cta_class}" href="/contact/?type={cta_type}">{cta_label}</a> &nbsp; <a class="btn ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p>
    </div>
    {art}
  </div>
</section>"""

def two_col(left_html: str, right_html: str) -> str:
    return f'<section><div class="wrap two-col"><div>{left_html}</div><div>{right_html}</div></div></section>'

def bone_section(html: str) -> str:
    return f'<section class="section-bone"><div class="wrap">{html}</div></section>'

def dark_cta(h2: str, body_html: str, cta_label: str, cta_type: str) -> str:
    return f"""<section class="section-dark"><div class="wrap">
<h2>{h2}</h2>
{body_html}
<p style="margin-top:1rem"><a class="btn alt" href="/contact/?type={cta_type}">{cta_label}</a></p>
</div></section>"""

def render(slug: str, title: str, description: str, body: str, extra_jsonld: str = "",
           breadcrumb=None) -> None:
    out = SITE_DIR / slug.strip("/") / "index.html" if slug != "/" else SITE_DIR / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    crumb_html = breadcrumb_html(breadcrumb) if breadcrumb else ""
    crumb_jsonld = breadcrumb_jsonld(breadcrumb) if breadcrumb else ""
    html = head(title, description, slug, extra_jsonld + crumb_jsonld) + HEADER + crumb_html + body + FOOTER
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {slug}")

# ---- Pages -------------------------------------------------------------------

def build_home():
    body = f"""<section class="hero">
  <div class="wrap">
    <p class="eyebrow-line">Polk County · Lake Livingston · East Texas</p>
    <h1>Local land work and timber sales — done right, by someone who works for you.</h1>
    <p class="lede">One Livingston-based outfit for the heavy land work most owners need, and an honest advocate when it&rsquo;s time to sell your timber. From raw timber to build-ready ground, we cover the whole job.</p>
    <div class="paths">
      <div class="path">
        <div class="path-art">""" + SVGS['pine'] + """</div>
        <p class="eyebrow">Own forested land?</p>
        <h2>Selling or harvesting timber</h2>
        <p>Most buyers work for themselves. I work for you — making sure your timber is measured honestly, bid competitively, and sold for what it&rsquo;s actually worth.</p>
        <a class="btn" href="/timber/">Get a Free Timber Evaluation</a>
      </div>
      <div class="path">
        <div class="path-art">""" + SVGS['dozer'] + """</div>
        <p class="eyebrow">Bought a lot or acreage?</p>
        <h2>Land clearing &amp; dirt work</h2>
        <p>Dozer, forestry mulcher, and excavator work for East Texas pine and hardwood. Lake Livingston lots, pads, roads, ponds, drainage — the real scope.</p>
        <a class="btn alt" href="/land/">Get a Free Estimate</a>
      </div>
    </div>
  </div>
</section>

<section class="section-bone"><div class="wrap two-col">
  <div>
    <p class="eyebrow-line">Why Rowe</p>
    <h2>Local. Owner-operated. On your side.</h2>
    <p>I&rsquo;m based right here in Livingston — not driving in from Walker County, not selling leads to somebody else. I walk the land before I quote it, and I run the equipment that does the work.</p>
    <p>On the timber side, that&rsquo;s the whole point. The Texas A&amp;M Forest Service tells landowners to hire a consultant who represents <em>their</em> interests, insist on competitive bids, and never trust a buyer blindly. That&rsquo;s the role I play.</p>
    <div class="pullquote">&ldquo;Most timber buyers work for themselves. I work for you — making sure your timber is measured honestly, bid competitively, and sold for what it&rsquo;s actually worth.&rdquo;</div>
  </div>
  <div>
    <h3>What I do</h3>
    <ul class="checks">
      <li><a href="/timber/sale-consulting/">Timber sale consulting &amp; competitive bidding</a></li>
      <li><a href="/timber/management/">Timber management plans</a></li>
      <li><a href="/timber/harvest/">Timber harvest oversight</a></li>
      <li><a href="/land/land-clearing/">Land clearing</a></li>
      <li><a href="/land/forestry-mulching/">Forestry mulching</a></li>
      <li><a href="/land/dozer-grading/">Dozer work &amp; grading</a></li>
      <li><a href="/land/roads-pads-drainage/">Roads, pads &amp; drainage</a></li>
      <li><a href="/land/ponds/">Ponds</a></li>
      <li><a href="/land/lake-livingston-lots/">Lake Livingston lot clearing</a></li>
    </ul>
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <h2>Two paths. One local number.</h2>
  <p>Not sure where you fit? Call or text <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> and tell me what you&rsquo;ve got. I&rsquo;ll tell you straight whether it&rsquo;s a timber conversation, a dirt-work conversation, or both.</p>
  <p style="margin-top:1.5rem">
    <a class="btn alt" href="/contact/">Send a message</a>
    &nbsp;
    <a class="btn ghost" href="tel:{PHONE_TEL}" style="color:#c89b3c;border-color:#c89b3c">Call {PHONE_DISPLAY}</a>
  </p>
</div></section>"""
    render("/",
           "Rowe Land, Timber & Dozer — Livingston, TX | Polk County Land Work & Timber Sales",
           "Local Livingston TX land clearing, dozer work, and timber sale consulting. We work for the landowner — not the timber buyers. Polk County and Lake Livingston.",
           body, LOCALBUSINESS_JSONLD)


def build_timber_pillar():
    body = service_hero(
        "For landowners · Polk County &amp; East Texas",
        "What&rsquo;s your timber actually worth?",
        "Selling standing timber is a once-or-twice-in-a-lifetime decision, and landowners get lowballed every day in East Texas. I&rsquo;ll walk your land, give you an honest evaluation, and represent <em>your</em> side of the sale — not the buyer&rsquo;s.",
        "Get a Free Timber Evaluation", "timber", icon="pine"
    ) + two_col(
        """<h2>Why the &ldquo;on your side&rdquo; part matters</h2>
        <p>The State of Texas itself warns landowners. The <strong>Texas A&amp;M Forest Service runs a Timber Theft Hotline (1-800-364-3470)</strong> and has pursued indictments against loggers who underpaid landowners. The state&rsquo;s standing advice: hire a consulting forester to represent your interests, insist on competitive bids, and never trust a buyer blindly.</p>
        <p>That&rsquo;s exactly the role I play. Most companies on the timber side are <em>buyers</em> — and a buyer&rsquo;s job is to pay you less. My job is the opposite.</p>
        <div class="pullquote">&ldquo;Most timber buyers work for themselves. I work for you — making sure your timber is measured honestly, bid competitively, and sold for what it&rsquo;s actually worth.&rdquo;</div>""",
        """<h3>What I help landowners with</h3>
        <ul class="checks">
          <li><a href="/timber/sale-consulting/">Timber sale consulting &amp; competitive bidding</a></li>
          <li><a href="/timber/management/">Long-term timber management plans</a></li>
          <li><a href="/timber/harvest/">Harvest oversight &amp; clean-up</a></li>
          <li>Walk-the-land evaluations, not desktop quotes</li>
          <li>Written contract before a tree comes down</li>
          <li>Optional replant or conversion to pasture/build site</li>
        </ul>"""
    ) + bone_section(
        """<h2>One call for the whole job</h2>
        <p>Most owners don&rsquo;t just want the timber sold — they want the land left usable. Because I also run the dozer side, I can handle the cleanup, road work, replant, or conversion to pasture or a build site without bringing in a second outfit. <a href="/land/">See land &amp; dozer services →</a></p>"""
    ) + dark_cta(
        "Free, no-obligation timber evaluation",
        "<p>Tell me where the land is and roughly how many acres. I&rsquo;ll come look at it. No pressure, no contract until you&rsquo;ve seen the numbers and decided you want to move forward.</p>",
        "Get a Free Timber Evaluation", "timber"
    )
    extra = service_jsonld(
        "Timber Sale Consulting and Forestry Services",
        "Timber sale consulting, forestry consulting, and timber management for landowners in Polk County, East Texas, and around Lake Livingston.",
        "/timber/",
    )
    breadcrumb = [("Home", "/"), ("Timber", "/timber/")]
    render("/timber/",
           "Timber Buyers Alternative in Livingston TX — Rowe Land, Timber & Dozer",
           "Selling timber in Polk County or East Texas? Get a free timber evaluation from a consultant who works for you — not the timber buyers. Local to Livingston.",
           body, extra, breadcrumb=breadcrumb)


def build_land_pillar():
    body = service_hero(
        "Polk County · Lake Livingston · East Texas",
        "From raw timber to build-ready ground.",
        "Dozer, forestry mulcher, excavator, and dump truck — the right equipment for East Texas pine and hardwood. Local to Livingston, not driving in from another county.",
        "Get a Free Estimate", "land", "btn alt", icon="dozer"
    ) + two_col(
        """<h2>What I do</h2>
        <ul class="checks">
          <li><a href="/land/land-clearing/"><strong>Land clearing</strong></a> — pine, hardwood, brush, stumps</li>
          <li><a href="/land/forestry-mulching/"><strong>Forestry mulching</strong></a> — selective, low-impact</li>
          <li><a href="/land/dozer-grading/"><strong>Dozer work &amp; grading</strong></a> — pads, contours, finish grade</li>
          <li><a href="/land/roads-pads-drainage/"><strong>Roads, pads &amp; drainage</strong></a> — base, crown, runoff</li>
          <li><a href="/land/ponds/"><strong>Ponds</strong></a> — design, dig, dam, spillway</li>
          <li><a href="/land/lake-livingston-lots/"><strong>Lake Livingston lot specialist</strong></a></li>
          <li>Site prep — for builds, barndominiums, ag, recreation</li>
          <li>Dump truck &amp; dirt hauling</li>
        </ul>""",
        """<h3>Lake Livingston lot specialist</h3>
        <p>Lake lots are not the same job as upland acreage. Sloped lakefront ground washes if you clear it wrong, and silt that ends up in the lake ends up being your problem. I clear and grade lakefront lots with erosion in mind — keeping the buffer where it belongs and the dirt where it belongs.</p>
        <h3>The right machine for East Texas</h3>
        <p>Real pine and hardwood need real equipment — not a landscaping crew with a small skid steer. If your project actually needs a dozer, you should hire a dozer.</p>"""
    ) + bone_section(
        """<h2>Straight pricing. Real quote after I see the site.</h2>
        <p>I don&rsquo;t quote a job off a Google Maps photo. Tell me where the land is and what you&rsquo;re trying to do — I&rsquo;ll come look, ask the right questions, and give you a real number. Local trip, no hidden charge for driving in.</p>
        <p style="margin-top:1rem"><a class="btn alt" href="/contact/?type=land">Get a Free Estimate</a></p>"""
    ) + dark_cta(
        "Got timber on it too?",
        "<p>If the land you want cleared has marketable timber standing on it, don&rsquo;t let a clearing crew bulldoze value into a brush pile. I can handle the timber side first — sold honestly and competitively — then come back and finish the clearing. <a href=\"/timber/\">See timber sales &amp; consulting →</a></p>",
        "Get a Free Estimate", "land"
    )
    extra = service_jsonld(
        "Land Clearing and Dozer Services",
        "Land clearing, forestry mulching, dozer work, grading, ponds, and site prep in Polk County and around Lake Livingston.",
        "/land/",
    )
    breadcrumb = [("Home", "/"), ("Land & Dozer", "/land/")]
    render("/land/",
           "Land Clearing Livingston TX — Dozer, Mulcher & Lot Clearing | Rowe",
           "Land clearing in Livingston TX and around Lake Livingston. Forestry mulching, dozer work, grading, ponds, and dirt work for Polk County. Free estimate.",
           body, extra, breadcrumb=breadcrumb)


def build_about():
    body = """<section class="hero"><div class="wrap">
  <p class="eyebrow-line">About</p>
  <h1>One local company. From raw timber to finished ground.</h1>
</div></section>

<section><div class="wrap" style="max-width:760px">
  <p>Rowe Land, Timber &amp; Dozer Services is a Livingston-based, owner-operated land and timber company serving Polk County and the Lake Livingston area.</p>
  <p>We do the heavy land work most landowners need — clearing, forestry mulching, dozer and dirt work, grading, roads, ponds, and site prep — with equipment built for East Texas pine and hardwood.</p>
  <p>And when it&rsquo;s time to sell or harvest your timber, we do something most companies won&rsquo;t: <strong>we work for you</strong>. As your timber consultant, we make sure your stand is measured honestly, bid competitively, and sold for what it&rsquo;s truly worth.</p>
  <p>One local company, from raw timber to finished ground.</p>

  <h2>Service area</h2>
  <p>Polk County is home — Livingston, Onalaska, Goodrich, Corrigan, Leggett, and the Lake Livingston shoreline. We also work San Jacinto, Trinity, Tyler, Angelina, and Walker counties for the right projects. <a href=\"/service-area/\">See the full service area →</a></p>

  <h2>Talk to Bob</h2>
  <p>I&rsquo;m the one who picks up the phone, walks your land, runs the quote, and runs the equipment. Call or text <a href=\"tel:""" + PHONE_TEL + """\">""" + PHONE_DISPLAY + """</a>, or <a href=\"/contact/\">send a message</a>.</p>
</div></section>"""
    render("/about/", "About Bob Rowe — Rowe Land, Timber & Dozer Services",
           "Owner-operated land and timber outfit in Livingston, Texas. One local company, from raw timber to finished ground.",
           body)


def build_contact():
    body = f"""<section class="hero"><div class="wrap">
  <p class="eyebrow-line">Contact</p>
  <h1>Tell me what you&rsquo;ve got.</h1>
  <p class="lede">Call or text <a href="tel:{PHONE_TEL}"><strong>{PHONE_DISPLAY}</strong></a>, or send the form below. I&rsquo;ll get back to you the same day in most cases.</p>
</div></section>

<section><div class="wrap two-col">
<div>
  <h2>Send a message</h2>
  <form class="lead" action="https://formspree.io/f/REPLACE_ME" method="POST">
    <div>
      <label>What do you need?</label>
      <div class="radios">
        <label><input type="radio" name="type" value="timber" checked> Timber evaluation / sale</label>
        <label><input type="radio" name="type" value="land"> Land clearing / dozer work</label>
        <label><input type="radio" name="type" value="both"> Both</label>
      </div>
    </div>
    <div><label for="name">Your name</label><input id="name" name="name" type="text" required></div>
    <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required></div>
    <div><label for="email">Email</label><input id="email" name="email" type="email"></div>
    <div><label for="location">Where&rsquo;s the property?</label><input id="location" name="location" type="text" placeholder="Address, road, or nearest town &amp; county"></div>
    <div><label for="acres">Roughly how many acres?</label><input id="acres" name="acres" type="text" placeholder="e.g. 12 acres, lake lot, ~80 acres"></div>
    <div><label for="notes">Tell me what you&rsquo;re trying to do</label><textarea id="notes" name="notes" placeholder="What&rsquo;s on the land, what you&rsquo;d like done, any timing"></textarea></div>
    <input type="hidden" name="_next" value="/thank-you/">
    <div><button class="btn" type="submit">Send it</button></div>
  </form>
</div>
<div>
  <h3>Rowe Land, Timber &amp; Dozer Services</h3>
  <p>668 Twin Creeks Dr<br>Livingston, TX 77351</p>
  <p><strong>Phone / text:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
  <h3>Service area</h3>
  <p>Polk County is home — and we work San Jacinto, Trinity, Tyler, Angelina, and Walker counties plus the Lake Livingston shoreline. <a href="/service-area/">See all counties</a>.</p>
  <h3>Hours</h3>
  <p>Working hours are daylight. Best to call. If you reach voicemail, I&rsquo;m on a piece of equipment — leave a message and I&rsquo;ll call back.</p>
</div>
</div></section>
<script>
  (function(){{
    var m = location.search.match(/[?&]type=(timber|land|both)/);
    if (!m) return;
    var r = document.querySelector('input[name="type"][value="'+m[1]+'"]');
    if (r) r.checked = true;
  }})();
</script>"""
    render("/contact/", "Contact — Rowe Land, Timber & Dozer Services, Livingston TX",
           "Call (936) 239-2664 or send a message for a free timber evaluation or land clearing estimate in Polk County and around Lake Livingston.",
           body)


def build_404():
    body = """<section class="hero"><div class="wrap">
  <p class="eyebrow-line">404</p>
  <h1>That page isn&rsquo;t here.</h1>
  <p class="lede">Either the link is wrong, or I haven&rsquo;t built that page yet. Easiest fix is to start from the home page or give me a call.</p>
  <p style="margin-top:1.5rem"><a class="btn" href="/">Back to the homepage</a> &nbsp; <a class="btn ghost" href="tel:""" + PHONE_TEL + """\">Call """ + PHONE_DISPLAY + """</a></p>
</div></section>
<section><div class="wrap two-col">
  <div>
    <h2>Looking for something specific?</h2>
    <ul class="checks">
      <li><a href="/timber/">Timber sales &amp; consulting</a></li>
      <li><a href="/land/">Land clearing &amp; dozer work</a></li>
      <li><a href="/service-area/">Service area</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul>
  </div>
  <div>
    <h3>Or just call</h3>
    <p>Working hours are daylight. <a href="tel:""" + PHONE_TEL + """\">""" + PHONE_DISPLAY + """</a></p>
  </div>
</div></section>"""
    # 404 lives at /404.html — render manually since render() expects a directory
    out = SITE_DIR / "404.html"
    html = head("Page not found — Rowe Land, Timber & Dozer Services",
                "That page isn't here. Try the home page or call (936) 239-2664.",
                "/404") + HEADER + body + FOOTER
    out.write_text(html, encoding="utf-8")
    print("  wrote /404.html")


def build_thank_you():
    body = """<section class="hero"><div class="wrap">
  <p class="eyebrow-line">Thanks</p>
  <h1>Got it. I&rsquo;ll be in touch.</h1>
  <p class="lede">Your message came through. I&rsquo;ll call or text back the same day in most cases — usually faster.</p>
  <p style="margin-top:1.5rem"><a class="btn ghost" href="tel:""" + PHONE_TEL + """">In a hurry? Call """ + PHONE_DISPLAY + """</a></p>
</div></section>
<section><div class="wrap" style="max-width:680px">
  <h2>While you wait</h2>
  <p>If you have photos of the property, the property tax record, or a rough sketch of the area you&rsquo;re thinking about, have them handy when I call — it makes the conversation faster and the quote more accurate.</p>
  <p><a href=\"/\">← Back to the homepage</a></p>
</div></section>"""
    render("/thank-you/", "Thanks — Rowe Land, Timber & Dozer Services",
           "Thanks for reaching out. Bob will be in touch the same day in most cases.",
           body)


# --- Land sub-services --------------------------------------------------------

LAND_SUB = [
    {
        "icon": "dozer",
        "slug": "/land/land-clearing/",
        "title": "Land Clearing Livingston TX & Polk County — Rowe Land, Timber & Dozer",
        "description": "Land clearing near you in Livingston TX, Polk County, and around Lake Livingston. Pine, hardwood, brush, and stumps cleared by a local owner-operator.",
        "eyebrow": "Land clearing · Polk County &amp; Lake Livingston",
        "h1": "Land clearing for real East Texas timber and brush.",
        "lede": "If your land has actual pine, hardwood, and stumps on it — not just lawn — you need real equipment and someone who knows what to leave standing. That&rsquo;s the work I do.",
        "left": """<h2>Standing timber + brush + stumps</h2>
        <p>Most clearing jobs in this part of Texas aren&rsquo;t a mower problem — they&rsquo;re a <em>dozer-and-mulcher</em> problem. Pine that&rsquo;s grown in too thick, hardwood thickets, yaupon, stumps, fence rows. I run the right machine for the job, sometimes two on the same site.</p>
        <p>If there&rsquo;s marketable timber on it, that&rsquo;s a conversation before any clearing starts. <a href="/timber/">See timber sales &amp; consulting</a> — letting a clearing crew bulldoze sellable timber into a brush pile is one of the most expensive mistakes a landowner can make.</p>
        <h3>Common land-clearing jobs</h3>
        <ul class="checks">
          <li>Raw acreage for a homesite or barndominium</li>
          <li>Pasture reclamation — clearing back encroaching brush</li>
          <li>Fence lines and right-of-way</li>
          <li>Hunting lanes, food plots, recreational access</li>
          <li>Whole-tract clearing for ag or development</li>
          <li>Lake Livingston lots (see specialty page below)</li>
        </ul>""",
        "right": """<h3>What you get</h3>
        <ul class="checks">
          <li>Walk-the-site visit before the quote</li>
          <li>Straight talk about timber value vs. clear-and-burn</li>
          <li>Right machine for the density — dozer, mulcher, or excavator</li>
          <li>Burn piles or mulched in place, your call</li>
          <li>Stump grinding or extraction if you want a clean grade</li>
          <li>Finish grade and seed if it&rsquo;s on the work order</li>
        </ul>
        <h3>Related services</h3>
        <ul class="checks">
          <li><a href="/land/forestry-mulching/">Forestry mulching</a></li>
          <li><a href="/land/dozer-grading/">Dozer work &amp; grading</a></li>
          <li><a href="/land/lake-livingston-lots/">Lake Livingston lot clearing</a></li>
        </ul>""",
        "cta_h2": "Get a real quote after I see the site.",
        "cta_body": "<p>Tell me where the land is and roughly what you&rsquo;ve got. I&rsquo;ll come walk it and give you a real number. Local trip — Polk County is home.</p>",
    },
    {
        "icon": "mulcher",
        "slug": "/land/forestry-mulching/",
        "title": "Forestry Mulching East Texas — Polk County & Lake Livingston | Rowe",
        "description": "Forestry mulching in East Texas — Polk County, Lake Livingston, and surrounding counties. Selective, low-impact underbrush and small-tree clearing. Free estimate.",
        "eyebrow": "Forestry mulching · Polk County",
        "h1": "Forestry mulching — keep the trees you want, lose the rest.",
        "lede": "A mulcher chews understory and small trees into mulch on the spot. No burn piles, no hauling, no scraped-bare earth. The right tool when you want a usable property without clear-cutting it.",
        "left": """<h2>When forestry mulching is the right call</h2>
        <ul class="checks">
          <li>Underbrush, yaupon, and small-diameter trees up to about 8&Prime;</li>
          <li>Selective clearing where you want mature trees left</li>
          <li>Trails, ATV lanes, hunting access</li>
          <li>Fence lines and survey lines</li>
          <li>Wildfire fuel reduction around a homestead</li>
          <li>Recreational properties where look-and-feel matters</li>
        </ul>
        <h2>When it&rsquo;s not the right call</h2>
        <p>If you&rsquo;re clearing for a building pad, road, or pond — a mulcher alone won&rsquo;t cut it. You&rsquo;ll want a <a href="/land/dozer-grading/">dozer and grading</a> in the mix. And if there&rsquo;s real timber on it, talk <a href="/timber/">timber sale</a> first.</p>""",
        "right": """<h3>What forestry mulching gets you</h3>
        <ul class="checks">
          <li>No burn piles or smoke</li>
          <li>Mulch left on the ground — slows erosion, improves soil</li>
          <li>One-pass operation, no follow-up haul-off</li>
          <li>Tracks instead of wheels, lower ground disturbance</li>
          <li>Can work close to standing trees you want kept</li>
        </ul>
        <h3>Pairs well with</h3>
        <ul class="checks">
          <li><a href="/land/land-clearing/">Land clearing</a> for the heavier areas</li>
          <li><a href="/land/lake-livingston-lots/">Lake lot clearing</a> where erosion matters</li>
        </ul>""",
        "cta_h2": "Walk-the-site quote — Polk County and surrounding.",
        "cta_body": "<p>Send a few photos or just tell me where it is and roughly the acreage. I&rsquo;ll come look and tell you whether mulching, clearing, or both is the right job.</p>",
    },
    {
        "icon": "dozer",
        "slug": "/land/dozer-grading/",
        "title": "Dozer Work Near Me — Livingston, Polk County & Lake Livingston | Rowe",
        "description": "Dozer work near you in Livingston, Polk County, and around Lake Livingston. Building pads, finish grading, earth-moving. Owner-operated, walk-the-site quote.",
        "eyebrow": "Dozer &amp; grading · Polk County",
        "h1": "Dozer work and grading for East Texas dirt.",
        "lede": "Building pads, finish grades, contours, fill, and earth-moving. Sandy uplands and clay creek bottoms behave differently — I&rsquo;ve been on both, and I quote accordingly.",
        "left": """<h2>What I run dozer on</h2>
        <ul class="checks">
          <li>Building pads for houses, barndominiums, shops</li>
          <li>Finish grading after a clearing job</li>
          <li>Contours, terraces, swales</li>
          <li>Cut-and-fill on sloped lots</li>
          <li>Fill placement and compaction prep</li>
          <li>Demolition push-out and clean-up</li>
          <li>Rough grading for driveways and pad approaches</li>
        </ul>
        <h2>East Texas terrain matters</h2>
        <p>Polk County&rsquo;s sandy uplands grade beautifully and drain fast. The clay creek bottoms toward the Trinity and the lake hold water and rut if you push them when they&rsquo;re wet. Knowing the difference is half the job — and it&rsquo;s the reason a local operator is worth more than a cheaper one driving in from a hundred miles away.</p>""",
        "right": """<h3>What you get</h3>
        <ul class="checks">
          <li>On-site visit before the quote, every time</li>
          <li>Honest read on what the dirt will do</li>
          <li>Right machine sized to the job</li>
          <li>Clean finish, not just &ldquo;close enough&rdquo;</li>
        </ul>
        <h3>Often paired with</h3>
        <ul class="checks">
          <li><a href="/land/land-clearing/">Land clearing</a> first</li>
          <li><a href="/land/roads-pads-drainage/">Roads, pads &amp; drainage</a></li>
          <li><a href="/land/ponds/">Pond construction</a></li>
        </ul>""",
        "cta_h2": "Real quote, after I see the dirt.",
        "cta_body": "<p>If you&rsquo;ve got a pad, a slope, or a stretch of ground that needs to be made flat, send me where it is. I&rsquo;ll come look.</p>",
    },
    {
        "icon": "pond",
        "slug": "/land/ponds/",
        "title": "Pond Digging in Polk County TX — Stock, Rec & Erosion Ponds | Rowe",
        "description": "Stock ponds, recreation ponds, and erosion-control ponds built with proper dam, spillway, and drainage. Polk County, Lake Livingston, surrounding counties.",
        "eyebrow": "Ponds · Polk County &amp; East Texas",
        "h1": "Ponds built to hold water — and to drain when they should.",
        "lede": "Anybody with a track-hoe can dig a hole. A pond that holds water through August, doesn&rsquo;t blow out in a hard rain, and doesn&rsquo;t silt in by year five is a different conversation.",
        "left": """<h2>What goes into a pond that lasts</h2>
        <ul class="checks">
          <li>Site selection — soil type, watershed, slope</li>
          <li>Properly built dam with a clay core</li>
          <li>A spillway sized for the watershed (this is what fails first on a cheap pond)</li>
          <li>Cleared and benched edges</li>
          <li>Berms and silt control during construction</li>
          <li>Stocking-ready depth in the right spot</li>
        </ul>
        <h2>Stock pond, rec pond, or runoff pond</h2>
        <p>Different jobs. A 1-acre fishing pond and a half-acre cattle watering hole aren&rsquo;t built the same. Tell me what you want it for, and I&rsquo;ll tell you what it actually takes.</p>""",
        "right": """<h3>The questions I&rsquo;ll ask on the site visit</h3>
        <ul class="checks">
          <li>What drains into this spot?</li>
          <li>What does the soil look like 4 ft down?</li>
          <li>Where&rsquo;s the natural low point?</li>
          <li>What happens in a 5-inch rain?</li>
          <li>Are you stocking it, swimming in it, or watering livestock?</li>
        </ul>
        <h3>Goes with</h3>
        <ul class="checks">
          <li><a href="/land/dozer-grading/">Dozer work &amp; grading</a></li>
          <li><a href="/land/roads-pads-drainage/">Drainage &amp; runoff control</a></li>
          <li><a href="/land/land-clearing/">Clearing the pond site</a></li>
        </ul>""",
        "cta_h2": "Pond evaluation — I&rsquo;ll come look at the spot.",
        "cta_body": "<p>Tell me where on the property you&rsquo;d like it and roughly how big. I&rsquo;ll walk the site with you and tell you what it&rsquo;ll really take.</p>",
    },
    {
        "icon": "lake",
        "slug": "/land/lake-livingston-lots/",
        "title": "Lot Clearing Lake Livingston — Lakefront Grading & Erosion Control | Rowe",
        "description": "Lakefront and near-lake lot clearing and grading around Lake Livingston — done with erosion control, buffer zones, and runoff in mind.",
        "eyebrow": "Lake Livingston · Onalaska, Coldspring, Trinity, Livingston shoreline",
        "h1": "Lake Livingston lots — cleared and graded without ruining the lake.",
        "lede": "Lakefront lots aren&rsquo;t the same job as upland acreage. Sloped ground washes if you clear it wrong, and silt that ends up in the lake ends up being your problem. I clear lake lots with erosion in mind.",
        "left": """<h2>What makes a lake lot different</h2>
        <ul class="checks">
          <li>Steeper slope to the water than most acreage</li>
          <li>Sandy or sandy-loam soils that move when exposed</li>
          <li>Buffer zones near the water you want to keep</li>
          <li>Runoff that goes straight into the lake — yours or your neighbor&rsquo;s</li>
          <li>HOA and TRA rules in some subdivisions</li>
          <li>Smaller working room than rural acreage</li>
        </ul>
        <h2>How I work a lake lot</h2>
        <p>Selective clearing where it matters, leave the right canopy where the slope is steepest, keep the dirt on the lot. Forestry mulching is often the right tool, not a bulldozer — especially close to the waterline. <a href="/land/forestry-mulching/">See forestry mulching</a>.</p>""",
        "right": """<h3>What I won&rsquo;t do</h3>
        <p>I won&rsquo;t scrape a lake lot bare, leave it to wash, and walk away. It&rsquo;s the easiest way to make a $40k mistake on a $300k lot. There&rsquo;s a smarter way to do it, and that&rsquo;s how I quote.</p>
        <h3>Goes with</h3>
        <ul class="checks">
          <li><a href="/land/forestry-mulching/">Forestry mulching</a></li>
          <li><a href="/land/dozer-grading/">Dozer &amp; grading</a> for the pad</li>
          <li><a href="/land/roads-pads-drainage/">Driveway &amp; drainage</a></li>
        </ul>""",
        "cta_h2": "Site visit on the lot, no charge.",
        "cta_body": "<p>Tell me which side of the lake and which subdivision. I&rsquo;ll meet you out there and walk it with you.</p>",
    },
    {
        "icon": "road",
        "slug": "/land/roads-pads-drainage/",
        "title": "Driveways, Pads & Drainage in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Driveways, building pads, culverts, and drainage on rural East Texas property. Polk County, Lake Livingston, and surrounding counties.",
        "eyebrow": "Driveways, pads &amp; drainage",
        "h1": "Driveways, pads, and drainage built to hold up.",
        "lede": "Rural East Texas roads, pads, and culverts. The difference between &ldquo;works in dry weather&rdquo; and &ldquo;works after three days of rain&rdquo; is mostly drainage — and that&rsquo;s where most jobs go wrong.",
        "left": """<h2>Driveways &amp; private roads</h2>
        <ul class="checks">
          <li>Long rural driveways</li>
          <li>Crown, ditches, and culverts</li>
          <li>Base material spread and compacted</li>
          <li>Approach pads at the county road</li>
          <li>Curves and grades that work for delivery trucks</li>
        </ul>
        <h2>Building pads</h2>
        <ul class="checks">
          <li>House pads, barndominium pads, shop pads</li>
          <li>Sized and oriented for your build</li>
          <li>Compacted properly so it doesn&rsquo;t settle</li>
          <li>Drainage off the pad — not into it</li>
        </ul>""",
        "right": """<h3>Drainage</h3>
        <ul class="checks">
          <li>Ditches and swales that actually move water</li>
          <li>Culverts sized to the watershed</li>
          <li>Runoff control during and after construction</li>
          <li>Stopping erosion before it cuts a gully</li>
        </ul>
        <h3>Often paired with</h3>
        <ul class="checks">
          <li><a href="/land/land-clearing/">Land clearing</a></li>
          <li><a href="/land/dozer-grading/">Dozer work &amp; grading</a></li>
          <li><a href="/land/ponds/">Ponds and runoff capture</a></li>
        </ul>""",
        "cta_h2": "Get a real quote on the work.",
        "cta_body": "<p>Driveway, pad, or drainage problem — tell me where the property is. I&rsquo;ll come look.</p>",
    },
]


def build_land_sub_pages():
    for p in LAND_SUB:
        body = service_hero(p["eyebrow"], p["h1"], p["lede"], "Get a Free Estimate", "land", "btn alt", icon=p.get("icon"))
        body += two_col(p["left"], p["right"])
        body += dark_cta(p["cta_h2"], p["cta_body"], "Get a Free Estimate", "land")
        breadcrumb = [("Home", "/"), ("Land & Dozer", "/land/"), (p["h1"], p["slug"])]
        extra = service_jsonld(p["h1"], p["description"], p["slug"])
        render(p["slug"], p["title"], p["description"], body, extra, breadcrumb=breadcrumb)


# --- Timber sub-services ------------------------------------------------------

TIMBER_SUB = [
    {
        "icon": "pine",
        "slug": "/timber/sale-consulting/",
        "title": "Timber Sale Consultant East Texas — Polk County | Rowe Land, Timber",
        "description": "Selling timber in East Texas or Polk County? Hire a timber sale consultant who works for the landowner — competitive bids, honest cruise, written contract.",
        "eyebrow": "Timber sale consulting",
        "h1": "Sell your timber for what it&rsquo;s actually worth.",
        "lede": "The single biggest difference between a fair timber sale and a bad one is having someone on your side of the table. That&rsquo;s the job I do.",
        "left": """<h2>How a Rowe-managed sale works</h2>
        <ol>
          <li><strong>I walk the land.</strong> No desktop quotes off a map.</li>
          <li><strong>Cruise and estimate the volume.</strong> Pine sawtimber, hardwood, pulpwood — measured honestly.</li>
          <li><strong>Put it out to multiple qualified buyers.</strong> Competitive bidding is what changes the price, not negotiating skill.</li>
          <li><strong>Written contract.</strong> Volume, price, payment terms, BMPs, clean-up — in writing, before a tree comes down.</li>
          <li><strong>I&rsquo;m on site during the harvest.</strong> Making sure what was sold is what gets cut.</li>
          <li><strong>Close out and clean up.</strong> Roads, decks, and any replant or follow-on land work.</li>
        </ol>
        <h2>Why this matters</h2>
        <p>The Texas A&amp;M Forest Service runs a <strong>Timber Theft Hotline (1-800-364-3470)</strong> for a reason. Underpayment and bad scaling are real problems in this industry. Standard state advice: hire a consultant, insist on competitive bids, get it in writing. That&rsquo;s exactly what I do.</p>""",
        "right": """<h3>You&rsquo;re a good fit if&hellip;</h3>
        <ul class="checks">
          <li>You own forested land in Polk or a surrounding county</li>
          <li>You&rsquo;re thinking about selling timber but haven&rsquo;t yet</li>
          <li>You inherited land and don&rsquo;t know what&rsquo;s on it</li>
          <li>You got a knock-on-the-door offer and want a second opinion</li>
          <li>You&rsquo;re clearing for a build and want to capture timber value first</li>
        </ul>
        <h3>Related</h3>
        <ul class="checks">
          <li><a href="/timber/management/">Long-term timber management plans</a></li>
          <li><a href="/timber/harvest/">Harvest oversight</a></li>
          <li><a href="/land/">Land clearing after harvest</a></li>
        </ul>""",
        "cta_h2": "Free timber evaluation. No pressure.",
        "cta_body": "<p>Tell me where the land is and roughly how many acres. I&rsquo;ll come look and tell you what it&rsquo;s worth — whether you sell with me or not.</p>",
    },
    {
        "icon": "hardwood",
        "slug": "/timber/management/",
        "title": "Timber Management Plans in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Long-term timber management for East Texas landowners — thinning schedules, replant, fire breaks, and harvest planning. Owner-operated, on your side.",
        "eyebrow": "Timber management",
        "h1": "Manage your timber for the long haul — not just one sale.",
        "lede": "A timber stand is a 30- to 40-year asset. Treating it like a one-time payday leaves money on the table and weakens the land. A real management plan does the opposite.",
        "left": """<h2>What a management plan covers</h2>
        <ul class="checks">
          <li>Stand inventory — what you actually have</li>
          <li>Thinning schedule — when to thin, how heavy</li>
          <li>Final harvest planning — what year, what method</li>
          <li>Replant plan — species, density, site prep</li>
          <li>Fire breaks and access roads</li>
          <li>BMPs for water quality and wildlife</li>
          <li>Tax and ag-valuation considerations to discuss with your CPA</li>
        </ul>
        <h2>For absentee owners</h2>
        <p>A lot of East Texas timberland is owned by people who don&rsquo;t live on it — inherited family land, weekend places, investment tracts. A management plan is how that land stays productive without you having to drive out every month.</p>""",
        "right": """<h3>When a plan pays off</h3>
        <ul class="checks">
          <li>20+ acres of pine or mixed stand</li>
          <li>Stand is over 10 years old or due for a thin</li>
          <li>You&rsquo;ve never had it cruised</li>
          <li>You&rsquo;re holding it long-term for kids or grandkids</li>
          <li>You want it to <em>keep producing</em>, not just liquidate it</li>
        </ul>
        <h3>Related</h3>
        <ul class="checks">
          <li><a href="/timber/sale-consulting/">Timber sale consulting</a></li>
          <li><a href="/timber/harvest/">Harvest oversight</a></li>
        </ul>""",
        "cta_h2": "Talk about a management plan.",
        "cta_body": "<p>Send a quick note — where the land is, roughly how many acres, and what you&rsquo;re hoping to do with it. I&rsquo;ll come walk it.</p>",
    },
    {
        "icon": "pine",
        "slug": "/timber/harvest/",
        "title": "Timber Harvest Oversight in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Independent oversight during your timber harvest — making sure what was sold is what gets cut, BMPs are followed, and the land is left right.",
        "eyebrow": "Timber harvest oversight",
        "h1": "Independent eyes on the harvest — for you, not the buyer.",
        "lede": "Once the contract is signed, the worst-case scenarios all involve nobody from your side being on the land while the crew is. That&rsquo;s when boundaries get crossed, BMPs get skipped, and value gets cut you didn&rsquo;t agree to sell.",
        "left": """<h2>What harvest oversight covers</h2>
        <ul class="checks">
          <li>Marking boundaries and leave trees before the crew arrives</li>
          <li>Confirming the right stand is being cut</li>
          <li>Spot-checking scaling and loads going out</li>
          <li>BMPs — stream-side management zones, road sets, erosion control</li>
          <li>Close-out walk: roads, decks, debris, ruts</li>
          <li>Final payment reconciliation</li>
        </ul>
        <h2>If you didn&rsquo;t list with me, I can still oversee</h2>
        <p>You don&rsquo;t have to have hired me as your sale consultant to bring me in for the harvest itself. Sometimes a landowner sells direct, signs a contract, and only after the fact realizes they want someone independent on the ground. That works too.</p>""",
        "right": """<h3>Why this matters</h3>
        <p>A timber crew is on your land for days or weeks. If nobody from your side ever sets foot on it during that window, you&rsquo;re taking it on faith that the contract gets honored. Some crews are fine. Some are not. Oversight removes the guessing.</p>
        <h3>Related</h3>
        <ul class="checks">
          <li><a href="/timber/sale-consulting/">Timber sale consulting</a></li>
          <li><a href="/timber/management/">Management plans</a></li>
          <li><a href="/land/">Post-harvest land cleanup</a></li>
        </ul>""",
        "cta_h2": "Bring me in for the harvest.",
        "cta_body": "<p>Tell me when the harvest is scheduled and where the land is. I&rsquo;ll be there when it counts.</p>",
    },
]


def build_timber_sub_pages():
    for p in TIMBER_SUB:
        body = service_hero(p["eyebrow"], p["h1"], p["lede"], "Get a Free Timber Evaluation", "timber", icon=p.get("icon"))
        body += two_col(p["left"], p["right"])
        body += dark_cta(p["cta_h2"], p["cta_body"], "Get a Free Timber Evaluation", "timber")
        breadcrumb = [("Home", "/"), ("Timber", "/timber/"), (p["h1"], p["slug"])]
        extra = service_jsonld(p["h1"], p["description"], p["slug"])
        render(p["slug"], p["title"], p["description"], body, extra, breadcrumb=breadcrumb)


# --- Service area -------------------------------------------------------------

def build_service_area():
    body = """<section class="hero hero-illustrated"><div class="wrap">
  <div>
    <p class="eyebrow-line">Service area</p>
    <h1>Polk County is home. Six counties is the working radius.</h1>
    <p class="lede">Based in Livingston, working the Lake Livingston shoreline and the surrounding Piney Woods. Local trip — no hidden charge for driving in.</p>
  </div>
  <div class="hero-art">""" + SVGS["compass"] + """</div>
</div></section>

<section><div class="wrap two-col">
  <div>
    <h2>Polk County (home)</h2>
    <p>Livingston, Onalaska, Goodrich, Corrigan, Leggett, Camden, Moscow, Seven Oaks, Indian Springs, Big Thicket, and the Lake Livingston shoreline. This is where I&rsquo;m based and where most jobs are.</p>

    <h2>Surrounding counties</h2>
    <ul class="checks">
      <li><strong>San Jacinto County</strong> — Coldspring, Point Blank, Oakhurst, the west side of Lake Livingston</li>
      <li><strong>Trinity County</strong> — Trinity, Groveton, Apple Springs, the northwest shoreline</li>
      <li><strong>Tyler County</strong> — Woodville, Colmesneil, Chester</li>
      <li><strong>Angelina County</strong> — Lufkin, Diboll, Huntington, Zavalla</li>
      <li><strong>Walker County</strong> — Huntsville, New Waverly (the same county the bigger out-of-area land-clearing outfits drive in from — we&rsquo;re happy to work it too)</li>
    </ul>
  </div>
  <div>
    <h3>Lake Livingston shoreline</h3>
    <p>The lake itself touches Polk, San Jacinto, Trinity, and Walker counties. I work all four sides. Lake lots are a specialty — sloped, erosion-prone, often inside an HOA. <a href="/land/lake-livingston-lots/">See lake lot clearing →</a></p>

    <h3>Outside the radius?</h3>
    <p>Ask. The right job is sometimes worth the trip. Tell me what it is and where, and I&rsquo;ll be straight about whether it&rsquo;s a fit.</p>
  </div>
</div></section>

<section class="section-bone"><div class="wrap">
  <h2>Why local matters</h2>
  <p>The biggest land-clearing outfit in the area is based in Walker County and openly drives 40+ minutes into Polk County for jobs. They&rsquo;re fine. But you&rsquo;re paying for that drive time, and you&rsquo;re not getting somebody who knows the difference between sandy upland and Trinity-bottom clay. Local matters here.</p>
</div></section>"""
    body += dark_cta("Call your county.",
                     "<p>Tell me where the property is and what you&rsquo;ve got. I&rsquo;ll tell you straight whether I&rsquo;m the right person for the job.</p>",
                     "Send a message", "both")
    render("/service-area/", "Service Area — Rowe Land, Timber & Dozer Services",
           "Polk County (Livingston, Onalaska, Lake Livingston) plus San Jacinto, Trinity, Tyler, Angelina, and Walker counties. Owner-operated, local trip.",
           body)


# --- Sitemap & build entry -----------------------------------------------------

# ---- Guides (informational / AEO-targeted) -----------------------------------

GUIDES = [
    # ---- Timber: how much is my timber worth ----
    {
        "slug": "/guides/how-much-is-my-timber-worth/",
        "title": "How Much Is My Timber Worth? East Texas Pricing Guide (2026)",
        "description": "Standing timber in East Texas typically sells for $8–$32 per ton depending on species, age, access, and market. Here's how the math really works.",
        "h1": "How much is my timber worth?",
        "eyebrow": "Timber pricing · East Texas",
        "category": "Timber",
        "icon": "pine",
        "answer": "<strong>Standing timber in East Texas typically sells in a range of about $8–$32 per ton at the stump</strong> depending on species, tree size, total volume, road access, and current mill demand. A 40-acre pine plantation ready for final harvest commonly nets $40,000–$120,000+ to the landowner, but the only way to know your number is a cruise — a walk-the-land volume estimate.",
        "body_html": """
<p>Most landowners hear two very different numbers about their timber. A buyer who knocks on the door gives one price. A consulting forester who puts the sale out to bid usually gets a higher one. The difference is sometimes 20–40%. Below is what actually drives the price — and why a free evaluation is the only way to know what you have.</p>

<h2>What determines timber value</h2>
<p>Six factors set the per-ton price more than anything else:</p>
<ol>
  <li><strong>Species mix.</strong> Pine sawtimber pays more than pine pulpwood. Hardwood sawtimber (oak, sweetgum, hickory) pays more again at the top end but moves slower.</li>
  <li><strong>Tree size and quality.</strong> Larger-diameter, straight, defect-free trees become sawtimber. Smaller or crooked trees go to pulpwood and chip mills at lower rates.</li>
  <li><strong>Volume.</strong> Bigger jobs attract more bidders and better prices. A 5-acre cut and an 80-acre cut behave like different markets.</li>
  <li><strong>Access.</strong> Frontage on a paved road, a good loading deck location, and no creek crossings can add $1–$3 per ton.</li>
  <li><strong>Distance to mill.</strong> Polk and surrounding counties feed multiple mills (pulp, OSB, sawmills), which generally helps prices.</li>
  <li><strong>Current market.</strong> Pulp prices, housing starts, and even weather move week to week. We refresh price ranges quarterly.</li>
</ol>

<h2>Rough East Texas ranges</h2>
<table>
  <thead><tr><th>Product</th><th>Typical range ($/ton)</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Pine sawtimber</td><td>$22–$32</td><td>Larger pine, &gt; ~12" DBH</td></tr>
    <tr><td>Pine chip-n-saw</td><td>$14–$22</td><td>Mid-size pine</td></tr>
    <tr><td>Pine pulpwood</td><td>$8–$14</td><td>Small pine, thinnings</td></tr>
    <tr><td>Hardwood sawtimber</td><td>$22–$45</td><td>Quality oak/hickory at the top</td></tr>
    <tr><td>Hardwood pulpwood</td><td>$5–$10</td><td>Low-grade, market-dependent</td></tr>
  </tbody>
</table>
<p class="source-note">Ranges based on East Texas regional reports and prevailing local-mill prices; updated quarterly. Texas A&amp;M Forest Service publishes statewide stumpage reports if you want to verify.</p>

<h2>How a per-acre estimate gets built</h2>
<p>Total payout per acre is <em>tons per acre × price per ton</em>. A mature pine plantation (25–30 years old, never thinned) might carry 100–150 tons per acre. At a blended $18/ton, that's $1,800–$2,700 per acre. A 40-acre block in that condition is in the $72,000–$108,000 range — <em>before</em> the difference a consultant can make on the sale.</p>

<h2>Why the same stand gets two different prices</h2>
<p>A buyer's job is to pay you less and resell to the mill at a margin. A consultant's job is the opposite. We put your sale out to multiple qualified buyers and let competitive bidding set the price. <a href="/timber/sale-consulting/">See how Rowe-managed timber sales work →</a></p>

<h2>What you can do today</h2>
<ul class="checks">
  <li>Walk your land and estimate the acreage in saleable timber</li>
  <li>Note rough tree size and species mix</li>
  <li>Check road access and any creek/wetland constraints</li>
  <li>Pull up the county appraisal record for total acres</li>
  <li>Call for a free evaluation — we'll come walk it and give you a real number</li>
</ul>
""",
        "faqs": [
            ("How much does a free timber evaluation cost?",
             "Nothing. We walk the land, give you an honest volume estimate, and a range of what it should bring at sale. You're under no obligation to list with us afterward."),
            ("How many tons per acre is normal?",
             "It varies wildly. Young pine thinnings might be 20–40 tons per acre. A mature unthinned pine plantation can carry 100–150+ tons. A natural hardwood bottom is harder to predict. A cruise gives you the real number."),
            ("Will my timber be worth more if I wait?",
             "Sometimes. Trees keep growing and adding volume, but prices fluctuate and severe weather, beetles, or fire can wipe out years of growth in a day. A consultant can model your specific stand and tell you whether it's at peak value now or worth holding."),
            ("How is timber sold — by the ton or by the tract?",
             "Both. Most sales today are by the ton with a written contract specifying boundaries, products, and price per product. Lump-sum sales (one flat price for the whole stand) still happen but expose the landowner to more measurement risk."),
            ("Does selling timber affect my property taxes?",
             "It can affect ag/wildlife valuation and income tax. Talk to your CPA before you sell. We can refer you to forestry-friendly accountants in the area."),
        ],
        "related": ["/guides/should-i-sell-my-timber/", "/guides/how-to-sell-timber-in-texas/", "/guides/timber-buyer-vs-consultant/", "/timber/sale-consulting/"],
        "cta": ("Get a Free Timber Evaluation", "timber"),
    },

    # ---- Timber: should I sell ----
    {
        "slug": "/guides/should-i-sell-my-timber/",
        "title": "Should I Sell My Timber? A Decision Guide for East Texas Landowners",
        "description": "The right time to harvest timber depends on stand age, market, and your land goals. Here's a straight-talk decision framework — and the signs to wait.",
        "h1": "Should I sell my timber?",
        "eyebrow": "Timber decision guide",
        "category": "Timber",
        "icon": "pine",
        "answer": "<strong>Sell when the stand is mature, the market is reasonable, and the timing fits your land plan</strong> — typically a final harvest of pine plantations at 25–35 years, or a commercial thinning every 8–12 years. <strong>Wait when the stand is young, prices are temporarily depressed, or you haven't had it cruised by someone working for you.</strong>",
        "body_html": """
<p>This is one of the highest-stakes decisions a rural landowner makes. The wrong sale leaves five figures on the table; the right one funds a build, pays off the land, or sets up the next 30 years.</p>

<h2>When selling probably makes sense</h2>
<ul class="checks">
  <li><strong>Pine plantation aged 25–35 years</strong> that's never had a final harvest</li>
  <li><strong>Overdue thinning</strong> — stands grown so thick that growth is stalling</li>
  <li><strong>Clearing for a build, pasture, or pond</strong> and the timber would otherwise become a brush pile</li>
  <li><strong>Salvaging beetle, wind, or fire damage</strong> before value disappears</li>
  <li><strong>Estate planning or sale of the land</strong> — selling timber separately can net more than selling the property with timber on it</li>
  <li><strong>You need the cash</strong> for a clear purpose and the stand is at or near maturity</li>
</ul>

<h2>When to wait</h2>
<ul class="checks">
  <li><strong>Young pine</strong> (under 15 years) — let it grow</li>
  <li><strong>You only have one offer</strong> — never sell without competitive bids</li>
  <li><strong>Local market is temporarily soft</strong> — sometimes 6–12 months changes the picture</li>
  <li><strong>You haven't had it cruised</strong> by someone independent of the buyer</li>
  <li><strong>You're emotionally undecided</strong> — pressure-selling is how landowners get hurt</li>
</ul>

<h2>The three numbers to know before you decide</h2>
<ol>
  <li><strong>Volume.</strong> Tons of pine sawtimber, chip-n-saw, pulpwood, hardwood — separately. Pulled from a cruise.</li>
  <li><strong>Current prices.</strong> Per-ton stumpage by product, in your area, this quarter. <a href="/guides/east-texas-pine-timber-prices/">See current East Texas pine prices →</a></li>
  <li><strong>Cleanup obligations.</strong> What does the contract require the buyer to leave behind? Roads, decks, debris, replant?</li>
</ol>

<h2>Red flags that mean wait</h2>
<ul class="checks">
  <li>A buyer offers you a flat lump sum &ldquo;today only&rdquo;</li>
  <li>They don't want a written contract or scaling records</li>
  <li>They scaled the stand &ldquo;by eye&rdquo; from the road</li>
  <li>The price seems too good (it usually is)</li>
  <li>The price seems too low (way more common)</li>
</ul>

<h2>How a consultant helps you make this call</h2>
<p>The Texas A&amp;M Forest Service's standing advice to landowners is to hire a consultant before you sell. <a href="/timber/sale-consulting/">See how Rowe-managed timber sales work</a> — we walk the land, run the numbers, give you the honest yes/no, and only list it if it's the right move for you.</p>
""",
        "faqs": [
            ("How old does pine need to be before final harvest?",
             "Most loblolly pine plantations in East Texas are harvested between 25 and 35 years old. Earlier if growth has stalled; later if you're managing for sawtimber premium. Thinnings happen along the way at roughly 12–15 and 18–22 years."),
            ("Can I sell timber and keep the land?",
             "Yes. Timber sales are separate from land sales. Most clients sell timber, replant or convert to pasture, and keep the property."),
            ("What happens to the land after the harvest?",
             "It's your call. Common options: replant pine, convert to pasture, leave for natural regeneration, build on it, or sell as raw land. A management plan covers this."),
            ("Is it better to clear-cut or thin?",
             "Depends on stand age and goals. Final harvest cuts everything; commercial thinning removes 30–50% of trees to let the rest grow. Most stands get thinned 1–2 times before final harvest."),
            ("How long does the actual harvest take?",
             "Most jobs in East Texas wrap in 1–4 weeks once a crew starts. Wet weather extends it. Bigger jobs run longer."),
        ],
        "related": ["/guides/how-much-is-my-timber-worth/", "/guides/how-to-sell-timber-in-texas/", "/timber/sale-consulting/", "/timber/management/"],
        "cta": ("Get a Free Timber Evaluation", "timber"),
    },

    # ---- Timber: how to sell ----
    {
        "slug": "/guides/how-to-sell-timber-in-texas/",
        "title": "How to Sell Timber in Texas — The 6-Step Process",
        "description": "Selling standing timber in Texas, step by step: cruise, contract, competitive bids, harvest oversight, payment, cleanup. What every landowner needs to know.",
        "h1": "How to sell timber in Texas",
        "eyebrow": "Process guide",
        "category": "Timber",
        "icon": "pine",
        "answer": "<strong>A proper Texas timber sale follows six steps:</strong> (1) walk the land and cruise the timber, (2) write a stand prescription and contract terms, (3) put the sale out to multiple qualified buyers, (4) sign a written contract before any cutting, (5) oversee the harvest, and (6) close out with cleanup and final payment. Skipping any of these is where landowners lose money.",
        "body_html": """
<p>The biggest mistakes in Texas timber sales aren't sophisticated — they're skipping basic steps because someone showed up with a check. Here's the right order, and why each step matters.</p>

<h2>Step 1 — Walk the land and cruise the timber</h2>
<p>A timber cruise is a systematic sample of the stand. Diameter at breast height, tree height, species, defects — pulled from enough plots to estimate total volume by product. A desktop quote off Google Maps is not a cruise.</p>

<h2>Step 2 — Decide what to sell and how</h2>
<p>Final harvest, commercial thinning, salvage, select cut. Each has different economics. <a href="/guides/should-i-sell-my-timber/">See should-I-sell decision guide →</a></p>

<h2>Step 3 — Put it out to multiple qualified buyers</h2>
<p>This is the single biggest price driver. Competitive bidding from 3+ qualified buyers routinely lifts the final price 15–40% over a single-buyer offer. The Texas A&amp;M Forest Service's <strong>Timber Theft Hotline (1-800-364-3470)</strong> exists because landowners who skip this step get underpaid.</p>

<h2>Step 4 — Written contract before a tree comes down</h2>
<p>The contract must specify:</p>
<ul class="checks">
  <li>Exact boundaries (often marked on the ground)</li>
  <li>Trees to leave (boundary trees, seed trees, riparian buffers)</li>
  <li>Volume estimate and price per product</li>
  <li>Payment schedule (most commonly weekly off mill scale tickets)</li>
  <li>BMPs — Best Management Practices for water quality</li>
  <li>Performance bond or escrow</li>
  <li>Cleanup standard at completion</li>
  <li>End date</li>
</ul>

<h2>Step 5 — Harvest oversight</h2>
<p>Someone independent of the buyer needs to be on the land while it's being cut. Boundaries can drift. Trees that were supposed to be left can disappear. Loads can be miscounted. <a href="/timber/harvest/">See harvest oversight →</a></p>

<h2>Step 6 — Close out, payment, cleanup</h2>
<ul class="checks">
  <li>Reconcile scale tickets to contract price</li>
  <li>Walk the closeout — roads, decks, ruts, debris</li>
  <li>Settle final payment</li>
  <li>Decide on replant, pasture conversion, or natural regen</li>
</ul>

<h2>Tax and ag-valuation</h2>
<p>Timber sales are taxable. Most landowners qualify for long-term capital gains treatment if the timber has been held over a year, but the rules are specific. Talk to a CPA who knows forestry. Also: a poorly timed cut can affect your ag/wildlife valuation. Plan ahead.</p>
""",
        "faqs": [
            ("Do I need a real estate license or forestry license to sell my timber?",
             "No. You can sell your own timber directly. A licensed consultant can represent you, but it's not legally required."),
            ("What's a stumpage price vs. delivered price?",
             "Stumpage is what the landowner gets per ton for trees standing in the woods. Delivered is what the buyer pays the mill per ton at the mill gate. The difference covers cutting, hauling, and the buyer's margin."),
            ("Can I sell timber to multiple buyers at once?",
             "Not the same trees, but you can split a tract into blocks and sell separately if it makes economic sense. More common: one buyer wins competitive bidding for the whole job."),
            ("How is the volume measured?",
             "Today most jobs are paid by mill scale — the weight of each truck delivered to the mill, recorded on scale tickets. The contract specifies which mill(s) and how scale tickets are reconciled to landowner payment."),
            ("How long from first call to a check in my hand?",
             "Typical timeline: 1–2 weeks to cruise, 2–4 weeks to bid and sign, 2–8 weeks to harvest, 1–4 weeks of payments depending on volume. Total: 2–4 months from start to final payment is common."),
        ],
        "related": ["/guides/should-i-sell-my-timber/", "/guides/how-much-is-my-timber-worth/", "/guides/timber-buyer-vs-consultant/", "/timber/sale-consulting/"],
        "cta": ("Get a Free Timber Evaluation", "timber"),
    },

    # ---- Timber: buyer vs consultant — the differentiator ----
    {
        "slug": "/guides/timber-buyer-vs-consultant/",
        "title": "Timber Buyer vs. Timber Consultant — What's the Difference?",
        "description": "A timber buyer works for themselves and pays you less. A timber consultant works for you and gets you competitive bids. Here's why it matters for your sale.",
        "h1": "Timber buyer vs. timber consultant",
        "eyebrow": "Compare",
        "category": "Timber",
        "icon": "pine",
        "answer": "<strong>A timber buyer purchases your trees to resell at a margin — their incentive is to pay you less. A timber consultant works for the landowner, runs a competitive sale on your behalf, and gets paid a percentage of what your timber actually sells for — their incentive is to get you more.</strong> Texas A&amp;M Forest Service formally recommends using a consultant for any significant sale.",
        "body_html": """
<p>This is the single most important distinction in a timber sale. The two roles look similar from the outside — both have business cards that say &ldquo;timber.&rdquo; They sit on opposite sides of the table.</p>

<h2>Quick comparison</h2>
<table>
  <thead><tr><th></th><th>Timber buyer</th><th>Timber consultant</th></tr></thead>
  <tbody>
    <tr><td><strong>Who they work for</strong></td><td>Themselves / the mill</td><td>You, the landowner</td></tr>
    <tr><td><strong>How they get paid</strong></td><td>Margin between what they pay you and what they sell to the mill</td><td>Percentage (typically 8–12%) of the sale price they negotiate for you</td></tr>
    <tr><td><strong>Their incentive on price</strong></td><td>Pay you less</td><td>Get you more</td></tr>
    <tr><td><strong>Who runs the cruise</strong></td><td>They do, usually for themselves</td><td>They do, on your behalf — and you see the numbers</td></tr>
    <tr><td><strong>Bidding</strong></td><td>One buyer, take-it-or-leave-it</td><td>Multiple buyers, competitive bids</td></tr>
    <tr><td><strong>Contract</strong></td><td>Their standard contract</td><td>Negotiated terms in your favor</td></tr>
    <tr><td><strong>On-site during harvest</strong></td><td>Their crew, no one watching for you</td><td>Consultant oversees on your behalf</td></tr>
    <tr><td><strong>Typical price difference</strong></td><td>Baseline</td><td>15–40% higher in most cases</td></tr>
  </tbody>
</table>

<h2>Why the price gap is real</h2>
<p>Competitive bidding is the single biggest price driver in a timber sale. A landowner alone usually gets one offer. A consultant routinely runs three to seven qualified buyers against each other on the same stand. The top bid often comes in 15–40% above the lone &ldquo;knock on the door&rdquo; offer.</p>
<p>On a 40-acre pine harvest that might have netted $80,000 from a direct sale to a buyer, a consultant-run sale netting 25% more is an extra $20,000 — minus a consultant's 10% fee, the landowner still nets ~$92,000 vs $80,000.</p>

<h2>When a direct sale to a buyer is fine</h2>
<ul class="checks">
  <li>Very small volume — a few trees for a personal sawmill</li>
  <li>You already know the buyer well and trust them</li>
  <li>Salvage situation with one mill nearby</li>
</ul>

<h2>When you should hire a consultant</h2>
<ul class="checks">
  <li>Stand is over ~10 acres</li>
  <li>You've never done a timber sale before</li>
  <li>You inherited the land and don't know what's on it</li>
  <li>Someone knocked on your door with an offer</li>
  <li>You're clearing for a build and want to capture timber value first</li>
</ul>

<h2>What about an &ldquo;independent contractor&rdquo; or a logger who says they'll get you a fair price?</h2>
<p>Ask three questions: (1) Who pays you? (2) Will you put my sale out to bid? (3) Will you put it in writing? If the answers are <em>the mill pays me</em>, <em>no</em>, and <em>no</em>, they're a buyer, not a consultant. Both are valid jobs — they're just different jobs.</p>

<h2>The role Texas A&amp;M tells landowners to hire</h2>
<p>The State of Texas, through Texas A&amp;M Forest Service, formally recommends that landowners hire a consulting forester before a significant timber sale, insist on competitive bids, and get the agreement in writing. The Forest Service also operates a <strong>Timber Theft Hotline at 1-800-364-3470</strong> specifically because the buyer-landowner imbalance is well documented.</p>
""",
        "faqs": [
            ("Are you a forester or a buyer?",
             "I work as a consultant for the landowner. My job is to get you the best price for your timber — I never buy your timber directly. I also handle the dozer side of land work if you want one company for the whole job."),
            ("How much does a consultant cost?",
             "Typically 8–12% of the final sale price. The fee is paid out of the proceeds, so it's effectively self-funding — and the higher price competitive bidding produces usually more than covers it."),
            ("What if I already have an offer in hand?",
             "Bring it. We can evaluate whether it's a fair offer for your stand before you sign anything. If it is, great. If it's low, we can run a quick bid against it and see what the market actually pays."),
            ("Do consultants have to be licensed in Texas?",
             "Texas doesn't license consulting foresters specifically — anyone can call themselves one. That's why credentials, references, and a clear written agreement matter."),
            ("Will the same consultant who lists my sale also do the cleanup?",
             "Some do, some don't. We do — because we run the dozer side too. One contract, one company from cruise to clean ground."),
        ],
        "related": ["/timber/sale-consulting/", "/guides/how-much-is-my-timber-worth/", "/guides/should-i-sell-my-timber/", "/guides/how-to-sell-timber-in-texas/"],
        "cta": ("Get a Free Timber Evaluation", "timber"),
    },

    # ---- Timber: East Texas pine prices ----
    {
        "slug": "/guides/east-texas-pine-timber-prices/",
        "title": "East Texas Pine Timber Prices — Current Stumpage Ranges",
        "description": "Current per-ton stumpage prices for East Texas pine sawtimber, chip-n-saw, and pulpwood. Updated quarterly. Plus what moves the market.",
        "h1": "East Texas pine timber prices",
        "eyebrow": "Prices · Updated quarterly",
        "category": "Timber",
        "icon": "pine",
        "answer": "<strong>Current East Texas pine stumpage prices run roughly: pine sawtimber $22–$32/ton, pine chip-n-saw $14–$22/ton, pine pulpwood $8–$14/ton.</strong> Hardwood sawtimber ranges $22–$45/ton depending on species and grade. Prices vary by tract size, road access, distance to mill, and current mill demand.",
        "body_html": """
<p>These ranges reflect typical Polk, San Jacinto, Trinity, Tyler, Angelina, and Walker county sales — and update with the market. Your specific stand could fall above or below depending on the factors covered <a href="/guides/how-much-is-my-timber-worth/">in the timber value guide</a>.</p>

<h2>Pine stumpage — per-ton ranges</h2>
<table>
  <thead><tr><th>Product</th><th>Range ($/ton)</th><th>Typical use</th></tr></thead>
  <tbody>
    <tr><td>Pine sawtimber</td><td>$22–$32</td><td>Lumber at sawmills</td></tr>
    <tr><td>Pine chip-n-saw</td><td>$14–$22</td><td>Smaller lumber + chips</td></tr>
    <tr><td>Pine pulpwood</td><td>$8–$14</td><td>Paper / OSB mills</td></tr>
    <tr><td>Pine plylogs</td><td>$26–$36</td><td>Plywood mills (where accessible)</td></tr>
  </tbody>
</table>

<h2>Hardwood stumpage — per-ton ranges</h2>
<table>
  <thead><tr><th>Product</th><th>Range ($/ton)</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Mixed hardwood sawtimber</td><td>$22–$35</td><td>Sweetgum, hickory, mixed</td></tr>
    <tr><td>Premium hardwood (oak)</td><td>$30–$45+</td><td>Quality oak veneer at the top</td></tr>
    <tr><td>Hardwood pulpwood</td><td>$5–$10</td><td>Pulpmill / chipmill</td></tr>
  </tbody>
</table>

<h2>What's moving prices right now</h2>
<ul class="checks">
  <li><strong>Housing starts</strong> drive sawtimber demand</li>
  <li><strong>OSB and pulpmill capacity</strong> sets pulp prices</li>
  <li><strong>Mill weather and seasonal swings</strong> tighten or loosen capacity</li>
  <li><strong>Local logger availability</strong> can swing prices week to week</li>
</ul>

<h2>How to use these numbers</h2>
<p>Multiply expected tons per acre by the per-ton range. A mature pine plantation often carries 100–150 tons per acre. At a blended $18/ton, that's $1,800–$2,700 per acre. Use the bottom of the range for conservative planning.</p>

<h2>The number that actually matters</h2>
<p>The above ranges are <em>averages</em>. Your specific stand has a specific number. A free cruise is the only way to find out. <a href="/timber/sale-consulting/">See how a Rowe-managed sale works →</a></p>

<p class="source-note">Updated quarterly. We pull from Texas A&amp;M Forest Service stumpage reports, prevailing mill prices, and local sale-comparable data. Ranges shown are at-the-stump (what the landowner gets), not delivered-to-mill prices.</p>
""",
        "faqs": [
            ("Are these prices going up or down?",
             "Pulp has been softer than 2022 highs but stable through 2025-26. Sawtimber tracks housing starts and is in a normal range. Hardwood premium grades are firm. Check back quarterly for updates."),
            ("Does my tract size affect the per-ton price?",
             "Yes. Larger tracts attract more bidders and better unit prices. A 5-acre cut typically prices below a 40-acre cut at the same stand quality."),
            ("Does road access really make $1–3/ton difference?",
             "Yes — and sometimes more. Buyers price in trucking efficiency. A paved-road frontage tract with a clear loading deck is materially cheaper to log than one requiring a long, soft pull-out."),
            ("How is per-ton price agreed before harvest?",
             "Either: (a) lump-sum sale where the buyer pays a single negotiated total, or (b) per-product per-ton sale paid off mill scale tickets. Per-ton off scale is more common today and protects both sides."),
            ("Where do you source these price ranges?",
             "Texas A&M Forest Service publishes statewide stumpage reports. We supplement with local mill conversations and the actual sales we close. We refresh the ranges quarterly."),
        ],
        "related": ["/guides/how-much-is-my-timber-worth/", "/guides/should-i-sell-my-timber/", "/timber/sale-consulting/"],
        "cta": ("Get a Free Timber Evaluation", "timber"),
    },

    # ---- Land: clearing cost per acre ----
    {
        "slug": "/guides/land-clearing-cost-per-acre-texas/",
        "title": "Land Clearing Cost Per Acre in Texas — 2026 Pricing Guide",
        "description": "Land clearing in Texas typically runs $1,500–$6,500 per acre depending on density, tree size, terrain, and method. Here's how the math breaks down.",
        "h1": "Land clearing cost per acre in Texas",
        "eyebrow": "Cost guide",
        "category": "Land & Dozer",
        "icon": "dozer",
        "answer": "<strong>Land clearing in Texas typically runs $1,500–$6,500 per acre</strong>, with the most common East Texas projects landing in the $2,500–$4,500 range. The four biggest cost drivers are tree density, average tree size, terrain (slope, wet/dry, accessibility), and method (mulching vs. push-and-pile vs. selective).",
        "body_html": """
<p>Per-acre clearing prices vary more than almost any other contracting job. The same dollar figure can buy wildly different work — from light underbrush mulching to dozer-pushed pine and hardwood with stump removal. This guide breaks down what drives the number, with East Texas–specific ranges.</p>

<h2>Typical East Texas per-acre ranges by method</h2>
<table>
  <thead><tr><th>Method</th><th>Per-acre range</th><th>Best for</th></tr></thead>
  <tbody>
    <tr><td>Forestry mulching, light brush</td><td>$1,500–$2,800</td><td>Under-story, small trees up to ~6&Prime;</td></tr>
    <tr><td>Forestry mulching, moderate</td><td>$2,500–$4,500</td><td>Mixed pine/hardwood up to ~8&Prime;</td></tr>
    <tr><td>Dozer clearing + piling, no stumps</td><td>$2,800–$4,800</td><td>Pasture conversion, light timber</td></tr>
    <tr><td>Dozer clearing + stumps + grade</td><td>$3,800–$6,500</td><td>Building pads, full clean</td></tr>
    <tr><td>Selective hand + machine</td><td>$3,500–$7,000</td><td>Lake lots, keep specific trees</td></tr>
  </tbody>
</table>

<h2>What pushes you up the range</h2>
<ul class="checks">
  <li><strong>Heavy timber</strong> — large pine and hardwood take longer and require bigger machines</li>
  <li><strong>Stumps</strong> — grinding or pulling stumps doubles the per-acre time</li>
  <li><strong>Wet ground</strong> — clay bottoms in winter add days; rescheduling is common</li>
  <li><strong>Sloped land</strong> — Lake Livingston lots especially; erosion control adds cost</li>
  <li><strong>Restricted access</strong> — narrow gates, soft soils, neighbors' fences</li>
  <li><strong>Burn vs. haul-off vs. mulch in place</strong> — disposal choice affects price</li>
  <li><strong>Finish grade required</strong> — &ldquo;cleared&rdquo; vs. &ldquo;build-ready&rdquo; are different jobs</li>
</ul>

<h2>What can pull you down the range</h2>
<ul class="checks">
  <li>Open pasture with scattered brush rather than continuous canopy</li>
  <li>Small/light vegetation suitable for mulching alone</li>
  <li>Mulched-in-place disposal (no haul-off)</li>
  <li>Large continuous tracts (better per-acre economics)</li>
  <li>Dry weather scheduling</li>
</ul>

<h2>The hidden costs people forget</h2>
<ul class="checks">
  <li><strong>Stump removal</strong> — often not in the base price</li>
  <li><strong>Burn permits</strong> and tending</li>
  <li><strong>Erosion control</strong> after clearing, especially on slopes</li>
  <li><strong>Driveways and culverts</strong> needed to get equipment in</li>
  <li><strong>Replant or seed</strong> for pasture or pine</li>
  <li><strong>Mobilization</strong> if the crew is coming from far away (one reason to hire local)</li>
</ul>

<h2>If your land has marketable timber on it</h2>
<p>Don't pay to clear timber you could be paid for. Even small stands of mature pine can offset clearing costs significantly. <a href="/timber/sale-consulting/">See timber sale consulting →</a> first, then clear.</p>

<h2>What we typically recommend</h2>
<p>For most projects: walk the site with us, identify what method fits, get a real per-acre number based on what's actually there. <a href="/contact/?type=land">Free estimate →</a></p>
""",
        "faqs": [
            ("What's the cheapest way to clear an acre?",
             "Forestry mulching on light brush, mulched in place with no stump work — typically $1,500–$2,500/acre on the low end. But it only works on appropriate stands."),
            ("Is push-and-pile or mulching cheaper?",
             "Mulching is often cheaper on lighter vegetation (no burn, no haul). Dozer push-and-pile is usually cheaper when you have heavy timber and large stumps and want everything gone. The right choice depends on the site."),
            ("How long does it take to clear an acre?",
             "Light mulching: 0.5–1 hour per acre. Mixed brush + small trees: 2–4 hours. Heavy timber with stumps: 6–12+ hours per acre, plus follow-up grading."),
            ("Do I need a burn permit in Polk County?",
             "Often yes, especially during burn bans. We handle the conversation with the county or the Texas A&M Forest Service before any burn pile work."),
            ("Will clearing cause erosion on my Lake Livingston lot?",
             "It can, badly, if done wrong. Sloped lakefront lots need careful staging, kept buffers, and active runoff control during and after clearing. See our Lake Livingston lot page."),
        ],
        "related": ["/guides/forestry-mulching-cost/", "/guides/forestry-mulching-vs-land-clearing/", "/land/land-clearing/", "/land/lake-livingston-lots/"],
        "cta": ("Get a Free Estimate", "land"),
    },

    # ---- Land: forestry mulching cost ----
    {
        "slug": "/guides/forestry-mulching-cost/",
        "title": "Forestry Mulching Cost in Texas — What to Expect Per Acre",
        "description": "Forestry mulching in Texas typically costs $1,500–$4,500 per acre, with most jobs landing $2,000–$3,500. Here's what determines the number.",
        "h1": "Forestry mulching cost",
        "eyebrow": "Cost guide",
        "category": "Land & Dozer",
        "icon": "mulcher",
        "answer": "<strong>Forestry mulching in Texas typically costs $1,500–$4,500 per acre.</strong> Light underbrush jobs run $1,500–$2,500. Moderate brush with small trees runs $2,500–$3,500. Heavy mixed pine and hardwood up to ~8″ runs $3,500–$4,500. Per-hour pricing is also common — typically $175–$275/hr — for irregular small jobs.",
        "body_html": """
<p>Forestry mulching is often the most cost-effective way to clear underbrush, small trees, and trail corridors in East Texas. It's also priced very differently depending on what's actually growing on your land.</p>

<h2>Per-acre vs. per-hour pricing</h2>
<p>Large continuous jobs are usually quoted per acre. Small or irregular jobs — trail clearing, fence lines, hand-shape work — are often quoted per hour or per job. East Texas hourly rates typically run $175–$275/hr for a mulching machine and operator.</p>

<h2>Per-acre ranges</h2>
<table>
  <thead><tr><th>Density</th><th>Per-acre range</th><th>Example use</th></tr></thead>
  <tbody>
    <tr><td>Light underbrush</td><td>$1,500–$2,500</td><td>Pasture cleanup, scattered yaupon</td></tr>
    <tr><td>Moderate brush + small trees</td><td>$2,500–$3,500</td><td>Reclaiming overgrown pasture</td></tr>
    <tr><td>Heavy mixed brush/trees to 6″</td><td>$3,000–$4,000</td><td>Selective clearing, hunting lanes</td></tr>
    <tr><td>Heavy timber to ~8″</td><td>$3,500–$4,500</td><td>Larger tree mulching</td></tr>
  </tbody>
</table>

<h2>When mulching is the right tool</h2>
<ul class="checks">
  <li>Underbrush and small-diameter trees up to ~8″</li>
  <li>Selective clearing where mature trees stay</li>
  <li>Trail and ATV lane creation</li>
  <li>Fence-line and survey-line maintenance</li>
  <li>Wildfire fuel reduction around a home</li>
  <li>Recreational properties where appearance matters</li>
</ul>

<h2>When mulching alone isn't enough</h2>
<ul class="checks">
  <li>Heavy hardwood over ~10″ — slow to mulch, faster to dozer</li>
  <li>Stump removal needed for a build pad</li>
  <li>Final grade required after</li>
  <li>Complete clear-cut where everything goes</li>
</ul>

<h2>Why mulching can save money</h2>
<p>No burn piles (no burn permits, no smoke, no fire-watch labor). No haul-off (mulch stays on the ground as nutrient cover). One-pass machine instead of multiple equipment moves. Lower ground disturbance means less erosion remediation later.</p>

<h2>When dozer + mulcher together is the right call</h2>
<p>Plenty of jobs need both: dozer for heavier trees and stumps, mulcher for selective finish work and edges. The right pricing model for those jobs is a project quote, not a flat per-acre number. <a href="/contact/?type=land">Walk-the-land estimate →</a></p>
""",
        "faqs": [
            ("Is forestry mulching cheaper than traditional clearing?",
             "For light-to-moderate brush and small trees, usually yes — no burn piles, no haul-off, fewer equipment moves. For heavy timber with stumps, dozer-based clearing is often cheaper."),
            ("How thick can a forestry mulcher cut?",
             "Most mulchers handle trees up to about 8″ diameter efficiently. Above that, mulching gets slow and a dozer becomes more cost-effective."),
            ("Does mulching kill the roots?",
             "It cuts to ground level. Many species re-sprout from roots. For permanent clearing, you'll want stump grinding or a follow-up herbicide depending on the site."),
            ("Will the mulch help my soil?",
             "Yes — it acts as organic cover that slows erosion, holds moisture, and breaks down into the soil over a few seasons."),
            ("How long does a one-acre mulching job take?",
             "Light brush: ~1–2 hours. Heavy small-tree stands: 4–6+ hours per acre. The hour-per-acre number is a useful planning shortcut."),
        ],
        "related": ["/guides/land-clearing-cost-per-acre-texas/", "/guides/forestry-mulching-vs-land-clearing/", "/land/forestry-mulching/"],
        "cta": ("Get a Free Estimate", "land"),
    },

    # ---- Land: mulching vs clearing comparison ----
    {
        "slug": "/guides/forestry-mulching-vs-land-clearing/",
        "title": "Forestry Mulching vs. Land Clearing — Which Do You Need?",
        "description": "Forestry mulching is selective and low-impact. Traditional land clearing is total removal with dozer and burn piles. Here's how to pick.",
        "h1": "Forestry mulching vs. land clearing",
        "eyebrow": "Compare",
        "category": "Land & Dozer",
        "icon": "mulcher",
        "answer": "<strong>Choose forestry mulching when you want to keep mature trees, leave the ground covered, and clear underbrush or small trees up to ~8″. Choose traditional land clearing (dozer push-and-pile or push-and-burn) when you need everything gone, stumps removed, and the ground graded.</strong>",
        "body_html": """
<p>The two are not interchangeable. Each one solves a different problem, and using the wrong tool wastes money on both sides — too expensive for the light job, too slow for the heavy one. Quick comparison:</p>

<table>
  <thead><tr><th></th><th>Forestry mulching</th><th>Traditional land clearing</th></tr></thead>
  <tbody>
    <tr><td><strong>What it removes</strong></td><td>Underbrush, small trees up to ~8″</td><td>Everything — trees, stumps, brush</td></tr>
    <tr><td><strong>What it leaves</strong></td><td>Mulched ground cover</td><td>Bare or graded soil</td></tr>
    <tr><td><strong>Stumps</strong></td><td>Left in ground at ground level</td><td>Pushed, piled, or ground out</td></tr>
    <tr><td><strong>Burn piles</strong></td><td>None</td><td>Usually yes (or haul-off)</td></tr>
    <tr><td><strong>Ground disturbance</strong></td><td>Low</td><td>High</td></tr>
    <tr><td><strong>Erosion risk</strong></td><td>Low</td><td>Higher; needs runoff control</td></tr>
    <tr><td><strong>Best for</strong></td><td>Selective clearing, trails, fire breaks</td><td>Build pads, full conversion, pasture</td></tr>
    <tr><td><strong>Typical cost/acre</strong></td><td>$1,500–$4,500</td><td>$2,800–$6,500</td></tr>
  </tbody>
</table>

<h2>When to mulch</h2>
<ul class="checks">
  <li>You want to keep canopy trees and clean out everything below</li>
  <li>Lake Livingston lots where erosion matters</li>
  <li>Trails, ATV lanes, hunting access</li>
  <li>Fence lines and survey lines</li>
  <li>Wildfire fuel reduction around a home</li>
  <li>Recreational property where look-and-feel matters</li>
</ul>

<h2>When to clear</h2>
<ul class="checks">
  <li>You need a build pad</li>
  <li>Converting woods to pasture</li>
  <li>Heavy hardwood that mulchers can't handle efficiently</li>
  <li>Stumps need to be gone</li>
  <li>You want a finish grade ready for construction</li>
</ul>

<h2>The hybrid play</h2>
<p>Plenty of jobs use both. Dozer takes the big trees and stumps; mulcher does selective edges, slopes, and finish work. Right machine for each part of the job. We run both.</p>

<h2>What about timber sale first?</h2>
<p>If you have marketable pine or hardwood on it, don't pay either method to destroy value. <a href="/timber/sale-consulting/">Sell the timber first →</a>, then clear or mulch what's left.</p>
""",
        "faqs": [
            ("Can you mulch a 20-acre tract in a day?",
             "Generally no. Light brush runs about an hour per acre, but moderate-to-heavy density is closer to 4–8 hours per acre. A 20-acre moderate-density job is typically 2–5 days."),
            ("Will mulching kill blackberry, yaupon, and similar regrowth?",
             "It cuts them flat. Without herbicide follow-up, most resprout from the root system. Mulching is a knock-down, not a kill."),
            ("Can I do both — mulch the edges, dozer the middle?",
             "Yes, and it's often the most cost-effective plan on mixed sites. We quote those as project jobs rather than flat per-acre."),
            ("Which is better for hunting habitat?",
             "Mulching, almost always. It keeps mature canopy, creates edge habitat, leaves cover and food on the ground, and opens lanes without scraping the land."),
            ("Do I need a permit for either one?",
             "Usually not for clearing your own property in Polk County and surrounding rural counties. Wetlands, near-water work, and burn piles are the common exceptions. Always check before you start."),
        ],
        "related": ["/guides/forestry-mulching-cost/", "/guides/land-clearing-cost-per-acre-texas/", "/land/forestry-mulching/", "/land/land-clearing/"],
        "cta": ("Get a Free Estimate", "land"),
    },
]


def build_guide(g):
    related_html = "".join(f'<li><a href="{u}">{u.strip("/").replace("guides/", "").replace("-", " ").title()}</a></li>' for u in g["related"])
    cta_label, cta_type = g["cta"]
    art = SVGS.get(g.get("icon", ""), "")
    art_html = f'<div class="hero-art">{art}</div>' if art else ""
    hero_class = "hero hero-illustrated" if art_html else "hero"

    body = f'''<section class="{hero_class}"><div class="wrap">
  <div>
    <p class="eyebrow-line">{g["eyebrow"]}</p>
    <h1>{g["h1"]}</h1>
    <p class="meta">Updated June 2026 · By Bob Rowe, Rowe Land, Timber &amp; Dozer Services</p>
  </div>
  {art_html}
</div></section>

<section><div class="wrap guide-body">
<div class="answer-box">{g["answer"]}</div>
{g["body_html"]}
<h2>Related</h2>
<ul class="checks">{related_html}</ul>
</div></section>
'''

    body += faq_html(g["faqs"])
    body += dark_cta(
        f"Free consultation on your specific land.",
        f"<p>Every property is different. Tell us where the land is and what you&rsquo;re thinking. We&rsquo;ll come walk it and give you a real number.</p>",
        cta_label, cta_type,
    )

    extra = article_jsonld(g["h1"], g["description"], g["slug"]) + faq_jsonld(g["faqs"])
    breadcrumb = [("Home", "/"), ("Guides", "/guides/"), (g["h1"], g["slug"])]
    render(g["slug"], g["title"], g["description"], body, extra, breadcrumb=breadcrumb)


def build_guides():
    for g in GUIDES:
        build_guide(g)


def build_guides_index():
    cards = "".join(
        f'<article class="guide-card"><p class="eyebrow">{g["category"]}</p>'
        f'<h3><a href="{g["slug"]}">{g["h1"]}</a></h3>'
        f'<p>{g["description"]}</p></article>'
        for g in GUIDES
    )
    body = f'''<section class="hero"><div class="wrap">
  <p class="eyebrow-line">Guides &amp; pricing</p>
  <h1>Straight answers about timber and land work in East Texas.</h1>
  <p class="lede">No fluff, no upsell. Just the questions landowners actually ask before they sign anything — answered in plain English with real numbers.</p>
</div></section>

<section><div class="wrap">
<div class="guides-grid">{cards}</div>
</div></section>
'''
    breadcrumb = [("Home", "/"), ("Guides", "/guides/")]
    render("/guides/", "Guides — Rowe Land, Timber & Dozer Services",
           "Plain-English guides to selling timber, land clearing costs, forestry mulching, and East Texas land work.",
           body, breadcrumb=breadcrumb)


# ---- URL list for sitemap ----------------------------------------------------

ALL_URLS = [
    "/",
    "/timber/",
    "/timber/sale-consulting/",
    "/timber/management/",
    "/timber/harvest/",
    "/land/",
    "/land/land-clearing/",
    "/land/forestry-mulching/",
    "/land/dozer-grading/",
    "/land/ponds/",
    "/land/lake-livingston-lots/",
    "/land/roads-pads-drainage/",
    "/service-area/",
    "/guides/",
] + [g["slug"] for g in GUIDES] + [
    "/about/",
    "/contact/",
]


def build_sitemap():
    urls = "\n".join(f"  <url><loc>{CANONICAL_BASE}{u}</loc></url>" for u in ALL_URLS)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    (SITE_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("  wrote /sitemap.xml")


def main():
    print(f"Building Rowe site → {SITE_DIR}  (DEV_NOINDEX={DEV_NOINDEX})")
    build_home()
    build_timber_pillar()
    build_land_pillar()
    build_land_sub_pages()
    build_timber_sub_pages()
    build_service_area()
    build_about()
    build_contact()
    build_thank_you()
    build_404()
    build_guides_index()
    build_guides()
    build_sitemap()
    print("Done.")


if __name__ == "__main__":
    main()
