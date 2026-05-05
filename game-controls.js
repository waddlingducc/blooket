(function () {
  var STYLE_ID = 'kiwi-game-controls-style';
  var FAV_KEY = 'kiwi:favs';
  var MUTE_KEY = 'kiwi:muted';

  if (!document.getElementById(STYLE_ID)) {
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = [
      '.kiwi-dock{',
      '  position:fixed;right:14px;bottom:14px;z-index:9999;',
      '  display:flex;flex-direction:row;gap:8px;padding:8px;',
      '  background:rgba(8,18,8,0.78);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);',
      '  border:1px solid rgba(48,255,0,0.18);border-radius:12px;',
      '  box-shadow:0 6px 24px rgba(0,0,0,0.5),0 0 12px rgba(48,255,0,0.10);',
      '}',
      '.kiwi-dock-btn{',
      '  appearance:none;background:rgba(48,255,0,0.06);border:1px solid rgba(48,255,0,0.18);',
      '  color:#cfffc0;width:38px;height:38px;border-radius:9px;padding:0;',
      '  display:inline-flex;align-items:center;justify-content:center;cursor:pointer;',
      '  transition:background .15s ease,color .15s ease,border-color .15s ease,transform .15s ease,box-shadow .15s ease;',
      '}',
      '.kiwi-dock-btn:hover{background:rgba(48,255,0,0.14);color:#fff;border-color:rgba(48,255,0,0.40);transform:translateY(-1px)}',
      '.kiwi-dock-btn:active{transform:translateY(0)}',
      '.kiwi-dock-btn.active{background:rgba(48,255,0,0.22);color:#30FF00;border-color:rgba(48,255,0,0.55);box-shadow:0 0 12px rgba(48,255,0,0.25)}',
      '.kiwi-dock-btn svg{display:block;pointer-events:none}',
      '#kiwiFav.active{background:rgba(255,210,63,0.18);color:#FFD23F;border-color:rgba(255,210,63,0.55);box-shadow:0 0 12px rgba(255,210,63,0.30)}',
      '#kiwiFav.active svg{fill:currentColor}',
      '.kiwi-toast{',
      '  position:fixed;left:50%;top:60px;transform:translateX(-50%) translateY(-10px);',
      '  background:rgba(8,18,8,0.92);color:#cfffc0;border:1px solid rgba(48,255,0,0.4);',
      '  padding:8px 14px;border-radius:8px;font:500 12px/1.2 "Inter",sans-serif;letter-spacing:0.3px;',
      '  z-index:10001;opacity:0;pointer-events:none;transition:opacity .25s ease,transform .25s ease;',
      '  box-shadow:0 6px 24px rgba(0,0,0,0.5),0 0 12px rgba(48,255,0,0.25);',
      '}',
      '.kiwi-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}',
      '.kiwi-socials{display:flex;align-items:center;gap:8px}',
      '.kiwi-socials-label{font:600 16px/1 "Inter",sans-serif;color:#ffffff;letter-spacing:0.3px;white-space:nowrap}',
      '.kiwi-social-link{',
      '  display:inline-flex;align-items:center;justify-content:center;',
      '  width:26px;height:26px;border-radius:6px;overflow:hidden;',
      '  text-decoration:none;',
      '  transition:transform .15s ease,box-shadow .15s ease,filter .15s ease;',
      '}',
      '.kiwi-social-link:hover{transform:translateY(-1px);box-shadow:0 0 12px rgba(48,255,0,0.35);filter:brightness(1.1)}',
      '.kiwi-social-link img{display:block;width:100%;height:100%;object-fit:cover;pointer-events:none;-webkit-user-drag:none}',
      '@media (max-width:900px){.kiwi-dock{left:10px;bottom:10px;padding:6px;gap:6px}.kiwi-dock-btn{width:34px;height:34px}.kiwi-socials{gap:6px}.kiwi-socials-label{font-size:14px}.kiwi-social-link{width:24px;height:24px}}',
      '@media (max-width:600px){.kiwi-socials{gap:5px}.kiwi-socials-label{display:none}.kiwi-social-link{width:22px;height:22px}}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function gamePath() {
    var p = location.pathname.replace(/index\.html$/, '');
    if (p.charAt(p.length - 1) !== '/') p += '/';
    return p;
  }
  function gameName() {
    var t = document.querySelector('.kiwi-game-title');
    return (t && t.textContent.trim()) || gamePath();
  }

  var toastEl;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'kiwi-toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toastEl.classList.remove('show'); }, 1400);
  }

  // ---------- favorites (shared with homepage: kiwi:favs is array of paths) ----------
  function loadFavs() {
    try {
      var v = JSON.parse(localStorage.getItem(FAV_KEY) || '[]');
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }
  function saveFavs(arr) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(arr)); } catch (e) {}
  }
  function isFav() { return loadFavs().indexOf(gamePath()) !== -1; }
  function renderFav(btn) {
    var on = isFav();
    btn.classList.toggle('active', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.title = on ? 'remove from favorites' : 'add to favorites';
  }
  function toggleFav(btn) {
    var favs = loadFavs();
    var p = gamePath();
    var idx = favs.indexOf(p);
    if (idx !== -1) {
      favs.splice(idx, 1);
      toast('removed from favorites');
    } else {
      favs = [p].concat(favs.filter(function (x) { return x !== p; }));
      toast('added to favorites');
    }
    saveFavs(favs);
    renderFav(btn);
  }

  // ---------- mute (always defaults to unmuted on page open) ----------
  var muted = false;
  var contexts = [];

  function patchAudioContext(win) {
    try {
      ['AudioContext', 'webkitAudioContext'].forEach(function (name) {
        var Original = win[name];
        if (!Original || Original.__kiwiPatched) return;
        function Patched(opts) {
          var ctx = new Original(opts);
          contexts.push(ctx);
          if (muted) { try { ctx.suspend(); } catch (e) {} }
          return ctx;
        }
        Patched.prototype = Original.prototype;
        Patched.__kiwiPatched = true;
        try { win[name] = Patched; } catch (e) {}
      });
    } catch (e) {}
  }

  function applyMuteToDoc(doc) {
    if (!doc) return;
    try {
      var media = doc.querySelectorAll('audio,video');
      for (var i = 0; i < media.length; i++) {
        media[i].muted = muted;
        if (muted) media[i].volume = 0;
      }
    } catch (e) {}
  }

  function applyMute(iframe) {
    var doc;
    try { doc = iframe.contentDocument; } catch (e) { return; }
    applyMuteToDoc(doc);
    for (var i = 0; i < contexts.length; i++) {
      try { muted ? contexts[i].suspend() : contexts[i].resume(); } catch (e) {}
    }
  }

  function renderMute(btn) {
    btn.classList.toggle('active', muted);
    btn.setAttribute('aria-pressed', muted ? 'true' : 'false');
    btn.title = muted ? 'unmute' : 'mute';
    var on = btn.querySelector('.icon-on');
    var off = btn.querySelector('.icon-off');
    if (on) on.style.display = muted ? 'none' : 'block';
    if (off) off.style.display = muted ? 'block' : 'none';
  }

  function setupIframeMute(iframe) {
    var win, doc;
    try { win = iframe.contentWindow; doc = iframe.contentDocument; } catch (e) { return; }
    if (!win || !doc) return;
    patchAudioContext(win);
    applyMute(iframe);
    try {
      var mo = new MutationObserver(function () { applyMute(iframe); });
      mo.observe(doc.documentElement || doc, { childList: true, subtree: true });
    } catch (e) {}
    try {
      ['play', 'volumechange', 'loadeddata', 'canplay', 'focus', 'click', 'pointerdown', 'keydown'].forEach(function (ev) {
        doc.addEventListener(ev, function () { applyMute(iframe); }, true);
      });
    } catch (e) {}
    try {
      win.addEventListener('focus', function () { applyMute(iframe); });
    } catch (e) {}
  }

  var muteWatchTimer = null;
  function startMuteWatcher(iframe) {
    if (muteWatchTimer) return;
    muteWatchTimer = setInterval(function () {
      if (!muted) return;
      applyMute(iframe);
    }, 400);
  }

  function injectSocials() {
    var navRight = document.querySelector('.kiwi-nav-right');
    if (!navRight || navRight.querySelector('.kiwi-socials')) return;
    var wrap = document.createElement('div');
    wrap.className = 'kiwi-socials';
    wrap.innerHTML = [
      '<span class="kiwi-socials-label">links posted on</span>',
      '<a class="kiwi-social-link" href="https://discord.com/invite/g3C9T5EdKx" target="_blank" rel="noopener noreferrer" aria-label="Discord" title="Discord">',
        '<img src="/images/social-discord.png" alt="Discord"/>',
      '</a>',
      '<a class="kiwi-social-link" href="https://www.tiktok.com/@max9max9max9max" target="_blank" rel="noopener noreferrer" aria-label="TikTok" title="TikTok">',
        '<img src="/images/social-tiktok.png" alt="TikTok"/>',
      '</a>'
    ].join('');
    navRight.appendChild(wrap);
  }

  function init() {
    injectSocials();
    var iframe = document.getElementById('kiwiGame');
    var favBtn = document.getElementById('kiwiFav');
    var muteBtn = document.getElementById('kiwiMute');

    if (favBtn) {
      favBtn.addEventListener('click', function () { toggleFav(favBtn); });
      renderFav(favBtn);
    }

    if (muteBtn && iframe) {
      muteBtn.addEventListener('click', function () {
        muted = !muted;
        applyMute(iframe);
        renderMute(muteBtn);
        toast(muted ? 'audio muted' : 'audio on');
      });
      renderMute(muteBtn);

      iframe.addEventListener('load', function () { setupIframeMute(iframe); });
      setTimeout(function () { setupIframeMute(iframe); }, 500);
      startMuteWatcher(iframe);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
