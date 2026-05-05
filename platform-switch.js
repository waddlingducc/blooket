(function () {
  var ua = navigator.userAgent || '';
  var uaData = navigator.userAgentData;
  var isWindows = false;

  if (uaData && typeof uaData.platform === 'string') {
    isWindows = uaData.platform.toLowerCase() === 'windows';
  } else {
    isWindows = /Windows NT|Win64|Win32|Windows /i.test(ua);
  }

  if (!isWindows) return;

  var ADS = {
    box: { key: 'cca6e5f238bfb4e9f1b482f73b15c7b2', w: 300, h: 250 },
    leaderboard: { key: 'aeb0dc35e1a9a93d2ad33966d116c87a', w: 728, h: 90 }
  };

  function buildSrcdoc(cfg) {
    return '<!doctype html><html><head><meta charset="utf-8">' +
      '<style>html,body{margin:0;padding:0;background:transparent;overflow:hidden;}</style>' +
      '</head><body>' +
      '<script type="text/javascript">' +
      'atOptions = {' +
      "'key':'" + cfg.key + "'," +
      "'format':'iframe'," +
      "'height':" + cfg.h + ',' +
      "'width':" + cfg.w + ',' +
      "'params':{}" +
      '};' +
      '<\/script>' +
      '<script type="text/javascript" src="https://creaturefeaturesmouse.com/' +
      cfg.key + '/invoke.js"><\/script>' +
      '</body></html>';
  }

  function inject(container, cfg) {
    if (!container) return;
    container.innerHTML = '';
    var iframe = document.createElement('iframe');
    iframe.width = cfg.w;
    iframe.height = cfg.h;
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('frameborder', '0');
    iframe.style.cssText =
      'border:0;display:block;width:' + cfg.w + 'px;height:' + cfg.h + 'px;';
    iframe.srcdoc = buildSrcdoc(cfg);
    container.appendChild(iframe);
  }

  function run() {
    var rightSlots = document.querySelectorAll(
      '.right-ad-container, .right-unblocker-container'
    );
    rightSlots.forEach(function (el) {
      el.style.width = ADS.box.w + 'px';
      el.style.height = ADS.box.h + 'px';
      inject(el, ADS.box);
    });

    var bottomInner = document.querySelector('.bottom-ad-container > div');
    inject(bottomInner, ADS.leaderboard);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
