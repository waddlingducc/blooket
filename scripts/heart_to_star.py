import glob

OLD = ('<button id="kiwiFav" class="kiwi-dock-btn" type="button" aria-label="favorite" aria-pressed="false">'
       '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>'
       '</svg>'
       '</button>')

NEW = ('<button id="kiwiFav" class="kiwi-dock-btn" type="button" aria-label="favorite" aria-pressed="false">'
       '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
       '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
       '</svg>'
       '</button>')

files = sorted(glob.glob("_/*/index.html"))
ok = skip = 0
for path in files:
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if NEW in src:
        skip += 1
        continue
    if OLD not in src:
        print("not found:", path)
        skip += 1
        continue
    src = src.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    ok += 1

print(f"updated {ok}, skipped {skip}, total {len(files)}")
