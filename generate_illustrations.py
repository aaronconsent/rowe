#!/usr/bin/env python3
"""Generate vintage-engraving illustrations via Recraft API.

Usage:
  source .env  (or export RECRAFT_API_KEY=...)
  python3 generate_illustrations.py [name ...]

Without args, generates all illustrations. With names, only those.
Idempotent: skips files that already exist in site/assets/img/.
Pass --force to regenerate everything.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

API = "https://external.api.recraft.ai/v1/images/generations"
OUT_DIR = Path(__file__).parent / "site" / "assets" / "img"

# Composition guidance baked into every prompt so the output reads as a
# proper engraving on paper rather than a black-bg poster.
BASE_STYLE = (
    "vintage engraving illustration, classic 19th-century woodcut style, "
    "fine crosshatched ink lines on plain white paper background, "
    "black ink line art only, no shading fill, no solid black masses, "
    "subject centered with generous white margin around it, "
    "isolated subject, no border, no frame, no text, no labels, "
    "high contrast crisp lines"
)

ILLUSTRATIONS = {
    "pine": "single mature longleaf pine tree, tall and slender, full from base to top, "
            "visible textured bark trunk, layered horizontal pine branches with detailed needle clusters, "
            "small grass tufts at the base, " + BASE_STYLE,

    "hardwood": "single mature oak tree, broad spreading round canopy of leaves, "
                "visible textured trunk with bark detail and exposed roots, "
                "small grass at the base, " + BASE_STYLE,

    "dozer": "side view of a classic Caterpillar bulldozer with a large angled push blade, "
             "tracked treads with visible wheels, raised operator cab with cross window, "
             "exhaust stack on top, " + BASE_STYLE,

    "mulcher": "side view of a tracked forestry mulcher excavator with a large rotating drum cutter head "
               "on a hydraulic boom arm, tracked treads, operator cab, " + BASE_STYLE,

    "pond": "small farm pond in cross section view from outside, calm water with concentric ripples, "
            "tall cattail reeds with characteristic brown sausage-shaped flower heads on both sides, "
            "grassy banks, " + BASE_STYLE,

    "lake": "lake scene with a wooden fishing dock extending into the water, "
            "small sailboat on the water in the distance, "
            "wave lines on water surface, distant tree-lined shore, " + BASE_STYLE,

    "road": "vintage view of a quiet rural country dirt road in perspective, "
            "tall pine trees on both sides of the road, wooden fence posts along the shoulder, "
            "" + BASE_STYLE,

    "compass": "antique nautical compass rose with 8 cardinal direction points, "
               "ornate decorative details, fleur-de-lis at north, "
               "double circular border ring, " + BASE_STYLE,

    "mark": "simple emblematic single pine tree silhouette inside a decorative circular badge frame, "
            "ornamental medallion style, " + BASE_STYLE,
}


def generate(name: str, prompt: str, api_key: str) -> Path:
    out = OUT_DIR / f"{name}.svg"
    payload = {
        "prompt": prompt,
        "style": "vector_illustration",
        "substyle": "engraving",
        "size": "1024x1024",
        "n": 1,
        "model": "recraftv3",
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        body = json.loads(r.read())
    url = body["data"][0]["url"]
    print(f"  {name}: generated, downloading…")
    dl = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (rowe-build/1.0)"})
    with urllib.request.urlopen(dl, timeout=60) as r:
        svg = r.read()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.write_bytes(svg)
    print(f"  {name}: wrote {out} ({len(svg):,} bytes)")
    return out


def main():
    api_key = os.environ.get("RECRAFT_API_KEY")
    if not api_key:
        # Try loading .env in cwd
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("RECRAFT_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key:
        print("ERROR: RECRAFT_API_KEY not set. Either export it or put it in .env")
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv

    names = args or list(ILLUSTRATIONS.keys())
    for name in names:
        if name not in ILLUSTRATIONS:
            print(f"  unknown illustration: {name}; valid: {list(ILLUSTRATIONS)}")
            continue
        out = OUT_DIR / f"{name}.svg"
        if out.exists() and not force:
            print(f"  {name}: exists, skipping (use --force to regenerate)")
            continue
        try:
            generate(name, ILLUSTRATIONS[name], api_key)
        except Exception as e:
            print(f"  {name}: FAILED — {e}")
        time.sleep(0.5)  # polite spacing


if __name__ == "__main__":
    main()
