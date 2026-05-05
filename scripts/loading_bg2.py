import glob

OLD = """  .kiwi-loading{
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

WAVE_SVG = (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='1200' height='600' viewBox='0 0 1200 600' "
    "preserveAspectRatio='none'%3E"
    "%3Cpath d='M0 110 Q300 60 600 120 T1200 110' stroke='%2330ff00' stroke-opacity='0.22' stroke-width='1' fill='none'/%3E"
    "%3Cpath d='M0 200 Q300 240 600 190 T1200 210' stroke='%2330ff00' stroke-opacity='0.15' stroke-width='1' fill='none'/%3E"
    "%3Cpath d='M0 300 Q300 260 600 320 T1200 295' stroke='%2330ff00' stroke-opacity='0.18' stroke-width='1' fill='none'/%3E"
    "%3Cpath d='M0 400 Q300 440 600 380 T1200 410' stroke='%2330ff00' stroke-opacity='0.13' stroke-width='1' fill='none'/%3E"
    "%3Cpath d='M0 490 Q300 450 600 510 T1200 485' stroke='%2330ff00' stroke-opacity='0.10' stroke-width='1' fill='none'/%3E"
    "%3C/svg%3E"
)

NEW = (
    "  .kiwi-loading{\n"
    "    position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;\n"
    "    color:#e8ffe0;font-family:'Inter',sans-serif;pointer-events:none;\n"
    "    background:\n"
    "      radial-gradient(ellipse 70% 65% at 50% 45%, rgba(48,255,0,0.32) 0%, rgba(48,255,0,0.08) 38%, transparent 75%),\n"
    "      radial-gradient(ellipse at center, #0a2410 0%, #061509 60%, #020806 100%);\n"
    "    transition:opacity 0.6s ease;z-index:1;overflow:hidden\n"
    "  }\n"
    "  .kiwi-loading.hide{opacity:0}\n"
    "  .kiwi-loading::before{\n"
    "    content:\"\";position:absolute;inset:0;\n"
    "    background-image:\n"
    "      radial-gradient(1.4px 1.4px at 23px 78px, rgba(180,255,160,0.85), transparent),\n"
    "      radial-gradient(1px 1px at 67px 23px, rgba(48,255,0,0.6), transparent),\n"
    "      radial-gradient(1.8px 1.8px at 145px 130px, rgba(200,255,180,0.75), transparent),\n"
    "      radial-gradient(1px 1px at 200px 50px, rgba(48,255,0,0.55), transparent),\n"
    "      radial-gradient(1.2px 1.2px at 310px 175px, rgba(180,255,160,0.7), transparent),\n"
    "      radial-gradient(1px 1px at 50px 220px, rgba(48,255,0,0.55), transparent),\n"
    "      radial-gradient(2px 2px at 380px 90px, rgba(48,255,0,0.7), transparent),\n"
    "      radial-gradient(1px 1px at 250px 300px, rgba(180,255,160,0.55), transparent),\n"
    "      radial-gradient(1.5px 1.5px at 100px 360px, rgba(48,255,0,0.6), transparent),\n"
    "      radial-gradient(1px 1px at 420px 250px, rgba(180,255,160,0.6), transparent),\n"
    "      radial-gradient(1.2px 1.2px at 360px 380px, rgba(48,255,0,0.55), transparent),\n"
    "      radial-gradient(1px 1px at 460px 30px, rgba(180,255,160,0.5), transparent);\n"
    "    background-size:480px 400px;background-repeat:repeat;\n"
    "    animation:kiwiTwinkle 5s ease-in-out infinite;\n"
    "    opacity:0.95;\n"
    "  }\n"
    "  .kiwi-loading::after{\n"
    "    content:\"\";position:absolute;left:-10%;right:-10%;top:0;bottom:0;\n"
    f"    background-image:url(\"data:image/svg+xml;utf8,{WAVE_SVG}\");\n"
    "    background-repeat:no-repeat;background-position:center;background-size:120% 100%;\n"
    "    opacity:0.85;animation:kiwiWaveDrift 22s ease-in-out infinite;\n"
    "  }"
)

OLD_KF = ("  @keyframes kiwiBlobA{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(18vmax,12vmax) scale(1.15)}}\n"
          "  @keyframes kiwiBlobB{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-14vmax,-10vmax) scale(1.1)}}")

NEW_KF = ("  @keyframes kiwiTwinkle{0%,100%{opacity:0.95}50%{opacity:0.55}}\n"
          "  @keyframes kiwiWaveDrift{0%,100%{transform:translateX(0)}50%{transform:translateX(-30px)}}")

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
    else:
        print("CSS pattern not found:", path)
    if OLD_KF in src:
        src = src.replace(OLD_KF, NEW_KF, 1); changed = True
    else:
        print("KF pattern not found:", path)
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        ok += 1
    else:
        skip += 1

print(f"updated {ok}, skipped {skip}, total {len(files)}")
