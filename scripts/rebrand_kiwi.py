#!/usr/bin/env python3
import os, re, html as htmllib

ROOT = "_"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
<meta http-equiv="Pragma" content="no-cache"/>
<meta http-equiv="Expires" content="0"/>
<title>Home - Classroom</title>
<link rel="icon" id="favicon" type="image/x-icon" href=""/>
<script src="/stealth.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<meta name="description" content="play {title_html} on kiwi - free unblocked games"/>
<meta name="robots" content="index, follow"/>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{height:100%;width:100%;overflow:hidden;background:#000;color:#fff;font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}
  body{{
    background:
      radial-gradient(ellipse 70% 50% at 50% 0%, rgba(48,255,0,0.10) 0%, transparent 60%),
      radial-gradient(ellipse 50% 40% at 90% 90%, rgba(48,255,0,0.06) 0%, transparent 55%),
      #050a05;
  }}
  img{{-webkit-user-drag:none;user-select:none}}
  .kiwi-nav{{
    position:fixed;top:0;left:0;right:0;height:44px;z-index:10000;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 16px;
    background:rgba(8,18,8,0.78);
    backdrop-filter:blur(18px) saturate(1.4);
    -webkit-backdrop-filter:blur(18px) saturate(1.4);
    border-bottom:1px solid rgba(48,255,0,0.18);
  }}
  .kiwi-nav-left{{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;transition:transform .2s ease}}
  .kiwi-nav-left:hover{{transform:translateY(-1px)}}
  .kiwi-nav-left img{{height:30px;width:30px;border-radius:6px;object-fit:contain;filter:drop-shadow(0 0 4px rgba(48,255,0,0.3))}}
  .kiwi-brand{{font-weight:700;font-size:20px;color:#30FF00;letter-spacing:-0.5px}}
  .kiwi-game-title{{
    position:absolute;left:50%;transform:translateX(-50%);
    font-size:14px;font-weight:500;color:rgba(255,255,255,0.9);
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46%;
    letter-spacing:0.3px
  }}
  .kiwi-stage{{
    position:fixed;top:54px;left:10px;right:320px;bottom:110px;
    padding:0;
  }}
  .kiwi-frame-wrap{{
    width:100%;height:100%;border-radius:12px;overflow:hidden;
    background:#0a0f0a;
    border:1px solid rgba(48,255,0,0.2);
    box-shadow:0 4px 30px rgba(0,0,0,0.5),0 0 24px rgba(48,255,0,0.08);
    position:relative
  }}
  .kiwi-frame-wrap iframe{{
    position:absolute;top:0;left:0;width:100%;height:100%;border:0;display:block;
    opacity:0;transition:opacity 0.6s ease
  }}
  .kiwi-frame-wrap iframe.loaded{{opacity:1}}
  .kiwi-loading{{
    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#30FF00;font-weight:600;letter-spacing:1px;font-size:13px;pointer-events:none;
    background:#0a0f0a;
    transition:opacity 0.5s ease;z-index:1
  }}
  .kiwi-loading.hide{{opacity:0}}
  .kiwi-loading img{{width:64px;height:64px;animation:kiwiSpin 2s linear infinite;filter:drop-shadow(0 0 12px rgba(48,255,0,0.55));margin-bottom:14px}}
  @keyframes kiwiSpin{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
  .right-ad-container{{
    position:fixed;right:10px;top:54px;width:300px;height:250px;z-index:9999;
    background:rgba(8,18,8,0.78);
    backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);
    border:1px solid rgba(48,255,0,0.15);
    border-radius:0;
    box-shadow:0 4px 20px rgba(0,0,0,0.5);
    display:flex;align-items:center;justify-content:center;overflow:hidden
  }}
  .right-unblocker-container{{
    position:fixed;right:10px;top:314px;width:300px;height:250px;z-index:9999;
    background:rgba(8,18,8,0.78);
    backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);
    border:1px solid rgba(48,255,0,0.15);
    border-radius:0;
    box-shadow:0 4px 20px rgba(0,0,0,0.5);overflow:hidden
  }}
  .right-unblocker-container iframe{{position:absolute;top:0;left:0;width:1024px;height:768px;border:none}}
  .bottom-ad-container{{
    position:fixed;left:calc(50% - 155px);bottom:10px;transform:translateX(-50%);
    width:728px;height:90px;z-index:9999;
    background:rgba(8,18,8,0.78);
    backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);
    border:1px solid rgba(48,255,0,0.15);
    border-radius:0;
    display:flex;align-items:center;justify-content:center;overflow:hidden
  }}
  .bottom-ad-container > div{{width:728px;height:90px;position:relative;overflow:hidden}}
  @media (max-width:900px){{
    .right-ad-container,.right-unblocker-container,.bottom-ad-container{{display:none}}
    .kiwi-stage{{right:0;bottom:0}}
  }}
  @media (max-width:600px){{
    .kiwi-brand{{display:none}}
    .kiwi-game-title{{max-width:60%}}
  }}
</style>
</head>
<body>
<nav class="kiwi-nav">
  <a class="kiwi-nav-left" href="/" title="back to kiwi">
    <img src="/images/kiwi-logo.png" alt=""/>
    <span class="kiwi-brand">kiwi</span>
  </a>
  <span class="kiwi-game-title">{title_html}</span>
  <div class="kiwi-nav-right"></div>
</nav>
<main class="kiwi-stage">
  <div class="kiwi-frame-wrap" id="kiwiWrap">
    <iframe id="kiwiGame" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-popups allow-modals" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad" allowfullscreen data-src="{src_html}"></iframe>
    <div class="kiwi-loading" id="kiwiLoading"><img src="/images/kiwi-logo.png" alt=""/>loading {title_html_lower}</div>
  </div>
</main>
<div class="right-ad-container">
  <iframe src="https://bmwguide.org/models.html" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-popups allow-modals" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad" style="position:absolute;top:0;left:0;width:1024px;height:768px;border:none;"></iframe>
</div>
<div class="right-unblocker-container">
  <iframe src="https://bmwguide.org/home.html" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-popups allow-modals" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad"></iframe>
</div>
<div class="bottom-ad-container">
  <div>
    <iframe src="https://bmwguide.org/cars.html" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-popups allow-modals" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad" style="border:0;padding:0;width:1024px;height:768px;display:block;position:absolute;top:0;left:0"></iframe>
  </div>
</div>
<script>
document.addEventListener("contextmenu",function(e){{e.preventDefault();}});
(function(){{
  var f=document.getElementById("kiwiGame");
  var l=document.getElementById("kiwiLoading");
  if(!f)return;
  setTimeout(function(){{
    f.src=f.getAttribute("data-src");
    f.addEventListener("load",function(){{
      f.classList.add("loaded");
      if(l){{l.classList.add("hide");setTimeout(function(){{l.remove();}},600);}}
    }});
  }},150);
}})();
</script>
</body>
</html>
"""

def extract_src(s):
    m = re.search(r'data-delayed-src="([^"]+)"', s)
    if m: return m.group(1)
    m = re.search(r'data-src="([^"]+)"', s)
    if m: return m.group(1)
    m = re.search(r'<div class="game-container">.*?<iframe[^>]*\bsrc="([^"]+)"', s, re.S)
    if m: return m.group(1)
    m = re.search(r'<iframe[^>]*\bsrc="(/storage/[^"]+)"', s)
    if m: return m.group(1)
    return None

def extract_title(s):
    m = re.search(r'<span class="game-title-nav">([^<]+)</span>', s)
    if m: return m.group(1).strip()
    m = re.search(r'<span class="kiwi-game-title">([^<]+)</span>', s)
    if m: return m.group(1).strip()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if m:
        t = m.group(1).strip()
        t = re.sub(r"^kiwi[\s\-:|·]+", "", t, flags=re.I)
        t = re.sub(r"^Play\s+", "", t, flags=re.I)
        t = re.sub(r"\s+Unblocked.*$", "", t, flags=re.I)
        t = re.sub(r"\s*\|\s*NebulaPlay.*$", "", t, flags=re.I)
        return t.strip() or "game"
    return "game"

ok = 0
fail = 0
for name in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, name, "index.html")
    if not os.path.isfile(p): continue
    with open(p, "r", encoding="utf-8") as f:
        s = f.read()
    src = extract_src(s)
    if not src:
        print("NO SRC:", p); fail += 1; continue
    title = extract_title(s)
    title_lc = title.lower()
    out = TEMPLATE.format(
        title_html=htmllib.escape(title_lc),
        title_html_lower=htmllib.escape(title_lc),
        src_html=htmllib.escape(src, quote=True),
    )
    with open(p, "w", encoding="utf-8") as f:
        f.write(out)
    ok += 1
print(f"Rebranded: {ok}, Failed: {fail}")
