import re, glob

OLD = """  .kiwi-loading{
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
  }"""

NEW = """  .kiwi-loading{
    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#e8ffe0;font-family:'Inter',sans-serif;pointer-events:none;
    background:
      repeating-linear-gradient(0deg, rgba(48,255,0,0.025) 0px, rgba(48,255,0,0.025) 1px, transparent 1px, transparent 4px),
      radial-gradient(ellipse at 25% 25%, rgba(0,80,40,0.45) 0%, transparent 55%),
      radial-gradient(ellipse at 75% 75%, rgba(0,40,80,0.30) 0%, transparent 55%),
      linear-gradient(135deg, #04100a 0%, #07180e 50%, #03100c 100%);
    transition:opacity 0.6s ease;z-index:1;overflow:hidden
  }
  .kiwi-loading.hide{opacity:0}
  .kiwi-loading::before{
    content:"";position:absolute;width:70vmax;height:70vmax;border-radius:50%;
    top:-25vmax;left:-25vmax;
    background:radial-gradient(circle, rgba(48,255,0,0.22) 0%, rgba(48,255,0,0.06) 35%, transparent 70%);
    filter:blur(60px);
    animation:kiwiBlobA 14s ease-in-out infinite;
    mix-blend-mode:screen;
  }
  .kiwi-loading::after{
    content:"";position:absolute;width:60vmax;height:60vmax;border-radius:50%;
    bottom:-20vmax;right:-20vmax;
    background:radial-gradient(circle, rgba(0,220,160,0.18) 0%, rgba(48,255,0,0.05) 40%, transparent 70%);
    filter:blur(60px);
    animation:kiwiBlobB 18s ease-in-out infinite;
    mix-blend-mode:screen;
  }"""

OLD_KF = "  @keyframes kiwiGridPan{0%{background-position:0 0}100%{background-position:42px 42px}}"
NEW_KF = ("  @keyframes kiwiBlobA{0%,100%{transform:translate(0,0) scale(1)}"
          "50%{transform:translate(18vmax,12vmax) scale(1.15)}}\n"
          "  @keyframes kiwiBlobB{0%,100%{transform:translate(0,0) scale(1)}"
          "50%{transform:translate(-14vmax,-10vmax) scale(1.1)}}")

files = sorted(glob.glob("_/*/index.html"))
ok = skip = 0
for path in files:
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if NEW in src and NEW_KF in src:
        skip += 1
        continue
    changed = False
    if OLD in src:
        src = src.replace(OLD, NEW, 1); changed = True
    if OLD_KF in src:
        src = src.replace(OLD_KF, NEW_KF, 1); changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        ok += 1
    else:
        skip += 1
        print("no changes:", path)

print(f"updated {ok}, skipped {skip}, total {len(files)}")
