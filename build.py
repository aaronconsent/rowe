#!/usr/bin/env python3
"""Build the Rowe site from a manifest. Static HTML in/out.

Run: python3 build.py
Writes pages into site/ at the slugs defined below.
"""
from pathlib import Path

SITE_DIR = Path(__file__).parent / "site"

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
<link rel="stylesheet" href="/assets/css/site.css">
<meta name="theme-color" content="#2a4a32">
{extra_jsonld}
</head>
<body>"""

HEADER = f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">Rowe Land, Timber &amp; Dozer<small>Livingston, TX · Polk County</small></a>
    <nav class="nav">
      <a href="/timber/">Timber</a>
      <a href="/land/">Land &amp; Dozer</a>
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

# ---- Page helpers ------------------------------------------------------------

def service_hero(eyebrow: str, h1: str, lede: str, cta_label: str, cta_type: str, cta_class: str = "btn") -> str:
    return f"""<section class="hero">
  <div class="wrap">
    <p class="eyebrow-line">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <p><a class="{cta_class}" href="/contact/?type={cta_type}">{cta_label}</a> &nbsp; <a class="btn ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p>
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

def render(slug: str, title: str, description: str, body: str, extra_jsonld: str = "") -> None:
    out = SITE_DIR / slug.strip("/") / "index.html" if slug != "/" else SITE_DIR / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = head(title, description, slug, extra_jsonld) + HEADER + body + FOOTER
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
        <p class="eyebrow">Own forested land?</p>
        <h2>Selling or harvesting timber</h2>
        <p>Most buyers work for themselves. I work for you — making sure your timber is measured honestly, bid competitively, and sold for what it&rsquo;s actually worth.</p>
        <a class="btn" href="/timber/">Get a Free Timber Evaluation</a>
      </div>
      <div class="path">
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
    <a class="btn ghost" href="tel:{PHONE_TEL}" style="color:var(--gold);border-color:var(--gold)">Call {PHONE_DISPLAY}</a>
  </p>
</div></section>"""
    render("/", "Rowe Land, Timber & Dozer Services — Livingston, TX",
           "Polk County's local land, timber, and dozer outfit. We clear, grade, and prep your land — and when it's time to sell timber, we work for you, not the buyer.",
           body, LOCALBUSINESS_JSONLD)


def build_timber_pillar():
    body = service_hero(
        "For landowners · Polk County &amp; East Texas",
        "What&rsquo;s your timber actually worth?",
        "Selling standing timber is a once-or-twice-in-a-lifetime decision, and landowners get lowballed every day in East Texas. I&rsquo;ll walk your land, give you an honest evaluation, and represent <em>your</em> side of the sale — not the buyer&rsquo;s.",
        "Get a Free Timber Evaluation", "timber"
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
    render("/timber/", "Timber Sales & Consulting in Polk County, TX — Rowe Land, Timber & Dozer",
           "Selling standing timber in Polk County or around Lake Livingston? Get an honest evaluation and a consultant who works for you — not the buyer.",
           body)


def build_land_pillar():
    body = service_hero(
        "Polk County · Lake Livingston · East Texas",
        "From raw timber to build-ready ground.",
        "Dozer, forestry mulcher, excavator, and dump truck — the right equipment for East Texas pine and hardwood. Local to Livingston, not driving in from another county.",
        "Get a Free Estimate", "land", "btn alt"
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
    render("/land/", "Land Clearing & Dozer Work in Polk County, TX — Rowe Land, Timber & Dozer",
           "Land clearing, forestry mulching, dozer, grading, roads, pads, ponds and drainage for Polk County and the Lake Livingston area. Local, owner-operated.",
           body)


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
        "slug": "/land/land-clearing/",
        "title": "Land Clearing in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Clearing pine, hardwood, brush, and stumps on raw acreage and lake lots around Livingston and Lake Livingston. Dozer + mulcher + excavator.",
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
        "slug": "/land/forestry-mulching/",
        "title": "Forestry Mulching in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Selective, low-impact forestry mulching for underbrush, small trees, and trail clearing around Livingston and Lake Livingston. Keep the trees you want, lose the rest.",
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
        "slug": "/land/dozer-grading/",
        "title": "Dozer Work & Grading in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Dozer work, building pads, finish grading, and earth-moving around Livingston, Onalaska, and Lake Livingston. Real machine, real operator, real quote.",
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
        "slug": "/land/ponds/",
        "title": "Pond Construction in Polk County, TX — Rowe Land, Timber & Dozer",
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
        "slug": "/land/lake-livingston-lots/",
        "title": "Lake Livingston Lot Clearing & Grading — Rowe Land, Timber & Dozer",
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
        body = service_hero(p["eyebrow"], p["h1"], p["lede"], "Get a Free Estimate", "land", "btn alt")
        body += two_col(p["left"], p["right"])
        body += dark_cta(p["cta_h2"], p["cta_body"], "Get a Free Estimate", "land")
        render(p["slug"], p["title"], p["description"], body)


# --- Timber sub-services ------------------------------------------------------

TIMBER_SUB = [
    {
        "slug": "/timber/sale-consulting/",
        "title": "Timber Sale Consulting in Polk County, TX — Rowe Land, Timber & Dozer",
        "description": "Selling timber in East Texas? Get a consultant who represents you — honest cruise, competitive bids, written contract before a tree comes down.",
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
        body = service_hero(p["eyebrow"], p["h1"], p["lede"], "Get a Free Timber Evaluation", "timber")
        body += two_col(p["left"], p["right"])
        body += dark_cta(p["cta_h2"], p["cta_body"], "Get a Free Timber Evaluation", "timber")
        render(p["slug"], p["title"], p["description"], body)


# --- Service area -------------------------------------------------------------

def build_service_area():
    body = """<section class="hero"><div class="wrap">
  <p class="eyebrow-line">Service area</p>
  <h1>Polk County is home. Six counties is the working radius.</h1>
  <p class="lede">Based in Livingston, working the Lake Livingston shoreline and the surrounding Piney Woods. Local trip — no hidden charge for driving in.</p>
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
    build_sitemap()
    print("Done.")


if __name__ == "__main__":
    main()
