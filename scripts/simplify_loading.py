import os, re, glob

ROOT = os.path.join(os.path.dirname(__file__), '..')
PAGES = sorted(glob.glob(os.path.join(ROOT, '_', '*', 'index.html')))

NEW_CSS = """  .kiwi-loading{
    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#e8ffe0;font-family:'Inter',sans-serif;pointer-events:none;
    background:
      radial-gradient(ellipse 70% 65% at 50% 45%, rgba(48,255,0,0.32) 0%, rgba(48,255,0,0.08) 38%, transparent 75%),
      radial-gradient(ellipse at center, #0a2410 0%, #061509 60%, #020806 100%);
    transition:opacity 0.6s ease;z-index:1;overflow:hidden
  }
  .kiwi-loading.hide{opacity:0}
  .kiwi-loading::before{
    content:"";position:absolute;inset:0;
    background-image:
      radial-gradient(1.4px 1.4px at 23px 78px, rgba(180,255,160,0.85), transparent),
      radial-gradient(1px 1px at 67px 23px, rgba(48,255,0,0.6), transparent),
      radial-gradient(1.8px 1.8px at 145px 130px, rgba(200,255,180,0.75), transparent),
      radial-gradient(1px 1px at 200px 50px, rgba(48,255,0,0.55), transparent),
      radial-gradient(1.2px 1.2px at 310px 175px, rgba(180,255,160,0.7), transparent),
      radial-gradient(1px 1px at 50px 220px, rgba(48,255,0,0.55), transparent),
      radial-gradient(2px 2px at 380px 90px, rgba(48,255,0,0.7), transparent),
      radial-gradient(1px 1px at 250px 300px, rgba(180,255,160,0.55), transparent),
      radial-gradient(1.5px 1.5px at 100px 360px, rgba(48,255,0,0.6), transparent),
      radial-gradient(1px 1px at 420px 250px, rgba(180,255,160,0.6), transparent),
      radial-gradient(1.2px 1.2px at 360px 380px, rgba(48,255,0,0.55), transparent),
      radial-gradient(1px 1px at 460px 30px, rgba(180,255,160,0.5), transparent);
    background-size:480px 400px;background-repeat:repeat;
    animation:kiwiTwinkle 5s ease-in-out infinite;
    opacity:0.95;
  }
  .kiwi-loader-stack{position:relative;display:flex;flex-direction:column;align-items:center;z-index:2}
  .kiwi-logo-wrap{
    position:relative;display:flex;align-items:center;justify-content:center;
    margin-bottom:22px;
  }
  .kiwi-logo-wrap img{
    width:72px;height:72px;border-radius:14px;object-fit:contain;
    animation:kiwiPulse 2.4s ease-in-out infinite;
    filter:drop-shadow(0 0 18px rgba(48,255,0,0.55));
  }
  .kiwi-loading-sub{
    font-size:13px;font-weight:500;letter-spacing:0.3px;
    color:rgba(48,255,0,0.85);margin-bottom:18px;
  }
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
  @keyframes kiwiPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
  @keyframes kiwiProgress{0%{left:-40%}100%{left:100%}}
  @keyframes kiwiTwinkle{0%,100%{opacity:0.95}50%{opacity:0.55}}"""

OLD_CSS_RE = re.compile(
    r'  \.kiwi-loading\{.*?(?=\n  \.right-ad-container\{)',
    re.DOTALL,
)

LOADING_DIV_RE = re.compile(
    r'<div class="kiwi-loading" id="kiwiLoading">.*?</div></div></div>',
    re.DOTALL,
)
NEW_LOADING_DIV = (
    '<div class="kiwi-loading" id="kiwiLoading">'
    '<div class="kiwi-loader-stack">'
    '<div class="kiwi-logo-wrap"><img src="/images/kiwi-logo.png" alt=""/></div>'
    '<div class="kiwi-loading-sub">loading</div>'
    '<div class="kiwi-progress"></div>'
    '</div></div>'
)

changed = 0
skipped = 0
for path in PAGES:
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    new = s
    new, n1 = OLD_CSS_RE.subn(NEW_CSS, new, count=1)
    new, n2 = LOADING_DIV_RE.subn(NEW_LOADING_DIV, new, count=1)
    if n1 == 1 and n2 == 1 and new != s:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        changed += 1
    else:
        skipped += 1
        print(f'SKIP {path}: css={n1} html={n2}')

print(f'Done. changed={changed} skipped={skipped}')
