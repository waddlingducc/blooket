// Load the remaining animations as they appear on screen
const riveAnimsDeferred = [
  'question',
  'graph',
  'wizard',
  // 'games',
  'fishing',
];
const path = 'https://ac.blooket.com/www/assets/animations/';
const ext = '.riv';

const visibilityObserverDeferred = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    const r = entry.target.__riveInstance;
    if (!r) return;
    if (entry.isIntersecting) {
      try { r.play(); } catch (_) {}
    } else {
      try { r.pause(); } catch (_) {}
    }
  });
}, { rootMargin: '100px 0px 100px 0px' });

document.addEventListener('visibilitychange', () => {
  document.querySelectorAll('canvas.sectionCanvas').forEach((el) => {
    const r = el.__riveInstance;
    if (!r) return;
    try { document.hidden ? r.pause() : r.play(); } catch (_) {}
  });
});

const callback = (entries, obs) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    if (!entry.target.classList.contains('loaded')) {
      var r = new rive.Rive({
        src: path.concat(entry.target.id, ext),
        canvas: entry.target,
        autoplay: false,
        onLoad: () => {
          r.resizeDrawingSurfaceToCanvas();
          entry.target.__riveInstance = r;
          setTimeout(() => {
            r.play();
            entry.target.classList.add('loaded');
            visibilityObserverDeferred.observe(entry.target);
          }, 10);
          obs.unobserve(entry.target);
        },
      });
    }
  });
};

let animationObserver;
let options = {
  root: null,
  rootMargin: '500px 0px 500px 0px',
};
animationObserver = new IntersectionObserver(callback, options);

riveAnimsDeferred.forEach((id) => {
  const el = document.getElementById(id);
  if (el) animationObserver.observe(el);
});
