import os, re, glob

NEW_CSS = """  .kiwi-loading{
    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#e8ffe0;font-family:'Inter',sans-serif;pointer-events:none;
    background:
      radial-gradient(ellipse 60% 50% at 50% 40%, rgba(48,255,0,0.10) 0%, transparent 70%),
      radial-gradient(circle at 50% 110%, rgba(48,255,0,0.08) 0%, transparent 60%),
      #0a0f0a;
    transition:opacity 0.6s ease;z-index:1;overflow:hidden
  }
  .kiwi-loading.hide{opacity:0}
  .kiwi-loading::before{
    content:"";position:absolute;inset:0;
    background-image:
      linear-gradient(rgba(48,255,0,0.045) 1px, transparent 1px),
      linear-gradient(90deg, rgba(48,255,0,0.045) 1px, transparent 1px);
    background-size:42px 42px;
    mask-image:radial-gradient(ellipse 70% 60% at 50% 50%, #000 30%, transparent 75%);
    -webkit-mask-image:radial-gradient(ellipse 70% 60% at 50% 50%, #000 30%, transparent 75%);
    animation:kiwiGridPan 18s linear infinite;
    opacity:0.7;
  }
  .kiwi-loader-stack{position:relative;display:flex;flex-direction:column;align-items:center;z-index:2}
  .kiwi-logo-wrap{
    position:relative;width:128px;height:128px;display:flex;align-items:center;justify-content:center;
    margin-bottom:26px;
  }
  .kiwi-logo-wrap img{
    width:72px;height:72px;border-radius:14px;object-fit:contain;
    animation:kiwiPulse 2.4s ease-in-out infinite;
    filter:drop-shadow(0 0 18px rgba(48,255,0,0.55));
    z-index:3;
  }
  .kiwi-ring{
    position:absolute;inset:0;border-radius:50%;
    border:2px solid transparent;
    border-top-color:#30FF00;border-right-color:rgba(48,255,0,0.35);
    animation:kiwiSpin 1.6s linear infinite;
    box-shadow:0 0 18px rgba(48,255,0,0.25), inset 0 0 18px rgba(48,255,0,0.10);
  }
  .kiwi-ring.alt{
    inset:14px;border-top-color:transparent;border-right-color:transparent;
    border-bottom-color:rgba(48,255,0,0.55);border-left-color:rgba(48,255,0,0.18);
    animation:kiwiSpinRev 2.4s linear infinite;
    box-shadow:none;
  }
  .kiwi-ring-glow{
    position:absolute;inset:-14px;border-radius:50%;
    background:radial-gradient(circle, rgba(48,255,0,0.18) 0%, transparent 65%);
    animation:kiwiGlow 2.4s ease-in-out infinite;
    filter:blur(2px);
  }
  .kiwi-loading-title{
    font-size:18px;font-weight:700;letter-spacing:0.4px;
    background:linear-gradient(90deg, #ffffff 0%, #30FF00 50%, #ffffff 100%);
    background-size:200% auto;
    -webkit-background-clip:text;background-clip:text;color:transparent;
    -webkit-text-fill-color:transparent;
    animation:kiwiShimmer 3s linear infinite;
    margin-bottom:6px;text-align:center;max-width:80vw;
    text-overflow:ellipsis;overflow:hidden;white-space:nowrap;
  }
  .kiwi-loading-sub{
    font-size:11px;font-weight:500;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(48,255,0,0.85);margin-bottom:18px;display:flex;align-items:center;gap:6px;
  }
  .kiwi-dot{
    width:5px;height:5px;border-radius:50%;background:#30FF00;
    box-shadow:0 0 6px rgba(48,255,0,0.7);
    animation:kiwiDot 1.2s ease-in-out infinite;
  }
  .kiwi-dot:nth-child(2){animation-delay:0.15s}
  .kiwi-dot:nth-child(3){animation-delay:0.3s}
  .kiwi-progress{
    width:240px;max-width:60vw;height:3px;border-radius:3px;
    background:rgba(48,255,0,0.12);overflow:hidden;position:relative;
  }
  .kiwi-progress::after{
    content:"";position:absolute;top:0;left:-40%;width:40%;height:100%;
    background:linear-gradient(90deg, transparent, #30FF00, transparent);
    box-shadow:0 0 12px rgba(48,255,0,0.7);
    animation:kiwiProgress 1.6s cubic-bezier(.6,0,.4,1) infinite;
  }
  @keyframes kiwiSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
  @keyframes kiwiSpinRev{from{transform:rotate(0)}to{transform:rotate(-360deg)}}
  @keyframes kiwiPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
  @keyframes kiwiGlow{0%,100%{opacity:0.5}50%{opacity:1}}
  @keyframes kiwiShimmer{0%{background-position:200% center}100%{background-position:-200% center}}
  @keyframes kiwiDot{0%,80%,100%{transform:scale(0.6);opacity:0.4}40%{transform:scale(1);opacity:1}}
  @keyframes kiwiProgress{0%{left:-40%}100%{left:100%}}
  @keyframes kiwiGridPan{0%{background-position:0 0}100%{background-position:42px 42px}}"""

OLD_CSS_PATTERN = re.compile(
    r"  \.kiwi-loading\{\s*\n"
    r"    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;\s*\n"
    r"    color:#30FF00;font-weight:600;letter-spacing:1px;font-size:13px;pointer-events:none;\s*\n"
    r"    background:#0a0f0a;\s*\n"
    r"    transition:opacity 0\.5s ease;z-index:1\s*\n"
    r"  \}\s*\n"
    r"  \.kiwi-loading\.hide\{opacity:0\}\s*\n"
    r"  \.kiwi-loading img\{[^}]+\}\s*\n"
    r"  @keyframes kiwiSpin\{from\{transform:rotate\(0\)\}to\{transform:rotate\(360deg\)\}\}"
)

HTML_PATTERN = re.compile(
    r'<div class="kiwi-loading" id="kiwiLoading"><img src="/images/kiwi-logo\.png" alt=""/>loading ([^<]+)</div>'
)

def new_html(game_name):
    return (
        '<div class="kiwi-loading" id="kiwiLoading">'
        '<div class="kiwi-loader-stack">'
        '<div class="kiwi-logo-wrap">'
        '<div class="kiwi-ring-glow"></div>'
        '<div class="kiwi-ring"></div>'
        '<div class="kiwi-ring alt"></div>'
        '<img src="/images/kiwi-logo.png" alt=""/>'
        '</div>'
        f'<div class="kiwi-loading-title">{game_name}</div>'
        '<div class="kiwi-loading-sub">'
        '<span>loading</span>'
        '<span class="kiwi-dot"></span>'
        '<span class="kiwi-dot"></span>'
        '<span class="kiwi-dot"></span>'
        '</div>'
        '<div class="kiwi-progress"></div>'
        '</div>'
        '</div>'
    )

files = sorted(glob.glob("_/*/index.html"))
css_ok = html_ok = css_skip = html_skip = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    new_src, css_subs = OLD_CSS_PATTERN.subn(NEW_CSS, src, count=1)
    if css_subs:
        css_ok += 1
    else:
        css_skip += 1
        print("CSS not matched:", path)
    def repl(m):
        return new_html(m.group(1))
    new_src, html_subs = HTML_PATTERN.subn(repl, new_src, count=1)
    if html_subs:
        html_ok += 1
    else:
        html_skip += 1
        print("HTML not matched:", path)
    if css_subs or html_subs:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_src)

print(f"Total files: {len(files)}  CSS replaced: {css_ok}  HTML replaced: {html_ok}  CSS skip: {css_skip}  HTML skip: {html_skip}")
