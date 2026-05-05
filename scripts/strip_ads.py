#!/usr/bin/env python3
import os, re, sys

ROOT = "_"

def transform(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    m = re.search(r'data-delayed-src="([^"]+)"', html)
    if not m:
        m = re.search(r'<iframe[^>]*\sclass="[^"]*"?[^>]*\ssrc="([^"]+)"[^>]*>\s*</iframe>', html)
    src = m.group(1) if m else None
    if not src:
        sm = re.search(r'<div class="game-container">.*?<iframe[^>]*\bsrc="([^"]+)"', html, re.S)
        if sm:
            src = sm.group(1)
    if not src:
        print("NO GAME SRC:", path)
        return False

    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = title_m.group(1).strip() if title_m else "Game"

    new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<link rel="icon" type="image/x-icon" href="/images/site-icon.ico">
<style>
  html, body {{ margin:0; padding:0; height:100%; width:100%; overflow:hidden; background:#000; }}
  iframe {{ position:fixed; top:0; left:0; width:100vw; height:100vh; border:0; display:block; }}
</style>
</head>
<body>
<iframe src="{src}" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-popups allow-modals" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad" allowfullscreen></iframe>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True

count = 0
fail = 0
for name in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, name, "index.html")
    if os.path.isfile(p):
        if transform(p):
            count += 1
        else:
            fail += 1
print(f"Updated: {count}, Failed: {fail}")
