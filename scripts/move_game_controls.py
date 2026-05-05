import glob, re

NEW_NAV_PATTERN = re.compile(
    r'<div class="kiwi-nav-right"><button id="kiwiFav".*?</button><button id="kiwiMute".*?</button></div>',
    re.DOTALL,
)
EMPTY_NAV = '<div class="kiwi-nav-right"></div>'

DOCK_HTML = (
    '<div class="kiwi-dock" id="kiwiDock">'
    '<button id="kiwiFav" class="kiwi-dock-btn" type="button" aria-label="favorite" aria-pressed="false">'
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>'
    '</svg>'
    '</button>'
    '<button id="kiwiMute" class="kiwi-dock-btn" type="button" aria-label="mute" aria-pressed="false">'
    '<svg class="icon-on" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>'
    '<path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>'
    '<path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>'
    '</svg>'
    '<svg class="icon-off" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none">'
    '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>'
    '<line x1="23" y1="9" x2="17" y2="15"/>'
    '<line x1="17" y1="9" x2="23" y2="15"/>'
    '</svg>'
    '</button>'
    '</div>'
)

DOCK_INSERT_ANCHOR = '<div class="bottom-ad-container">'

files = sorted(glob.glob("_/*/index.html"))
ok = skip = 0
for path in files:
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    changed = False

    new_src, n = NEW_NAV_PATTERN.subn(EMPTY_NAV, src, count=1)
    if n:
        src = new_src
        changed = True

    if 'id="kiwiDock"' not in src and DOCK_INSERT_ANCHOR in src:
        src = src.replace(DOCK_INSERT_ANCHOR, DOCK_HTML + DOCK_INSERT_ANCHOR, 1)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        ok += 1
    else:
        skip += 1
        print("no changes:", path)

print(f"updated {ok}, skipped {skip}, total {len(files)}")
