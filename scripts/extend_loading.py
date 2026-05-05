import re, glob

OLD = """  setTimeout(function(){
    f.src=f.getAttribute("data-src");
    f.addEventListener("load",function(){
      f.classList.add("loaded");
      if(l){l.classList.add("hide");setTimeout(function(){l.remove();},600);}
    });
  },150);"""

NEW = """  var minShow=2800, started=Date.now(), done=false;
  function hide(){
    if(done) return; done=true;
    var elapsed=Date.now()-started;
    var wait=Math.max(0, minShow-elapsed);
    setTimeout(function(){
      f.classList.add("loaded");
      if(l){l.classList.add("hide");setTimeout(function(){l.remove();},700);}
    },wait);
  }
  setTimeout(function(){
    f.src=f.getAttribute("data-src");
    f.addEventListener("load",hide);
    setTimeout(hide,15000);
  },150);"""

files = sorted(glob.glob("_/*/index.html"))
ok = skip = 0
for path in files:
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if NEW in src:
        skip += 1
        continue
    if OLD not in src:
        print("pattern not found:", path)
        skip += 1
        continue
    src = src.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    ok += 1

print(f"updated {ok}, skipped {skip}, total {len(files)}")
