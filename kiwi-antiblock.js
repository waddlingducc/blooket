(function () {
  if (window.__kiwiAntiblockLoaded) return;
  window.__kiwiAntiblockLoaded = true;

  var ACCENT = "#30FF00";
  var OVERLAY_ID = "kiwi-adblock-overlay";
  var STYLE_ID = "kiwi-adblock-style";
  var CHECK_INTERVAL_MS = 4000;

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement("style");
    s.id = STYLE_ID;
    s.textContent =
      "#" + OVERLAY_ID + " * { box-sizing: border-box; }" +
      "#" + OVERLAY_ID + " button:hover { background-color: " + ACCENT + "33 !important; box-shadow: 0 0 0 4px " + ACCENT + "22 !important; }";
    document.head.appendChild(s);
  }

  async function detectAdblock() {
    var blocked = false;
    var bait = document.createElement("div");
    bait.className = "adsbox ad-banner ad-placement ad-unit advertisement google-ads sponsored-ads";
    bait.setAttribute("style", "position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;");
    bait.innerHTML = "&nbsp;";
    document.body.appendChild(bait);
    await new Promise(function (r) { setTimeout(r, 100); });
    try {
      var cs = window.getComputedStyle(bait);
      if (
        bait.offsetParent === null ||
        bait.offsetHeight === 0 ||
        bait.offsetWidth === 0 ||
        cs.display === "none" ||
        cs.visibility === "hidden"
      ) blocked = true;
    } catch (e) { blocked = true; }
    bait.remove();
    if (!blocked) {
      try {
        await fetch("https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js", {
          method: "HEAD", mode: "no-cors", cache: "no-store"
        });
      } catch (e) { blocked = true; }
    }
    return blocked;
  }

  function showOverlay() {
    if (document.getElementById(OVERLAY_ID)) return;
    injectStyle();

    var overlay = document.createElement("div");
    overlay.id = OVERLAY_ID;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-labelledby", "kiwi-adblock-title");
    overlay.setAttribute("data-testid", "adblock-overlay");
    overlay.style.cssText =
      "position:fixed;inset:0;z-index:2147483647;" +
      "background-color:rgba(0,0,0,0.45);" +
      "backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);" +
      "display:flex;align-items:center;justify-content:center;padding:20px;" +
      "font-family:'Inter',sans-serif;overflow-y:auto;";

    overlay.innerHTML =
      '<div style="width:100%;max-width:720px;background-color:rgba(15,20,15,0.95);' +
        'border:1px solid ' + ACCENT + '55;border-radius:20px;padding:32px;' +
        'box-shadow:0 0 0 1px ' + ACCENT + '22, 0 20px 60px rgba(0,0,0,0.6), 0 0 80px ' + ACCENT + '22;' +
        'color:#f0f0f0;max-height:calc(100vh - 40px);overflow-y:auto;">' +
        '<div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">' +
          '<div aria-hidden="true" style="width:44px;height:44px;border-radius:12px;' +
            'background-color:' + ACCENT + '1f;border:1px solid ' + ACCENT + '55;' +
            'display:flex;align-items:center;justify-content:center;flex-shrink:0;">' +
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="' + ACCENT + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
              '<path d="M12 9v4"></path><path d="M12 17h.01"></path>' +
              '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>' +
            '</svg>' +
          '</div>' +
          '<h2 id="kiwi-adblock-title" style="font-size:24px;font-weight:800;color:#fff;margin:0;letter-spacing:-0.5px;">ad blocker detected</h2>' +
        '</div>' +
        '<p style="font-size:15px;line-height:1.6;color:#cfcfcf;margin:0 0 22px 0;">' +
          "looks like you're using an ad blocker. kiwi relies on ads to stay free. please disable your ad blocker for this site to continue, then refresh the page." +
        '</p>' +
        '<div style="background-color:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:18px;margin-bottom:18px;">' +
          '<h3 style="font-size:14px;font-weight:700;color:' + ACCENT + ';margin:0 0 14px 0;text-transform:uppercase;letter-spacing:0.5px;">how to disable</h3>' +
          '<ol style="margin:0;padding:0 0 0 20px;color:#e0e0e0;font-size:14px;line-height:1.7;">' +
            '<li>click the extensions icon in the top right of your browser</li>' +
            '<li>find your ad blocker and disable it for this site</li>' +
            '<li>refresh the page</li>' +
          '</ol>' +
          '<div style="display:flex;flex-direction:column;align-items:center;gap:14px;margin-top:16px;">' +
            '<figure style="margin:0;width:100%;max-width:320px;">' +
              '<img src="/images/extensions-icon.jpg" alt="click the extensions icon in the top right of chrome" ' +
                'style="width:100%;height:auto;display:block;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background-color:#000;">' +
              '<figcaption style="font-size:12px;color:#9a9a9a;margin-top:8px;text-align:center;">step 1: click the extensions icon</figcaption>' +
            '</figure>' +
            '<figure style="margin:0;width:100%;max-width:320px;">' +
              '<video src="/images/chrome-abp.webm" autoplay loop muted playsinline ' +
                'style="width:100%;height:auto;display:block;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background-color:#000;"></video>' +
              '<figcaption style="font-size:12px;color:#9a9a9a;margin-top:8px;text-align:center;">step 2: disable your ad blocker for this site</figcaption>' +
            '</figure>' +
          '</div>' +
        '</div>' +
        '<button type="button" data-testid="button-refresh" id="kiwi-adblock-refresh" ' +
          'style="width:100%;padding:14px 20px;border-radius:12px;border:1px solid ' + ACCENT + ';' +
          'background-color:' + ACCENT + '1f;color:#eaffe0;font-size:15px;font-weight:700;font-family:inherit;cursor:pointer;transition:all 0.15s;">' +
          "i've disabled it  refresh" +
        '</button>' +
      '</div>';

    document.body.appendChild(overlay);
    document.body.style.overflow = "hidden";
    var btn = document.getElementById("kiwi-adblock-refresh");
    if (btn) {
      btn.addEventListener("click", function () { window.location.reload(); });
      try { btn.focus(); } catch (e) {}
    }
  }

  function hideOverlay() {
    var el = document.getElementById(OVERLAY_ID);
    if (el) { el.remove(); document.body.style.overflow = ""; }
  }

  async function tick() {
    try {
      var blocked = await detectAdblock();
      if (blocked) showOverlay(); else hideOverlay();
    } catch (e) {}
  }

  function start() {
    tick();
    setInterval(tick, CHECK_INTERVAL_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
