# Rowe Land, Timber & Dozer Services

Lead-gen website for Rowe Land, Timber & Dozer Services (Livingston, TX).

- **Stack:** Static HTML/CSS, deployed to Cloudflare Pages
- **Publish directory:** `site/`
- **Domain (planned):** rowelandtimber.com

## Local preview

```
cd site && python3 -m http.server 8000
```

## Deploy

Cloudflare Pages → connect repo → build command empty, output dir `site`.

## Structure

```
site/
  index.html          # Home — two-path hero (timber | land)
  timber/             # Timber sales & consulting pillar
  land/               # Land clearing & dozer pillar
  about/
  contact/            # Split lead form (timber | land | both)
  assets/css/site.css
  robots.txt
  sitemap.xml
  _headers
```

## Pre-launch open items (from positioning brief §9)

1. Confirm Bob's credentials, years operating, certifications
2. Claim Google Business Profile
3. Kick off review generation
4. Collect photos + video of equipment, crew, completed jobs
5. Replace `formspree.io/f/REPLACE_ME` in `contact/index.html` with real endpoint
